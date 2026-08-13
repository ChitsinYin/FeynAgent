import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAMES = [
    "physics_card.schema.json",
    "convention_card.schema.json",
    "rule_registry.schema.json",
    "diagram_ir.schema.json",
    "amplitude_ir.schema.json",
    "backend_profile.schema.json",
    "execution_request.schema.json",
]


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_parse_as_json(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                path = ROOT / "schemas" / name
                with path.open("r", encoding="utf-8") as handle:
                    schema = json.load(handle)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")

    def test_top_level_schemas_are_strict(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                path = ROOT / "schemas" / name
                with path.open("r", encoding="utf-8") as handle:
                    schema = json.load(handle)
                self.assertIs(schema["additionalProperties"], False)
                self.assertIn("schema_version", schema["required"])
                self.assertIn("object_id", schema["required"])

    def test_notes_are_metadata_only_at_top_level(self):
        for name in SCHEMA_NAMES:
            with self.subTest(schema=name):
                path = ROOT / "schemas" / name
                with path.open("r", encoding="utf-8") as handle:
                    schema = json.load(handle)
                self.assertNotIn("notes", schema["properties"])
                self.assertIn("metadata", schema["properties"])


if __name__ == "__main__":
    unittest.main()

