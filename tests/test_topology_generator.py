import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.diagrams import DiagramGenerationError, diagram_signature, generate_tree_2_to_2


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


def load_yaml(path):
    if yaml is None:
        raise unittest.SkipTest("PyYAML is not installed; install with: python -m pip install -e .[dev]")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_validates(testcase, instance, schema_name):
    if jsonschema is None:
        raise unittest.SkipTest("jsonschema is not installed; install with: python -m pip install -e .[dev]")
    with (ROOT / "schemas" / schema_name).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator_cls(schema).validate(instance)


def synthetic_scalar_fixture():
    physics = {
        "schema_version": "0.1.2",
        "object_id": "physics_card:synthetic_abcd",
        "status": "approved",
        "process_id": "process:synthetic_abcd",
        "process_type": "scattering_2_to_2",
        "perturbative_order": {"loop_order": 0, "restriction": "tree_level_only"},
        "coupling_order": {"mode": "explicit", "orders": [{"coupling": "g", "power": 2}]},
        "particles": {
            "incoming": [
                {"slot": 1, "particle_id": "alpha", "state_role": "incoming", "momentum_label": "pa"},
                {"slot": 2, "particle_id": "beta", "state_role": "incoming", "momentum_label": "pb"},
            ],
            "outgoing": [
                {"slot": 3, "particle_id": "chi", "state_role": "outgoing", "momentum_label": "pc"},
                {"slot": 4, "particle_id": "delta", "state_role": "outgoing", "momentum_label": "pd"},
            ],
        },
        "selected_rule_set": {
            "registry_id": "registry:synthetic_scalar",
            "rule_set_ids": ["ruleset:synthetic_scalar"],
        },
        "internal_species_policy": {"allowed_particle_ids": ["xray"]},
        "requested_outputs": ["diagram_ir"],
        "approval": {
            "topology": {"status": "approved"},
            "amplitude_generation": {"status": "not_requested"},
            "heavy_calculation": {"status": "not_requested"},
        },
    }
    convention = {
        "schema_version": "0.1.1",
        "object_id": "convention_card:synthetic",
        "status": "approved",
        "spacetime_dimension": {"symbol": "D", "value": 4},
        "metric_signature": "+---",
        "momentum_convention": {
            "fourier_phase": "exp_minus_i_p_x",
            "propagator_momentum_flow": "explicit_per_line",
        },
        "all_momenta_incoming_vertex_convention": True,
        "external_state_momentum_convention": {
            "incoming_particles": "physical_incoming_momenta",
            "outgoing_particles": "physical_outgoing_momenta",
        },
        "natural_units": {"hbar": "1", "c": "1"},
        "spin_polarization_policy": {
            "spin_sum": "do_not_sum",
            "polarization_sum": "do_not_sum",
            "initial_state_average": "do_not_average",
        },
    }
    registry = {
        "schema_version": "0.1.1",
        "object_id": "rule_registry:synthetic_scalar",
        "status": "draft",
        "registry_id": "registry:synthetic_scalar",
        "particle_catalog": [
            {
                "particle_id": particle,
                "display_name": particle,
                "field_role": "scalar",
                "self_conjugate": True,
                "antiparticle_id": particle,
                "fermion_number": 0,
            }
            for particle in ["alpha", "beta", "chi", "delta", "xray"]
        ],
        "rule_sets": [
            {
                "rule_set_id": "ruleset:synthetic_scalar",
                "display_name": "Synthetic scalar",
                "status": "draft",
            }
        ],
        "vertices": [
            _scalar_vertex("rule:synthetic:alpha_beta_xray", ["alpha", "beta", "xray"]),
            _scalar_vertex("rule:synthetic:chi_delta_xray", ["chi", "delta", "xray"]),
        ],
        "propagators": [_scalar_propagator("rule:synthetic:xray_propagator", "xray")],
    }
    return physics, convention, registry


def _scalar_vertex(rule_id, particles):
    return {
        "rule_id": rule_id,
        "rule_type": "vertex",
        "rule_set_id": "ruleset:synthetic_scalar",
        "participating_fields": [
            {
                "slot": index,
                "field_id": f"field:synthetic:{particle}",
                "particle_id": particle,
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            }
            for index, particle in enumerate(particles, start=1)
        ],
        "momentum_labels_order": [f"p{index}" for index in range(1, len(particles) + 1)],
        "lorentz_index_structure": {"form": "template", "expression": "1"},
        "latex": "i g",
        "feyncalc": {"template": "I g"},
        "coupling_order": [{"coupling": "g", "power": 1}],
        "mass_dimension": 1,
        "symmetries": ["none"],
        "provenance": [
            {
                "source_type": "user_supplied",
                "citation": "synthetic unit fixture",
                "notes": "arbitrary scalar fixture for topology generator tests",
                "checked_by": "test",
                "checked_at": "2026-08-12T00:00:00+08:00",
            }
        ],
        "trust_status": "untrusted",
    }


