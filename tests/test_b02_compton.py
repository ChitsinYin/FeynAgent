import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B02 = ROOT / "benchmarks" / "B02_compton"


try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in incomplete dev envs
    yaml = None

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised only in incomplete dev envs
    jsonschema = None


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class B02ComptonBenchmarkTests(unittest.TestCase):
    def setUp(self):
        if jsonschema is None:
            raise unittest.SkipTest("jsonschema is not installed; install with: python -m pip install -e .[dev]")
        self.physics = load_yaml(B02 / "physics_card.yaml")
        self.convention = load_yaml(B02 / "convention_card.yaml")
        self.rules = load_yaml(B02 / "rule_manifest.yaml")
        self.diagrams_doc = load_yaml(B02 / "diagrams.yaml")
        self.expected = load_yaml(B02 / "expected.yaml")
        self.diagrams = self.diagrams_doc["diagrams"]

    def assert_validates(self, instance, schema_name):
        schema = load_json(ROOT / "schemas" / schema_name)
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator_cls(schema).validate(instance)

    def test_canonical_objects_validate_against_schemas(self):
        self.assert_validates(self.physics, "physics_card.schema.json")
        self.assert_validates(self.convention, "convention_card.schema.json")
        self.assert_validates(self.rules, "rule_registry.schema.json")
        self.assert_validates(self.diagrams_doc, "diagram_ir.schema.json")

    def test_exactly_two_tree_diagrams_with_s_and_u_channels(self):
        self.assertEqual(len(self.diagrams), 2)
        self.assertEqual({diagram["channel"] for diagram in self.diagrams}, {"s", "u"})
        self.assertTrue(all(diagram["loop_order"] == 0 for diagram in self.diagrams))

    def test_internal_species_and_momenta_match_gold_topology(self):
        expected_momenta = self.expected["expected_topology"]["internal_momenta"]
        for diagram in self.diagrams:
            channel = diagram["channel"]
            self.assertEqual(len(diagram["internal_lines"]), 1)
            line = diagram["internal_lines"][0]
            self.assertEqual(line["particle_id"], "e-")
            self.assertEqual(line["momentum"]["expression"], expected_momenta[channel])
            self.assertEqual(line["momentum"]["external_convention"], "physical_external_momenta")

    def test_rule_references_resolve_and_include_required_qed_rules(self):
        vertex_id = self.expected["expected_topology"]["required_rule_ids"]["vertex"]
        propagator_id = self.expected["expected_topology"]["required_rule_ids"]["propagator"]
        available = {rule["rule_id"] for rule in self.rules["vertices"] + self.rules["propagators"]}
        self.assertIn(vertex_id, available)
        self.assertIn(propagator_id, available)

        for diagram in self.diagrams:
            refs = {ref["rule_id"] for ref in diagram["rule_references"]}
            self.assertEqual(refs, {vertex_id, propagator_id})
            for vertex in diagram["vertex_instances"]:
                self.assertEqual(vertex["rule_id"], vertex_id)
            for line in diagram["internal_lines"]:
                self.assertEqual(line["propagator_rule_id"], propagator_id)
            self.assertTrue(refs <= available)

    def test_coupling_order_is_qed_tree_order(self):
        for diagram in self.diagrams:
            self.assertEqual(diagram["coupling_order"], [{"coupling": "e", "power": 2}])
            self.assertEqual(diagram["symmetry_factor"], "1")

    def test_every_required_provenance_field_is_present(self):
        for rule in self.rules["vertices"] + self.rules["propagators"]:
            self.assertIn(rule["trust_status"], {"validated", "validated_pending_convention_review", "trusted"})
            self.assertGreaterEqual(len(rule["provenance"]), 1)
            for entry in rule["provenance"]:
                for field in ["source_type", "citation", "section", "page", "notes", "checked_by", "checked_at"]:
                    self.assertIn(field, entry)
                    self.assertIsNotNone(entry[field])
                    self.assertNotEqual(str(entry[field]).strip(), "")


if __name__ == "__main__":
    unittest.main()
