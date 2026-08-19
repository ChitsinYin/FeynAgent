import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_topology import (
    build_rule_registry_from_locked_rules,
    build_topology_convention_card,
    compare_generated_to_gold,
    expected_gold_topologies,
    annotate_diagram_ir,
    physics_card_for_topology,
    rule_usage_audit,
)
from feynagent.diagrams import diagram_signature, generate_tree_2_to_2
from feynagent.render import render_tikz_feynman

try:
    import jsonschema
    import yaml
except ImportError:  # pragma: no cover
    jsonschema = None
    yaml = None


B04 = ROOT / "benchmarks" / "B04_phi_phi_to_hh"


MODEL_FIXTURE = {
    "fields": [
        {"particle_id": "phi", "field_type": "real_scalar", "self_conjugate": True, "role": "inflaton"},
        {"particle_id": "h", "field_type": "massless_spin2_symmetric_tensor", "self_conjugate": True, "role": "graviton"},
    ]
}

RULES_FIXTURE = {
    "rules": [
        {"rule_id": "propagator:phi", "rule_type": "propagator", "fields": ["phi", "phi"], "momentum": "q", "latex": "i/(q^2-M^2+i epsilon)", "feyncalc_template": "I/(SP[q,q]-M^2+I epsilon)", "trust_status": "trusted_literature_and_gold_match"},
        {"rule_id": "vertex:h_phi_phi", "rule_type": "vertex", "fields": ["h", "phi", "phi"], "latex": "(i kappa/2)[...]", "trust_status": "trusted_literature_and_gold_match"},
        {"rule_id": "propagator:h", "rule_type": "propagator", "fields": ["h", "h"], "momentum": "q", "latex": "i tensor/(2 q^2)", "trust_status": "trusted_literature_and_gold_match"},
        {"rule_id": "vertex:h_h_h", "rule_type": "vertex", "fields": ["h", "h", "h"], "latex_compact_source_form": "i kappa [Sym]{...}", "trust_status": "trusted_literature_and_gold_match"},
        {"rule_id": "vertex:h_h_phi_phi", "rule_type": "vertex", "fields": ["h", "h", "phi", "phi"], "latex": "-i kappa^2 {...}", "trust_status": "trusted_corrected_gold_and_literature"},
    ]
}


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is required")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_validates(testcase, instance, schema_name):
    if jsonschema is None:
        raise unittest.SkipTest("jsonschema is required")
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    errors = sorted(validator_cls(schema).iter_errors(instance), key=lambda error: list(error.path))
    testcase.assertEqual(errors, [])


