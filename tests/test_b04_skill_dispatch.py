import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent import init as init_mod
from feynagent import runner
from feynagent.backends.b04_custom import B04CustomBackendError, validate_b04_custom_execution
from feynagent.custom_knowledge import CONFLICT_REQUIRES_REVIEW, KnowledgeVerification
from feynagent.dispatch import (
    B04_CUSTOM_BACKEND,
    NATIVE_QED_BACKEND,
    DispatchError,
    resolve_backend_route,
)

try:
    import jsonschema
    import yaml
except ImportError:  # pragma: no cover
    jsonschema = None
    yaml = None


B04_CARD = ROOT / "benchmarks" / "B04_phi_phi_to_hh" / "physics_card.yaml"
B04_PROFILE = ROOT / "profiles" / "backends" / "b04_custom_gravity_audited.yaml"
QED_CARD = ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml"
QED_PROFILE = ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class B04DispatchTests(unittest.TestCase):
    def setUp(self):
        if yaml is None or jsonschema is None:
            raise unittest.SkipTest("PyYAML/jsonschema are required")

    def test_standard_qed_route_is_unchanged(self):
        route = resolve_backend_route(load_yaml(QED_CARD), load_yaml(QED_PROFILE), custom_model_ids={"reheating_scalar_gravity_v1"})
        self.assertEqual(route.classification, "standard_native")
        self.assertEqual(route.backend_id, NATIVE_QED_BACKEND)
        self.assertTrue(route.standard_qed_authority)

    def test_b04_routes_only_to_audited_custom_backend(self):
        route = resolve_backend_route(load_yaml(B04_CARD), load_yaml(B04_PROFILE), custom_model_ids={"reheating_scalar_gravity_v1"})
        self.assertEqual(route.classification, "custom_audited")
        self.assertEqual(route.backend_id, B04_CUSTOM_BACKEND)
        self.assertFalse(route.standard_qed_authority)
        with self.assertRaises(DispatchError):
            resolve_backend_route(load_yaml(B04_CARD), load_yaml(QED_PROFILE), custom_model_ids={"reheating_scalar_gravity_v1"})

    def test_arbitrary_registered_bsm_has_no_execution_route(self):
        card = load_yaml(B04_CARD)
        card["model_id"] = "arbitrary_bsm_model"
        card["process_id"] = "process:arbitrary_bsm"
        card["sector"] = "bsm"
        with self.assertRaisesRegex(DispatchError, "only locked B04"):
            resolve_backend_route(card, load_yaml(B04_PROFILE), custom_model_ids={"arbitrary_bsm_model"})

    def test_audited_custom_profile_validates(self):
        schema = json.loads((ROOT / "schemas" / "backend_profile.schema.json").read_text(encoding="utf-8"))
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        errors = list(validator_cls(schema).iter_errors(load_yaml(B04_PROFILE)))
        self.assertEqual(errors, [])

    def test_custom_backend_requires_explicit_approved_execution_request(self):
        card = load_yaml(B04_CARD)
        profile = load_yaml(B04_PROFILE)
        route = resolve_backend_route(card, profile, custom_model_ids={"reheating_scalar_gravity_v1"})
        request = b04_execution_request()
        request["status"] = "draft"
        with self.assertRaisesRegex(B04CustomBackendError, "approved ExecutionRequest"):
            validate_b04_custom_execution(ROOT, card, profile, request, route)
        request = b04_execution_request()
        request["allowed_operations"].remove("amplitude_generation")
        with self.assertRaisesRegex(B04CustomBackendError, "amplitude_generation"):
            validate_b04_custom_execution(ROOT, card, profile, request, route)

    def test_capability_conflict_is_reported_as_conflict(self):
        capability = KnowledgeVerification(
            model_id="reheating_scalar_gravity_v1",
            status=CONFLICT_REQUIRES_REVIEW,
        ).as_capability()
        self.assertEqual(capability["status"], "CONFLICT")
        result = init_mod.ProbeResult(
            status="PASS",
            environment={},
            capabilities={
                "checks": {name: {"status": "PASS"} for name in ("wolfram", "feyncalc", "feynarts", "native_qed_tree_capability", "latex")},
                "custom_models": [capability],
            },
            reference_index={},
        )
        self.assertIn("custom_model:reheating_scalar_gravity_v1 CONFLICT", init_mod._doctor_text(result))

    def test_skill_natural_language_eval(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "skills" / "feynagent" / "scripts" / "run_feynagent.py"), "eval"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["passed"])
        b04 = next(item for item in payload["results"] if item["id"] == "b04_natural_language_custom_route")
        self.assertEqual(b04["actual"]["backend"], B04_CUSTOM_BACKEND)
        self.assertFalse(b04["actual"]["standard_qed_authority"])


