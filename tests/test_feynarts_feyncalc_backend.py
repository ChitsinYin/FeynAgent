import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.backends import (
    BackendConfig,
    NativeBackendError,
    backend_config_from_dict,
    build_native_qed_script,
    build_native_qed_m2_script,
    native_qed_channel_plan,
    run_native_qed_m2_generator,
    validate_native_qed_artifact_metadata,
    validate_native_qed_request,
)

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class FeynArtsFeynCalcBackendTests(unittest.TestCase):
    def load_physics(self, benchmark):
        return load_yaml(ROOT / "benchmarks" / benchmark / "physics_card.yaml")

    def native_config(self):
        return backend_config_from_dict(load_yaml(ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml"))

    def test_b01_script_uses_native_feynarts_feyncalc_calls(self):
        script = build_native_qed_script(self.load_physics("B01_ee_to_mumu"), self.native_config())
        self.assertIn('$LoadAddOns = {"FeynArts"};', script)
        self.assertIn("backend_profile_id = ", script)
        self.assertNotIn("$LoadFeynArts = True", script)
        self.assertIn("CreateTopologies[0, 2 -> 2", script)
        self.assertIn("InsertFields[topologies, {F[2, {1}], -F[2, {1}]} -> {F[2, {2}], -F[2, {2}]}", script)
        self.assertIn('Model -> "SM"', script)
        self.assertIn("Restrictions -> QEDOnly", script)
        self.assertIn("InsertionLevel -> {Classes}", script)
        self.assertIn("CreateFeynAmp[inserted, PreFactor -> 1]", script)
        self.assertNotIn("Truncated -> True", script)
        self.assertIn("FCFAConvert[", script)
        self.assertIn("raw_feynarts_amplitude.m", script)
        self.assertIn("feyncalc_amplitude.inputform.txt", script)
        self.assertNotIn("qed_tree_v1", script)
        self.assertNotIn("RuleRegistry", script)

    def test_b02_particle_mapping_is_backend_profile_local(self):
        script = build_native_qed_script(self.load_physics("B02_compton"), self.native_config())
        self.assertIn("InsertFields[topologies, {F[2, {1}], V[1]} -> {F[2, {1}], V[1]}", script)
        self.assertIn("IncomingMomenta -> {p1, k1}", script)
        self.assertIn("OutgoingMomenta -> {p2, k2}", script)
        self.assertIn("TransversePolarizationVectors -> {k1, k2}", script)

    def test_backend_config_from_yaml_dict(self):
        config = self.native_config()
        self.assertEqual(config.backend_id, "feynarts_feyncalc_native")
        self.assertEqual(config.backend_profile_id, "backend_profile:feynarts_sm_qed")
        self.assertEqual(config.model_id, "sm_qed")
        self.assertEqual(config.sector, "qed")
        self.assertEqual(config.model, "SM")
        self.assertEqual(config.restrictions, "QEDOnly")
        self.assertEqual(config.particle_to_feynarts["gamma"], "V[1]")
        script = build_native_qed_script(self.load_physics("B02_compton"), config)
        self.assertIn("Restrictions -> QEDOnly", script)

    def test_b03_script_uses_electron_muon_scattering_mapping(self):
        script = build_native_qed_script(self.load_physics("B03_emu_to_emu"), self.native_config())
        self.assertIn("InsertFields[topologies, {F[2, {1}], F[2, {2}]} -> {F[2, {1}], F[2, {2}]}", script)
        self.assertNotIn("TransversePolarizationVectors", script)

    def test_native_channel_plan_for_release_benchmarks(self):
        cases = {
            "B01_ee_to_mumu": [("s", "gamma", "p1+p2")],
            "B02_compton": [("s", "e-", "p1+k1"), ("u", "e-", "p1-k2")],
            "B03_emu_to_emu": [("t", "gamma", "p1-p3")],
        }
        for benchmark, expected in cases.items():
            with self.subTest(benchmark=benchmark):
                channels = native_qed_channel_plan(self.load_physics(benchmark))
                observed = [(item.channel, item.internal_particle, item.routing) for item in channels]
                self.assertEqual(observed, expected)

    def test_script_emits_native_diagram_amplitude_latex_artifacts_without_m2(self):
        script = build_native_qed_script(self.load_physics("B02_compton"), self.native_config())
        self.assertIn("Paint[", script)
        self.assertIn("diagram_source.m", script)
        self.assertIn("diagram_source.paint.inputform.txt", script)
        self.assertIn("diagrams.pdf", script)
        self.assertIn("rawDiagramAmplitudes = List @@ rawAmplitude", script)
        self.assertIn("feyncalcDiagramAmplitudes = FCFAConvert[", script)
        self.assertIn("feyncalcTotalAmplitude = Plus @@ feyncalcDiagramAmplitudes", script)
        self.assertIn("feyncalc_amplitudes.m", script)
        self.assertIn("amplitudes.tex", script)
        self.assertIn("amplitudes.pdf", script)
        self.assertIn("amplitudes.json", script)
        self.assertIn("% expression-id: ", script)
        self.assertIn("StringReplace[ToString[TeXForm[expr]], \"^*^{\" -> \"^{* \"]", script)
        self.assertIn("term_expression_ids", script)
        self.assertIn('"m2_computed" -> False', script)
        self.assertNotIn("FermionSpinSum", script)
        self.assertNotIn("DoPolarizationSums", script)

    def test_artifact_metadata_validator_accepts_benchmark_counts_and_expression_ids(self):
        for benchmark in ["B01_ee_to_mumu", "B02_compton", "B03_emu_to_emu"]:
            with self.subTest(benchmark=benchmark):
                physics = self.load_physics(benchmark)
                channels = native_qed_channel_plan(physics)
                expression_ids = [f"expr:{physics['process_id']}:diagram:{index}" for index in range(1, len(channels) + 1)]
                metadata = {
                    "diagram_count": len(channels),
                    "channel_count": len(channels),
                    "per_diagram_amplitude_count": len(channels),
                    "diagrams": [
                        {
                            "diagram_id": f"native:diagram:{index}",
                            "expression_id": expression_ids[index - 1],
                            "channel": channel.channel,
                            "internal_particle": channel.internal_particle,
                            "expected_routing": channel.routing,
                            "propagators": [],
                            "amplitude_file": "feyncalc_amplitudes.m",
                            "latex_file": "amplitudes.tex",
                        }
                        for index, channel in enumerate(channels, start=1)
                    ],
                    "total_amplitude": {
                        "expression_id": f"expr:{physics['process_id']}:total",
                        "definition": "Plus @@ per_diagram_amplitudes",
                        "term_expression_ids": expression_ids,
                        "amplitude_file": "feyncalc_amplitudes.m",
                        "latex_file": "amplitudes.tex",
                    },
                    "consistency": {
                        "diagram_count_matches_channel_plan": True,
                        "diagram_count_matches_per_diagram_amplitudes": True,
                        "total_is_sum_of_per_diagram_amplitudes": True,
                        "m2_computed": False,
                    },
                }
                self.assertEqual(validate_native_qed_artifact_metadata(metadata, physics), [])

    def test_artifact_metadata_validator_rejects_total_not_matching_terms(self):
        physics = self.load_physics("B02_compton")
        channels = native_qed_channel_plan(physics)
        metadata = {
            "diagram_count": 2,
            "channel_count": 2,
            "per_diagram_amplitude_count": 2,
            "diagrams": [
                {
                    "expression_id": f"expr:{physics['process_id']}:diagram:{index}",
                    "channel": channel.channel,
                    "amplitude_file": "feyncalc_amplitudes.m",
                    "latex_file": "amplitudes.tex",
                }
                for index, channel in enumerate(channels, start=1)
            ],
            "total_amplitude": {
                "definition": "Plus @@ per_diagram_amplitudes",
                "term_expression_ids": ["expr:wrong"],
            },
            "consistency": {
                "diagram_count_matches_channel_plan": True,
                "diagram_count_matches_per_diagram_amplitudes": True,
                "total_is_sum_of_per_diagram_amplitudes": True,
                "m2_computed": False,
            },
        }
        issues = validate_native_qed_artifact_metadata(metadata, physics)
        self.assertIn("total amplitude terms do not match per-diagram expression IDs", issues)

    def test_m2_script_derives_workflow_from_external_state_metadata(self):
        script = build_native_qed_m2_script(
            self.load_physics("B02_compton"),
            self.native_config(),
            gold_expression='-2 SMP["e"]^4 (s^2 + u^2)/(s u)',
        )
        self.assertIn("m2Product = ampTotal * ComplexConjugate[ampTotal]", script)
        self.assertIn("m2DenExplicit = FeynAmpDenominatorExplicit[m2Product]", script)
        self.assertIn("DoPolarizationSums[m2AfterPolarization, k1, 0]", script)
        self.assertIn("DoPolarizationSums[m2AfterPolarization, k2, 0]", script)
        self.assertNotIn("DoPolarizationSums[m2AfterPolarization, p1", script)
        self.assertNotIn("DoPolarizationSums[m2AfterPolarization, p2", script)
        self.assertIn("m2Raw = FermionSpinSum[m2AfterPolarization, ExtraFactor -> initialSpinAverageFactor]", script)
        self.assertIn("initialSpinAverageFactor = 1/(2*2)", script)
        self.assertIn('setMandelstamCall = "SetMandelstam[s, t, u, p1, k1, -p2, -k2, SMP[\\"m_e\\"], 0, SMP[\\"m_e\\"], 0]"', script)
        self.assertIn("m2_raw.m", script)
        self.assertIn("m2_simplified.m", script)
        self.assertIn("m2_inputform.txt", script)
        self.assertIn("m2_manifest.json", script)

    def test_m2_set_mandelstam_for_release_benchmarks(self):
        cases = {
            "B01_ee_to_mumu": 'SetMandelstam[s, t, u, p1, p2, -p3, -p4, SMP["m_e"], SMP["m_e"], SMP["m_mu"], SMP["m_mu"]]',
            "B02_compton": 'SetMandelstam[s, t, u, p1, k1, -p2, -k2, SMP["m_e"], 0, SMP["m_e"], 0]',
            "B03_emu_to_emu": 'SetMandelstam[s, t, u, p1, p2, -p3, -p4, SMP["m_e"], SMP["m_mu"], SMP["m_e"], SMP["m_mu"]]',
        }
        for benchmark, expected in cases.items():
            with self.subTest(benchmark=benchmark):
                script = build_native_qed_m2_script(self.load_physics(benchmark), self.native_config())
                self.assertIn(expected, script)

    def test_m2_amplitude_only_generates_script_without_execution(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            request = {
                "status": "approved",
                "execution_mode": "amplitude_only",
                "timeout_policy": {"kind": "none"},
                "allowed_operations": ["amplitude_generation"],
            }
            result = run_native_qed_m2_generator(
                self.load_physics("B01_ee_to_mumu"),
                Path(tmp),
                self.native_config(),
                request,
            )
            self.assertFalse(result["executed"])
            self.assertEqual(result["status"], "SCRIPT_GENERATED_ONLY")
            self.assertTrue((Path(tmp) / "compute_m2.wl").exists())
            self.assertFalse((Path(tmp) / "m2_raw.m").exists())

    def test_m2_benchmark_regression_requires_fixed_timeout_and_operations(self):
        request = {
            "status": "approved",
            "execution_mode": "benchmark_regression",
            "timeout_policy": {"kind": "none"},
            "allowed_operations": ["m2_regression", "spin_sums", "heavy_simplification"],
        }
        with self.assertRaisesRegex(NativeBackendError, "fixed_seconds"):
            run_native_qed_m2_generator(self.load_physics("B01_ee_to_mumu"), ROOT / "runs" / "unit_unused", self.native_config(), request)
        request["timeout_policy"] = {"kind": "fixed_seconds", "seconds": 120}
        with self.assertRaisesRegex(NativeBackendError, "polarization_sums"):
            run_native_qed_m2_generator(self.load_physics("B02_compton"), ROOT / "runs" / "unit_unused", self.native_config(), request)
    def test_unsupported_particle_refusal(self):
        physics = copy.deepcopy(self.load_physics("B01_ee_to_mumu"))
        physics["particles"]["incoming"][0]["particle_id"] = "tau-"
        with self.assertRaisesRegex(NativeBackendError, "unsupported native QED particle"):
            build_native_qed_script(physics, self.native_config())

    def test_non_qed_refusal(self):
        physics = copy.deepcopy(self.load_physics("B02_compton"))
        physics["coupling_order"]["orders"] = [{"coupling": "gs", "power": 2}]
        with self.assertRaisesRegex(NativeBackendError, "QED coupling order only"):
            validate_native_qed_request(physics, self.native_config())

    def test_backend_config_refuses_non_qed_restrictions(self):
        physics = self.load_physics("B01_ee_to_mumu")
        config = BackendConfig(restrictions="NoElectronHCoupling")
        with self.assertRaisesRegex(NativeBackendError, "QEDOnly"):
            build_native_qed_script(physics, config)

    def test_backend_profile_model_mismatch_refusal(self):
        physics = copy.deepcopy(self.load_physics("B01_ee_to_mumu"))
        physics["model_id"] = "other_model"
        with self.assertRaisesRegex(NativeBackendError, "model_id/sector"):
            validate_native_qed_request(physics, self.native_config())

    def test_no_benchmark_name_hardcoding_in_backend_source(self):
        source = (ROOT / "src" / "feynagent" / "backends" / "feynarts_feyncalc.py").read_text(encoding="utf-8")
        self.assertNotIn("PARTICLE_TO_FEYNARTS", source)
        for marker in ["B01", "B02", "B03", "b01", "b02", "b03", "ee_to_mumu", "compton"]:
            self.assertNotIn(marker, source)


if __name__ == "__main__":
    unittest.main()
