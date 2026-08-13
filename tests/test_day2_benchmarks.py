import hashlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.diagrams import diagram_signature, generate_tree_2_to_2
from test_topology_generator import synthetic_scalar_fixture


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


BENCHMARKS = {
    "B01_ee_to_mumu": {"channels": {"s"}},
    "B02_compton": {"channels": {"s", "u"}},
}


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalized_sha256(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Day2BenchmarkGenerationTests(unittest.TestCase):
    def setUp(self):
        self.registry_path = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"
        self.registry = load_yaml(self.registry_path)
        self.legacy_profile = load_yaml(ROOT / "profiles" / "backends" / "legacy_sm_qed.yaml")
        self.rule_ids = {
            rule["rule_id"]
            for rule in self.registry["vertices"] + self.registry["propagators"]
        }

    def generated_and_gold(self, benchmark):
        bench_dir = ROOT / "benchmarks" / benchmark
        physics = load_yaml(bench_dir / "physics_card.yaml")
        convention = load_yaml(bench_dir / "convention_card.yaml")
        gold = load_yaml(bench_dir / "legacy" / "diagrams.yaml")
        generated = generate_tree_2_to_2(physics, convention, self.registry, self.legacy_profile)
        generated_again = generate_tree_2_to_2(physics, convention, self.registry, self.legacy_profile)
        return bench_dir, generated, generated_again, gold

    def test_b01_and_b02_generated_channels_match_expected(self):
        for benchmark, expected in BENCHMARKS.items():
            with self.subTest(benchmark=benchmark):
                _, generated, _, _ = self.generated_and_gold(benchmark)
                self.assertEqual({diagram["channel"] for diagram in generated["diagrams"]}, expected["channels"])

    def test_b02_does_not_generate_t_or_contact(self):
        _, generated, _, _ = self.generated_and_gold("B02_compton")
        self.assertNotIn("t", {diagram["channel"] for diagram in generated["diagrams"]})
        self.assertNotIn("contact", {diagram["channel"] for diagram in generated["diagrams"]})

    def test_generated_matches_gold_by_structural_signature(self):
        for benchmark in BENCHMARKS:
            with self.subTest(benchmark=benchmark):
                _, generated, _, gold = self.generated_and_gold(benchmark)
                generated_sigs = {diagram_signature(diagram) for diagram in generated["diagrams"]}
                gold_sigs = {diagram_signature(diagram) for diagram in gold["diagrams"]}
                self.assertEqual(generated_sigs, gold_sigs)

    def test_generator_is_deterministic_on_repeated_runs(self):
        for benchmark in BENCHMARKS:
            with self.subTest(benchmark=benchmark):
                _, generated, generated_again, _ = self.generated_and_gold(benchmark)
                first = [diagram_signature(diagram) for diagram in generated["diagrams"]]
                second = [diagram_signature(diagram) for diagram in generated_again["diagrams"]]
                self.assertEqual(first, second)

    def test_every_generated_vertex_has_complete_slot_bindings(self):
        for benchmark in BENCHMARKS:
            with self.subTest(benchmark=benchmark):
                _, generated, _, _ = self.generated_and_gold(benchmark)
                vertex_rules = {rule["rule_id"]: rule for rule in self.registry["vertices"]}
                for diagram in generated["diagrams"]:
                    for vertex in diagram["vertex_instances"]:
                        expected_slots = {
                            field["slot"]
                            for field in vertex_rules[vertex["rule_id"]]["participating_fields"]
                        }
                        bound_slots = [binding["rule_slot"] for binding in vertex["slot_bindings"]]
                        self.assertEqual(set(bound_slots), expected_slots)
                        self.assertEqual(len(bound_slots), len(set(bound_slots)))

    def test_all_generated_rule_ids_resolve_against_canonical_registry(self):
        for benchmark in BENCHMARKS:
            with self.subTest(benchmark=benchmark):
                _, generated, _, _ = self.generated_and_gold(benchmark)
                for diagram in generated["diagrams"]:
                    for reference in diagram["rule_references"]:
                        self.assertIn(reference["rule_id"], self.rule_ids)
                    for vertex in diagram["vertex_instances"]:
                        self.assertIn(vertex["rule_id"], self.rule_ids)
                    for line in diagram["internal_lines"]:
                        self.assertIn(line["propagator_rule_id"], self.rule_ids)

    def test_benchmark_manifests_are_not_editable_rule_copies(self):
        canonical_hash = normalized_sha256(self.registry_path)
        for benchmark in BENCHMARKS:
            with self.subTest(benchmark=benchmark):
                manifest = load_yaml(ROOT / "benchmarks" / benchmark / "legacy" / "rule_manifest.yaml")
                self.assertNotIn("vertices", manifest)
                self.assertNotIn("propagators", manifest)
                self.assertEqual(manifest["canonical_registry"]["registry_id"], self.registry["registry_id"])
                self.assertEqual(manifest["canonical_registry"]["source_sha256"], canonical_hash)

    def test_synthetic_anti_hardcoding_fixture_still_works(self):
        physics, convention, registry = synthetic_scalar_fixture()
        generated = generate_tree_2_to_2(physics, convention, registry)
        self.assertEqual({diagram["channel"] for diagram in generated["diagrams"]}, {"s"})
        self.assertEqual(generated["diagrams"][0]["internal_lines"][0]["particle_id"], "xray")


if __name__ == "__main__":
    unittest.main()

