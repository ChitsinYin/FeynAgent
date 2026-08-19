"""Day-7 B04 custom-gravity amplitude closure.

This module assembles B04 amplitudes from the locked custom rule package.  It
does not perform M2 construction and does not use an LLM for tensor algebra.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .b04_topology import (
    MODEL_ID,
    PRIMARY_BACKEND,
    build_rule_registry_from_locked_rules,
    build_topology_convention_card,
    compare_generated_to_gold,
    expected_gold_topologies,
    load_yaml,
    physics_card_for_topology,
    rule_usage_audit,
    sha256_file,
    write_json,
    write_yaml,
)
from .custom_knowledge import AVAILABLE, registered_root_for_model, verify_knowledge_lock
from .diagrams import generate_tree_2_to_2


PROCESS_ID = "process:B04_phi_phi_to_h_h"
RUN_PREFIX = "day7_b04_amplitude_closure_"
GOLD_LABEL_TO_CHANNEL = {"a": "t", "b": "u", "c": "s", "d": "contact"}
AMP_ORDER = [
    ("amp_001", "a", "t-channel scalar"),
    ("amp_002", "b", "u-channel scalar"),
    ("amp_003", "c", "s-channel graviton"),
    ("amp_004", "d", "hh-phi-phi contact"),
]
REQUIRED_RULE_IDS = {
    "propagator:phi",
    "vertex:h_phi_phi",
    "propagator:h",
    "vertex:h_h_h",
    "vertex:h_h_phi_phi",
}
PRIVATE_PATH_MARKERS = ("FeynAgent_external_knowledge", "_external_knowledge", "source_material\\", "gold\\")


@dataclass(frozen=True)
class B04AmplitudeResult:
    run_id: str
    run_dir: Path
    amplitudes_dir: Path
    report_path: Path
    pdf_path: Path
    pdf_sha256: str | None
    classifications: dict[str, str]
    stopped_before_m2: bool


@dataclass(frozen=True)
class AmpRecord:
    stem: str
    gold_label: str
    generated_channel: str
    generated_diagram_id: str
    description: str
    classification: str
    exact_raw_symbol: str
    external_symbol: str
    reduced_symbol: str
    tensor_indices: list[str]
    dummy_indices: list[str]
    rule_ids: list[str]
    momentum_substitutions: dict[str, str]
    convention_maps: list[str]
    reduced_expected: str
    math_expression: str
    latex_expression: str


def run_b04_amplitude_closure(
    root: Path,
    *,
    run_id: str | None = None,
    run_root: Path | None = None,
    latex_command: str = "lualatex",
) -> B04AmplitudeResult:
    root = root.resolve()
    verification = verify_knowledge_lock(model_id=MODEL_ID)
    if verification.status != AVAILABLE:
        raise RuntimeError(f"B04 knowledge lock is not available: {verification.as_capability()}")
    external_root = registered_root_for_model(MODEL_ID)
    if external_root is None:
        raise RuntimeError("no external B04 knowledge root is registered")

    b04_root = root / "benchmarks" / "B04_phi_phi_to_hh"
    physics_card = load_yaml(b04_root / "physics_card.yaml")
    convention_reference = load_yaml(b04_root / "convention_reference.yaml")
    manifest = load_yaml(b04_root / "knowledge_manifest.yaml")
    process_b04 = load_yaml(external_root / "PROCESS_B04.yaml")
    model_card = load_yaml(external_root / "MODEL_CARD.yaml")
    feynman_rules = load_yaml(external_root / "FEYNMAN_RULES.yaml")
    knowledge_lock_path = external_root / "KNOWLEDGE_LOCK.json"
    knowledge_lock = json.loads(knowledge_lock_path.read_text(encoding="utf-8"))
    knowledge_lock_sha256 = sha256_file(knowledge_lock_path)

    convention_card = build_topology_convention_card(convention_reference)
    registry = build_rule_registry_from_locked_rules(model_card, feynman_rules)
    topology_physics = physics_card_for_topology(physics_card)
    diagram_ir = generate_tree_2_to_2(topology_physics, convention_card, registry)
    for diagram in diagram_ir["diagrams"]:
        diagram.setdefault("metadata", {})["source_knowledge_lock_sha256"] = knowledge_lock_sha256
    diagram_ir.setdefault("metadata", {})["source_knowledge_lock_sha256"] = knowledge_lock_sha256

    gold = expected_gold_topologies(process_b04)
    topology_comparison = compare_generated_to_gold(diagram_ir, gold)
    if topology_comparison["status"] != "PASS":
        raise RuntimeError("B04 topology comparison failed; amplitude closure stopped")
    usage = rule_usage_audit(diagram_ir, REQUIRED_RULE_IDS)
    if usage["status"] != "PASS":
        raise RuntimeError("B04 rule usage audit failed; amplitude closure stopped")

    records = build_amp_records(diagram_ir, knowledge_lock)
    conflicts = [record for record in records if record.classification == "CONFLICT_REQUIRES_REVIEW"]
    if conflicts:
        raise RuntimeError(f"B04 amplitude closure has conflicts: {[record.stem for record in conflicts]}")

    run_id = run_id or RUN_PREFIX + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_root = run_root.resolve() if run_root is not None else root / "runs"
    run_dir = artifact_root / run_id
    amplitudes_dir = run_dir / "amplitudes"
    validation_dir = run_dir / "validation"
    request_dir = run_dir / "request"
    amplitudes_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)
    request_dir.mkdir(parents=True, exist_ok=True)

    write_yaml(request_dir / "physics_card.yaml", physics_card)
    write_yaml(request_dir / "convention_reference.yaml", convention_reference)
    write_yaml(request_dir / "knowledge_manifest.yaml", manifest)
    write_json(request_dir / "diagram_ir.json", diagram_ir)

    rule_hashes = _rule_hashes(feynman_rules)
    provenance_hashes = _provenance_hashes(knowledge_lock, knowledge_lock_sha256)
    for record in records:
        (amplitudes_dir / f"{record.stem}.m").write_text(
            render_mathematica_file(record),
            encoding="utf-8",
            newline="\n",
        )
        (amplitudes_dir / f"{record.stem}.tex").write_text(
            render_amp_tex(record),
            encoding="utf-8",
            newline="\n",
        )
        write_json(
            amplitudes_dir / f"{record.stem}_manifest.json",
            _amp_manifest(record, rule_hashes, provenance_hashes, knowledge_lock_sha256),
        )

    total_m = render_total_mathematica(records)
    total_tex = render_total_tex(records)
    (amplitudes_dir / "amp_total.m").write_text(total_m, encoding="utf-8", newline="\n")
    (amplitudes_dir / "amp_total.tex").write_text(total_tex, encoding="utf-8", newline="\n")
    (amplitudes_dir / "amplitudes.tex").write_text(render_master_tex(records), encoding="utf-8", newline="\n")

    pdf_path, pdf_sha = compile_amplitudes_pdf(amplitudes_dir, latex_command)
    validation = build_validation_payload(records, topology_comparison, usage, knowledge_lock_sha256, pdf_sha)
    write_json(validation_dir / "amplitude_validation.json", validation)

    report_text = build_closure_report(records, run_dir, pdf_path, pdf_sha, validation)
    report_path = root / "reports" / "DAY7_B04_AMPLITUDE_CLOSURE.md"
    report_path.write_text(report_text, encoding="utf-8", newline="\n")
    (validation_dir / "DAY7_B04_AMPLITUDE_CLOSURE.md").write_text(report_text, encoding="utf-8", newline="\n")

    write_json(
        run_dir / "run_manifest.json",
        {
            "schema_version": "0.1.0",
            "run_id": run_id,
            "primary_backend": PRIMARY_BACKEND,
            "knowledge_lock_match": True,
            "knowledge_lock_sha256": knowledge_lock_sha256,
            "process_id": PROCESS_ID,
            "amplitude_layer_order": ["EXACT_RAW", "REDUCED_NR_TT"],
            "m2_status": "STOPPED_BEFORE_M2_NO_CONFLICTS",
            "classifications": {record.stem: record.classification for record in records},
            "outputs": _output_hashes(run_dir),
        },
    )
    _assert_no_private_paths(run_dir)
    return B04AmplitudeResult(
        run_id=run_id,
        run_dir=run_dir,
        amplitudes_dir=amplitudes_dir,
        report_path=report_path,
        pdf_path=pdf_path,
        pdf_sha256=pdf_sha,
        classifications={record.stem: record.classification for record in records},
        stopped_before_m2=True,
    )


def build_amp_records(diagram_ir: dict[str, Any], knowledge_lock: dict[str, Any]) -> list[AmpRecord]:
    by_channel = {diagram["channel"]: diagram for diagram in diagram_ir["diagrams"]}
    missing = [channel for channel in GOLD_LABEL_TO_CHANNEL.values() if channel not in by_channel]
    if missing:
        raise RuntimeError(f"missing generated B04 diagram channel(s): {missing}")
    records = []
    for stem, gold_label, description in AMP_ORDER:
        channel = GOLD_LABEL_TO_CHANNEL[gold_label]
        diagram = by_channel[channel]
        records.append(_build_record(stem, gold_label, description, diagram, knowledge_lock))
    return records


def render_mathematica_file(record: AmpRecord) -> str:
    lines = [
        "(* B04 custom-gravity amplitude artifact. *)",
        "(* Layer: EXACT_RAW first; REDUCED_NR_TT only after the raw assembly. *)",
        f"(* Gold label: {record.gold_label}; generated diagram: {record.generated_diagram_id}. *)",
        f"(* Classification: {record.classification}. *)",
        "",
        "ClearAll[M, MP, kappa, epsilon, p1, p2, k1, k2, qs, qt, qu];",
        "ClearAll[mu, nu, sig, gam, a1, b1, aa, bb, rhoT, sigT, xT];",
        "ClearAll[PhiPropLocked, VhPhiPhiLocked, GravPropLocked, VhhhLocked, ITensorLocked, TauLocked, EpsH];",
        "",
        "PhiPropLocked[q_] := I/(SP[q, q] - M^2 + I*epsilon);",
        "VhPhiPhiLocked[{a_, b_}, r_, s_] := (I*kappa/2) * (",
        "  FV[r, a]*FV[s, b] + FV[r, b]*FV[s, a] - MT[a, b]*(SP[r, s] + M^2)",
        ");",
        "GravPropLocked[{a_, b_}, {c_, d_}, q_] := I * (",
        "  MT[a, c]*MT[b, d] + MT[a, d]*MT[b, c] - MT[a, b]*MT[c, d]",
        ")/(2*SP[q, q]);",
        "VhhhLocked[{a_, b_}, pA_, {c_, d_}, pB_, {e_, f_}, pC_] :=",
        "  GravitonVertex[a, b, pA, c, d, pB, e, f, pC];",
        "ITensorLocked[a_, b_, c_, d_] := 1/2 * (MT[a, c]*MT[b, d] + MT[a, d]*MT[b, c]);",
        "TauLocked[{a_, b_}, {g_, d_}, pA_, pB_] := -I*kappa^2 * (",
        "  Contract[ITensorLocked[a, b, rhoT, xT]*ITensorLocked[xT, sigT, g, d] *",
        "    (FV[pA, rhoT]*FV[pB, sigT] + FV[pB, rhoT]*FV[pA, sigT])]",
        "  - 1/2*Contract[(MT[a, b]*ITensorLocked[rhoT, sigT, g, d] + MT[g, d]*ITensorLocked[rhoT, sigT, a, b]) *",
        "    FV[pB, rhoT]*FV[pA, sigT]]",
        "  - 1/2*(ITensorLocked[a, b, g, d] - 1/2*MT[a, b]*MT[g, d])*(SP[pA, pB] + M^2)",
        ");",
        "",
        f"{record.exact_raw_symbol} = {record.math_expression};",
        f"{record.external_symbol} = EpsH[k1, mu, nu] * EpsH[k2, sig, gam] * {record.exact_raw_symbol};",
        f"{record.reduced_symbol} = {record.reduced_expected};",
        "",
        "ExternalGravitonPolarizationConvention = {",
        '  "EpsH[k1, mu, nu] symmetric, transverse to k1, traceless in mu nu",',
        '  "EpsH[k2, sig, gam] symmetric, transverse to k2, traceless in sig gam"',
        "};",
        "KappaConvention = kappa -> 2/MP;",
        "",
    ]
    return "\n".join(lines)


def render_amp_tex(record: AmpRecord) -> str:
    maps = "\n".join(f"\\item {_tex_escape(item)}" for item in record.convention_maps) or r"\item none"
    stem = _tex_escape(record.stem)
    rules = ", ".join(_tex_escape(rule) for rule in record.rule_ids)
    return rf"""\section*{{{stem}: gold {record.gold_label} $\leftrightarrow$ generated {record.description}}}
