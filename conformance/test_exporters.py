import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]


def implementation_root(name: str) -> Path | None:
    for candidate in (ROOT.parent / name, ROOT / "implementations" / name):
        if candidate.is_dir():
            return candidate
    return None


def load_exporter(name: str, relative_path: str):
    root = implementation_root(name)
    if root is None:
        return None
    spec = importlib.util.spec_from_file_location(
        f"{name.replace('-', '_')}_export", root / relative_path
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExporterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schemas = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (ROOT / "schemas").glob("*.schema.json")
        ]
        registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema)) for schema in schemas
        )
        cycle_schema = next(
            schema for schema in schemas if schema["title"] == "ESRA Cycle Event"
        )
        cls.cycle_validator = Draft202012Validator(
            cycle_schema, registry=registry, format_checker=FormatChecker()
        )

    def validate_events(self, events: list[dict]) -> None:
        self.assertTrue(events)
        for event in events:
            self.cycle_validator.validate(event)

    def test_portable_event_log_exporters(self):
        paths = {
            "esra-agents": "runtime/esra_export.py",
            "chatgpt-esra": "scripts/esra_export.py",
            "claude-esra": "scripts/esra_export.py",
        }
        for implementation, relative_path in paths.items():
            exporter = load_exporter(implementation, relative_path)
            if exporter is None:
                self.skipTest(f"{implementation} checkout is unavailable")
            with self.subTest(implementation=implementation), tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                (base / "events.jsonl").write_text(
                    json.dumps({
                        "timestamp": "2026-09-12T18:00:00Z",
                        "ts": "2026-09-12T18:00:00Z",
                        "kind": "cycle",
                        "event": "cycle_record",
                        "outcome": "success",
                        "evidence": ["contract fixture"],
                        "prompt": "must not be exported",
                    }) + "\n",
                    encoding="utf-8",
                )
                events = exporter.export_events(base)
                self.validate_events(events)
                self.assertNotIn("must not be exported", json.dumps(events))

    def test_hermes_exporter(self):
        exporter = load_exporter("hermes-esra", "tools/esra_export.py")
        if exporter is None:
            self.skipTest("hermes-esra checkout is unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            (home / "evolution_history.json").write_text(
                '[{"timestamp":"2026-09-12T18:00:00Z","triggered":true}]',
                encoding="utf-8",
            )
            events = exporter.export_events(home)
            self.validate_events(events)


if __name__ == "__main__":
    unittest.main()
