import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.amplitudes import build_amplitude_ir, render_backends

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


def normalized_sha256(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_inputs(benchmark):
    bench_dir = ROOT / "benchmarks" / benchmark
    registry_path = ROOT / "rules" / "qed" / "qed_tree_v1.yaml"
    diagrams_path = bench_dir / "legacy" / "diagrams.yaml"
    return (
        load_yaml(bench_dir / "physics_card.yaml"),
        load_yaml(bench_dir / "convention_card.yaml"),
        load_yaml(registry_path),
        load_yaml(diagrams_path),
        {"rule_registry": normalized_sha256(registry_path), "diagram_ir": normalized_sha256(diagrams_path)},
    )


def build(benchmark):
    physics, convention, registry, diagrams, hashes = load_inputs(benchmark)
    return build_amplitude_ir(physics, convention, registry, diagrams, source_hashes=hashes)


def all_factor_ids(amplitude_ir):
    keys = [
        "external_state_factors",
        "vertex_factors",
        "propagator_factors",
        "bosonic_external_polarization_factors",
        "non_chain_factors",
    ]
    return [factor["factor_id"] for amp in amplitude_ir["amplitudes"] for key in keys for factor in amp.get(key, [])]


def all_index_ids(amplitude_ir):
    return [
        index["index_id"]
        for amp in amplitude_ir["amplitudes"]
        for group in ("lorentz", "dirac")
        for index in amp["local_indices"][group]
    ]


class AmplitudeBackendRenderTests(unittest.TestCase):
    def render(self, benchmark):
        amplitude_ir = build(benchmark)
        if jsonschema is None:
            raise unittest.SkipTest("jsonschema is not installed; install with: python -m pip install -e .[dev]")
        with (ROOT / "schemas" / "amplitude_ir.schema.json").open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        jsonschema.validate(amplitude_ir, schema)
        return amplitude_ir, render_backends(amplitude_ir, benchmark, "2026-08-12T20:00:00+08:00")

    def test_latex_and_wolfram_trace_factor_ids_to_amplitude_ir(self):
        for benchmark in ["B01_ee_to_mumu", "B02_compton"]:
            with self.subTest(benchmark=benchmark):
                amplitude_ir, rendered = self.render(benchmark)
                for factor_id in all_factor_ids(amplitude_ir):
                    self.assertIn(f"factor-id: {factor_id}", rendered.latex)
                    self.assertIn(f"factor-id: {factor_id}", rendered.wolfram)
                    self.assertIn(f"`{factor_id}`", rendered.audit_markdown)
                for amplitude in amplitude_ir["amplitudes"]:
                    self.assertIn(f"amplitude-id: {amplitude['amplitude_id']}", rendered.latex)
                    self.assertIn(f"amplitude-id: {amplitude['amplitude_id']}", rendered.wolfram)
                    self.assertIn(amplitude["diagram_id"], rendered.audit_markdown)

    def test_outputs_trace_index_maps_to_amplitude_ir(self):
        for benchmark in ["B01_ee_to_mumu", "B02_compton"]:
            with self.subTest(benchmark=benchmark):
                amplitude_ir, rendered = self.render(benchmark)
                for index_id in all_index_ids(amplitude_ir):
                    self.assertIn(f"index-map: {index_id}", rendered.latex)
                    self.assertIn(f"index-map: {index_id}", rendered.wolfram)
                    self.assertIn(f"`{index_id}`", rendered.audit_markdown)

    def test_b01_latex_contains_two_currents_and_photon_propagator_from_ir(self):
        amplitude_ir, rendered = self.render("B01_ee_to_mumu")
        self.assertIn(r"\bar v(p_{2})", rendered.latex)
        self.assertIn(r"u(p_{1})", rendered.latex)
        self.assertIn(r"\bar u(p_{3})", rendered.latex)
        self.assertIn(r"v(p_{4})", rendered.latex)
        self.assertIn(r"q_{s} = p_{1}+p_{2}", rendered.latex)
        self.assertIn(r"\frac{-i g^{\mu_{1}\mu_{2}}", rendered.latex)
        self.assertEqual(amplitude_ir["total_amplitude"]["term_amplitude_ids"], ["amplitude:b01_ee_to_mumu:amp_s"])

    def test_b02_wolfram_preserves_diagrams_q_substitutions_and_outgoing_photon_conjugation(self):
        amplitude_ir, rendered = self.render("B02_compton")
        self.assertIn("ampS =", rendered.wolfram)
        self.assertIn("ampU =", rendered.wolfram)
        self.assertIn("ampTotal = ampS + ampU;", rendered.wolfram)
        self.assertIn('"q_s" -> HoldForm[qS == p1 + k1]', rendered.wolfram)
        self.assertIn('"q_u" -> HoldForm[qU == p1 - k2]', rendered.wolfram)
        self.assertIn("ComplexConjugate[PolarizationVector[k2, mu4]]", rendered.wolfram)
        self.assertIn("PolarizationVector[k1, mu3]", rendered.wolfram)
        self.assertIn("PolarizationVector[k1, mu4]", rendered.wolfram)
        self.assertIn("ComplexConjugate[PolarizationVector[k2, mu3]]", rendered.wolfram)
        self.assertRegex(rendered.wolfram, re.compile(r"ampS = .*GS\[qS\].*PolarizationVector\[k1", re.DOTALL))
        self.assertRegex(rendered.wolfram, re.compile(r"ampU = .*GS\[qU\].*ComplexConjugate\[PolarizationVector\[k2", re.DOTALL))
        self.assertEqual(
            amplitude_ir["total_amplitude"]["term_amplitude_ids"],
            ["amplitude:b02_compton:amp_s", "amplitude:b02_compton:amp_u"],
        )

    def test_heavy_and_ward_scripts_are_staged_but_not_smoke_scripts(self):
        _, b01 = self.render("B01_ee_to_mumu")
        _, b02 = self.render("B02_compton")
        self.assertIn("HEAVY COMPUTATION START", b01.compute_m2_wolfram)
        self.assertIn("FermionSpinSum", b01.compute_m2_wolfram)
        self.assertIn("DoPolarizationSums", b01.compute_m2_wolfram)
        self.assertIn("DONE", b01.compute_m2_wolfram)
        self.assertIn("Existing successful M2 detected", b02.compute_m2_wolfram)
        self.assertIsNone(b01.ward_check_wolfram)
        self.assertIsNotNone(b02.ward_check_wolfram)
        self.assertIn("WARD CHECK START", b02.ward_check_wolfram)
        self.assertNotIn("FermionSpinSum", b02.smoke_wolfram)
        self.assertNotIn("DoPolarizationSums", b02.smoke_wolfram)


if __name__ == "__main__":
    unittest.main()
