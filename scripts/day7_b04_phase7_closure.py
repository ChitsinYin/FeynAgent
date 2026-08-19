"""Close Day-7 B04 after the authorized manual reduced-M2 run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_phase7_closure import (
    AMPLITUDE_RUN_DEFAULT,
    M2_RUN_DEFAULT,
    run_phase7_closure,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--amplitude-run-id", default=AMPLITUDE_RUN_DEFAULT)
    parser.add_argument("--m2-run-id", default=M2_RUN_DEFAULT)
    args = parser.parse_args(argv)

    result = run_phase7_closure(
        ROOT,
        amplitude_run_id=args.amplitude_run_id,
        m2_run_id=args.m2_run_id,
    )
    print(f"phase7_status={result.status}")
    print(f"amplitude_run_id={result.amplitude_run_id}")
    print(f"m2_run_id={result.m2_run_id}")
    print(f"report={result.report_path}")
    print(f"validation={result.validation_path}")
    print(f"validation_sha256={result.validation_sha256}")
    print(f"run_manifest={result.run_manifest_path}")
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
