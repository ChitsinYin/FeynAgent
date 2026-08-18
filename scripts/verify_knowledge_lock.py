"""Verify a registered external custom knowledge lock without running amplitudes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.custom_knowledge import AVAILABLE, DEFAULT_B04_MANIFEST, DEFAULT_MAPPING_PATH, verify_knowledge_lock


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", default="reheating_scalar_gravity_v1")
    parser.add_argument("--benchmark-manifest", default=str(DEFAULT_B04_MANIFEST))
    parser.add_argument("--mapping", default=str(DEFAULT_MAPPING_PATH))
    args = parser.parse_args(argv)

    result = verify_knowledge_lock(
        model_id=args.model_id,
        benchmark_manifest_path=Path(args.benchmark_manifest),
        mapping_path=Path(args.mapping),
    )
    print(f"custom_model:{result.model_id} {result.status}")
    print(f"checked_hashes: {result.checked_hashes}")
    if result.readiness:
        print(f"readiness: {result.readiness}")
    if result.process_id:
        print(f"process_id: {result.process_id}")
    for issue in result.issues:
        print(f"issue: {issue}")
    return 0 if result.status == AVAILABLE else 1


if __name__ == "__main__":
    raise SystemExit(main())