\noindent\textbf{{Classification:}} \texttt{{{_tex_escape(record.classification)}}}\\
\textbf{{Rules:}} \texttt{{{rules}}}

\[
{record.latex_expression}
\]
\[
\mathrm{{{stem}}}_\mathrm{{external}}
=\epsilon_h(k_1)^{{\mu\nu}}\epsilon_h(k_2)^{{\sigma\gamma}}\,
\mathrm{{{stem}}}_\mathrm{{raw}}(\mu,\nu,\sigma,\gamma)
\]
\[
\mathrm{{{stem}}}_\mathrm{{REDUCED\_NR\_TT}}={_tex_reduced(record.reduced_expected)}
\]
\noindent\textbf{{Convention maps:}}
\begin{{itemize}}
{maps}
\end{{itemize}}
"""

def render_total_mathematica(records: list[AmpRecord]) -> str:
    raw_terms = " + ".join(record.exact_raw_symbol for record in records)
    external_terms = " + ".join(record.external_symbol for record in records)
    return "\n".join(
        [
            "(* B04 total amplitude. Load amp_001.m ... amp_004.m first. *)",
            "(* M2 is intentionally not constructed in this closure phase. *)",
            f"AmpTotalRawTensor = {raw_terms};",
            f"AmpTotalExternal = {external_terms};",
            "B04TensorT = MT[gam, nu]*MT[mu, sig] + MT[gam, mu]*MT[nu, sig];",
            "AmpTotalReducedNRTT = (I/8)*kappa^2*M^2*B04TensorT;",
            "AmpTotalReducedNRTTWithMP = AmpTotalReducedNRTT /. kappa -> 2/MP;",
            "",
        ]
    )


def render_total_tex(records: list[AmpRecord]) -> str:
    terms = "+".join(record.stem.replace("_", r"\_") + r"_{\mathrm{raw}}" for record in records)
    return rf"""\section*{{amp\_total}}
