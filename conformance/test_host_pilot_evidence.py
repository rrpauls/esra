import json
import unittest
from pathlib import Path

from benchmarks.run import PRIVATE_KEYS, ROOT, load_validators


class HostPilotEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validators()["cycle-event"]

    def test_committed_exports_are_schema_valid_and_private(self):
        evidence_files = sorted((ROOT / "conformance" / "host-pilots").glob("*.events.jsonl"))
        self.assertTrue(evidence_files)
        for path in evidence_files:
            with self.subTest(path=path.name):
                events = [
                    json.loads(line)
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
                self.assertTrue(events)
                for event in events:
                    self.validator.validate(event)
                    self.assertTrue(PRIVATE_KEYS.isdisjoint(self._keys(event)))
                serialized = json.dumps(events).casefold()
                for prompt_fragment in (
                    "amber",
                    "cobalt",
                    "birch",
                    "persistent host configuration",
                ):
                    self.assertNotIn(prompt_fragment, serialized)

    def _keys(self, value):
        if isinstance(value, dict):
            keys = {str(key).casefold() for key in value}
            for child in value.values():
                keys.update(self._keys(child))
            return keys
        if isinstance(value, list):
            keys = set()
            for child in value:
                keys.update(self._keys(child))
            return keys
        return set()


if __name__ == "__main__":
    unittest.main()
