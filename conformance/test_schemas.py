import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            path.name.removesuffix(".schema.json"): load_json(path)
            for path in SCHEMAS_DIR.glob("*.schema.json")
        }
        cls.registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema))
            for schema in cls.schemas.values()
        )

    def validator(self, schema_name: str) -> Draft202012Validator:
        return Draft202012Validator(
            self.schemas[schema_name],
            registry=self.registry,
            format_checker=FormatChecker(),
        )

    def test_schemas_are_valid_draft_2020_12(self):
        for name, schema in self.schemas.items():
            with self.subTest(schema=name):
                Draft202012Validator.check_schema(schema)

    def test_valid_fixtures(self):
        for path in sorted((FIXTURES_DIR / "valid").glob("*.valid.json")):
            schema_name = path.name.removesuffix(".valid.json")
            with self.subTest(fixture=path.name):
                self.validator(schema_name).validate(load_json(path))

    def test_invalid_fixtures_are_rejected(self):
        for path in sorted((FIXTURES_DIR / "invalid").glob("*.invalid.json")):
            schema_name = path.name.removesuffix(".invalid.json")
            with self.subTest(fixture=path.name):
                self.assertFalse(
                    self.validator(schema_name).is_valid(load_json(path))
                )

    def test_available_sibling_implementation_manifests(self):
        candidates = [
            ROOT.parent / "esra-agents" / "esra-conformance.json",
            ROOT.parent / "chatgpt-esra" / "esra-conformance.json",
            ROOT.parent / "claude-esra" / "esra-conformance.json",
            ROOT.parent / "hermes-esra" / "esra-conformance.json",
        ]
        for path in candidates:
            if path.exists():
                with self.subTest(manifest=str(path)):
                    self.validator("implementation-manifest").validate(
                        load_json(path)
                    )

    def test_compatibility_matrix_covers_known_implementations(self):
        matrix = load_json(FIXTURES_DIR.parent / "compatibility-matrix.json")
        self.validator("conformance-matrix").validate(matrix)
        entries = {
            item["implementation"]: item for item in matrix["implementations"]
        }
        self.assertEqual(len(matrix["implementations"]), 4)
        self.assertEqual(
            set(entries),
            {"esra-agents", "chatgpt-esra", "claude-esra", "hermes-esra"},
        )
        for implementation, entry in entries.items():
            with self.subTest(implementation=implementation):
                self.assertEqual(entry["exporter"]["status"], "verified")
                self.assertIn(
                    "cycle-event@1.0.0", entry["exporter"]["record_formats"]
                )


if __name__ == "__main__":
    unittest.main()
