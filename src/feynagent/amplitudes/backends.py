"""Derived LaTeX and FeynCalc backends for Day-3 AmplitudeIR.

The functions in this module render only from AmplitudeIR. They deliberately do
not inspect PhysicsCard, ConventionCard, RuleRegistry, or DiagramIR, which keeps
the human-readable and executable forms tied to the same derived structure.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RenderedAmplitudeBackend:
    """Rendered backend payloads derived from one AmplitudeIR."""

    latex: str
    wolfram: str
    smoke_wolfram: str
    compute_m2_wolfram: str
    audit_markdown: str
    ward_check_wolfram: str | None = None


def render_backends(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> RenderedAmplitudeBackend:
    """Render all Day-3 backend payloads from a single AmplitudeIR."""

    return RenderedAmplitudeBackend(
        latex=render_latex_document(amplitude_ir, benchmark_id, generated_at),
        wolfram=render_wolfram_amplitudes(amplitude_ir, benchmark_id, generated_at),
        smoke_wolfram=render_smoke_wolfram(amplitude_ir, benchmark_id),
        compute_m2_wolfram=render_compute_m2_wolfram(amplitude_ir, benchmark_id, generated_at),
        audit_markdown=render_audit_markdown(amplitude_ir, benchmark_id, generated_at),
        ward_check_wolfram=render_ward_check_wolfram(amplitude_ir, benchmark_id, generated_at)
        if benchmark_id == "B02_compton"
        else None,
    )


def write_backend_outputs(
    amplitude_ir: dict[str, Any],
    benchmark_dir: Path,
    benchmark_id: str,
    generated_at: str,
) -> list[Path]:
    """Write stable benchmark outputs derived from AmplitudeIR."""

    import yaml

    rendered = render_backends(amplitude_ir, benchmark_id, generated_at)
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "amplitude_ir.yaml": yaml.safe_dump(amplitude_ir, sort_keys=False, allow_unicode=False),
        "amplitudes.tex": rendered.latex,
        "amplitudes.wl": rendered.wolfram,
        "amplitude_audit.md": rendered.audit_markdown,
        "amplitude_smoke.wl": rendered.smoke_wolfram,
        "compute_m2.wl": rendered.compute_m2_wolfram,
    }
    if rendered.ward_check_wolfram is not None:
        outputs["ward_check.wl"] = rendered.ward_check_wolfram

    written = []
    for name, payload in outputs.items():
        path = benchmark_dir / name
        path.write_text(payload, encoding="utf-8", newline="\n")
        written.append(path)
    return written


def render_latex_document(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> str:
    lines = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[a4paper,margin=1in]{geometry}",
        r"\usepackage{amsmath,amssymb,booktabs,longtable}",
        r"\begin{document}",
        rf"\section*{{Day-3 Amplitudes: \texttt{{{_tex_escape(benchmark_id)}}}}}",
        rf"Generated at \texttt{{{_tex_escape(generated_at)}}} from AmplitudeIR \texttt{{{_tex_escape(amplitude_ir['object_id'])}}}.",
        "",
        r"\subsection*{Momentum Definitions}",
    ]
    for label, expression in _momentum_definitions(amplitude_ir):
        lines.append(rf"\[{_latex_momentum(label)} = {_latex_momentum_expression(expression)}\]")

    lines += ["", r"\subsection*{Diagram Amplitudes}"]
    for amplitude in amplitude_ir["amplitudes"]:
        context = _RenderContext(amplitude)
        channel = _channel(amplitude)
        lines.append(_latex_factor_comments(amplitude, context))
        lines.append(r"\begin{equation}")
        lines.append(rf"\mathcal{{M}}_{{{channel}}} = {_latex_amplitude_expression(amplitude, context)}")
        lines.append(r"\end{equation}")
        lines.append("")

    total_terms = " + ".join(
        rf"\mathcal{{M}}_{{{_channel(_amplitude_by_id(amplitude_ir, amp_id))}}}"
        for amp_id in amplitude_ir["total_amplitude"]["term_amplitude_ids"]
    )
    lines += [
        r"\subsection*{Total Amplitude}",
        r"\begin{equation}",
        rf"\mathcal{{M}} = {total_terms}",
        r"\end{equation}",
        "",
        r"\subsection*{Rule/Source Audit}",
        r"\begin{longtable}{p{0.24\linewidth}p{0.22\linewidth}p{0.38\linewidth}}",
        r"\toprule",
        r"amplitude & rule id & source \\",
        r"\midrule",
    ]
    for amplitude in amplitude_ir["amplitudes"]:
        for rule_id in amplitude["source_rule_ids"]:
            lines.append(
                rf"\texttt{{{_tex_escape(amplitude['amplitude_id'])}}} & "
                rf"\texttt{{{_tex_escape(rule_id)}}} & "
                rf"\texttt{{{_tex_escape(amplitude['audit_metadata']['convention_audit_path'])}}} \\"
            )
    lines += [
        r"\bottomrule",
        r"\end{longtable}",
        r"\end{document}",
        "",
    ]
    return "\n".join(lines)


def render_wolfram_amplitudes(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> str:
    all_symbols = sorted(_all_momentum_symbols(amplitude_ir) | {"e", "epsilon", "me", "mmu"})
    for amplitude in amplitude_ir["amplitudes"]:
        context = _RenderContext(amplitude)
        all_symbols.extend(context.wl_index(index["index_id"]) for index in amplitude["local_indices"]["lorentz"])
    amp_assignments = []
    amp_assoc_entries = []
    factor_entries = []
    index_entries = []
    for amplitude in amplitude_ir["amplitudes"]:
        context = _RenderContext(amplitude)
        symbol = _amp_symbol(amplitude)
        amp_assignments.append(f"{symbol} = {_wolfram_amplitude_expression(amplitude, context)};")
        amp_assoc_entries.append(f'"amp_{_channel(amplitude)}" -> {symbol}')
        factor_ids = _all_factor_ids(amplitude)
        factor_entries.append(f'"amp_{_channel(amplitude)}" -> {{{", ".join(_wl_string(factor_id) for factor_id in factor_ids)}}}')
        for index_id, symbol_name in context.wl_index_map.items():
            index_entries.append(f"{_wl_string(index_id)} -> {_wl_string(symbol_name)}")
    total = " + ".join(_amp_symbol(_amplitude_by_id(amplitude_ir, amp_id)) for amp_id in amplitude_ir["total_amplitude"]["term_amplitude_ids"])
    q_entries = [f"{_wl_string(label)} -> HoldForm[{_wl_momentum_symbol(label)} == {_wl_momentum_expression(expr)}]" for label, expr in _momentum_definitions(amplitude_ir)]
    q_rules = [f"{_wl_momentum_symbol(label)} -> {_wl_momentum_expression(expr)}" for label, expr in _momentum_definitions(amplitude_ir)]
    lines = [
        f"(* Day-3 generated amplitudes for {benchmark_id}. *)",
        f"(* generated-at: {generated_at} *)",
        f"(* source-amplitude-ir: {amplitude_ir['object_id']} *)",
        "(* This file is derived from AmplitudeIR only; no amplitude reconstruction is performed here. *)",
        "$LoadFeynArts = False;",
        'If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];',
        f"ClearAll[{', '.join(_unique_preserve_order(all_symbols + [_amp_symbol(amp) for amp in amplitude_ir['amplitudes']] + ['ampTotal']))}];",
        "",
    ]
    lines.extend(_wolfram_factor_comments(amplitude_ir))
    lines += [
        f"qDefinitions = <|{', '.join(q_entries)}|>;",
        f"qSubstitutions = {{{', '.join(q_rules)}}};",
        f"amplitudeFactorIDs = <|{', '.join(factor_entries)}|>;",
        f"amplitudeIndexMap = <|{', '.join(index_entries)}|>;",
        "",
    ]
    lines.extend(amp_assignments)
    lines += [
        f"diagramAmplitudes = <|{', '.join(amp_assoc_entries)}|>;",
        f"ampTotal = {total};",
        f'Print["Loaded generated amplitudes for {benchmark_id}"];',
        "",
    ]
    return "\n".join(lines)


def render_smoke_wolfram(amplitude_ir: dict[str, Any], benchmark_id: str) -> str:
    expected = [_amp_symbol(amp) for amp in amplitude_ir["amplitudes"]] + ["ampTotal"]
    expected_keys = [f"amp_{_channel(amp)}" for amp in amplitude_ir["amplitudes"]]
    return "\n".join(
        [
            f"(* Lightweight smoke test for {benchmark_id}; intentionally no simplification. *)",
            "$LoadFeynArts = False;",
            "status = Check[",
            '  If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];',
            "  Get[FileNameJoin[{DirectoryName[$InputFileName], \"amplitudes.wl\"}]];",
            f"  expectedSymbols = {{{', '.join(expected)}}};",
            f"  expectedKeys = {{{', '.join(_wl_string(key) for key in expected_keys)}}};",
            "  symbolsOK = And @@ (ValueQ /@ expectedSymbols);",
            "  keysOK = Sort[Keys[diagramAmplitudes]] === Sort[expectedKeys];",
            "  Print[\"SMOKE structural summary: diagrams=\", Length[diagramAmplitudes], \"; keys=\", Keys[diagramAmplitudes], \"; q=\", Keys[qDefinitions]];",
            "  If[symbolsOK && keysOK, 0, 2],",
            "  Print[\"SMOKE generation-time exception: \", $MessageList]; 1",
            "];",
            "Quit[status];",
            "",
        ]
    )


def render_compute_m2_wolfram(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> str:
    average = "1/4"
    process_tail = amplitude_ir["process_id"].split(":")[-1]
    return "\n".join(
        [
            f"(* Human-run heavy M2 script for {benchmark_id}; generated at {generated_at}. *)",
            "(* DO NOT run from the live agent loop. This script performs spin/polarization sums and simplification. *)",
            "$LoadFeynArts = False;",
            "outputDir = FileNameJoin[{DirectoryName[$InputFileName], \"m2_outputs\"}];",
            "doneSentinel = FileNameJoin[{outputDir, \"DONE\"}];",
            "force = TrueQ[$ForceM2];",
            "If[FileExistsQ[doneSentinel] && !force, Print[\"Existing successful M2 detected; set $ForceM2=True to overwrite.\"]; Quit[2]];",
            "If[!DirectoryQ[outputDir], CreateDirectory[outputDir]];",
            "stdoutPath = FileNameJoin[{outputDir, \"compute_m2.stdout.log\"}];",
            "stderrPath = FileNameJoin[{outputDir, \"compute_m2.stderr.log\"}];",
            "stdout = OpenWrite[stdoutPath];",
            "stderr = OpenWrite[stderrPath];",
            "log[msg_] := (Print[msg]; WriteString[stdout, ToString[msg] <> \"\\n\"]);",
            "fail[msg_] := (WriteString[stderr, ToString[msg] <> \"\\n\"]; Close /@ {stdout, stderr}; Quit[1]);",
            "log[\"HEAVY COMPUTATION START: spin sums, polarization sums, averaging, and simplification.\"];",
            "status = Check[",
            '  If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];',
            "  Get[FileNameJoin[{DirectoryName[$InputFileName], \"amplitudes.wl\"}]];",
            f"  initialAverage = {average};",
            "  rawInterference = ampTotal ComplexConjugate[ampTotal];",
            "  spinSummed = FermionSpinSum[rawInterference];",
            "  polSummed = spinSummed;",
            "  Do[polSummed = DoPolarizationSums[polSummed, mom], {mom, {p1, p2, p3, p4, k1, k2}}];",
            "  m2Raw = initialAverage polSummed;",
            "  Put[m2Raw, FileNameJoin[{outputDir, \"m2_raw.m\"}]];",
            "  m2Simplified = FullSimplify[Contract[m2Raw /. qSubstitutions]];",
            "  Put[m2Simplified, FileNameJoin[{outputDir, \"m2_simplified.m\"}]];",
            f"  Put[<|\"benchmark\" -> \"{benchmark_id}\", \"process\" -> \"{process_tail}\", \"status\" -> \"DONE\"|>, FileNameJoin[{{outputDir, \"compute_m2_report.m\"}}]];",
            "  Put[DateString[], doneSentinel];",
            "  log[\"DONE: raw and simplified M2 saved.\"]; 0,",
            "  fail[\"Heavy computation failed; DONE sentinel was not written.\"]",
            "];",
            "Close /@ {stdout, stderr};",
            "Quit[status];",
            "",
        ]
    )


def render_ward_check_wolfram(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> str:
    return "\n".join(
        [
            f"(* Human-run Ward identity check for {benchmark_id}; generated at {generated_at}. *)",
            "(* Not executed by default in Day-3 generation. *)",
            "$LoadFeynArts = False;",
            'If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];',
            "Get[FileNameJoin[{DirectoryName[$InputFileName], \"amplitudes.wl\"}]];",
            "Print[\"WARD CHECK START: replaces external photon polarization by corresponding momentum.\"];",
            "wardIncomingRaw = ampTotal /. PolarizationVector[k1, mu_] :> Momentum[k1, mu];",
            "wardOutgoingRaw = ampTotal /. ComplexConjugate[PolarizationVector[k2, mu_]] :> Momentum[k2, mu];",
            "Put[wardIncomingRaw, FileNameJoin[{DirectoryName[$InputFileName], \"ward_incoming_raw.m\"}]];",
            "Put[wardOutgoingRaw, FileNameJoin[{DirectoryName[$InputFileName], \"ward_outgoing_raw.m\"}]];",
            "Print[\"WARD CHECK RAW EXPRESSIONS SAVED; simplify manually if desired.\"];",
            "Quit[0];",
            "",
        ]
    )


def render_audit_markdown(amplitude_ir: dict[str, Any], benchmark_id: str, generated_at: str) -> str:
    lines = [
        f"# Day-3 Amplitude Backend Audit: {benchmark_id}",
        "",
        f"- generated_at: `{generated_at}`",
        f"- source_amplitude_ir: `{amplitude_ir['object_id']}`",
        f"- process_id: `{amplitude_ir['process_id']}`",
        "- backend_source: `AmplitudeIR only`",
        "- heavy_calculation_executed: `false`",
        "",
        "| amplitude_id | diagram_id | canonical rule IDs | factor IDs | index map |",
        "|---|---|---|---|---|",
    ]
    for amplitude in amplitude_ir["amplitudes"]:
        context = _RenderContext(amplitude)
        factors = "<br>".join(f"`{factor_id}`" for factor_id in _all_factor_ids(amplitude))
        indices = "<br>".join(f"`{index_id}` -> `{context.label(index_id)}`" for index_id in context.index_ids)
        rules = "<br>".join(f"`{rule_id}`" for rule_id in amplitude["source_rule_ids"])
        lines.append(f"| `{amplitude['amplitude_id']}` | `{amplitude['diagram_id']}` | {rules} | {factors} | {indices} |")
    lines += [
        "",
        "## Backend Constraints",
        "",
        "- LaTeX and FeynCalc are rendered from the same AmplitudeIR object.",
        "- Diagram amplitudes are preserved separately and the total amplitude is an ordered symbolic sum.",
        "- Gamma chains are not simplified.",
        "- Squared amplitudes, spin sums, and polarization sums are not performed during generation or smoke tests.",
        "- `compute_m2.wl` is a human-run heavy script and was not executed by generation.",
        "",
    ]
    return "\n".join(lines)


class _RenderContext:
    def __init__(self, amplitude: dict[str, Any]):
        self.amplitude = amplitude
        self.index_ids = [
            index["index_id"]
            for group in ("lorentz", "dirac")
            for index in amplitude["local_indices"][group]
        ]
        self.latex_index_map: dict[str, str] = {}
        self.wl_index_map: dict[str, str] = {}
        for position, index in enumerate(amplitude["local_indices"]["lorentz"], start=1):
            self.latex_index_map[index["index_id"]] = rf"\mu_{{{position}}}"
            self.wl_index_map[index["index_id"]] = f"mu{position}"
        for position, index in enumerate(amplitude["local_indices"]["dirac"], start=1):
            self.latex_index_map[index["index_id"]] = rf"a_{{{position}}}"
            self.wl_index_map[index["index_id"]] = f"a{position}"

    def label(self, index_id: str) -> str:
        return self.latex_index_map[index_id]

    def wl_index(self, index_id: str) -> str:
        return self.wl_index_map[index_id]


def _latex_amplitude_expression(amplitude: dict[str, Any], context: _RenderContext) -> str:
    if amplitude["non_chain_factors"]:
        chain_terms = [_latex_chain(amplitude, chain, context) for chain in amplitude["fermion_chains"]]
        non_chain_terms = [_latex_non_chain_factor(amplitude, factor, context) for factor in amplitude["non_chain_factors"]]
        return r" \, ".join(chain_terms[:1] + non_chain_terms + chain_terms[1:])
    return r" \, ".join(_latex_chain(amplitude, chain, context) for chain in amplitude["fermion_chains"])


def _latex_chain(amplitude: dict[str, Any], chain: dict[str, Any], context: _RenderContext) -> str:
    factors = _factor_lookup(amplitude)
    rendered = []
    for factor_id in chain["ordered_factor_ids"]:
        factor = factors[factor_id]
        if factor_id in _vertex_factor_ids(amplitude):
            rendered.append(_latex_vertex_with_polarization(amplitude, factor, context))
        elif factor_id in _propagator_factor_ids(amplitude):
            rendered.append(_latex_propagator(factor, context))
        else:
            rendered.append(_latex_external_spinor(factor, context))
    return "".join(rendered)


def _latex_vertex_with_polarization(amplitude: dict[str, Any], vertex: dict[str, Any], context: _RenderContext) -> str:
    vertex_lorentz_id = vertex["lorentz_index_ids"][0]
    lorentz = context.label(vertex_lorentz_id)
    term = rf"\left(-i e \gamma^{{{lorentz}}}\right)"
    pol = _polarization_for_vertex(amplitude, vertex["factor_id"])
    if pol is not None:
        term = rf"\left(-i e \gamma^{{{lorentz}}}\right){_latex_polarization(pol, context, vertex_lorentz_id)}"
    return term


def _latex_external_spinor(factor: dict[str, Any], context: _RenderContext) -> str:
    momentum = _latex_momentum(factor["momentum_label"])
    index = context.label(factor["index_ids"][0])
    spinor = {"u": "u", "ubar": r"\bar u", "v": "v", "vbar": r"\bar v"}[factor["spinor_type"]]
    return rf"{spinor}({momentum})_{{{index}}}"


def _latex_polarization(pol: dict[str, Any], context: _RenderContext, contracted_index_id: str | None = None) -> str:
    momentum = _latex_momentum(pol["momentum_label"])
    index = context.label(contracted_index_id or pol["lorentz_index_id"])
    star = "^{*}" if pol["conjugation"] == "complex_conjugate" else ""
    return rf"\epsilon{star}_{{{index}}}({momentum})"


def _latex_propagator(factor: dict[str, Any], context: _RenderContext) -> str:
    q = _latex_momentum(factor["momentum_label"])
    if factor["particle_id"] == "gamma":
        left, right = [context.label(index_id) for index_id in factor["index_ids"]]
        return rf"\frac{{-i g^{{{left}{right}}}}}{{{q}^2+i\epsilon}}"
    mass = _latex_mass(factor["particle_id"])
    return rf"\frac{{i(\not{{{q}}}+{mass})}}{{{q}^2-{mass}^2+i\epsilon}}"


def _latex_non_chain_factor(amplitude: dict[str, Any], factor: dict[str, Any], context: _RenderContext) -> str:
    source = _factor_lookup(amplitude)[factor["source_factor_ids"][0]]
    return _latex_boson_link(amplitude, source, context)


def _latex_boson_link(amplitude: dict[str, Any], factor: dict[str, Any], context: _RenderContext) -> str:
    if factor["particle_id"] != "gamma":
        return _latex_propagator(factor, context)
    q = _latex_momentum(factor["momentum_label"])
    left, right = [context.label(index_id) for index_id in _contracted_partner_indices(amplitude, factor)]
    return rf"\frac{{-i g^{{{left}{right}}}}}{{{q}^2+i\epsilon}}"


def _wolfram_amplitude_expression(amplitude: dict[str, Any], context: _RenderContext) -> str:
    if amplitude["non_chain_factors"]:
        chain_terms = [_wolfram_chain(amplitude, chain, context) for chain in amplitude["fermion_chains"]]
        non_chain_terms = [_wolfram_non_chain_factor(amplitude, factor, context) for factor in amplitude["non_chain_factors"]]
        return " * ".join(chain_terms[:1] + non_chain_terms + chain_terms[1:])
    return " * ".join(_wolfram_chain(amplitude, chain, context) for chain in amplitude["fermion_chains"])


def _wolfram_chain(amplitude: dict[str, Any], chain: dict[str, Any], context: _RenderContext) -> str:
    factors = _factor_lookup(amplitude)
    dot_terms = []
    scalar_terms = []
    for factor_id in chain["ordered_factor_ids"]:
        factor = factors[factor_id]
        if factor_id in _vertex_factor_ids(amplitude):
            dot_terms.append(_wolfram_vertex(factor, context))
            pol = _polarization_for_vertex(amplitude, factor_id)
            if pol is not None:
                scalar_terms.append(_wolfram_polarization(pol, context, factor["lorentz_index_ids"][0]))
        elif factor_id in _propagator_factor_ids(amplitude):
            dot_terms.append(_wolfram_propagator(factor, context))
        else:
            dot_terms.append(_wolfram_external_spinor(factor))
    expr = "(" + " . ".join(dot_terms) + ")"
    if scalar_terms:
        expr += " * " + " * ".join(scalar_terms)
    return expr


def _wolfram_vertex(vertex: dict[str, Any], context: _RenderContext) -> str:
    return f"((-I e) GA[{context.wl_index(vertex['lorentz_index_ids'][0])}])"


def _wolfram_external_spinor(factor: dict[str, Any]) -> str:
    mass = _wl_mass(factor["particle_id"])
    momentum = _wl_momentum_symbol(factor["momentum_label"])
    head = {"u": "SpinorU", "ubar": "SpinorUBar", "v": "SpinorV", "vbar": "SpinorVBar"}[factor["spinor_type"]]
    return f"{head}[{momentum}, {mass}]"


def _wolfram_polarization(pol: dict[str, Any], context: _RenderContext, contracted_index_id: str | None = None) -> str:
    expr = f"PolarizationVector[{_wl_momentum_symbol(pol['momentum_label'])}, {context.wl_index(contracted_index_id or pol['lorentz_index_id'])}]"
    if pol["conjugation"] == "complex_conjugate":
        return f"ComplexConjugate[{expr}]"
    return expr


def _wolfram_propagator(factor: dict[str, Any], context: _RenderContext) -> str:
    q = _wl_momentum_symbol(factor["momentum_label"])
    if factor["particle_id"] == "gamma":
        left, right = [context.wl_index(index_id) for index_id in factor["index_ids"]]
        return f"((-I MT[{left}, {right}])/(SP[{q}, {q}] + I epsilon))"
    mass = _wl_mass(factor["particle_id"])
    return f"(I (GS[{q}] + {mass})/(SP[{q}, {q}] - {mass}^2 + I epsilon))"


def _wolfram_non_chain_factor(amplitude: dict[str, Any], factor: dict[str, Any], context: _RenderContext) -> str:
    source = _factor_lookup(amplitude)[factor["source_factor_ids"][0]]
    return _wolfram_boson_link(amplitude, source, context)


def _wolfram_boson_link(amplitude: dict[str, Any], factor: dict[str, Any], context: _RenderContext) -> str:
    if factor["particle_id"] != "gamma":
        return _wolfram_propagator(factor, context)
    q = _wl_momentum_symbol(factor["momentum_label"])
    left, right = [context.wl_index(index_id) for index_id in _contracted_partner_indices(amplitude, factor)]
    return f"((-I MT[{left}, {right}])/(SP[{q}, {q}] + I epsilon))"


def _contracted_partner_indices(amplitude: dict[str, Any], factor: dict[str, Any]) -> list[str]:
    partners = []
    for index_id in factor["index_ids"]:
        partner = None
        for contraction in amplitude["index_contractions"]:
            refs = contraction["factor_indices"]
            this_refs = [ref for ref in refs if ref["factor_id"] == factor["factor_id"] and ref["index_id"] == index_id]
            if not this_refs:
                continue
            other_refs = [ref for ref in refs if ref["factor_id"] != factor["factor_id"]]
            if other_refs:
                partner = other_refs[0]["index_id"]
                break
        partners.append(partner or index_id)
    return partners

def _polarization_for_vertex(amplitude: dict[str, Any], vertex_factor_id: str) -> dict[str, Any] | None:
    pol_by_id = {factor["factor_id"]: factor for factor in amplitude["bosonic_external_polarization_factors"]}
    for contraction in amplitude["index_contractions"]:
        factor_ids = [ref["factor_id"] for ref in contraction["factor_indices"]]
        if vertex_factor_id not in factor_ids:
            continue
        for factor_id in factor_ids:
            if factor_id in pol_by_id:
                return pol_by_id[factor_id]
    return None


def _momentum_definitions(amplitude_ir: dict[str, Any]) -> list[tuple[str, str]]:
    definitions: list[tuple[str, str]] = []
    seen = set()
    for amplitude in amplitude_ir["amplitudes"]:
        for prop in amplitude["propagator_factors"]:
            key = (prop["momentum_label"], prop["momentum_expression"])
            if key not in seen:
                seen.add(key)
                definitions.append(key)
    return definitions


def _all_momentum_symbols(amplitude_ir: dict[str, Any]) -> set[str]:
    symbols = set()
    for label, expression in _momentum_definitions(amplitude_ir):
        symbols.add(_wl_momentum_symbol(label))
        symbols.update(_wl_momentum_symbol(part) for part in _split_momentum_expression(expression))
    for amplitude in amplitude_ir["amplitudes"]:
        for factor in amplitude["external_state_factors"] + amplitude["bosonic_external_polarization_factors"]:
            symbols.add(_wl_momentum_symbol(factor["momentum_label"]))
    return symbols


def _latex_factor_comments(amplitude: dict[str, Any], context: _RenderContext) -> str:
    lines = [rf"% amplitude-id: {amplitude['amplitude_id']}"]
    for factor_id in _all_factor_ids(amplitude):
        lines.append(rf"% factor-id: {factor_id}")
    for index_id in context.index_ids:
        lines.append(rf"% index-map: {index_id} => {context.label(index_id)}")
    return "\n".join(lines)


def _wolfram_factor_comments(amplitude_ir: dict[str, Any]) -> list[str]:
    lines = []
    for amplitude in amplitude_ir["amplitudes"]:
        context = _RenderContext(amplitude)
        lines.append(f"(* amplitude-id: {amplitude['amplitude_id']} *)")
        for factor_id in _all_factor_ids(amplitude):
            lines.append(f"(* factor-id: {factor_id} *)")
        for index_id in context.index_ids:
            lines.append(f"(* index-map: {index_id} -> {context.wl_index(index_id)} *)")
    return lines + [""]


def _all_factor_ids(amplitude: dict[str, Any]) -> list[str]:
    ids = []
    for key in [
        "external_state_factors",
        "vertex_factors",
        "propagator_factors",
        "bosonic_external_polarization_factors",
        "non_chain_factors",
    ]:
        ids.extend(factor["factor_id"] for factor in amplitude.get(key, []))
    return ids


def _factor_lookup(amplitude: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        factor["factor_id"]: factor
        for key in [
            "external_state_factors",
            "vertex_factors",
            "propagator_factors",
            "bosonic_external_polarization_factors",
            "non_chain_factors",
        ]
        for factor in amplitude.get(key, [])
    }


def _vertex_factor_ids(amplitude: dict[str, Any]) -> set[str]:
    return {factor["factor_id"] for factor in amplitude["vertex_factors"]}


def _propagator_factor_ids(amplitude: dict[str, Any]) -> set[str]:
    return {factor["factor_id"] for factor in amplitude["propagator_factors"]}


def _amplitude_by_id(amplitude_ir: dict[str, Any], amplitude_id: str) -> dict[str, Any]:
    for amplitude in amplitude_ir["amplitudes"]:
        if amplitude["amplitude_id"] == amplitude_id:
            return amplitude
    raise KeyError(amplitude_id)


def _channel(amplitude: dict[str, Any]) -> str:
    return amplitude["amplitude_id"].rsplit("amp_", 1)[-1]


def _amp_symbol(amplitude: dict[str, Any]) -> str:
    return "amp" + _channel(amplitude).upper()


def _latex_momentum(label: str) -> str:
    if "_" in label:
        head, tail = label.split("_", 1)
        return rf"{head}_{{{tail}}}"
    if len(label) > 1 and label[-1].isdigit():
        return rf"{label[:-1]}_{{{label[-1]}}}"
    return label


def _latex_momentum_expression(expression: str) -> str:
    pieces = []
    for token in _tokenize_momentum_expression(expression):
        if token in {"+", "-"}:
            pieces.append(token)
        else:
            pieces.append(_latex_momentum(token))
    return "".join(pieces)


def _wl_momentum_expression(expression: str) -> str:
    pieces = []
    for token in _tokenize_momentum_expression(expression):
        if token == "+":
            pieces.append(" + ")
        elif token == "-":
            pieces.append(" - ")
        else:
            pieces.append(_wl_momentum_symbol(token))
    return "".join(pieces).strip()


def _tokenize_momentum_expression(expression: str) -> list[str]:
    tokens = []
    current = []
    for char in expression.replace(" ", ""):
        if char in "+-":
            if current:
                tokens.append("".join(current))
                current = []
            tokens.append(char)
        else:
            current.append(char)
    if current:
        tokens.append("".join(current))
    return tokens


def _split_momentum_expression(expression: str) -> list[str]:
    return [token for token in _tokenize_momentum_expression(expression) if token not in {"+", "-"}]


def _wl_momentum_symbol(label: str) -> str:
    if label == "q_s":
        return "qS"
    if label == "q_u":
        return "qU"
    return label.replace("_", "")


def _latex_mass(particle_id: str) -> str:
    return r"m_\mu" if particle_id.startswith("mu") else "m_e"


def _wl_mass(particle_id: str) -> str:
    return "mmu" if particle_id.startswith("mu") else "me"


def _tex_escape(text: str) -> str:
    return text.replace("\\", r"\textbackslash{}").replace("_", r"\_")


def _wl_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _unique_preserve_order(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
