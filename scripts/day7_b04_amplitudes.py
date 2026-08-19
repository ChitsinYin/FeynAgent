"""Run Day-7 B04 custom-gravity amplitude closure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_amplitudes import run_b04_amplitude_closure


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", help="Stable run id under runs/. Defaults to a UTC timestamp.")
    parser.add_argument("--latex-command", default="lualatex")
    args = parser.parse_args(argv)

    result = run_b04_amplitude_closure(ROOT, run_id=args.run_id, latex_command=args.latex_command)
    print(f"run_id={result.run_id}")
    print(f"run_dir={result.run_dir}")
    print(f"amplitudes_dir={result.amplitudes_dir}")
    print(f"report={result.report_path}")
    print(f"amplitudes_pdf={result.pdf_path}")
    print(f"amplitudes_pdf_sha256={result.pdf_sha256}")
    for amp, classification in result.classifications.items():
        print(f"{amp}={classification}")
    print(f"m2_stopped_before={result.stopped_before_m2}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
