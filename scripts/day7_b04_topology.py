"""Run Day-7 Phase 5 B04 topology and diagram closure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_topology import run_b04_topology_phase


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", help="Stable run id under runs/. Defaults to a UTC timestamp.")
    parser.add_argument("--latex-command", default="lualatex")
    args = parser.parse_args(argv)

    result = run_b04_topology_phase(ROOT, run_id=args.run_id, latex_command=args.latex_command)
    print(f"run_id={result.run_id}")
    print(f"run_dir={result.run_dir}")
    print(f"report={result.report_path}")
    print(f"gold_topology_count={result.gold_topology_count}")
    print(f"generated_topology_count={result.generated_topology_count}")
    print(f"topology_comparison={'PASS' if result.topology_comparison_pass else 'FAIL'}")
    print(f"rule_usage_audit={'PASS' if result.rule_usage_audit_pass else 'FAIL'}")
    print(f"diagram_pdf={'PASS' if result.diagram_pdf_pass else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
