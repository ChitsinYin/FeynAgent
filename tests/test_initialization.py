import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent import init as init_mod


PROBE_JSON = {
    "wolfram": {"version": "15.0.1 for Microsoft Windows"},
    "feyncalc": {"loaded": True, "version": "10.1.0", "directory": "C:/FeynCalc"},
    "feynarts": {"loaded": True, "version": "3.12", "directory": "C:/FeynArts", "loaded_via_feyncalc_addon": True},
    "paths": {"feyncalc_examples_root": None, "feynarts_models_root": "C:/FeynArts/Models"},
}


def completed(stdout):
    return subprocess.CompletedProcess(["wolframscript"], 0, stdout=stdout, stderr="")


class InitCliTests(unittest.TestCase):
    def probe_stdout(self):
        return "\n".join([
            "noise",
            "FEYNAGENT_PROBE_JSON_BEGIN",
            json.dumps(PROBE_JSON),
            "FEYNAGENT_PROBE_JSON_END",
        ])

    def test_probe_script_uses_feyncalc_addon_pattern(self):
        script = init_mod._wolfram_probe_script(None)
        self.assertIn('$LoadAddOns = {"FeynArts"};', script)
        self.assertIn('Get["FeynCalc`"]', script)
        self.assertNotIn('$LoadFeynArts = True', script)

    @mock.patch("feynagent.init._detect_latex_engine", return_value={"status": "WARNING", "engine": None})
    @mock.patch("feynagent.init.shutil.which")
    @mock.patch("feynagent.init.subprocess.run")
    def test_init_writes_local_files_with_mocked_probe(self, run, which, _latex):
        which.side_effect = lambda name: "wolframscript" if name == "wolframscript" else None
        run.return_value = completed(self.probe_stdout())
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(init_mod, "LOCAL_DIR", Path(tmp) / ".feynagent"), \
                 mock.patch.object(init_mod, "ENVIRONMENT_YAML", Path(tmp) / ".feynagent" / "environment.yaml"), \
                 mock.patch.object(init_mod, "CAPABILITY_REPORT_JSON", Path(tmp) / ".feynagent" / "capability_report.json"), \
                 mock.patch.object(init_mod, "REFERENCE_INDEX_JSON", Path(tmp) / ".feynagent" / "reference_index.json"):
                args = argparse.Namespace(wolframscript=None, feyncalc_dir=None, timeout=5)
                result = init_mod.run_init(args)
                self.assertEqual(result.status, "WARNING")
                self.assertTrue(init_mod.ENVIRONMENT_YAML.exists())
                self.assertTrue(init_mod.CAPABILITY_REPORT_JSON.exists())
                self.assertTrue(init_mod.REFERENCE_INDEX_JSON.exists())
                report = json.loads(init_mod.CAPABILITY_REPORT_JSON.read_text(encoding="utf-8"))
                self.assertEqual(report["checks"]["wolfram"]["status"], "PASS")
                self.assertEqual(report["checks"]["latex"]["status"], "WARNING")

    @mock.patch("feynagent.init.shutil.which", return_value=None)
    def test_missing_wolframscript_fails_without_installing(self, _which):
        args = argparse.Namespace(wolframscript=None, feyncalc_dir=None, timeout=1)
        result = init_mod.probe_environment(args)
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(result.capabilities["checks"]["wolfram"]["status"], "FAIL")

    @mock.patch("feynagent.init._detect_latex_engine", return_value={"status": "PASS", "engine": "lualatex"})
    @mock.patch("feynagent.init.shutil.which")
    @mock.patch("feynagent.init.subprocess.run")
    def test_explicit_wolframscript_is_used(self, run, which, _latex):
        which.return_value = None
        run.return_value = completed(self.probe_stdout())
        args = argparse.Namespace(wolframscript="C:/Wolfram/wolframscript.exe", feyncalc_dir="C:/FeynCalc", timeout=5)
        result = init_mod.probe_environment(args)
        self.assertEqual(result.capabilities["checks"]["wolfram"]["status"], "PASS")
        self.assertEqual(run.call_args.args[0][0], "C:/Wolfram/wolframscript.exe")

    def test_reference_index_hashes_metadata_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Examples"
            root.mkdir()
            example = root / "Example.m"
            example.write_text("(* Example title *)\nPrint[1]", encoding="utf-8")
            probe = {"paths": {"feyncalc_examples_root": str(root)}}
            index = init_mod._build_reference_index(probe)
            self.assertEqual(index["entry_count"], 1)
            self.assertEqual(index["entries"][0]["relative_path"], "Example.m")
            self.assertIn("sha256", index["entries"][0])


class LocalSmokeTests(unittest.TestCase):
    def test_real_local_doctor_probe_if_wolframscript_available(self):
        wolframscript = shutil.which("wolframscript")
        if not wolframscript:
            self.skipTest("wolframscript not available on PATH")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        completed = subprocess.run(
            [sys.executable, "-m", "feynagent", "doctor", "--timeout", "45"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
        )
        self.assertIn("FeynAgent doctor:", completed.stdout)
        self.assertIn(completed.returncode, {0, 1})


if __name__ == "__main__":
    unittest.main()
