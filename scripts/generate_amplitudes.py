"""Generate Day-3 AmplitudeIR backend artifacts for approved benchmarks."""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.amplitudes import build_amplitude_ir, write_backend_outputs

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required; install with python -m pip install -e .[dev]") from exc


BENCHMARKS = ["B01_ee_to_mumu", "B02_compton"]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalized_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_for_benchmark(benchmark: str) -> dict:
    bench_dir = ROOT / "benchmarks" / benchmark
    physics = load_yaml(bench_dir / "physics_card.yaml")
    convention = load_yaml(bench_dir / "convention_card.yaml")
    registry_path = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"
    diagrams_path = bench_dir / "diagrams.yaml"
    registry = load_yaml(registry_path)
    diagrams = load_yaml(diagrams_path)
    hashes = {
        "rule_registry": normalized_sha256(registry_path),
        "diagram_ir": normalized_sha256(diagrams_path),
    }
    return build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmarks", nargs="*")
    args = parser.parse_args()

    selected = args.benchmarks or BENCHMARKS
    unknown = sorted(set(selected) - set(BENCHMARKS))
    if unknown:
        parser.error(f"unknown benchmark(s): {unknown}")

    generated_at = datetime.now(ZoneInfo("Asia/Shanghai")).astimezone().isoformat()
    for benchmark in selected:
        amplitude_ir = build_for_benchmark(benchmark)
        written = write_backend_outputs(amplitude_ir, ROOT / "benchmarks" / benchmark, benchmark, generated_at)
        for path in written:
            print(path.relative_to(ROOT).as_posix())
    print(f"generated_at={generated_at}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
