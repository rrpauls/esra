#!/usr/bin/env python3
"""Run the deterministic ESRA exporter-conformance benchmark."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_VERSION = "1.2"
SCHEMA_VERSION = "1.0.0"
DEFAULT_IMPLEMENTATIONS = (
    "esra-agents",
    "chatgpt-esra",
    "claude-esra",
    "hermes-esra",
)
PRIVATE_KEYS = {
    "command_output",
    "hidden_reasoning",
    "prompt",
    "raw_session",
    "session",
    "session_id",
    "stdout",
    "transcript",
}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def _native_openai_record(record: dict[str, Any], claude: bool) -> Any:
    record_type = record["record_type"]
    if record_type == "malformed":
        return "malformed-record"
    timestamp_key = "ts" if claude else "timestamp"
    kind_key = "event" if claude else "kind"
    if record_type == "completed-cycle":
        native: dict[str, Any] = {
            timestamp_key: record.get("timestamp", "2026-09-12T18:00:00Z"),
            kind_key: "cycle_record" if claude else "cycle",
            "outcome": "success" if record.get("success", True) else "failure",
            "evidence": record.get("evidence", []),
        }
    else:
        native = {
            timestamp_key: record.get("timestamp", "2026-09-12T18:00:00Z"),
            kind_key: "trigger_blocked" if claude else "trigger-blocked",
            "outcome": "blocked",
            "recommend_cycle" if claude else "recommended": record.get("recommended", True),
        }
    if record.get("source_id"):
        native["id"] = record["source_id"]
    native.update(record.get("private_values", {}))
    return native


def build_openai_layout(data_dir: Path, scenario: dict[str, Any], claude: bool) -> None:
    records = [_native_openai_record(record, claude) for record in scenario["records"]]
    if not records:
        return
    lines = "".join(json.dumps(record, sort_keys=True) + "\n" for record in records)
    (data_dir / "events.jsonl").write_text(lines, encoding="utf-8")


def build_hermes_layout(data_dir: Path, scenario: dict[str, Any]) -> None:
    history: list[Any] = []
    cycles: list[dict[str, Any]] = []
    for record in scenario["records"]:
        record_type = record["record_type"]
        if record_type == "malformed":
            history.append("malformed-record")
            continue
        if record_type == "trigger-recommendation":
            native: dict[str, Any] = {
                "timestamp": record.get("timestamp", "2026-09-12T18:00:00Z"),
                "trigger_decision": record.get("recommended", True),
            }
            if record.get("source_id"):
                native["id"] = record["source_id"]
            private = record.get("private_values", {})
            if private:
                native["task_context"] = private
            history.append(native)
            continue
        private = record.get("private_values", {})
        cycle = {
            "timestamp": record.get("timestamp", "2026-09-12T18:00:00Z"),
            "input_state": private,
            "orchestrator_decisions": {"skills_activated": ["ooda-framework"]},
            "outputs": {
                "success": record.get("success", True),
                "improvements_applied": record.get("evidence", []),
                "anomalies": [],
            },
            "duration_and_resources": {
                "duration_seconds": 0.0,
                "command_output": private.get("command_output", ""),
            },
        }
        if record.get("source_id"):
            cycle["id"] = record["source_id"]
        cycles.append(cycle)
    if history:
        _write_json(data_dir / "evolution_history.json", history)
    if cycles:
        log_dir = data_dir / "evolution-logs"
        log_dir.mkdir()
        for index, cycle in enumerate(cycles, start=1):
            _write_json(log_dir / f"esra_cycle_{index:03d}.json", cycle)


IMPLEMENTATIONS: dict[str, tuple[str, Callable[[Path, dict[str, Any]], None]]] = {
    "esra-agents": (
        "runtime/esra_export.py",
        lambda path, scenario: build_openai_layout(path, scenario, False),
    ),
    "chatgpt-esra": (
        "scripts/esra_export.py",
        lambda path, scenario: build_openai_layout(path, scenario, False),
    ),
    "claude-esra": (
        "scripts/esra_export.py",
        lambda path, scenario: build_openai_layout(path, scenario, True),
    ),
    "hermes-esra": ("tools/esra_export.py", build_hermes_layout),
}


def load_validators() -> dict[str, Draft202012Validator]:
    schemas = {
        path.name.removesuffix(".schema.json"): json.loads(path.read_text(encoding="utf-8"))
        for path in (ROOT / "schemas").glob("*.schema.json")
    }
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas.values()
    )
    return {
        name: Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        for name, schema in schemas.items()
    }


def load_scenarios(
    scenarios_dir: Path, validator: Draft202012Validator
) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for path in sorted(scenarios_dir.glob("*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(scenario), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise ValueError(f"invalid benchmark scenario {path.name}: {details}")
        expected = scenario["expected"]
        if len(expected["event_types"]) != expected["event_count"]:
            raise ValueError(
                f"invalid benchmark scenario {path.name}: event_types length must match event_count"
            )
        if len(expected["outcomes"]) != expected["event_count"]:
            raise ValueError(
                f"invalid benchmark scenario {path.name}: outcomes length must match event_count"
            )
        private_values = {
            value
            for record in scenario["records"]
            for value in record.get("private_values", {}).values()
        }
        if not private_values.issubset(set(expected["forbidden_values"])):
            raise ValueError(
                f"invalid benchmark scenario {path.name}: every private value must be forbidden"
            )
        scenarios.append(scenario)
    if not scenarios:
        raise ValueError(f"no benchmark scenarios found in {scenarios_dir}")
    ids = [scenario["id"] for scenario in scenarios]
    if len(ids) != len(set(ids)):
        raise ValueError("benchmark scenario IDs must be unique")
    return scenarios


def _read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return events, ["exporter did not create an output file"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"output line {line_number} is not JSON: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"output line {line_number} is not an object")
            continue
        events.append(value)
    return events, errors


def _private_key_paths(value: Any, path: str = "$") -> list[str]:
    violations: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.casefold() in PRIVATE_KEYS:
                violations.append(f"forbidden key at {child_path}")
            violations.extend(_private_key_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            violations.extend(_private_key_paths(child, f"{path}[{index}]"))
    return violations


def _failure_result(
    implementation: str,
    version: str,
    scenario: dict[str, Any],
    error: str,
) -> dict[str, Any]:
    return {
        "implementation": implementation,
        "implementation_version": version,
        "scenario_id": scenario["id"],
        "required": scenario["required"],
        "status": "fail",
        "duration_ms": 0.0,
        "event_count": 0,
        "output_bytes": 0,
        "deterministic": False,
        "schema_errors": [],
        "privacy_violations": [],
        "errors": [error],
    }


def _preflight(
    implementation: str,
    implementations_root: Path,
    manifest_validator: Draft202012Validator,
) -> tuple[Path | None, str, str | None]:
    root = implementations_root / implementation
    if not root.is_dir():
        return None, "unknown", f"implementation checkout is missing: {root}"
    manifest_path = root / "esra-conformance.json"
    if not manifest_path.is_file():
        return None, "unknown", f"implementation manifest is missing: {manifest_path}"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, "unknown", f"cannot read implementation manifest: {exc}"
    version = str(manifest.get("implementation_version", "unknown"))
    manifest_errors = sorted(
        manifest_validator.iter_errors(manifest), key=lambda error: list(error.path)
    )
    if manifest_errors:
        details = "; ".join(error.message for error in manifest_errors)
        return None, version, f"implementation manifest is incompatible: {details}"
    exporter_relative, _ = IMPLEMENTATIONS[implementation]
    exporter = root / exporter_relative
    if not exporter.is_file():
        return None, version, f"exporter is missing: {exporter}"
    return root, version, None


def run_case(
    implementation: str,
    implementation_root: Path,
    version: str,
    scenario: dict[str, Any],
    cycle_validator: Draft202012Validator,
) -> dict[str, Any]:
    exporter_relative, builder = IMPLEMENTATIONS[implementation]
    with tempfile.TemporaryDirectory(prefix="esra-benchmark-") as temporary:
        workspace = Path(temporary)
        data_dir = workspace / "data"
        data_dir.mkdir()
        builder(data_dir, scenario)
        outputs = [workspace / "output-1.jsonl", workspace / "output-2.jsonl"]
        durations: list[float] = []
        process_errors: list[str] = []
        for output in outputs:
            started = time.perf_counter()
            try:
                process = subprocess.run(
                    [
                        sys.executable,
                        str(implementation_root / exporter_relative),
                        "--data-dir",
                        str(data_dir),
                        "--output",
                        str(output),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30,
                )
            except subprocess.TimeoutExpired:
                durations.append((time.perf_counter() - started) * 1000)
                process_errors.append("exporter exceeded the 30 second timeout")
                continue
            durations.append((time.perf_counter() - started) * 1000)
            if process.returncode != 0:
                detail = process.stderr.strip() or process.stdout.strip() or "no diagnostic"
                process_errors.append(f"exporter exited {process.returncode}: {detail}")
        first_bytes = outputs[0].read_bytes() if outputs[0].exists() else b""
        second_bytes = outputs[1].read_bytes() if outputs[1].exists() else b""
        deterministic = first_bytes == second_bytes and not process_errors
        events, parse_errors = _read_jsonl(outputs[0])

    schema_errors: list[str] = []
    for index, event in enumerate(events):
        for error in cycle_validator.iter_errors(event):
            schema_errors.append(f"event {index}: {error.message}")
    privacy_violations = _private_key_paths(events)
    for marker in scenario["expected"]["forbidden_values"]:
        if marker.encode() in first_bytes:
            privacy_violations.append(f"forbidden value exported: {marker}")

    expected = scenario["expected"]
    semantic_errors: list[str] = []
    if len(events) != expected["event_count"]:
        semantic_errors.append(
            f"expected {expected['event_count']} events, received {len(events)}"
        )
    actual_types = [event.get("event_type") for event in events]
    if actual_types != expected["event_types"]:
        semantic_errors.append(
            f"expected event types {expected['event_types']}, received {actual_types}"
        )
    actual_outcomes = [event.get("outcome", "absent") for event in events]
    if actual_outcomes != expected["outcomes"]:
        semantic_errors.append(
            f"expected outcomes {expected['outcomes']}, received {actual_outcomes}"
        )
    if not deterministic:
        semantic_errors.append("repeated export was not byte-for-byte deterministic")

    errors = process_errors + parse_errors + semantic_errors
    passed = not errors and not schema_errors and not privacy_violations
    return {
        "implementation": implementation,
        "implementation_version": version,
        "scenario_id": scenario["id"],
        "required": scenario["required"],
        "status": "pass" if passed else "fail",
        "duration_ms": round(durations[0], 3),
        "event_count": len(events),
        "output_bytes": len(first_bytes),
        "deterministic": deterministic,
        "schema_errors": schema_errors,
        "privacy_violations": privacy_violations,
        "errors": errors,
    }


def run_benchmark(
    scenarios_dir: Path,
    implementations_root: Path,
    implementations: tuple[str, ...] = DEFAULT_IMPLEMENTATIONS,
) -> dict[str, Any]:
    unknown = sorted(set(implementations) - set(IMPLEMENTATIONS))
    if unknown:
        raise ValueError(f"unknown implementations: {', '.join(unknown)}")
    validators = load_validators()
    scenarios = load_scenarios(scenarios_dir, validators["benchmark-scenario"])
    results: list[dict[str, Any]] = []
    for implementation in implementations:
        root, version, preflight_error = _preflight(
            implementation, implementations_root, validators["implementation-manifest"]
        )
        for scenario in scenarios:
            if preflight_error or root is None:
                results.append(
                    _failure_result(implementation, version, scenario, preflight_error or "preflight failed")
                )
            else:
                results.append(
                    run_case(
                        implementation,
                        root,
                        version,
                        scenario,
                        validators["cycle-event"],
                    )
                )

    passed_cases = sum(result["status"] == "pass" for result in results)
    required_failures = [
        result for result in results if result["required"] and result["status"] != "pass"
    ]
    report = {
        "schema_version": SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "benchmark_type": "exporter-conformance",
        "run_id": str(uuid.uuid4()),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "fail" if required_failures else "pass",
        "summary": {
            "implementations": len(implementations),
            "total_cases": len(results),
            "passed_cases": passed_cases,
            "failed_cases": len(results) - passed_cases,
            "pass_rate": round(passed_cases / len(results), 6),
            "event_count": sum(result["event_count"] for result in results),
            "output_bytes": sum(result["output_bytes"] for result in results),
            "duration_ms": round(sum(result["duration_ms"] for result in results), 3),
            "schema_errors": sum(len(result["schema_errors"]) for result in results),
            "privacy_violations": sum(len(result["privacy_violations"]) for result in results),
        },
        "results": results,
    }
    validators["benchmark-result"].validate(report)
    return report


def markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# ESRA exporter benchmark",
        "",
        f"- Status: **{report['status'].upper()}**",
        f"- Protocol: `{report['protocol_version']}`",
        f"- Cases: {summary['passed_cases']}/{summary['total_cases']} passed",
        f"- Events: {summary['event_count']}",
        f"- Output: {summary['output_bytes']} bytes",
        f"- Measured duration: {summary['duration_ms']:.3f} ms (informational)",
        f"- Schema errors: {summary['schema_errors']}",
        f"- Privacy violations: {summary['privacy_violations']}",
        "",
        "| Implementation | Version | Scenario | Status | Events | Bytes | Duration ms |",
        "|---|---:|---|---|---:|---:|---:|",
    ]
    for result in report["results"]:
        lines.append(
            "| {implementation} | {implementation_version} | {scenario_id} | {status} | "
            "{event_count} | {output_bytes} | {duration_ms:.3f} |".format(**result)
        )
        details = result["errors"] + result["schema_errors"] + result["privacy_violations"]
        for detail in details:
            lines.append(f"|  |  | ↳ {detail.replace('|', '/')} |  |  |  |  |")
    lines.extend(
        [
            "",
            "> Duration and output size are recorded as baselines, not pass/fail gates.",
            "> This benchmark verifies exporter conformance, not native host lifecycle behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenarios-dir",
        type=Path,
        default=ROOT / "benchmarks" / "scenarios",
    )
    parser.add_argument(
        "--implementations-root",
        type=Path,
        default=ROOT.parent,
        help="directory containing esra-agents and the legacy host implementations",
    )
    parser.add_argument(
        "--implementations",
        nargs="+",
        choices=sorted(IMPLEMENTATIONS),
        default=list(DEFAULT_IMPLEMENTATIONS),
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=ROOT / "benchmark-results" / "exporter-benchmark.json",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        default=ROOT / "benchmark-results" / "exporter-benchmark.md",
    )
    args = parser.parse_args(argv)
    try:
        report = run_benchmark(
            args.scenarios_dir,
            args.implementations_root,
            tuple(args.implementations),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    _atomic_write(args.json_output, json.dumps(report, indent=2, sort_keys=True) + "\n")
    _atomic_write(args.markdown_output, markdown_report(report))
    print(
        f"{report['status'].upper()}: {report['summary']['passed_cases']}/"
        f"{report['summary']['total_cases']} exporter benchmark cases passed"
    )
    print(f"JSON report: {args.json_output}")
    print(f"Markdown report: {args.markdown_output}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
