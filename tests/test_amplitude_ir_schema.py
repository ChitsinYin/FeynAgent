import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "amplitude_ir.schema.json"
FIXTURES = {
    "B01": ROOT / "benchmarks" / "B01_ee_to_mumu" / "amplitude_ir.example.yaml",
    "B02": ROOT / "benchmarks" / "B02_compton" / "amplitude_ir.example.yaml",
}

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


def load_schema():
    if jsonschema is None:
        raise unittest.SkipTest("jsonschema is not installed; install with: python -m pip install -e .[dev]")
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class AmplitudeIRSchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = load_schema()
        validator_cls = jsonschema.validators.validator_for(self.schema)
        validator_cls.check_schema(self.schema)
        self.validator = validator_cls(self.schema)

    def load_fixture(self, name):
        fixture = load_yaml(FIXTURES[name])
        self.validator.validate(fixture)
        return fixture

    def test_hand_readable_fixtures_validate(self):
        for name in FIXTURES:
            with self.subTest(fixture=name):
                fixture = self.load_fixture(name)
                self.assertEqual(fixture["ir_type"], "derived_amplitude_ir")
                self.assertEqual(fixture["status"], "derived_candidate")
                self.assertTrue(fixture["audit_metadata"]["approved_for_amplitude_generation"])
                self.assertFalse(fixture["audit_metadata"]["heavy_calculation_approved"])

    def test_b01_represents_two_currents_linked_by_photon_propagator(self):
        fixture = self.load_fixture("B01")
        self.assertEqual(len(fixture["amplitudes"]), 1)
        amp = fixture["amplitudes"][0]
        self.assertEqual(amp["diagram_id"], "diagram:generated:b01-ee-to-mumu:s:gamma")
        self.assertEqual(len(amp["fermion_chains"]), 2)
        self.assertEqual(
            {chain["chain_id"] for chain in amp["fermion_chains"]},
            {"chain:b01:s:e_current", "chain:b01:s:mu_current"},
        )
        self.assertEqual(len(amp["bosonic_external_polarization_factors"]), 0)
        self.assertTrue(
            any(factor["factor_kind"] == "boson_propagator_between_currents" for factor in amp["non_chain_factors"])
        )
        self.assertIn("rule:qed_tree_v1:photon_propagator", amp["source_rule_ids"])

    def test_b02_represents_s_and_u_single_chain_compton_amplitudes(self):
        fixture = self.load_fixture("B02")
        self.assertEqual(
            {amp["diagram_id"] for amp in fixture["amplitudes"]},
            {"diagram:generated:b02-compton:s:e-", "diagram:generated:b02-compton:u:e-"},
        )
        for amp in fixture["amplitudes"]:
            with self.subTest(amplitude=amp["amplitude_id"]):
                self.assertEqual(len(amp["fermion_chains"]), 1)
                self.assertEqual(len(amp["bosonic_external_polarization_factors"]), 2)
                self.assertEqual(len(amp["non_chain_factors"]), 0)
                self.assertIn("rule:qed_tree_v1:electron_propagator", amp["source_rule_ids"])
                self.assertTrue(
                    any(pol["conjugation"] == "complex_conjugate" for pol in amp["bosonic_external_polarization_factors"])
                )

    def test_local_index_ids_are_unique_and_references_resolve(self):
        for name in FIXTURES:
            fixture = self.load_fixture(name)
            for amp in fixture["amplitudes"]:
                with self.subTest(fixture=name, amplitude=amp["amplitude_id"]):
                    local_ids = [
                        index["index_id"]
                        for group in ("lorentz", "dirac")
                        for index in amp["local_indices"][group]
                    ]
                    self.assertEqual(len(local_ids), len(set(local_ids)))
                    local_id_set = set(local_ids)
                    for factor in amp["external_state_factors"]:
                        self.assertTrue(set(factor["index_ids"]) <= local_id_set)
                    for factor in amp["vertex_factors"]:
                        self.assertTrue(set(factor["lorentz_index_ids"]) <= local_id_set)
                        self.assertTrue(set(factor["dirac_index_ids"]) <= local_id_set)
                        for slot in factor["slot_factors"]:
                            self.assertTrue(set(slot["index_ids"]) <= local_id_set)
                    for factor in amp["propagator_factors"]:
                        self.assertTrue(set(factor["index_ids"]) <= local_id_set)
                    for factor in amp["bosonic_external_polarization_factors"]:
                        self.assertIn(factor["lorentz_index_id"], local_id_set)
                    for contraction in amp["index_contractions"]:
                        for ref in contraction["factor_indices"]:
                            self.assertIn(ref["index_id"], local_id_set)

    def test_fixtures_do_not_replace_structure_with_opaque_final_strings(self):
        forbidden_keys = {"latex", "feyncalc", "final_latex", "final_feyncalc", "amplitude_string"}
        for name in FIXTURES:
            fixture = self.load_fixture(name)
            stack = [fixture]
            while stack:
                item = stack.pop()
                if isinstance(item, dict):
                    self.assertTrue(forbidden_keys.isdisjoint(item))
                    stack.extend(item.values())
                elif isinstance(item, list):
                    stack.extend(item)


if __name__ == "__main__":
    unittest.main()