class B04RunnerDispatchTests(unittest.TestCase):
    def setUp(self):
        if yaml is None or jsonschema is None:
            raise unittest.SkipTest("PyYAML/jsonschema are required")

    def test_runner_dispatches_b04_without_executing_m2(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            request_path = tmp_path / "execution_request.yaml"
            request_path.write_text(yaml.safe_dump(b04_execution_request(), sort_keys=False), encoding="utf-8", newline="\n")
            with mock.patch("feynagent.runner.probe_environment", return_value=ready_custom_doctor()), \
                 mock.patch("feynagent.runner.validate_b04_custom_execution", return_value={"status": "PASS"}), \
                 mock.patch("feynagent.runner.run_b04_custom_backend", side_effect=fake_custom_backend):
                result = runner.run_from_files(
                    physics_card_path=B04_CARD,
                    backend_profile_path=B04_PROFILE,
                    execution_request_path=request_path,
                    run_root=tmp_path / "runs",
                )
            self.assertEqual(result.status, "PASS")
            self.assertEqual(result.manifest["dispatch"]["classification"], "custom_audited")
            self.assertEqual(result.manifest["dispatch"]["backend_id"], B04_CUSTOM_BACKEND)
            self.assertFalse(result.manifest["dispatch"]["standard_qed_authority"])
            self.assertEqual(result.manifest["custom_manifest"]["topology"]["diagram_count"], 4)
            self.assertEqual(result.manifest["custom_manifest"]["amplitudes"]["per_diagram_count"], 4)
            self.assertEqual(result.manifest["m2_policy"]["status"], "NOT_AUTHORIZED")
            self.assertFalse(result.manifest["m2_policy"]["executed"])


def b04_execution_request():
    return {
        "schema_version": "0.1.0",
        "object_id": "execution_request:b04_skill_test",
        "status": "approved",
        "request_id": "execution_request:b04_skill_test",
        "physics_card_id": "physics_card:b04_phi_phi_to_hh",
        "backend_profile_id": "backend_profile:b04_custom_gravity_audited",
        "execution_mode": "amplitude_only",
        "authorized_by": "unit-test",
        "authorized_at": "2026-08-19T12:00:00+08:00",
        "timeout_policy": {"kind": "fixed_seconds", "seconds": 120},
        "allowed_operations": ["schema_validation", "diagram_generation", "amplitude_generation", "latex_render"],
        "metadata": {"created_by": "unit-test"},
    }


def ready_custom_doctor():
    return SimpleNamespace(
        status="PASS",
        capabilities={
            "checks": {"native_qed_tree_capability": {"status": "PASS"}},
            "custom_models": [{"model_id": "reheating_scalar_gravity_v1", "status": "AVAILABLE"}],
        },
    )


def fake_custom_backend(_root, *, run_id, run_dir, **_kwargs):
    return {
        "status": "PASS",
        "backend_id": B04_CUSTOM_BACKEND,
        "standard_qed_authority": False,
        "topology": {"status": "PASS", "diagram_count": 4, "rule_usage_audit": "PASS"},
        "amplitudes": {
            "status": "PASS",
            "per_diagram_count": 4,
            "classifications": {
                "amp_001": "PASS_AFTER_EXPLICIT_CONVENTION_MAP",
                "amp_002": "PASS_AFTER_EXPLICIT_CONVENTION_MAP",
                "amp_003": "PASS",
                "amp_004": "PASS",
            },
        },
        "m2_policy": {"status": "NOT_AUTHORIZED", "executed": False, "automatic_execution": False},
        "validation_report": {"schema_version": "0.1.0", "status": "PASS", "checks": []},
    }


if __name__ == "__main__":
    unittest.main()
