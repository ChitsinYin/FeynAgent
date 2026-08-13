import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.amplitudes import AmplitudeBuildError, build_amplitude_ir, validate_amplitude_ir_semantics

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


def normalized_sha256(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assert_validates(testcase, instance, schema_name):
    if jsonschema is None:
        raise unittest.SkipTest("jsonschema is not installed; install with: python -m pip install -e .[dev]")
    with (ROOT / "schemas" / schema_name).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator_cls(schema).validate(instance)


class AmplitudeBuilderTests(unittest.TestCase):
    def load_inputs(self, benchmark):
        bench_dir = ROOT / "benchmarks" / benchmark
        physics = load_yaml(bench_dir / "physics_card.yaml")
        convention = load_yaml(bench_dir / "convention_card.yaml")
        registry = load_yaml(ROOT / "rules" / "qed" / "qed_tree_v1.yaml")
        diagrams = load_yaml(bench_dir / "legacy" / "diagrams.yaml")
        hashes = {
            "rule_registry": normalized_sha256(ROOT / "rules" / "qed" / "qed_tree_v1.yaml"),
            "diagram_ir": normalized_sha256(bench_dir / "legacy" / "diagrams.yaml"),
        }
        return physics, convention, registry, diagrams, hashes

    def build(self, benchmark):
        return build_amplitude_ir(*self.load_inputs(benchmark)[:4], source_hashes=self.load_inputs(benchmark)[4])

    def test_generated_amplitude_ir_validates_against_schema(self):
        for benchmark in ["B01_ee_to_mumu", "B02_compton"]:
            with self.subTest(benchmark=benchmark):
                generated = self.build(benchmark)
                assert_validates(self, generated, "amplitude_ir.schema.json")
                validate_amplitude_ir_semantics(generated)
                self.assertTrue(generated["audit_metadata"]["approved_for_amplitude_generation"])
                self.assertFalse(generated["audit_metadata"]["heavy_calculation_approved"])

    def test_b01_gold_structural_chains_and_photon_link(self):
        generated = self.build("B01_ee_to_mumu")
        self.assertEqual(generated["total_amplitude"]["term_amplitude_ids"], ["amplitude:b01_ee_to_mumu:amp_s"])
        amp = generated["amplitudes"][0]
        chains = [chain["ordered_factor_ids"] for chain in amp["fermion_chains"]]
        self.assertEqual(
            chains,
            [
                ["factor:b01_ee_to_mumu:s:ext:2:vbar", "factor:b01_ee_to_mumu:s:vertex:1", "factor:b01_ee_to_mumu:s:ext:1:u"],
                ["factor:b01_ee_to_mumu:s:ext:3:ubar", "factor:b01_ee_to_mumu:s:vertex:2", "factor:b01_ee_to_mumu:s:ext:4:v"],
            ],
        )
        photon = amp["propagator_factors"][0]
        self.assertEqual(photon["particle_id"], "gamma")
        self.assertEqual(photon["momentum_label"], "q_s")
        self.assertEqual(photon["momentum_expression"], "p1+p2")
        self.assertEqual(amp["non_chain_factors"][0]["factor_kind"], "boson_propagator_between_currents")
        self.assertEqual(len(amp["non_chain_factors"][0]["connects"]), 2)

    def test_b02_gold_structural_chains_and_photon_polarizations(self):
        generated = self.build("B02_compton")
        self.assertEqual(
            generated["total_amplitude"]["term_amplitude_ids"],
            ["amplitude:b02_compton:amp_s", "amplitude:b02_compton:amp_u"],
        )
        by_id = {amp["amplitude_id"]: amp for amp in generated["amplitudes"]}
        self.assertEqual(
            by_id["amplitude:b02_compton:amp_s"]["fermion_chains"][0]["ordered_factor_ids"],
            ["factor:b02_compton:s:ext:3:ubar", "factor:b02_compton:s:vertex:2", "factor:b02_compton:s:prop:1", "factor:b02_compton:s:vertex:1", "factor:b02_compton:s:ext:1:u"],
        )
        self.assertEqual(by_id["amplitude:b02_compton:amp_s"]["propagator_factors"][0]["momentum_expression"], "p1+k1")
        self.assertEqual(
            by_id["amplitude:b02_compton:amp_u"]["fermion_chains"][0]["ordered_factor_ids"],
            ["factor:b02_compton:u:ext:3:ubar", "factor:b02_compton:u:vertex:2", "factor:b02_compton:u:prop:1", "factor:b02_compton:u:vertex:1", "factor:b02_compton:u:ext:1:u"],
        )
        self.assertEqual(by_id["amplitude:b02_compton:amp_u"]["propagator_factors"][0]["momentum_expression"], "p1-k2")
        for amp in by_id.values():
            pols = amp["bosonic_external_polarization_factors"]
            self.assertEqual(len(pols), 2)
            self.assertEqual({pol["conjugation"] for pol in pols}, {"none", "complex_conjugate"})
            self.assertEqual(len(amp["non_chain_factors"]), 0)

    def test_builder_refuses_unapproved_amplitude_generation(self):
        physics, convention, registry, diagrams, hashes = self.load_inputs("B01_ee_to_mumu")
        physics = copy.deepcopy(physics)
        physics["approval"]["amplitude_generation"] = {"status": "not_requested"}
        with self.assertRaisesRegex(AmplitudeBuildError, "amplitude_generation"):
            build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)

    def test_builder_does_not_require_heavy_calculation_approval(self):
        physics, convention, registry, diagrams, hashes = self.load_inputs("B02_compton")
        self.assertEqual(physics["approval"]["heavy_calculation"]["status"], "not_requested")
        generated = build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)
        self.assertEqual(len(generated["amplitudes"]), 2)

    def test_builder_refuses_rule_below_audited_status(self):
        physics, convention, registry, diagrams, hashes = self.load_inputs("B01_ee_to_mumu")
        registry = copy.deepcopy(registry)
        registry["vertices"][0]["trust_status"] = "validated_pending_convention_review"
        with self.assertRaisesRegex(AmplitudeBuildError, "below project-audited"):
            build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)

    def test_wrong_flow_negative(self):
        physics, convention, registry, diagrams, hashes = self.load_inputs("B02_compton")
        diagrams = copy.deepcopy(diagrams)
        diagrams["diagrams"][0]["vertex_instances"][0]["slot_bindings"][0]["fermion_flow"]["field_orientation"] = "psi"
        with self.assertRaisesRegex(AmplitudeBuildError, "wrong fermion flow|expected exactly one"):
            build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)

    def test_wrong_q_negative(self):
        physics, convention, registry, diagrams, hashes = self.load_inputs("B02_compton")
        diagrams = copy.deepcopy(diagrams)
        diagrams["diagrams"][1]["internal_lines"][0]["momentum"]["expression"] = "p1+k1"
        with self.assertRaisesRegex(AmplitudeBuildError, "internal momentum"):
            build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)

    def test_duplicate_index_collision_negative(self):
        generated = self.build("B02_compton")
        amp = generated["amplitudes"][0]
        amp["local_indices"]["dirac"][1]["index_id"] = amp["local_indices"]["dirac"][0]["index_id"]
        with self.assertRaisesRegex(AmplitudeBuildError, "duplicate local index_id"):
            validate_amplitude_ir_semantics(generated)


if __name__ == "__main__":
    unittest.main()