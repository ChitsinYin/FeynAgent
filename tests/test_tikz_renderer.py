import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.diagrams import generate_tree_2_to_2
from feynagent.render.tikz import RenderError, build_tikz_document
from test_topology_generator import synthetic_scalar_fixture


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


class TikzRendererTests(unittest.TestCase):
    def b02_inputs(self):
        physics = load_yaml(ROOT / "benchmarks" / "B02_compton" / "physics_card.yaml")
        convention = load_yaml(ROOT / "benchmarks" / "B02_compton" / "convention_card.yaml")
        registry = load_yaml(ROOT / "rules" / "qed" / "qed_tree_v1.yaml")
        diagram_ir = generate_tree_2_to_2(physics, convention, registry)
        return physics, convention, diagram_ir

    def test_deterministic_tex_generation_orders_channels(self):
        physics, _, diagram_ir = self.b02_inputs()
        tex = build_tikz_document(physics, diagram_ir)
        tex_again = build_tikz_document(physics, diagram_ir)
        self.assertEqual(tex, tex_again)
        self.assertLess(tex.index(r"\mathrm{s}-channel"), tex.index(r"\mathrm{u}-channel"))
        self.assertIn(r"electron\;(p1)", tex)
        self.assertIn(r"photon\;(k2)", tex)
        self.assertIn(r"e-\;(q\_s=p1+k1)", tex)
        self.assertIn("[fermion", tex)
        self.assertIn("[photon", tex)

    def test_missing_flow_data_fails_instead_of_guessing(self):
        physics, _, diagram_ir = self.b02_inputs()
        broken = copy.deepcopy(diagram_ir)
        del broken["diagrams"][0]["vertex_instances"][0]["slot_bindings"][0]["fermion_flow"]
        with self.assertRaises(RenderError):
            build_tikz_document(physics, broken)

    def test_repeated_renders_from_same_input_are_equivalent(self):
        physics, _, diagram_ir = self.b02_inputs()
        first = build_tikz_document(physics, diagram_ir)
        second = build_tikz_document(physics, diagram_ir)
        self.assertEqual(first, second)

    def test_contact_diagram_tex_generation_for_supported_day2_shape(self):
        physics, convention, registry = synthetic_scalar_fixture()
        contact = copy.deepcopy(registry["vertices"][0])
        contact["rule_id"] = "rule:synthetic:alpha_beta_chi_delta"
        contact["participating_fields"] = [
            {
                "slot": 1,
                "field_id": "field:synthetic:alpha",
                "particle_id": "alpha",
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
            {
                "slot": 2,
                "field_id": "field:synthetic:beta",
                "particle_id": "beta",
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
            {
                "slot": 3,
                "field_id": "field:synthetic:chi",
                "particle_id": "chi",
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
            {
                "slot": 4,
                "field_id": "field:synthetic:delta",
                "particle_id": "delta",
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
        ]
        contact["coupling_order"] = [{"coupling": "g", "power": 2}]
        registry["vertices"] = [contact]
        physics["internal_species_policy"] = {"allowed_particle_ids": []}
        diagram_ir = generate_tree_2_to_2(physics, convention, registry)
        self.assertEqual({diagram["channel"] for diagram in diagram_ir["diagrams"]}, {"contact"})
        tex = build_tikz_document(physics, diagram_ir)
        self.assertIn(r"\mathrm{contact}-channel", tex)
        self.assertIn("alpha", tex)


if __name__ == "__main__":
    unittest.main()