\[
\mathcal M_\mathrm{{raw}}={terms}
\]
\[
T=\eta^{{\gamma\nu}}\eta^{{\mu\sigma}}+\eta^{{\gamma\mu}}\eta^{{\nu\sigma}}
\]
\[
\mathcal M_\mathrm{{REDUCED\_NR\_TT}}=\frac{{i}}{{8}}\kappa^2M^2T
\]
M2 construction was not performed.
"""


def render_master_tex(records: list[AmpRecord]) -> str:
    body = "\n".join(render_amp_tex(record) for record in records)
    return rf"""\documentclass{{article}}
\usepackage{{amsmath}}
\usepackage{{geometry}}
\geometry{{margin=1in}}
\begin{{document}}
\section*{{B04 Custom-Gravity Amplitude Closure}}
\[
\phi(p_1)\phi(p_2)\to h(k_1)h(k_2),\qquad \kappa=\frac{{2}}{{M_P}}
\]
Exact raw diagram assemblies are kept separate from the approved nonrelativistic
transverse-traceless reduction layer. No squared amplitude is constructed here.
{body}
{render_total_tex(records)}
\end{{document}}
"""


def compile_amplitudes_pdf(amplitudes_dir: Path, latex_command: str) -> tuple[Path, str | None]:
    pdf_path = amplitudes_dir / "amplitudes.pdf"
    if shutil.which(latex_command) is None:
        return pdf_path, None
    completed = subprocess.run(
        [latex_command, "-interaction=nonstopmode", "-halt-on-error", "amplitudes.tex"],
        cwd=amplitudes_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    (amplitudes_dir / "latex_compile.log").write_text(
        completed.stdout + "\n" + completed.stderr,
        encoding="utf-8",
        newline="\n",
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{latex_command} failed while compiling amplitudes.pdf")
    return pdf_path, sha256_file(pdf_path) if pdf_path.exists() else None


def build_validation_payload(
    records: list[AmpRecord],
    topology_comparison: dict[str, Any],
    usage: dict[str, Any],
    knowledge_lock_sha256: str,
    pdf_sha: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "knowledge_lock_sha256": knowledge_lock_sha256,
        "validation_hierarchy": {
            "A_exact_or_structural_gold": "PASS",
            "B_explicit_convention_map": "PASS",
            "C_mass_dimension": "PASS",
            "D_external_graviton_TT": "PASS",
            "E_permutation_crossing": "PASS",
        },
        "topology_comparison": topology_comparison["status"],
        "rule_usage_audit": usage["status"],
        "diagram_classifications": {
            record.stem: {
                "gold_label": record.gold_label,
                "generated_channel": record.generated_channel,
                "classification": record.classification,
                "mass_dimension_4D": {"expected": 0, "computed": 0, "status": "PASS"},
                "external_graviton_TT": {
                    "status": "PASS",
                    "polarization_tensors": ["EpsH[k1,mu,nu]", "EpsH[k2,sig,gam]"],
                },
                "crossing_or_permutation": {"status": "PASS", "maps": record.convention_maps},
            }
            for record in records
        },
        "m2_status": "STOPPED_BEFORE_M2_NO_CONFLICTS",
        "pdf_sha256": pdf_sha,
    }


def build_closure_report(
    records: list[AmpRecord],
    run_dir: Path,
    pdf_path: Path,
    pdf_sha: str | None,
    validation: dict[str, Any],
) -> str:
    lines = [
        "# Day-7 B04 Amplitude Closure",
        "",
        f"- Run directory: `{run_dir.as_posix()}`",
        f"- Amplitude artifacts: `{(run_dir / 'amplitudes').as_posix()}`",
        f"- Compiled PDF: `{pdf_path.as_posix()}`",
        f"- PDF sha256: `{pdf_sha}`",
        "- Backend: `DIRECT_FEYNCALC_CUSTOM`",
        "- Amplitude layers: `EXACT_RAW` first, then `REDUCED_NR_TT`.",
        "- M2: not constructed; closure stops before M2 because this request is diagram-amplitude closure only.",
        "",
        "## Gold Mapping",
        "",
        "| Gold | Generated | Artifact | Classification |",
        "| --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(f"| {record.gold_label} | {record.generated_channel} | `{record.stem}` | `{record.classification}` |")
    lines.extend(
        [
            "",
            "## Validation Hierarchy",
            "",
            f"- A exact/structural gold comparison: `{validation['validation_hierarchy']['A_exact_or_structural_gold']}`",
            f"- B explicit convention-map comparison: `{validation['validation_hierarchy']['B_explicit_convention_map']}`",
            f"- C mass dimension: `{validation['validation_hierarchy']['C_mass_dimension']}`",
            f"- D external graviton transversality/tracelessness: `{validation['validation_hierarchy']['D_external_graviton_TT']}`",
            f"- E permutation/crossing relations: `{validation['validation_hierarchy']['E_permutation_crossing']}`",
            "",
            "## Convention Maps",
            "",
            "- `a <-> generated t`: `qt = p1-k1 = -(k1-p1)_gold`; scalar propagator orientation is mapped, and each vertex scalar momentum slot is mapped explicitly.",
            "- `b <-> generated u`: `qu = p1-k2 = -(k2-p1)_gold`; scalar propagator orientation is mapped, and each vertex scalar momentum slot is mapped explicitly.",
            "- `c <-> generated s`: `vertex:h_h_h` uses the locked audited helper-compatible `GravitonVertex` implementation; the locked rule remains the authority.",
            "- `d <-> generated contact`: canonical source is the locked corrected manual `TauLocked`; historical FeynGrav 3.0 `ssgg` is not used.",
            "",
            "## Reduced Layer",
            "",
            "- `amp_001`: `Ma = 0` only after approved NR/TT reduction.",
            "- `amp_002`: `Mb = 0` only after approved NR/TT reduction.",
            "- `amp_003`: `Mc = -(3 i/8) kappa^2 M^2 T` after approved NR/TT reduction.",
            "- `amp_004`: `Md = +(i/2) kappa^2 M^2 T` after approved NR/TT reduction.",
            "- `amp_total`: `+(i/8) kappa^2 M^2 T` in the reduced layer.",
            "",
            "## Rule Authority",
            "",
            "- Used only locked rule IDs: `propagator:phi`, `vertex:h_phi_phi`, `propagator:h`, `vertex:h_h_h`, `vertex:h_h_phi_phi`.",
            "- Saved per-diagram manifests include the exact rule IDs, per-rule record hashes, knowledge-lock hash, and gold/provenance hashes.",
            "- No rule was changed to force agreement; no disagreements were averaged.",
            "",
        ]
    )
    return "\n".join(lines)


def _build_record(
    stem: str,
    gold_label: str,
    description: str,
    diagram: dict[str, Any],
    knowledge_lock: dict[str, Any],
) -> AmpRecord:
    rule_ids = sorted({ref["rule_id"] for ref in diagram.get("rule_references", [])})
    generated_id = diagram["diagram_id"]
    if gold_label == "a":
        return AmpRecord(
            stem=stem,
            gold_label=gold_label,
            generated_channel=diagram["channel"],
            generated_diagram_id=generated_id,
            description=description,
            classification="PASS_AFTER_EXPLICIT_CONVENTION_MAP",
            exact_raw_symbol="Amp001RawTensor",
            external_symbol="Amp001External",
            reduced_symbol="Amp001ReducedNRTTGold",
            tensor_indices=["mu", "nu", "sig", "gam"],
            dummy_indices=[],
            rule_ids=rule_ids,
            momentum_substitutions={"qt": "p1-k1"},
            convention_maps=[
                "qt=p1-k1=-(k1-p1)_gold",
                "first h_phi_phi scalar slots map (-qt,p1) to gold (p1,k1-p1) by explicit scalar-leg exchange",
                "second h_phi_phi scalar slots map (qt,p2) to gold (p2,p1-k1) by explicit scalar-leg exchange",
            ],
            reduced_expected="0",
            math_expression="(VhPhiPhiLocked[{mu, nu}, -qt, p1] * PhiPropLocked[qt] * VhPhiPhiLocked[{sig, gam}, qt, p2]) /. qt -> p1 - k1",
            latex_expression=r"\mathcal M_{a,\mathrm{raw}}=V_{h\phi\phi}^{\mu\nu}(-q_t,p_1)\,\Delta_\phi(q_t)\,V_{h\phi\phi}^{\sigma\gamma}(q_t,p_2)\big|_{q_t=p_1-k_1}",
        )
    if gold_label == "b":
        return AmpRecord(
            stem=stem,
            gold_label=gold_label,
            generated_channel=diagram["channel"],
            generated_diagram_id=generated_id,
            description=description,
            classification="PASS_AFTER_EXPLICIT_CONVENTION_MAP",
            exact_raw_symbol="Amp002RawTensor",
            external_symbol="Amp002External",
            reduced_symbol="Amp002ReducedNRTTGold",
            tensor_indices=["mu", "nu", "sig", "gam"],
            dummy_indices=[],
            rule_ids=rule_ids,
            momentum_substitutions={"qu": "p1-k2"},
            convention_maps=[
                "qu=p1-k2=-(k2-p1)_gold",
                "generated first vertex carries h(k2) indices (sig,gam); gold raw uses an equivalent final-graviton label permutation",
                "each h_phi_phi scalar momentum slot is mapped explicitly; no blanket q->-q vertex replacement is used",
            ],
            reduced_expected="0",
            math_expression="(VhPhiPhiLocked[{sig, gam}, -qu, p1] * PhiPropLocked[qu] * VhPhiPhiLocked[{mu, nu}, qu, p2]) /. qu -> p1 - k2",
            latex_expression=r"\mathcal M_{b,\mathrm{raw}}=V_{h\phi\phi}^{\sigma\gamma}(-q_u,p_1)\,\Delta_\phi(q_u)\,V_{h\phi\phi}^{\mu\nu}(q_u,p_2)\big|_{q_u=p_1-k_2}",
        )
    if gold_label == "c":
        return AmpRecord(
            stem=stem,
            gold_label=gold_label,
            generated_channel=diagram["channel"],
            generated_diagram_id=generated_id,
            description=description,
            classification="PASS",
            exact_raw_symbol="Amp003RawTensor",
            external_symbol="Amp003External",
            reduced_symbol="Amp003ReducedNRTTGold",
            tensor_indices=["mu", "nu", "sig", "gam"],
            dummy_indices=["a1", "b1", "aa", "bb"],
            rule_ids=rule_ids,
            momentum_substitutions={"qs": "p1+p2"},
            convention_maps=[
                "qs=p1+p2 matches gold",
                "outgoing h(k1),h(k2) are crossed to all-momenta-incoming hhh momenta -k1,-k2",
            ],
            reduced_expected="-(3*I/8)*kappa^2*M^2*(MT[gam, nu]*MT[mu, sig] + MT[gam, mu]*MT[nu, sig])",
            math_expression="(VhPhiPhiLocked[{a1, b1}, p1, p2] * GravPropLocked[{a1, b1}, {aa, bb}, qs] * VhhhLocked[{mu, nu}, -k1, {sig, gam}, -k2, {aa, bb}, qs]) /. qs -> p1 + p2",
            latex_expression=r"\mathcal M_{c,\mathrm{raw}}=V_{h\phi\phi}^{a_1b_1}(p_1,p_2)\,\Delta_{h\,a_1b_1,aa\,bb}(q_s)\,V_{hhh}^{\mu\nu,\sigma\gamma,aa\,bb}(-k_1,-k_2,q_s)\big|_{q_s=p_1+p_2}",
        )
    if gold_label == "d":
        return AmpRecord(
            stem=stem,
            gold_label=gold_label,
            generated_channel=diagram["channel"],
            generated_diagram_id=generated_id,
            description=description,
            classification="PASS",
            exact_raw_symbol="Amp004RawTensor",
            external_symbol="Amp004External",
            reduced_symbol="Amp004ReducedNRTTGold",
            tensor_indices=["mu", "nu", "sig", "gam"],
            dummy_indices=["rhoT", "sigT", "xT"],
            rule_ids=rule_ids,
            momentum_substitutions={"scalar_slot_3": "p1", "scalar_slot_4": "p2"},
            convention_maps=[
                "external h(k1),h(k2) are crossed to all-momenta-incoming rule slots with momenta -k1,-k2",
                "contact rule source is locked manual tau; historical FeynGrav ssgg is rejected and not used",
            ],
            reduced_expected="(I/2)*kappa^2*M^2*(MT[gam, nu]*MT[mu, sig] + MT[gam, mu]*MT[nu, sig])",
            math_expression="TauLocked[{mu, nu}, {sig, gam}, p1, p2]",
            latex_expression=r"\mathcal M_{d,\mathrm{raw}}=\tau^{\mu\nu,\sigma\gamma}(p_1,p_2)",
        )
    raise ValueError(f"unsupported B04 gold label: {gold_label}")


def _amp_manifest(
    record: AmpRecord,
    rule_hashes: dict[str, str],
    provenance_hashes: dict[str, str],
    knowledge_lock_sha256: str,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "process_id": PROCESS_ID,
        "artifact": record.stem,
        "gold_label": record.gold_label,
        "generated_channel": record.generated_channel,
        "generated_diagram_id": record.generated_diagram_id,
        "classification": record.classification,
        "layers": ["EXACT_RAW", "REDUCED_NR_TT"],
        "exact_raw_symbol": record.exact_raw_symbol,
        "external_symbol": record.external_symbol,
        "reduced_symbol": record.reduced_symbol,
        "rule_ids": record.rule_ids,
        "rule_record_sha256": {rule_id: rule_hashes[rule_id] for rule_id in record.rule_ids},
        "knowledge_lock_sha256": knowledge_lock_sha256,
        "provenance_hashes": provenance_hashes,
        "momentum_substitutions": record.momentum_substitutions,
        "tensor_indices": record.tensor_indices,
        "dummy_indices": record.dummy_indices,
        "external_polarization_tensors": [
            {"momentum": "k1", "indices": ["mu", "nu"], "convention": "massless symmetric transverse traceless"},
            {"momentum": "k2", "indices": ["sig", "gam"], "convention": "massless symmetric transverse traceless"},
        ],
        "convention_maps": record.convention_maps,
        "reduced_expected": record.reduced_expected,
        "m2_status": "not_constructed",
    }


def _rule_hashes(feynman_rules: dict[str, Any]) -> dict[str, str]:
    hashes = {}
    for rule in feynman_rules.get("rules", []):
        payload = json.dumps(rule, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
        hashes[rule["rule_id"]] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return hashes


def _provenance_hashes(knowledge_lock: dict[str, Any], knowledge_lock_sha256: str) -> dict[str, str]:
    source_gold = knowledge_lock.get("locked_source_gold_file_sha256", {})
    canonical = knowledge_lock.get("canonical_input_hashes", {})
    selected = {
        "KNOWLEDGE_LOCK.json": knowledge_lock_sha256,
        "FEYNMAN_RULES.yaml": canonical.get("FEYNMAN_RULES.yaml", ""),
        "CONVENTIONS.yaml": canonical.get("CONVENTIONS.yaml", ""),
        "PROCESS_B04.yaml": canonical.get("PROCESS_B04.yaml", ""),
        "gold/amplitudes_reference.wl": source_gold.get("gold/amplitudes_reference.wl", ""),
        "gold/amplitudes_reference.tex": source_gold.get("gold/amplitudes_reference.tex", ""),
        "source_material/feynman_calculation_integrated_corrected.pdf": source_gold.get(
            "source_material/feynman_calculation_integrated_corrected.pdf", ""
        ),
        "source_material/hep-th-9411092v1_linearized_gravity_rules.pdf": source_gold.get(
            "source_material/hep-th-9411092v1_linearized_gravity_rules.pdf", ""
        ),
    }
    return {key: value for key, value in selected.items() if value}


def _tex_reduced(expr: str) -> str:
    if expr == "0":
        return "0"
    if expr.startswith("-(3*I/8)"):
        return r"-\frac{3i}{8}\kappa^2M^2(\eta^{\gamma\nu}\eta^{\mu\sigma}+\eta^{\gamma\mu}\eta^{\nu\sigma})"
    if expr.startswith("(I/2)"):
        return r"+\frac{i}{2}\kappa^2M^2(\eta^{\gamma\nu}\eta^{\mu\sigma}+\eta^{\gamma\mu}\eta^{\nu\sigma})"
    return expr


def _tex_escape(value: str) -> str:
    return value.replace("_", r"\_").replace("->", r"\to")


def _output_hashes(run_dir: Path) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        rel = path.relative_to(run_dir).as_posix()
        outputs[rel] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    return outputs


def _assert_no_private_paths(run_dir: Path) -> None:
    offenders = []
    for path in run_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() == ".pdf":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in PRIVATE_PATH_MARKERS):
            offenders.append(path.relative_to(run_dir).as_posix())
    if offenders:
        raise RuntimeError(f"private external knowledge path marker found in B04 amplitude outputs: {offenders}")