def _scalar_propagator(rule_id, particle):
    return {
        "rule_id": rule_id,
        "rule_type": "propagator",
        "rule_set_id": "ruleset:synthetic_scalar",
        "participating_fields": [
            {
                "slot": 1,
                "field_id": f"field:synthetic:{particle}",
                "particle_id": particle,
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
            {
                "slot": 2,
                "field_id": f"field:synthetic:{particle}",
                "particle_id": particle,
                "field_role": "scalar",
                "quantum_field_role": "scalar_field",
            },
        ],
        "momentum_labels_order": ["q"],
        "lorentz_index_structure": {"form": "template", "expression": "1/(q^2-m^2)"},
        "latex": "i/(q^2-m^2)",
        "feyncalc": {"template": "I/(SP[q,q]-m^2)"},
        "coupling_order": [{"coupling": "g", "power": 0}],
        "mass_dimension": -2,
        "symmetries": ["none"],
        "provenance": [
            {
                "source_type": "user_supplied",
                "citation": "synthetic unit fixture",
                "notes": "arbitrary scalar fixture for topology generator tests",
                "checked_by": "test",
                "checked_at": "2026-08-12T00:00:00+08:00",
            }
        ],
        "trust_status": "untrusted",
    }


class TopologyGeneratorTests(unittest.TestCase):
    def test_b02_generation_finds_s_and_u_without_hard_coding_process_name(self):
        physics = load_yaml(ROOT / "benchmarks" / "B02_compton" / "physics_card.yaml")
        convention = load_yaml(ROOT / "benchmarks" / "B02_compton" / "convention_card.yaml")
        registry = load_yaml(ROOT / "rules" / "qed" / "qed_tree_v1.yaml")
        generated = generate_tree_2_to_2(physics, convention, registry)
        assert_validates(self, generated, "diagram_ir.schema.json")
        self.assertEqual({diagram["channel"] for diagram in generated["diagrams"]}, {"s", "u"})

    def test_canonical_channel_partitioning_and_internal_momenta(self):
        physics, convention, registry = synthetic_scalar_fixture()
        generated = generate_tree_2_to_2(physics, convention, registry)
        self.assertEqual(len(generated["diagrams"]), 1)
        diagram = generated["diagrams"][0]
        self.assertEqual(diagram["channel"], "s")
        self.assertEqual(diagram["internal_lines"][0]["particle_id"], "xray")
        self.assertEqual(diagram["internal_lines"][0]["momentum"]["expression"], "pa+pb")

    def test_rule_matching_and_slot_binding_completeness(self):
        physics, convention, registry = synthetic_scalar_fixture()
        diagram = generate_tree_2_to_2(physics, convention, registry)["diagrams"][0]
        for vertex in diagram["vertex_instances"]:
            slots = [binding["rule_slot"] for binding in vertex["slot_bindings"]]
            self.assertEqual(set(slots), {1, 2, 3})
            self.assertEqual(len(slots), len(set(slots)))
            self.assertNotIn("attached_endpoint_ids", vertex)

    def test_internal_species_policy_rejects_disallowed_exchange(self):
        physics, convention, registry = synthetic_scalar_fixture()
        physics["internal_species_policy"] = {"allowed_particle_ids": ["not_xray"]}
        generated = generate_tree_2_to_2(physics, convention, registry)
        self.assertEqual(generated["diagrams"], [])

    def test_deduplicates_identical_structures(self):
        physics, convention, registry = synthetic_scalar_fixture()
        registry["vertices"].append(copy.deepcopy(registry["vertices"][0]))
        registry["vertices"].append(copy.deepcopy(registry["vertices"][1]))
        generated = generate_tree_2_to_2(physics, convention, registry)
        signatures = [diagram_signature(diagram) for diagram in generated["diagrams"]]
        self.assertEqual(len(signatures), len(set(signatures)))
        self.assertEqual(len(generated["diagrams"]), 1)

    def test_particle_antiparticle_crossing_helper_behavior(self):
        from feynagent.diagrams.topology import _field_accepts_external

        catalog = {
            "ferm": {"particle_id": "ferm", "antiparticle_id": "anti", "self_conjugate": False},
            "anti": {"particle_id": "anti", "antiparticle_id": "ferm", "self_conjugate": False},
        }
        psi_bar_field = {
            "particle_id": "ferm",
            "field_role": "dirac_fermion",
            "quantum_field_role": "psi_bar",
        }
        incoming_antiparticle = {
            "particle_id": "anti",
            "state_role": "incoming",
        }
        self.assertTrue(_field_accepts_external(psi_bar_field, incoming_antiparticle, catalog))



    def test_external_dirac_fermion_flow_truth_table(self):
        physics = load_yaml(ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml")
        convention = load_yaml(ROOT / "benchmarks" / "B01_ee_to_mumu" / "convention_card.yaml")
        registry = load_yaml(ROOT / "rules" / "qed" / "qed_tree_v1.yaml")
        diagram = generate_tree_2_to_2(physics, convention, registry)["diagrams"][0]
        external_by_id = {leg["leg_id"]: leg for leg in diagram["external_legs"]}
        table = {}
        for vertex in diagram["vertex_instances"]:
            for binding in vertex["slot_bindings"]:
                if binding["endpoint_kind"] != "external_leg":
                    continue
                leg = external_by_id[binding["endpoint_id"]]
                table[(leg["state_role"], leg["particle_id"])] = (
                    binding["fermion_flow"]["field_orientation"],
                    binding["fermion_flow"]["flow_direction"],
                )

        self.assertEqual(table[("incoming", "e-")], ("psi", "into_vertex"))
        self.assertEqual(table[("outgoing", "mu-")], ("psi_bar", "out_of_vertex"))
        self.assertEqual(table[("incoming", "e+")], ("psi_bar", "out_of_vertex"))
        self.assertEqual(table[("outgoing", "mu+")], ("psi", "into_vertex"))

    def test_signature_includes_fermion_flow_direction(self):
        physics = load_yaml(ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml")
        convention = load_yaml(ROOT / "benchmarks" / "B01_ee_to_mumu" / "convention_card.yaml")
        registry = load_yaml(ROOT / "rules" / "qed" / "qed_tree_v1.yaml")
        diagram = generate_tree_2_to_2(physics, convention, registry)["diagrams"][0]
        altered = copy.deepcopy(diagram)
        altered["vertex_instances"][0]["slot_bindings"][0]["fermion_flow"]["flow_direction"] = "into_vertex"
        self.assertNotEqual(diagram_signature(diagram), diagram_signature(altered))

    def test_contact_diagram_when_compatible_four_point_rule_exists(self):
        physics, convention, registry = synthetic_scalar_fixture()
        contact = _scalar_vertex("rule:synthetic:alpha_beta_chi_delta", ["alpha", "beta", "chi", "delta"])
        contact["coupling_order"] = [{"coupling": "g", "power": 2}]
        registry["vertices"].append(contact)
        generated = generate_tree_2_to_2(physics, convention, registry)
        self.assertEqual({diagram["channel"] for diagram in generated["diagrams"]}, {"s", "contact"})
        contact_diagram = [diagram for diagram in generated["diagrams"] if diagram["channel"] == "contact"][0]
        self.assertEqual(contact_diagram["internal_lines"], [])
        self.assertEqual(len(contact_diagram["vertex_instances"]), 1)
        self.assertEqual(len(contact_diagram["vertex_instances"][0]["slot_bindings"]), 4)

    def test_unsupported_process_rejection(self):
        physics, convention, registry = synthetic_scalar_fixture()
        physics["process_type"] = "decay_1_to_n"
        with self.assertRaises(DiagramGenerationError):
            generate_tree_2_to_2(physics, convention, registry)

    def test_cli_writes_to_output_directory_and_refuses_overwrite(self):
        import subprocess

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            cmd = [
                sys.executable,
                str(ROOT / "scripts" / "generate_diagrams.py"),
                "--physics-card",
                str(ROOT / "benchmarks" / "B02_compton" / "physics_card.yaml"),
                "--convention-card",
                str(ROOT / "benchmarks" / "B02_compton" / "convention_card.yaml"),
                "--rule-registry",
                str(ROOT / "rules" / "qed" / "qed_tree_v1.yaml"),
                "--output",
                str(out),
            ]
            first = subprocess.run(cmd, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((out / "generated_diagrams.yaml").exists())
            second = subprocess.run(cmd, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("refusing to overwrite", second.stderr)


if __name__ == "__main__":
    unittest.main()

