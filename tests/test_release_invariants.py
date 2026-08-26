import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseInvariantTests(unittest.TestCase):
    def test_release_invariant_script_passes(self):
        completed = subprocess.run(
            [sys.executable, "scripts/check_release_invariants.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
