"""Day-7 B04 topology closure helpers.

This module adapts the locked custom gravity knowledge package into the existing
backend-neutral RuleRegistry/DiagramIR topology machinery. It does not assemble
FeynCalc amplitudes and does not compute M2.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .custom_knowledge import AVAILABLE, registered_root_for_model, verify_knowledge_lock
from .diagrams import generate_tree_2_to_2
from .render import render_tikz_feynman

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


MODEL_ID = "reheating_scalar_gravity_v1"
PRIMARY_BACKEND = "DIRECT_FEYNCALC_CUSTOM"
RULE_SET_ID = "ruleset:reheating_scalar_gravity_v1"
REGISTRY_ID = "registry:reheating_scalar_gravity_v1"
PROCESS_ID = "process:B04_phi_phi_to_h_h"
PRIVATE_PATH_MARKERS = ("FeynAgent_external_knowledge", "_external_knowledge", "source_material\\", "gold\\")


@dataclass(frozen=True)
class Phase5Result:
    run_id: str
    run_dir: Path
    report_path: Path
    knowledge_lock_match: bool
    primary_backend: str
    gold_topology_count: int
    generated_topology_count: int
    topology_comparison_pass: bool
    rule_usage_audit_pass: bool
    diagram_pdf_pass: bool
    diagram_pdf_sha256: str | None


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML mapping in {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_topology_convention_card(convention_reference: dict[str, Any]) -> dict[str, Any]:
    essentials = convention_reference.get("essentials", {})
    return {
        "schema_version": "0.1.1",
        "object_id": "convention_card:b04_reheating_scalar_gravity_topology",
        "status": "approved",
        "spacetime_dimension": {"symbol": "D", "value": int(essentials.get("spacetime_dimension", 4))},
        "metric_signature": essentials.get("metric_signature", "+---"),
        "momentum_convention": {
            "fourier_phase": "exp_minus_i_p_x",
            "propagator_momentum_flow": "explicit_per_line",
        },
        "all_momenta_incoming_vertex_convention": essentials.get("vertex_rule_default", "").startswith("all momenta incoming"),
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
        "gravity_convention": {
            "metric_expansion": "g_munu_equals_eta_plus_kappa_h",
            "planck_mass_convention": "reduced_planck_mass",
        },
        "metadata": {
            "notes": "Topology-only ConventionCard adapter from locked B04 convention reference; no amplitude or M2 convention changes.",
        },
    }


def build_rule_registry_from_locked_rules(model_card: dict[str, Any], feynman_rules: dict[str, Any]) -> dict[str, Any]:
    field_roles = {
        field["particle_id"]: _field_role(field["field_type"])
        for field in model_card.get("fields", [])
    }
    particle_catalog = []
    for field in model_card.get("fields", []):
        particle_id = field["particle_id"]
        particle_catalog.append(
            {
                "particle_id": particle_id,
                "display_name": field.get("role", particle_id),
                "field_role": field_roles[particle_id],
                "self_conjugate": bool(field.get("self_conjugate", True)),
                "antiparticle_id": particle_id,
                "fermion_number": 0,
            }
        )

    vertices = []
    propagators = []
    for rule in feynman_rules.get("rules", []):
        record = _rule_record(rule, field_roles)
        if record["rule_type"] == "vertex":
            vertices.append(record)
        elif record["rule_type"] == "propagator":
            propagators.append(record)
    return {
        "schema_version": "0.1.1",
        "object_id": "rule_registry:reheating_scalar_gravity_v1",
        "status": "approved",
        "registry_id": REGISTRY_ID,
        "particle_catalog": particle_catalog,
        "rule_sets": [
            {
                "rule_set_id": RULE_SET_ID,
                "display_name": "Locked B04 topology-only gravity rules",
                "status": "approved",
                "convention_card_id": "convention_card:b04_reheating_scalar_gravity_topology",
            }
        ],
        "vertices": vertices,
        "propagators": propagators,
        "metadata": {
            "notes": "Transient topology RuleRegistry adapter from locked FEYNMAN_RULES.yaml. FeynCalc expressions are placeholders for topology only.",
        },
    }


def physics_card_for_topology(physics_card: dict[str, Any]) -> dict[str, Any]:
    physics = json.loads(json.dumps(physics_card))
    physics["selected_rule_set"] = {"registry_id": REGISTRY_ID, "rule_set_ids": [RULE_SET_ID]}
    physics.setdefault("presentation", {})["particle_latex_labels"] = [
        {"particle_id": "phi", "latex_label": r"\phi"},
        {"particle_id": "h", "latex_label": r"h_{\mu\nu}"},
    ]
    return physics


def annotate_diagram_ir(diagram_ir: dict[str, Any], knowledge_lock_sha256: str) -> dict[str, Any]:
    annotated = json.loads(json.dumps(diagram_ir))
    annotated.setdefault("metadata", {})["source_knowledge_lock_sha256"] = knowledge_lock_sha256
    for diagram in annotated["diagrams"]:
        diagram.setdefault("metadata", {})["source_knowledge_lock_sha256"] = knowledge_lock_sha256
    return annotated


def expected_gold_topologies(process_b04: dict[str, Any]) -> list[dict[str, Any]]:
    if "expected_topology" in process_b04:
        return list(process_b04.get("expected_topology", {}).get("diagrams", []))
    return list(process_b04.get("diagrams", []))


def compare_generated_to_gold(diagram_ir: dict[str, Any], gold_topologies: list[dict[str, Any]]) -> dict[str, Any]:
    generated = [_generated_topology_record(diagram) for diagram in diagram_ir["diagrams"]]
    unmatched = list(range(len(generated)))
    rows = []
    for gold in gold_topologies:
        best_index = None
        best_status = "MISSING_GENERATED"
        best_map = ""
        for index in unmatched:
            status, representation_map = _compare_one(gold, generated[index])
            if status == "MATCH":
                best_index = index
                best_status = status
                best_map = representation_map
                break
            if status == "MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP" and best_index is None:
                best_index = index
                best_status = status
                best_map = representation_map
        if best_index is None:
            rows.append({"gold_label": gold.get("label"), "generated_diagram_id": None, "classification": best_status, "representation_map": ""})
            continue
        unmatched.remove(best_index)
        rows.append(
            {
                "gold_label": gold.get("label"),
                "gold_topology": gold.get("topology"),
                "gold_internal_species": gold.get("internal_species"),
                "gold_internal_momentum": gold.get("internal_momentum"),
                "generated_diagram_id": generated[best_index]["diagram_id"],
                "generated_channel": generated[best_index]["channel"],
                "generated_internal_species": generated[best_index]["internal_species"],
                "generated_internal_momentum": generated[best_index]["internal_momentum"],
                "classification": best_status,
                "representation_map": best_map,
            }
        )
    for index in unmatched:
        rows.append(
            {
                "gold_label": None,
                "generated_diagram_id": generated[index]["diagram_id"],
                "generated_channel": generated[index]["channel"],
                "classification": "UNEXPECTED_GENERATED",
                "representation_map": "",
            }
        )
    status = "PASS" if rows and all(row["classification"] in {"MATCH", "MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP"} for row in rows) else "FAIL"
    return {"status": status, "rows": rows, "generated": generated}


def rule_usage_audit(diagram_ir: dict[str, Any], approved_rule_ids: set[str]) -> dict[str, Any]:
    diagrams = []
    all_used: set[str] = set()
    for diagram in diagram_ir["diagrams"]:
        used = [ref["rule_id"] for ref in diagram.get("rule_references", [])]
        all_used.update(used)
        diagrams.append({"diagram_id": diagram["diagram_id"], "rule_ids": used})
    unexpected = sorted(all_used - approved_rule_ids)
    return {
        "status": "PASS" if not unexpected else "FAIL",
        "approved_rule_ids": sorted(approved_rule_ids),
        "used_rule_ids": sorted(all_used),
        "unexpected_rule_ids": unexpected,
        "diagrams": diagrams,
    }


def run_b04_topology_phase(
    root: Path,
    *,
    run_id: str | None = None,
    latex_command: str = "lualatex",
) -> Phase5Result:
    root = root.resolve()
    verification = verify_knowledge_lock(model_id=MODEL_ID)
    if verification.status != AVAILABLE:
        raise RuntimeError(f"knowledge lock is not available: {verification.as_capability()}")
    external_root = registered_root_for_model(MODEL_ID)
    if external_root is None:
        raise RuntimeError("no external knowledge root registered for B04")

    b04_root = root / "benchmarks" / "B04_phi_phi_to_hh"
    manifest = load_yaml(b04_root / "knowledge_manifest.yaml")
    physics_card = load_yaml(b04_root / "physics_card.yaml")
    convention_reference = load_yaml(b04_root / "convention_reference.yaml")
    process_b04 = load_yaml(external_root / "PROCESS_B04.yaml")
    model_card = load_yaml(external_root / "MODEL_CARD.yaml")
    feynman_rules = load_yaml(external_root / "FEYNMAN_RULES.yaml")
    knowledge_lock_path = external_root / "KNOWLEDGE_LOCK.json"
    knowledge_lock = json.loads(knowledge_lock_path.read_text(encoding="utf-8"))
    knowledge_lock_sha256 = sha256_file(knowledge_lock_path)

    convention_card = build_topology_convention_card(convention_reference)
    rule_registry = build_rule_registry_from_locked_rules(model_card, feynman_rules)
    topology_physics = physics_card_for_topology(physics_card)
    diagram_ir = annotate_diagram_ir(
        generate_tree_2_to_2(topology_physics, convention_card, rule_registry),
        knowledge_lock_sha256,
    )
    gold = expected_gold_topologies(process_b04)
    comparison = compare_generated_to_gold(diagram_ir, gold)
    approved_rules = set(knowledge_lock.get("required_rules", []))
    usage = rule_usage_audit(diagram_ir, approved_rules)
    if comparison["status"] != "PASS" or usage["status"] != "PASS":
        raise RuntimeError("B04 topology generation failed structural comparison or rule usage audit")

    run_id = run_id or "day7_b04_topology_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = root / "runs" / run_id
    request_dir = run_dir / "request"
    diagrams_dir = run_dir / "diagrams"
    validation_dir = run_dir / "validation"
    for directory in (request_dir, diagrams_dir, validation_dir):
        directory.mkdir(parents=True, exist_ok=True)

    write_yaml(request_dir / "physics_card.yaml", physics_card)
    write_yaml(request_dir / "convention_reference.yaml", convention_reference)
    write_yaml(request_dir / "convention_card.yaml", convention_card)
    write_yaml(request_dir / "knowledge_manifest.yaml", manifest)
    write_yaml(diagrams_dir / "diagram_source.yaml", diagram_ir)
    write_json(diagrams_dir / "diagram_source.json", diagram_ir)
    write_json(diagrams_dir / "diagrams.json", {"diagrams": comparison["generated"], "comparison": comparison["rows"]})
    write_json(run_dir / "rule_usage.json", usage)

    render_manifest = render_tikz_feynman(topology_physics, convention_card, diagram_ir, diagrams_dir, latex_command=latex_command)
    _sanitize_render_manifest(diagrams_dir / "render_manifest.json", run_dir)
    pdf_path = diagrams_dir / "diagrams.pdf"
    pdf_pass = pdf_path.exists() and pdf_path.stat().st_size > 0
    pdf_sha = sha256_file(pdf_path) if pdf_pass else None

    topology_report = build_topology_report(
        knowledge_lock_sha256=knowledge_lock_sha256,
        primary_backend=PRIMARY_BACKEND,
        gold=gold,
        diagram_ir=diagram_ir,
        comparison=comparison,
        usage=usage,
        pdf_path=pdf_path,
        pdf_sha256=pdf_sha,
        tests="pending",
        warnings=_warnings(),
    )
    (validation_dir / "topology_report.md").write_text(topology_report, encoding="utf-8", newline="\n")
    report_path = root / "reports" / "DAY7_B04_TOPOLOGY.md"
    report_path.write_text(topology_report.replace("tests=pending", "tests=see final regression command"), encoding="utf-8", newline="\n")

    manifest_payload = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "primary_backend": PRIMARY_BACKEND,
        "knowledge_lock_match": True,
        "knowledge_lock_sha256": knowledge_lock_sha256,
        "gold_topology_count": len(gold),
        "generated_topology_count": len(diagram_ir["diagrams"]),
        "topology_comparison": comparison["status"],
        "rule_usage_audit": usage["status"],
        "diagram_pdf": "PASS" if pdf_pass else "FAIL",
        "diagram_pdf_sha256": pdf_sha,
        "outputs": _output_hashes(run_dir),
        "notes": "Topology and diagram-rendering run only. No amplitudes, M2, or reheating approximations were calculated.",
    }
    write_json(run_dir / "run_manifest.json", manifest_payload)
    _assert_no_private_paths(run_dir)
    return Phase5Result(
        run_id=run_id,
        run_dir=run_dir,
        report_path=report_path,
        knowledge_lock_match=True,
        primary_backend=PRIMARY_BACKEND,
        gold_topology_count=len(gold),
        generated_topology_count=len(diagram_ir["diagrams"]),
        topology_comparison_pass=comparison["status"] == "PASS",
        rule_usage_audit_pass=usage["status"] == "PASS",
        diagram_pdf_pass=pdf_pass,
        diagram_pdf_sha256=pdf_sha,
    )


def build_topology_report(
    *,
    knowledge_lock_sha256: str,
    primary_backend: str,
    gold: list[dict[str, Any]],
    diagram_ir: dict[str, Any],
    comparison: dict[str, Any],
    usage: dict[str, Any],
    pdf_path: Path,
    pdf_sha256: str | None,
    tests: str,
    warnings: list[str],
) -> str:
    lines = [
        "# Day-7 B04 Topology Closure",
        "",
        f"- Knowledge lock hash: `{knowledge_lock_sha256}`",
        f"- Primary backend: `{primary_backend}`",
        "- Scope: topology generation, structural gold comparison, and diagram rendering only.",
        "- Amplitudes: not calculated.",
        "- M2: not calculated.",
        "- Reheating/nonrelativistic approximations: not applied.",
        "",
        "## Gold Topology",
        "",
    ]
    for item in gold:
        lines.append(f"- `{item.get('label')}`: {item.get('topology')}, internal={item.get('internal_species')}, momentum={item.get('internal_momentum')}")
    lines.extend(["", "## Generated Topology", ""])
    for diagram in diagram_ir["diagrams"]:
        internal = diagram.get("internal_lines", [])
        if internal:
            species = internal[0]["particle_id"]
            momentum = internal[0]["momentum"]["expression"]
        else:
            species = None
            momentum = None
        rules = ", ".join(ref["rule_id"] for ref in diagram.get("rule_references", []))
        order = ", ".join(f"{item['coupling']}^{item['power']}" for item in diagram.get("coupling_order", []))
        lines.append(f"- `{diagram['diagram_id']}`: channel={diagram['channel']}, internal={species}, momentum={momentum}, order={order}, rules={rules}")
    lines.extend(["", "## Structural Comparison", "", "| Gold | Generated | Classification | Representation Map |", "| --- | --- | --- | --- |"])
    for row in comparison["rows"]:
        lines.append(
            f"| {row.get('gold_label')} | {row.get('generated_diagram_id')} | {row['classification']} | {row.get('representation_map', '')} |"
        )
    lines.extend(["", "## Rule Usage", ""])
    lines.append(f"- Audit: `{usage['status']}`")
    lines.append(f"- Used rules: {', '.join(f'`{rule}`' for rule in usage['used_rule_ids'])}")
    lines.append(f"- Unexpected rules: {', '.join(usage['unexpected_rule_ids']) if usage['unexpected_rule_ids'] else 'none'}")
    lines.extend(["", "## Diagram Artifact", ""])
    lines.append(f"- PDF: `{pdf_path.as_posix()}`")
    lines.append(f"- PDF sha256: `{pdf_sha256}`")
    lines.extend(["", "## Representation Maps", ""])
    lines.append("- Scalar-exchange internal momenta are compared up to internal-line orientation: `p1-k1` maps to `-(k1-p1)` and `p1-k2` maps to `-(k2-p1)`.")
    lines.append("- External outgoing gravitons are crossed to all-momenta-incoming vertex bindings by the existing DiagramIR convention conversion.")
    lines.append("- FeynCalc is reserved for the later amplitude algebra phase and is not used as a topology enumerator here.")
    lines.extend(["", "## Tests", "", f"- {tests}", "", "## Warnings", ""])
    for warning in warnings:
        lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def _field_role(field_type: str) -> str:
    if field_type == "real_scalar":
        return "scalar"
    if field_type == "massless_spin2_symmetric_tensor":
        return "symmetric_rank_2_tensor"
    raise ValueError(f"unsupported locked field_type for topology: {field_type}")


def _quantum_field_role(field_role: str) -> str:
    if field_role == "scalar":
        return "scalar_field"
    if field_role == "symmetric_rank_2_tensor":
        return "symmetric_rank_2_tensor_field"
    raise ValueError(f"unsupported field_role for topology: {field_role}")


def _rule_record(rule: dict[str, Any], field_roles: dict[str, str]) -> dict[str, Any]:
    fields = rule.get("fields", [])
    participating = []
    for slot, particle_id in enumerate(fields, start=1):
        role = field_roles[particle_id]
        participating.append(
            {
                "slot": slot,
                "field_id": f"field:b04:{particle_id}:{slot}",
                "particle_id": particle_id,
                "field_role": role,
                "quantum_field_role": _quantum_field_role(role),
                "fermion_flow_role": "not_applicable",
                "arrow_flow": "none",
                "index_label": _index_label(particle_id, slot),
            }
        )
    expression = rule.get("latex") or rule.get("latex_compact_source_form") or rule.get("I_tensor") or "topology_only"
    return {
        "rule_id": rule["rule_id"],
        "rule_type": rule["rule_type"],
        "rule_set_id": RULE_SET_ID,
        "participating_fields": participating,
        "momentum_labels_order": [rule.get("momentum", "q")] if rule["rule_type"] == "propagator" else [f"p{index}" for index in range(1, len(fields) + 1)],
        "lorentz_index_structure": {"form": "symbolic", "expression": _lorentz_summary(fields)},
        "latex": expression,
        "feyncalc": {"template": rule.get("feyncalc_template", f"TOPOLOGY_ONLY[{rule['rule_id']}]")},
        "coupling_order": [{"coupling": "kappa", "power": _kappa_power(expression)}],
        "mass_dimension": 0,
        "symmetries": ["field_exchange_symmetric"] if len(set(fields)) < len(fields) else ["none"],
        "provenance": [
            {
                "source_type": "local_file",
                "local_source_path": "locked_knowledge_package/FEYNMAN_RULES.yaml",
                "notes": "Locked B04 topology-only adapter; raw private paths are not persisted in run artifacts.",
                "checked_by": "codex",
                "checked_at": "2026-08-19T00:00:00+08:00",
            }
        ],
        "trust_status": "trusted",
        "metadata": {"notes": f"Locked trust status: {rule.get('trust_status', 'unspecified')}"},
    }


def _index_label(particle_id: str, slot: int) -> str:
    if particle_id == "h":
        return f"h{slot}"
    return f"s{slot}"


def _lorentz_summary(fields: list[str]) -> str:
    h_count = sum(1 for field in fields if field == "h")
    if h_count == 0:
        return "scalar topology expression"
    return f"{h_count} symmetric rank-2 graviton index pair(s); topology phase records indices symbolically"


def _kappa_power(expression: str) -> int:
    if "kappa^2" in expression or "kappa**2" in expression:
        return 2
    if "kappa" in expression:
        return 1
    return 0


def _generated_topology_record(diagram: dict[str, Any]) -> dict[str, Any]:
    internal = diagram.get("internal_lines", [])
    return {
        "diagram_id": diagram["diagram_id"],
        "channel": diagram["channel"],
        "internal_species": internal[0]["particle_id"] if internal else None,
        "internal_momentum": internal[0]["momentum"]["expression"] if internal else None,
        "vertex_rule_ids": [vertex["rule_id"] for vertex in diagram.get("vertex_instances", [])],
        "rule_ids": [ref["rule_id"] for ref in diagram.get("rule_references", [])],
        "coupling_order": diagram.get("coupling_order", []),
        "symmetry_factor": diagram.get("symmetry_factor"),
    }


def _compare_one(gold: dict[str, Any], generated: dict[str, Any]) -> tuple[str, str]:
    if not _topology_species_compatible(gold, generated):
        return "CONFLICT", ""
    gold_momentum = gold.get("internal_momentum")
    generated_momentum = generated.get("internal_momentum")
    if gold_momentum == generated_momentum:
        return "MATCH", ""
    if gold_momentum is None and generated_momentum is None:
        return "MATCH", ""
    if _momenta_equal_up_to_sign(str(gold_momentum), str(generated_momentum)):
        return "MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP", "internal momentum differs by internal-line orientation sign"
    return "CONFLICT", ""


def _topology_species_compatible(gold: dict[str, Any], generated: dict[str, Any]) -> bool:
    if gold.get("internal_species") != generated.get("internal_species"):
        return False
    topology = gold.get("topology")
    if topology == "contact_h_h_phi_phi":
        return generated.get("channel") == "contact" and "vertex:h_h_phi_phi" in generated.get("rule_ids", [])
    if topology == "s_channel_graviton_exchange":
        return generated.get("internal_species") == "h" and "vertex:h_h_h" in generated.get("rule_ids", [])
    if topology == "scalar_exchange":
        return generated.get("internal_species") == "phi" and generated.get("channel") in {"t", "u"}
    return False


def _momenta_equal_up_to_sign(first: str, second: str) -> bool:
    return _momentum_vector(first) == _momentum_vector(second) or _momentum_vector(first) == {key: -value for key, value in _momentum_vector(second).items()}


def _momentum_vector(expression: str) -> dict[str, int]:
    clean = expression.replace(" ", "")
    terms: dict[str, int] = {}
    sign = 1
    token = ""
    for char in clean + "+":
        if char in "+-":
            if token:
                terms[token] = terms.get(token, 0) + sign
            token = ""
            sign = 1 if char == "+" else -1
        else:
            token += char
    return {key: value for key, value in sorted(terms.items()) if value != 0}


def _sanitize_render_manifest(path: Path, run_dir: Path) -> None:
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for group in ("outputs",):
        for key, value in list(data.get(group, {}).items()):
            if isinstance(value, str):
                data[group][key] = _relative_to(value, run_dir)
    command = data.get("compile", {}).get("command", [])
    data.get("compile", {})["command"] = [_relative_to(item, run_dir) if isinstance(item, str) else item for item in command]
    write_json(path, data)


def _relative_to(value: str, root: Path) -> str:
    path = Path(value)
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (OSError, ValueError):
        return value


def _output_hashes(run_dir: Path) -> dict[str, dict[str, Any]]:
    outputs: dict[str, dict[str, Any]] = {}
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        rel = path.relative_to(run_dir).as_posix()
        outputs[rel] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    return outputs


def _assert_no_private_paths(run_dir: Path) -> None:
    offenders = []
    for path in run_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".pdf"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in PRIVATE_PATH_MARKERS):
            offenders.append(path.relative_to(run_dir).as_posix())
    if offenders:
        raise RuntimeError(f"private external knowledge path marker found in run outputs: {offenders}")


def _warnings() -> list[str]:
    return [
        "Scalar-exchange gold momenta match generated routing only after explicit internal-line orientation mapping.",
        "Diagram rendering is presentation-only and does not modify DiagramIR physics.",
        "FeynCalc is intentionally unused in Phase 5 except as the selected future algebra backend.",
    ]




