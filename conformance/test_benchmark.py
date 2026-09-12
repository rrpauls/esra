import json
import tempfile
import unittest
from pathlib import Path

from benchmarks.run import (
    DEFAULT_IMPLEMENTATIONS,
    ROOT,
    load_scenarios,
    load_validators,
    markdown_report,
    run_benchmark,
)


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validators = load_validators()
        cls.scenarios_dir = ROOT / "benchmarks" / "scenarios"

    def test_required_scenario_coverage(self):
        scenarios = load_scenarios(
            self.scenarios_dir, self.validators["benchmark-scenario"]
        )
        self.assertEqual(
            {scenario["id"] for scenario in scenarios},
            {
                "completed-cycle",
                "empty-source",
                "invalid-timestamp",
                "malformed-record",
                "missing-id-private-fields",
                "recommended-not-run",
            },
        )
        self.assertTrue(all(scenario["required"] for scenario in scenarios))

    def test_available_implementations_pass_benchmark(self):
        available = tuple(
            name for name in DEFAULT_IMPLEMENTATIONS if (ROOT.parent / name).is_dir()
        )
        if not available:
            self.skipTest("sibling implementation checkouts are unavailable")
        report = run_benchmark(self.scenarios_dir, ROOT.parent, available)
        self.validators["benchmark-result"].validate(report)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["summary"]["pass_rate"], 1.0)
        self.assertEqual(report["summary"]["privacy_violations"], 0)
        self.assertEqual(report["summary"]["schema_errors"], 0)
        self.assertTrue(all(result["deterministic"] for result in report["results"]))
        rendered = markdown_report(report)
        self.assertIn("Duration and output size are recorded as baselines", rendered)
        self.assertIn("not native host lifecycle behavior", rendered)

    def test_missing_implementation_is_a_required_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            report = run_benchmark(
                self.scenarios_dir,
                Path(temporary),
                ("chatgpt-esra",),
            )
        self.assertEqual(report["status"], "fail")
        self.assertEqual(report["summary"]["passed_cases"], 0)
        self.assertTrue(
            all("checkout is missing" in result["errors"][0] for result in report["results"])
        )

    def test_incompatible_manifest_is_a_required_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "chatgpt-esra"
            root.mkdir()
            (root / "esra-conformance.json").write_text(
                json.dumps(
                    {
                        "implementation": "chatgpt-esra",
                        "implementation_version": "9.0.0",
                        "protocol_version": "9.9",
                        "runtime": "fixture",
                        "capabilities": {
                            "portable_cycle_event_export": {
                                "status": "planned",
                                "evidence": ["fixture"],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            report = run_benchmark(
                self.scenarios_dir,
                Path(temporary),
                ("chatgpt-esra",),
            )
        self.assertEqual(report["status"], "fail")
        self.assertTrue(
            all("manifest is incompatible" in result["errors"][0] for result in report["results"])
        )

    def test_invalid_scenario_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            scenarios = Path(temporary)
            (scenarios / "invalid.json").write_text(
                '{"schema_version":"1.0.0","protocol_version":"1.2"}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid benchmark scenario"):
                load_scenarios(scenarios, self.validators["benchmark-scenario"])


if __name__ == "__main__":
    unittest.main()
