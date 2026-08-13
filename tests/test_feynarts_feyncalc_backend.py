import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.backends import BackendConfig, NativeBackendError, backend_config_from_dict, build_native_qed_script, validate_native_qed_request

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
