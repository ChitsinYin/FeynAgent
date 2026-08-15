import json
import shutil
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
from feynagent.backends import native_qed_channel_plan

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


ALL_RUNNER_OPERATIONS = [
    "schema_validation",
    "diagram_generation",
    "amplitude_generation",
    "latex_render",
    "feyncalc_smoke",
    "m2_regression",
    "spin_sums",
    "polarization_sums",
    "heavy_simplification",
]


class DeterministicRunnerCliTests(unittest.TestCase):
    def setUp(self):
        if yaml is None:
            raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.profile = ROOT / "profiles" / "backends" / "feynarts_sm_qed.yaml"

    def tearDown(self):
        self.tmp.cleanup()

    def test_b01_full_runner(self):
        run_dir = self._run_cli_for_benchmark("B01_ee_to_mumu")
        self._assert_complete_public_bundle(run_dir, expected_channels=["s"])

    def test_b02_full_runner(self):
        run_dir = self._run_cli_for_benchmark("B02_compton")
        self._assert_complete_public_bundle(run_dir, expected_channels=["s", "u"])

    def test_b03_full_runner(self):
        run_dir = self._run_cli_for_benchmark("B03_emu_to_emu")
        self._assert_complete_public_bundle(run_dir, expected_channels=["t"])

    def test_refused_heavy_execution_returns_nonzero(self):
        physics = ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml"
        request = self._write_execution_request(
            physics_card_id="physics_card:b01_ee_to_mumu",
            execution_mode="production_heavy",
            allowed_operations=[op for op in ALL_RUNNER_OPERATIONS if op != "heavy_simplification"],
        )
        run_root = self.base / "runs"
        with mock.patch("feynagent.runner.probe_environment", return_value=_ready_doctor()), \
             mock.patch("feynagent.runner.run_native_qed_backend", side_effect=_fake_native_backend):
            exit_code = init_mod.main([
                "run",
                "--physics-card",
                str(physics),
                "--backend-profile",
                str(self.profile),
                "--execution-request",
                str(request),
                "--run-root",
                str(run_root),
            ])
        self.assertEqual(exit_code, 1)
        manifest = self._single_manifest(run_root)
        self.assertEqual(manifest["failure"]["gate"], "m2_authorization")
        self.assertIn("heavy_simplification", manifest["failure"]["message"])

    def test_timeout_returns_nonzero_and_manifest(self):
        physics = ROOT / "benchmarks" / "B02_compton" / "physics_card.yaml"
        request = self._write_execution_request(physics_card_id="physics_card:b02_compton")
        run_root = self.base / "runs"
        with mock.patch("feynagent.runner.probe_environment", return_value=_ready_doctor()), \
             mock.patch("feynagent.runner.run_native_qed_backend", side_effect=_fake_native_backend), \
             mock.patch(
                 "feynagent.runner.run_native_qed_m2_generator",
                 side_effect=subprocess.TimeoutExpired(["wolframscript"], timeout=1),
             ):
            exit_code = init_mod.main([
                "run",
                "--physics-card",
                str(physics),
                "--backend-profile",
                str(self.profile),
                "--execution-request",
                str(request),
                "--run-root",
                str(run_root),
            ])
        self.assertEqual(exit_code, 1)
        manifest = self._single_manifest(run_root)
        self.assertEqual(manifest["failure"]["gate"], "timeout")

    def test_invalid_profile_returns_nonzero(self):
        physics = ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml"
        bad_profile = self.base / "bad_profile.yaml"
        profile_data = yaml.safe_load(self.profile.read_text(encoding="utf-8"))
        del profile_data["native"]["feynarts"]["particle_mappings"]
        bad_profile.write_text(yaml.safe_dump(profile_data, sort_keys=False), encoding="utf-8")
        request = self._write_execution_request(physics_card_id="physics_card:b01_ee_to_mumu")
        exit_code = init_mod.main([
            "run",
            "--physics-card",
            str(physics),
            "--backend-profile",
            str(bad_profile),
            "--execution-request",
            str(request),
            "--run-root",
            str(self.base / "runs"),
        ])
        self.assertEqual(exit_code, 1)

    def _run_cli_for_benchmark(self, benchmark):
        physics = ROOT / "benchmarks" / benchmark / "physics_card.yaml"
        physics_card = yaml.safe_load(physics.read_text(encoding="utf-8"))
        request = self._write_execution_request(physics_card_id=physics_card["object_id"])
        run_root = self.base / "runs"
        with mock.patch("feynagent.runner.probe_environment", return_value=_ready_doctor()), \
             mock.patch("feynagent.runner.run_native_qed_backend", side_effect=_fake_native_backend), \
             mock.patch("feynagent.runner.run_native_qed_m2_generator", side_effect=_fake_m2_generator):
            exit_code = init_mod.main([
                "run",
                "--physics-card",
                str(physics),
                "--backend-profile",
                str(self.profile),
                "--execution-request",
                str(request),
                "--run-root",
                str(run_root),
            ])
        self.assertEqual(exit_code, 0)
        return next(path for path in run_root.iterdir() if path.is_dir())

    def _write_execution_request(
        self,
        *,
        physics_card_id,
        execution_mode="benchmark_regression",
        allowed_operations=None,
        timeout_policy=None,
    ):
        data = {
            "schema_version": "0.1.0",
            "object_id": f"execution_request:{physics_card_id.split(':')[-1]}",
            "status": "approved",
            "request_id": f"execution_request:{physics_card_id.split(':')[-1]}",
            "physics_card_id": physics_card_id,
            "backend_profile_id": "backend_profile:feynarts_sm_qed",
            "execution_mode": execution_mode,
            "authorized_by": "unit-test",
            "authorized_at": "2026-08-15T10:00:00+08:00",
            "timeout_policy": timeout_policy or {"kind": "fixed_seconds", "seconds": 60},
            "allowed_operations": allowed_operations or ALL_RUNNER_OPERATIONS,
            "metadata": {"created_by": "unit-test"},
        }
        path = self.base / f"{data['object_id'].replace(':', '_')}.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def _assert_complete_public_bundle(self, run_dir, *, expected_channels):
        required = [
            "diagrams.pdf",
            "diagram_source.m",
            "amplitudes.tex",
            "amplitudes.pdf",
            "amplitudes.json",
            "feyncalc_amplitudes.m",
            "native_amplitude.wl",
            "compute_m2.wl",
            "m2_manifest.json",
            "validation_report.json",
            "run_manifest.json",
            "stdout.log",
            "stderr.log",
        ]
        for name in required:
            self.assertTrue((run_dir / name).exists(), name)
        manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
        report = json.loads((run_dir / "validation_report.json").read_text(encoding="utf-8"))
        amplitudes = json.loads((run_dir / "amplitudes.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "PASS")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual([item["channel"] for item in amplitudes["diagrams"]], expected_channels)
        self.assertEqual(manifest["inputs"]["physics_card"]["sha256"], runner._sha256(run_dir / "inputs" / "physics_card.yaml"))

    def _single_manifest(self, run_root):
        run_dirs = [path for path in run_root.iterdir() if path.is_dir()]
        self.assertEqual(len(run_dirs), 1)
        return json.loads((run_dirs[0] / "run_manifest.json").read_text(encoding="utf-8"))


def _ready_doctor():
    return SimpleNamespace(
        status="PASS",
        capabilities={"checks": {"native_qed_tree_capability": {"status": "PASS"}}},
    )


def _fake_native_backend(physics_card, output_dir, config, **_kwargs):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    channels = native_qed_channel_plan(physics_card)
    expression_ids = [f"expr:{physics_card['process_id']}:diagram:{index}" for index in range(1, len(channels) + 1)]
    metadata = {
        "backend_profile_id": config.backend_profile_id,
        "backend_id": config.backend_id,
        "process_id": physics_card["process_id"],
        "diagram_count": len(channels),
        "channel_count": len(channels),
        "per_diagram_amplitude_count": len(channels),
        "diagram_rendering_route": "unit_fake",
        "diagram_source": "diagram_source.m",
        "diagrams_pdf": "diagrams.pdf",
        "feyncalc_amplitudes_file": "feyncalc_amplitudes.m",
        "latex_file": "amplitudes.tex",
        "latex_pdf": "amplitudes.pdf",
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
            "expression_id": f"expr:{physics_card['process_id']}:total",
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
    files = {
        "native_amplitude.wl": "native script",
        "stdout.log": "stdout",
        "stderr.log": "",
        "native_summary.json": json.dumps({"diagram_count": len(channels)}),
        "diagram_source.m": "diags",
        "diagram_source.inputform.txt": "diags",
        "diagram_source.paint.inputform.txt": "paint",
        "diagrams.pdf": "%PDF-1.4\n",
        "raw_feynarts_amplitude.m": "raw",
        "raw_feynarts_amplitude.inputform.txt": "raw",
        "raw_feynarts_amplitudes.m": "raw diagrams",
        "feyncalc_amplitude.m": "amp",
        "feyncalc_amplitude.inputform.txt": "amp",
        "feyncalc_amplitudes.m": "amps",
        "amplitudes.tex": "\\documentclass{article}",
        "amplitudes.pdf": "%PDF-1.4\n",
        "amplitudes.json": json.dumps(metadata),
        "run_manifest.json": json.dumps({"status": "native"}),
    }
    for name, content in files.items():
        (output / name).write_text(content, encoding="utf-8")
    return {"exit_code": 0, "artifact_validation": [], "amplitudes": metadata, "outputs": {}}


def _fake_m2_generator(physics_card, output_dir, config, execution_request, **_kwargs):
    output = Path(output_dir)
    result = {
        "backend_profile_id": config.backend_profile_id,
        "backend_id": config.backend_id,
        "process_id": physics_card["process_id"],
        "script_path": "compute_m2.wl",
        "script_sha256": "unit",
        "authorization": {"path": execution_request["execution_mode"], "execute": True},
        "executed": True,
        "exit_code": 0,
        "status": "PASS",
        "script_manifest": {"status": "PASS", "runtime_seconds": 0.01},
        "outputs": {},
    }
    for name in ["compute_m2.wl", "m2_raw.m", "m2_simplified.m", "m2_inputform.txt", "m2_stdout.log", "m2_stderr.log"]:
        (output / name).write_text(name, encoding="utf-8")
    (output / "m2_manifest.json").write_text(json.dumps(result), encoding="utf-8")
    return result


if __name__ == "__main__":
    unittest.main()
