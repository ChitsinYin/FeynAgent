import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_amplitudes import (
    build_amp_records,
    build_validation_payload,
    render_mathematica_file,
)
from feynagent.b04_topology import (
    annotate_diagram_ir,
    build_rule_registry_from_locked_rules,
    build_topology_convention_card,
    physics_card_for_topology,
    rule_usage_audit,
)
from feynagent.diagrams import generate_tree_2_to_2

try:
    import yaml
except ImportError:  # pragma: no cover
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


def build_fixture_diagram_ir():
    physics = load_yaml(B04 / "physics_card.yaml")
    convention_ref = load_yaml(B04 / "convention_reference.yaml")
    convention = build_topology_convention_card(convention_ref)
    registry = build_rule_registry_from_locked_rules(MODEL_FIXTURE, RULES_FIXTURE)
    topology_physics = physics_card_for_topology(physics)
    generated = generate_tree_2_to_2(topology_physics, convention, registry)
    return annotate_diagram_ir(generated, "a" * 64)


class B04AmplitudeClosureTests(unittest.TestCase):
    def test_gold_labels_map_to_generated_channels_not_enumeration_order(self):
        records = build_amp_records(build_fixture_diagram_ir(), {})
        self.assertEqual([(record.gold_label, record.generated_channel) for record in records], [("a", "t"), ("b", "u"), ("c", "s"), ("d", "contact")])
        self.assertEqual([record.stem for record in records], ["amp_001", "amp_002", "amp_003", "amp_004"])

    def test_scalar_exchange_keeps_exact_raw_before_reduced_zero(self):
        records = {record.gold_label: record for record in build_amp_records(build_fixture_diagram_ir(), {})}
        self.assertEqual(records["a"].classification, "PASS_AFTER_EXPLICIT_CONVENTION_MAP")
        self.assertEqual(records["b"].classification, "PASS_AFTER_EXPLICIT_CONVENTION_MAP")
        self.assertEqual(records["a"].momentum_substitutions, {"qt": "p1-k1"})
        self.assertEqual(records["b"].momentum_substitutions, {"qu": "p1-k2"})
        text = render_mathematica_file(records["a"])
        self.assertLess(text.index("Amp001RawTensor"), text.index("Amp001ReducedNRTTGold = 0"))
        self.assertIn("EpsH[k1, mu, nu] * EpsH[k2, sig, gam]", text)

    def test_contact_uses_manual_tau_not_rejected_feyngrav_ssgg(self):
        records = {record.gold_label: record for record in build_amp_records(build_fixture_diagram_ir(), {})}
        text = render_mathematica_file(records["d"])
        self.assertIn("TauLocked[{mu, nu}, {sig, gam}, p1, p2]", text)
        self.assertIn("Amp004ReducedNRTTGold", text)
        self.assertNotIn("ssgg", text)

    def test_validation_payload_stops_before_m2_without_conflict(self):
        records = build_amp_records(build_fixture_diagram_ir(), {})
        usage = rule_usage_audit(
            build_fixture_diagram_ir(),
            {"propagator:phi", "vertex:h_phi_phi", "propagator:h", "vertex:h_h_h", "vertex:h_h_phi_phi"},
        )
        payload = build_validation_payload(records, {"status": "PASS"}, usage, "b" * 64, "c" * 64)
        self.assertEqual(payload["m2_status"], "STOPPED_BEFORE_M2_NO_CONFLICTS")
        self.assertNotIn("CONFLICT_REQUIRES_REVIEW", json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
