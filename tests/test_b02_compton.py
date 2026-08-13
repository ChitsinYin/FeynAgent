import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
B02 = ROOT / "benchmarks" / "B02_compton"
B02_LEGACY = B02 / "legacy"
CANONICAL_QED = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    import jsonschema
except ImportError:  # pragma: no cover
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
        self.manifest = load_yaml(B02_LEGACY / "rule_manifest.yaml")
        self.rules = load_yaml(CANONICAL_QED)
        self.diagrams_doc = load_yaml(B02_LEGACY / "diagrams.yaml")
        self.expected = load_yaml(B02_LEGACY / "expected.yaml")
        self.diagrams = self.diagrams_doc["diagrams"]
        self.vertex_rules = {rule["rule_id"]: rule for rule in self.rules["vertices"]}
        self.propagator_rules = {rule["rule_id"]: rule for rule in self.rules["propagators"]}
        self.particles = {entry["particle_id"]: entry for entry in self.rules["particle_catalog"]}

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

    def test_schema_versions_migrated_to_0_1_2_where_semantics_changed(self):
        self.assertEqual(self.physics["schema_version"], "0.2.0")
        self.assertEqual(self.diagrams_doc["schema_version"], "0.1.2")
        self.assertEqual(self.expected["schema_version"], "0.1.2")
        self.assertEqual(self.convention["schema_version"], "0.1.1")
        self.assertEqual(self.rules["schema_version"], "0.1.1")

    def test_rule_manifest_is_lightweight_and_points_to_canonical_registry(self):
        self.assertNotIn("vertices", self.manifest)
        self.assertNotIn("propagators", self.manifest)
        self.assertEqual(self.manifest["status"], "derived_non_canonical")
        self.assertEqual(self.manifest["canonical_registry"]["registry_id"], self.rules["registry_id"])
        canonical_path = (B02_LEGACY / self.manifest["canonical_registry"]["relative_path"]).resolve()
        self.assertEqual(canonical_path, CANONICAL_QED.resolve())
        normalized_rules = CANONICAL_QED.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        actual_hash = hashlib.sha256(normalized_rules.encode("utf-8")).hexdigest()
        self.assertEqual(self.manifest["canonical_registry"]["source_sha256"], actual_hash)

    def test_approval_allows_amplitudes_but_not_heavy_calculation(self):
        approval = self.physics["approval"]
        self.assertEqual(approval["topology"]["status"], "approved")
        self.assertIn("approved_at", approval["topology"])
        self.assertEqual(approval["amplitude_generation"]["status"], "approved")
        self.assertEqual(approval["amplitude_generation"].get("approved_by"), "user")
        self.assertIn("approved_at", approval["amplitude_generation"])
        self.assertEqual(approval["heavy_calculation"]["status"], "not_requested")

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

    def test_rule_references_resolve_to_canonical_qed_registry(self):
        vertex_id = self.expected["expected_topology"]["required_rule_ids"]["vertex"]
        propagator_id = self.expected["expected_topology"]["required_rule_ids"]["propagator"]
        available = set(self.vertex_rules) | set(self.propagator_rules)
        self.assertIn(vertex_id, available)
        self.assertIn(propagator_id, available)
        self.assertEqual(self.manifest["selected_rule_ids"]["vertices"], [vertex_id])
        self.assertEqual(self.manifest["selected_rule_ids"]["propagators"], [propagator_id])

        for diagram in self.diagrams:
            refs = {ref["rule_id"] for ref in diagram["rule_references"]}
            self.assertEqual(refs, {vertex_id, propagator_id})
            self.assertTrue(refs <= available)

    def test_coupling_order_is_qed_tree_order(self):
        for diagram in self.diagrams:
            self.assertEqual(diagram["coupling_order"], [{"coupling": "e", "power": 2}])
            self.assertEqual(diagram["symmetry_factor"], "1")

    def test_every_required_provenance_field_is_present(self):
        for rule in self.rules["vertices"] + self.rules["propagators"]:
            self.assertEqual(rule["trust_status"], "validated")
            self.assertGreaterEqual(len(rule["provenance"]), 2)
            self.assertTrue(
                any(
                    entry.get("local_source_path") == "docs/QED_CONVENTION_AUDIT.md"
                    for entry in rule["provenance"]
                )
            )
            for entry in rule["provenance"]:
                for field in ["source_type", "notes", "checked_by", "checked_at"]:
                    self.assertIn(field, entry)
                    self.assertIsNotNone(entry[field])
                    self.assertNotEqual(str(entry[field]).strip(), "")
                self.assertTrue(entry.get("citation") or entry.get("local_source_path"))

    def test_rule_slot_bindings_are_complete_unique_and_existing(self):
        for diagram in self.diagrams:
            endpoint_ids = {leg["leg_id"] for leg in diagram["external_legs"]}
            endpoint_ids |= {line["line_id"] for line in diagram["internal_lines"]}
            for vertex in diagram["vertex_instances"]:
                rule = self.vertex_rules[vertex["rule_id"]]
                expected_slots = {field["slot"] for field in rule["participating_fields"]}
                bound_slots = [binding["rule_slot"] for binding in vertex["slot_bindings"]]
                self.assertEqual(set(bound_slots), expected_slots)
                self.assertEqual(len(bound_slots), len(set(bound_slots)))
                for binding in vertex["slot_bindings"]:
                    self.assertIn(binding["endpoint_id"], endpoint_ids)

    def test_rule_slot_bindings_match_rule_fields_and_endpoint_particles(self):
        for diagram in self.diagrams:
            external_by_id = {leg["leg_id"]: leg for leg in diagram["external_legs"]}
            internal_by_id = {line["line_id"]: line for line in diagram["internal_lines"]}
            for vertex in diagram["vertex_instances"]:
                rule = self.vertex_rules[vertex["rule_id"]]
                fields_by_slot = {field["slot"]: field for field in rule["participating_fields"]}
                for binding in vertex["slot_bindings"]:
                    field = fields_by_slot[binding["rule_slot"]]
                    endpoint = external_by_id.get(binding["endpoint_id"]) or internal_by_id.get(binding["endpoint_id"])
                    self.assertIsNotNone(endpoint)
                    self.assertEqual(binding["expected_particle_id"], field["particle_id"])
                    self.assertEqual(binding["expected_field_id"], field["field_id"])
                    self.assertEqual(binding["endpoint_particle_id"], endpoint["particle_id"])
                    compatible = binding["endpoint_particle_id"] == binding["expected_particle_id"]
                    antiparticle = self.particles[binding["expected_particle_id"]]["antiparticle_id"]
                    compatible = compatible or binding["endpoint_particle_id"] == antiparticle
                    self.assertTrue(compatible)
                    expected_orientation = field["quantum_field_role"] if field["field_role"] == "dirac_fermion" else "not_applicable"
                    self.assertEqual(binding["fermion_flow"]["field_orientation"], expected_orientation)
                    expected_flow = "not_applicable"
                    if expected_orientation == "psi":
                        expected_flow = "into_vertex"
                    elif expected_orientation == "psi_bar":
                        expected_flow = "out_of_vertex"
                    self.assertEqual(binding["fermion_flow"]["flow_direction"], expected_flow)

    def test_crossing_and_convention_conversion_are_explicit(self):
        for diagram in self.diagrams:
            external_by_id = {leg["leg_id"]: leg for leg in diagram["external_legs"]}
            for vertex in diagram["vertex_instances"]:
                for binding in vertex["slot_bindings"]:
                    self.assertEqual(binding["convention_conversion"]["target"], "all_momenta_incoming_vertex")
                    if binding["endpoint_kind"] == "external_leg":
                        leg = external_by_id[binding["endpoint_id"]]
                        self.assertEqual(binding["convention_conversion"]["source"], "physical_external_momenta")
                        if leg["state_role"] == "incoming":
                            self.assertEqual(binding["crossing_treatment"], "external_incoming_as_rule_incoming")
                            self.assertFalse(binding["momentum_substitution"].startswith("-"))
                        else:
                            self.assertEqual(binding["crossing_treatment"], "external_outgoing_crossed_to_rule_incoming")
                            self.assertTrue(binding["momentum_substitution"].startswith("-"))
                    else:
                        self.assertEqual(binding["crossing_treatment"], "internal_line_orientation")
                        self.assertEqual(binding["convention_conversion"]["source"], "internal_routing")


if __name__ == "__main__":
    unittest.main()
