import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.backends import (
    NativeBackendError,
    backend_config_from_dict,
    build_native_qed_m2_script,
    build_native_qed_script,
    native_qed_bremsstrahlung_plan,
    run_native_qed_m2_generator,
    validate_native_qed_artifact_metadata,
    validate_native_qed_request,
)
from feynagent.dispatch import resolve_backend_route

try:
    import jsonschema
    import yaml
except ImportError:  # pragma: no cover
    jsonschema = None
    yaml = None


class B05BremsstrahlungSpikeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if yaml is None or jsonschema is None:
            raise unittest.SkipTest("PyYAML and jsonschema are required")
        cls.physics = yaml.safe_load(
            (ROOT / "benchmarks" / "B05_emu_to_emu_gamma" / "physics_card.yaml").read_text(encoding="utf-8")
        )
        cls.profile = yaml.safe_load(
            (ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml").read_text(encoding="utf-8")
        )
        cls.request = yaml.safe_load(
            (ROOT / "benchmarks" / "B05_emu_to_emu_gamma" / "execution_request.amplitude_only.yaml").read_text(
                encoding="utf-8"
            )
        )
        cls.config = backend_config_from_dict(cls.profile)

    def test_physics_card_schema_enforces_exact_2_to_3_cardinality(self):
        schema = json.loads((ROOT / "schemas" / "physics_card.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(self.physics, schema)
        invalid = copy.deepcopy(self.physics)
        invalid["particles"]["outgoing"] = invalid["particles"]["outgoing"][:2]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(invalid, schema)

    def test_dispatch_and_backend_accept_only_bounded_particle_pattern(self):
        route = resolve_backend_route(self.physics, self.profile)
        self.assertEqual(route.classification, "standard_native")
        self.assertIn("bounded", route.production_ready_scope)
        validate_native_qed_request(self.physics, self.config)
        invalid = copy.deepcopy(self.physics)
        invalid["particles"]["outgoing"][1]["particle_id"] = "e-"
        with self.assertRaisesRegex(NativeBackendError, "supports exactly"):
            validate_native_qed_request(invalid, self.config)

    def test_plan_is_four_external_leg_emissions_not_stu_channels(self):
        plan = native_qed_bremsstrahlung_plan(self.physics)
        self.assertEqual(len(plan), 4)
        self.assertEqual(
            {item.emission_leg for item in plan},
            {"incoming:1", "incoming:2", "outgoing:3", "outgoing:4"},
        )
        self.assertEqual({item.exchanged_virtual_particle for item in plan}, {"gamma"})

    def test_native_script_uses_2_to_3_feynarts_and_persisted_feyncalc_objects(self):
        script = build_native_qed_script(self.physics, self.config)
        self.assertIn("CreateTopologies[0, 2 -> 3", script)
        self.assertIn(
            "InsertFields[topologies, {F[2, {1}], F[2, {2}]} -> {F[2, {1}], F[2, {2}], V[1]}",
            script,
        )
        self.assertIn("CreateFeynAmp[inserted, PreFactor -> 1]", script)
        self.assertIn("feyncalcDiagramAmplitudes = FCFAConvert[", script)
        self.assertIn("feyncalcTotalAmplitude = Plus @@ feyncalcDiagramAmplitudes", script)
        self.assertIn("classifyBremsstrahlungDiagram /@ feyncalcDiagramAmplitudes", script)
        self.assertIn('plan["exchange_routing_expression"]', script)
        self.assertIn("wardRaw = feyncalcTotalAmplitude", script)
        self.assertIn("Polarization[emittedPhotonMomentum, -I, ___] :> emittedPhotonMomentum", script)
        self.assertNotIn("FermionSpinSum", script)
        self.assertNotIn("m2Product", script)

    def test_m2_policy_is_script_only_and_contains_no_squaring(self):
        script = build_native_qed_m2_script(self.physics, self.config)
        self.assertIn("FEYNAGENT_2TO3_M2_POLICY=SCRIPT_GENERATED_ONLY", script)
        self.assertIn("Plus @@ perDiagramAmplitudes", script)
        self.assertNotIn("ComplexConjugate", script)
        self.assertNotIn("FermionSpinSum", script)
        with tempfile.TemporaryDirectory() as tmp:
            result = run_native_qed_m2_generator(self.physics, Path(tmp), self.config, self.request)
            self.assertEqual(result["status"], "SCRIPT_GENERATED_ONLY")
            self.assertFalse(result["executed"])
            self.assertTrue((Path(tmp) / "compute_m2.wl").exists())

    def test_metadata_contract_requires_four_classifications_and_total_checks(self):
        plan = native_qed_bremsstrahlung_plan(self.physics)
        expression_ids = [f"expr:{self.physics['process_id']}:diagram:{index}" for index in range(1, 5)]
        diagrams = []
        for index, item in enumerate(plan, start=1):
            diagrams.append(
                {
                    "diagram_id": f"native:diagram:{index}",
                    "expression_id": expression_ids[index - 1],
                    "emission_leg": item.emission_leg,
                    "emission_particle": item.emission_particle,
                    "emitted_particle": "gamma",
                    "exchanged_virtual_particle": item.exchanged_virtual_particle,
                    "radiating_fermion_routing": item.radiating_fermion_routing,
                    "exchange_routing": item.exchange_routing,
                    "propagators": [],
                    "amplitude_file": "feyncalc_amplitudes.m",
                    "latex_file": "amplitudes.tex",
                }
            )
        metadata = {
            "diagram_count": 4,
            "classification_count": 4,
            "per_diagram_amplitude_count": 4,
            "diagrams": diagrams,
            "topology_comparison": {"status": "PASS", "expected_diagram_count": 4},
            "ward_identity": {"status": "PASS"},
            "soft_limit": {"status": "PASS"},
            "total_amplitude": {
                "definition": "Plus @@ per_diagram_amplitudes",
                "term_expression_ids": expression_ids,
            },
            "consistency": {
                "diagram_count_matches_classification_plan": True,
                "diagram_count_matches_per_diagram_amplitudes": True,
                "total_is_sum_of_per_diagram_amplitudes": True,
                "m2_computed": False,
            },
        }
        self.assertEqual(validate_native_qed_artifact_metadata(metadata, self.physics), [])


if __name__ == "__main__":
    unittest.main()