class B04TopologyPhase5Tests(unittest.TestCase):
    def inputs(self):
        physics = load_yaml(B04 / "physics_card.yaml")
        convention_ref = load_yaml(B04 / "convention_reference.yaml")
        process = load_yaml(B04 / "expected_topology.yaml")
        convention = build_topology_convention_card(convention_ref)
        registry = build_rule_registry_from_locked_rules(MODEL_FIXTURE, RULES_FIXTURE)
        topology_physics = physics_card_for_topology(physics)
        generated = annotate_diagram_ir(generate_tree_2_to_2(topology_physics, convention, registry), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        return topology_physics, convention, registry, process, generated

    def test_expected_topology_count_from_sanitized_benchmark_fixture(self):
        _, _, _, process, generated = self.inputs()
        gold = expected_gold_topologies(process)
        self.assertEqual(len(gold), len(process["diagrams"]))
        self.assertEqual(len(generated["diagrams"]), len(gold))

    def test_stable_diagram_ids_internal_species_and_momentum_routing(self):
        _, _, _, _, generated = self.inputs()
        by_channel = {diagram["channel"]: diagram for diagram in generated["diagrams"]}
        self.assertEqual(by_channel["s"]["diagram_id"], "diagram:generated:b04-phi-phi-to-h-h:s:h")
        self.assertEqual(by_channel["t"]["diagram_id"], "diagram:generated:b04-phi-phi-to-h-h:t:phi")
        self.assertEqual(by_channel["u"]["diagram_id"], "diagram:generated:b04-phi-phi-to-h-h:u:phi")
        self.assertEqual(by_channel["contact"]["diagram_id"], "diagram:generated:b04-phi-phi-to-h-h:contact:h_h_phi_phi")
        self.assertEqual(by_channel["s"]["internal_lines"][0]["particle_id"], "h")
        self.assertEqual(by_channel["s"]["internal_lines"][0]["momentum"]["expression"], "p1+p2")
        self.assertEqual(by_channel["t"]["internal_lines"][0]["particle_id"], "phi")
        self.assertEqual(by_channel["t"]["internal_lines"][0]["momentum"]["expression"], "p1-k1")
        self.assertEqual(by_channel["u"]["internal_lines"][0]["momentum"]["expression"], "p1-k2")

    def test_rule_usage_and_duplicate_suppression(self):
        physics, convention, registry, _, generated = self.inputs()
        usage = rule_usage_audit(generated, {"propagator:phi", "vertex:h_phi_phi", "propagator:h", "vertex:h_h_h", "vertex:h_h_phi_phi"})
        self.assertEqual(usage["status"], "PASS")
        self.assertEqual(usage["unexpected_rule_ids"], [])
        duplicate_registry = json.loads(json.dumps(registry))
        duplicate_registry["vertices"].extend(json.loads(json.dumps(registry["vertices"])))
        duplicate_generated = generate_tree_2_to_2(physics, convention, duplicate_registry)
        signatures = [diagram_signature(diagram) for diagram in duplicate_generated["diagrams"]]
        self.assertEqual(len(signatures), len(set(signatures)))
        self.assertEqual(len(duplicate_generated["diagrams"]), len(generated["diagrams"]))

    def test_structural_gold_comparison_has_no_unexpected_topology(self):
        _, _, _, process, generated = self.inputs()
        comparison = compare_generated_to_gold(generated, expected_gold_topologies(process))
        self.assertEqual(comparison["status"], "PASS")
        classifications = {row["gold_label"]: row["classification"] for row in comparison["rows"]}
        self.assertEqual(classifications["c"], "MATCH")
        self.assertEqual(classifications["d"], "MATCH")
        self.assertEqual(classifications["a"], "MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP")
        self.assertEqual(classifications["b"], "MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP")
        self.assertNotIn("UNEXPECTED_GENERATED", {row["classification"] for row in comparison["rows"]})

    def test_diagram_ir_schema_accepts_locked_external_process_id(self):
        _, _, _, _, generated = self.inputs()
        assert_validates(self, generated, "diagram_ir.schema.json")

    def test_renderer_artifact_exists_for_b04_diagram_ir(self):
        if shutil.which("lualatex") is None:
            raise unittest.SkipTest("lualatex is not available")
        physics, convention, _, _, generated = self.inputs()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = render_tikz_feynman(physics, convention, generated, Path(tmp))
            pdf = Path(manifest["outputs"]["pdf"])
            self.assertTrue(pdf.exists())
            self.assertGreater(pdf.stat().st_size, 0)

    def test_no_b04_specific_logic_in_generic_topology_core(self):
        text = (ROOT / "src" / "feynagent" / "diagrams" / "topology.py").read_text(encoding="utf-8")
        self.assertNotIn("B04", text)
        self.assertNotIn("phi_phi_to_hh", text)

    def test_no_absolute_private_knowledge_path_in_generated_topology_outputs(self):
        _, _, _, _, generated = self.inputs()
        payload = json.dumps(generated, sort_keys=True)
        for token in ["FeynAgent_external_knowledge", "_external_knowledge", "source_material\\", "gold\\"]:
            self.assertNotIn(token, payload)


if __name__ == "__main__":
    unittest.main()


