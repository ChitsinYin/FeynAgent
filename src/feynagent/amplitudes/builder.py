"""Deterministic Day-3 tree-level AmplitudeIR builder."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


class AmplitudeBuildError(ValueError):
    """Raised when approved structured inputs cannot produce AmplitudeIR."""


AUDITED_RULE_STATUSES = {"validated", "trusted"}
CHANNEL_PARTITIONS = {
    "s": ((1, 2), (3, 4)),
    "t": ((1, 3), (2, 4)),
    "u": ((1, 4), (2, 3)),
}


def build_amplitude_ir(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    rule_registry: dict[str, Any],
    diagram_ir: dict[str, Any],
    *,
    source_hashes: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build derived tree-level AmplitudeIR from approved structured inputs."""

    _validate_inputs(physics_card, convention_card, rule_registry, diagram_ir)
    source_hashes = source_hashes or {}
    process_tail = _id_tail(physics_card["process_id"])
    amplitudes = [
        _build_diagram_amplitude(process_tail, diagram, rule_registry)
        for diagram in diagram_ir["diagrams"]
    ]
    result = {
        "schema_version": "0.1.0",
        "object_id": f"amplitude_ir:{process_tail}:generated",
        "ir_type": "derived_amplitude_ir",
        "status": "derived_candidate",
        "process_id": physics_card["process_id"],
        "source": {
            "physics_card_id": physics_card["object_id"],
            "convention_card_id": convention_card["object_id"],
            "rule_registry_id": rule_registry["registry_id"],
            "rule_registry_sha256": source_hashes.get("rule_registry", _stable_hash(rule_registry)),
            "diagram_ir_id": diagram_ir["object_id"],
            "diagram_ir_sha256": source_hashes.get("diagram_ir", _stable_hash(diagram_ir)),
        },
        "total_amplitude": {
            "term_amplitude_ids": [amplitude["amplitude_id"] for amplitude in amplitudes],
            "sum_kind": "ordered_symbolic_sum",
            "notes": "Symbolic sum of accepted diagram amplitudes; no simplification performed.",
        },
        "audit_metadata": {
            "convention_audit_path": "docs/QED_CONVENTION_AUDIT.md",
            "approved_for_amplitude_generation": True,
            "heavy_calculation_approved": False,
            "notes": "Derived after topology and amplitude-generation gates; heavy calculation not required.",
        },
        "amplitudes": amplitudes,
        "metadata": {"notes": "Derived AmplitudeIR; not a canonical user-input physics source."},
    }
    validate_amplitude_ir_semantics(result)
    return result


def validate_amplitude_ir_semantics(amplitude_ir: dict[str, Any]) -> None:
    """Validate semantic invariants not conveniently expressed in JSON Schema."""

    amplitude_ids = [amplitude["amplitude_id"] for amplitude in amplitude_ir.get("amplitudes", [])]
    if amplitude_ir.get("total_amplitude", {}).get("term_amplitude_ids") != amplitude_ids:
        raise AmplitudeBuildError("total_amplitude must be the ordered symbolic sum of diagram amplitudes")

    for amplitude in amplitude_ir.get("amplitudes", []):
        index_ids = [
            index["index_id"]
            for group in ("lorentz", "dirac")
            for index in amplitude["local_indices"][group]
        ]
        if len(index_ids) != len(set(index_ids)):
            raise AmplitudeBuildError(f"duplicate local index_id in {amplitude['amplitude_id']}")
        known_indices = set(index_ids)
        known_factors = _factor_ids(amplitude)
        for factor in amplitude["external_state_factors"]:
            _require_known_indices(factor["index_ids"], known_indices, factor["factor_id"])
        for factor in amplitude["vertex_factors"]:
            _require_known_indices(factor["lorentz_index_ids"], known_indices, factor["factor_id"])
            _require_known_indices(factor["dirac_index_ids"], known_indices, factor["factor_id"])
            for slot in factor["slot_factors"]:
                _require_known_indices(slot["index_ids"], known_indices, factor["factor_id"])
        for factor in amplitude["propagator_factors"]:
            _require_known_indices(factor["index_ids"], known_indices, factor["factor_id"])
        for factor in amplitude["bosonic_external_polarization_factors"]:
            _require_known_indices([factor["lorentz_index_id"]], known_indices, factor["factor_id"])
        for chain in amplitude["fermion_chains"]:
            _require_known_factors(chain["ordered_factor_ids"], known_factors, chain["chain_id"])
            _require_known_factors([chain["external_start_factor_id"], chain["external_end_factor_id"]], known_factors, chain["chain_id"])
            _require_known_factors(chain.get("attached_bosonic_factor_ids", []), known_factors, chain["chain_id"])
        for factor in amplitude["non_chain_factors"]:
            _require_known_factors(factor["source_factor_ids"], known_factors, factor["factor_id"])
            for connection in factor.get("connects", []):
                _require_known_indices([connection["index_id"]], known_indices, factor["factor_id"])
        for contraction in amplitude["index_contractions"]:
            for ref in contraction["factor_indices"]:
                _require_known_factors([ref["factor_id"]], known_factors, contraction["contraction_id"])
                _require_known_indices([ref["index_id"]], known_indices, contraction["contraction_id"])


def _validate_inputs(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    rule_registry: dict[str, Any],
    diagram_ir: dict[str, Any],
) -> None:
    approval = physics_card.get("approval", {})
    if approval.get("topology", {}).get("status") != "approved":
        raise AmplitudeBuildError("topology approval must be approved before amplitude generation")
    if approval.get("amplitude_generation", {}).get("status") != "approved":
        raise AmplitudeBuildError("amplitude_generation approval must be approved before amplitude generation")
    if convention_card.get("all_momenta_incoming_vertex_convention") is not True:
        raise AmplitudeBuildError("AmplitudeIR builder requires all-momenta-incoming vertex convention")
    if physics_card.get("process_id") != diagram_ir.get("process_id"):
        raise AmplitudeBuildError("PhysicsCard process_id does not match DiagramIR process_id")
    rules_by_id = _rules_by_id(rule_registry)
    for diagram in diagram_ir.get("diagrams", []):
        if diagram.get("loop_order") != 0:
            raise AmplitudeBuildError("AmplitudeIR builder is tree-level only")
        _validate_diagram_bindings(diagram, rules_by_id)
        _validate_internal_momenta(diagram)
        referenced = {ref["rule_id"] for ref in diagram.get("rule_references", [])}
        referenced |= {vertex["rule_id"] for vertex in diagram.get("vertex_instances", [])}
        referenced |= {line["propagator_rule_id"] for line in diagram.get("internal_lines", [])}
        for rule_id in referenced:
            rule = rules_by_id.get(rule_id)
            if rule is None:
                raise AmplitudeBuildError(f"referenced rule is missing from registry: {rule_id}")
            if rule.get("trust_status") not in AUDITED_RULE_STATUSES:
                raise AmplitudeBuildError(f"referenced rule is below project-audited QED status: {rule_id}")


def _validate_diagram_bindings(diagram: dict[str, Any], rules_by_id: dict[str, dict[str, Any]]) -> None:
    vertex_ids = {vertex["vertex_id"] for vertex in diagram.get("vertex_instances", [])}
    line_ids = {line["line_id"] for line in diagram.get("internal_lines", [])}
    leg_ids = {leg["leg_id"] for leg in diagram.get("external_legs", [])}
    endpoint_ids = vertex_ids | line_ids | leg_ids
    for vertex in diagram.get("vertex_instances", []):
        rule = rules_by_id.get(vertex.get("rule_id"))
        if rule is None:
            raise AmplitudeBuildError(f"missing vertex rule: {vertex.get('rule_id')}")
        expected_slots = {field["slot"] for field in rule["participating_fields"]}
        bindings = vertex.get("slot_bindings")
        if not bindings:
            raise AmplitudeBuildError(f"vertex has incomplete slot_bindings: {vertex['vertex_id']}")
        if {binding.get("rule_slot") for binding in bindings} != expected_slots:
            raise AmplitudeBuildError(f"vertex slot bindings do not match rule fields: {vertex['vertex_id']}")
        for binding in bindings:
            if binding.get("endpoint_id") not in endpoint_ids:
                raise AmplitudeBuildError(f"slot binding references unknown endpoint: {binding.get('endpoint_id')}")
            if "fermion_flow" not in binding:
                raise AmplitudeBuildError(f"slot binding missing fermion_flow: {vertex['vertex_id']}")
            flow = binding["fermion_flow"]
            if not flow.get("field_orientation") or not flow.get("flow_direction"):
                raise AmplitudeBuildError(f"slot binding has incomplete fermion_flow: {vertex['vertex_id']}")
            if "momentum_substitution" not in binding or "convention_conversion" not in binding:
                raise AmplitudeBuildError(f"slot binding missing convention conversion: {vertex['vertex_id']}")
    for line in diagram.get("internal_lines", []):
        if line["from"].get("id") not in vertex_ids or line["to"].get("id") not in vertex_ids:
            raise AmplitudeBuildError(f"internal line endpoints must be vertices: {line['line_id']}")
        if not line.get("momentum", {}).get("label") or not line.get("momentum", {}).get("expression"):
            raise AmplitudeBuildError(f"internal line missing momentum routing: {line['line_id']}")


def _validate_internal_momenta(diagram: dict[str, Any]) -> None:
    if not diagram.get("internal_lines"):
        return
    channel = diagram.get("channel")
    if channel not in CHANNEL_PARTITIONS:
        return
    external_by_slot = {leg["slot"]: leg for leg in diagram["external_legs"]}
    expected = _internal_momentum_expression(CHANNEL_PARTITIONS[channel][0], external_by_slot)
    routing_by_target = {item["target_id"]: item["definition"] for item in diagram.get("momentum_routing", [])}
    for line in diagram["internal_lines"]:
        actual = line["momentum"]["expression"]
        if actual != expected:
            raise AmplitudeBuildError(
                f"internal momentum for {line['line_id']} is {actual}, expected {expected} from channel {channel}"
            )
        if routing_by_target.get(line["line_id"]) != expected:
            raise AmplitudeBuildError(f"momentum_routing definition disagrees with internal line {line['line_id']}")


def _build_diagram_amplitude(process_tail: str, diagram: dict[str, Any], rule_registry: dict[str, Any]) -> dict[str, Any]:
    rules_by_id = _rules_by_id(rule_registry)
    particle_catalog = {particle["particle_id"]: particle for particle in rule_registry["particle_catalog"]}
    channel = diagram["channel"]
    prefix = f"{process_tail}:{channel}"
    external_by_id = {leg["leg_id"]: leg for leg in diagram["external_legs"]}
    lines_by_id = {line["line_id"]: line for line in diagram["internal_lines"]}
    vertex_by_id = {vertex["vertex_id"]: vertex for vertex in diagram["vertex_instances"]}
    vertex_order = {vertex["vertex_id"]: index for index, vertex in enumerate(diagram["vertex_instances"], start=1)}
    line_order = {line["line_id"]: index for index, line in enumerate(diagram["internal_lines"], start=1)}

    local_indices = {"lorentz": [], "dirac": []}
    index_ids: set[str] = set()
    external_state_factors = []
    polarizations = []
    external_factor_by_leg: dict[str, dict[str, Any]] = {}
    polarization_by_leg: dict[str, dict[str, Any]] = {}
    for leg in diagram["external_legs"]:
        particle = particle_catalog[leg["particle_id"]]
        if particle["field_role"] == "dirac_fermion":
            factor = _external_spinor_factor(prefix, leg, particle, local_indices, index_ids)
            external_state_factors.append(factor)
            external_factor_by_leg[leg["leg_id"]] = factor
        elif particle["field_role"] == "vector":
            factor = _polarization_factor(prefix, leg, local_indices, index_ids)
            polarizations.append(factor)
            polarization_by_leg[leg["leg_id"]] = factor

    vertex_factors = []
    vertex_slot_indices: dict[tuple[str, int], str] = {}
    for vertex in diagram["vertex_instances"]:
        factor, slot_indices = _vertex_factor(prefix, vertex, rules_by_id[vertex["rule_id"]], vertex_order[vertex["vertex_id"]], local_indices, index_ids)
        vertex_factors.append(factor)
        vertex_slot_indices.update(slot_indices)

    propagator_factors = []
    propagator_endpoint_indices: dict[tuple[str, str], str] = {}
    for line in diagram["internal_lines"]:
        factor, endpoint_indices = _propagator_factor(prefix, line, rules_by_id[line["propagator_rule_id"]], line_order[line["line_id"]], local_indices, index_ids)
        propagator_factors.append(factor)
        propagator_endpoint_indices.update(endpoint_indices)

    momentum_substitutions = _momentum_substitutions(prefix, diagram, rules_by_id, vertex_order)
    fermion_chains, dirac_contractions = _fermion_chains(
        prefix,
        diagram,
        rules_by_id,
        external_by_id,
        lines_by_id,
        vertex_by_id,
        vertex_order,
        line_order,
        vertex_slot_indices,
        propagator_endpoint_indices,
        external_factor_by_leg,
    )
    lorentz_contractions = _lorentz_contractions(
        prefix,
        diagram,
        rules_by_id,
        vertex_order,
        line_order,
        vertex_slot_indices,
        propagator_endpoint_indices,
        polarization_by_leg,
    )
    non_chain_factors = _non_chain_factors(prefix, diagram, rules_by_id, line_order, vertex_slot_indices, fermion_chains)
    amp = {
        "amplitude_id": f"amplitude:{process_tail}:amp_{channel}",
        "diagram_id": diagram["diagram_id"],
        "process_id": diagram["process_id"],
        "source_rule_ids": sorted({ref["rule_id"] for ref in diagram["rule_references"]}),
        "external_state_factors": external_state_factors,
        "vertex_factors": vertex_factors,
        "propagator_factors": propagator_factors,
        "local_indices": local_indices,
        "momentum_substitutions": momentum_substitutions,
        "fermion_chains": fermion_chains,
        "bosonic_external_polarization_factors": polarizations,
        "non_chain_factors": non_chain_factors,
        "index_contractions": dirac_contractions + lorentz_contractions,
        "overall_factor": {
            "scalar_prefactor": diagram.get("symmetry_factor", "1"),
            "relative_sign": "+1",
            "sign_source": "diagram_ir_symmetry_and_fermion_ordering",
            "notes": "No gamma-chain simplification, spin sums, polarization sums, or squaring performed.",
        },
        "generation_status": {
            "status": "derived_candidate",
            "generated_by": "feynagent.amplitudes.builder",
            "notes": "Deterministically derived from approved structured inputs.",
        },
        "audit_metadata": {
            "convention_audit_path": "docs/QED_CONVENTION_AUDIT.md",
            "approved_for_amplitude_generation": True,
            "heavy_calculation_approved": False,
            "notes": "Rule factors reference audited canonical rule IDs; heavy calculation approval not required.",
        },
        "metadata": {"notes": "Per-diagram derived amplitude structure; not a final rendered amplitude."},
    }
    validate_amplitude_ir_semantics({"amplitudes": [amp], "total_amplitude": {"term_amplitude_ids": [amp["amplitude_id"]]}})
    return amp


def _external_spinor_factor(prefix: str, leg: dict[str, Any], particle: dict[str, Any], local_indices: dict[str, list[dict[str, str]]], index_ids: set[str]) -> dict[str, Any]:
    spinor_type = _spinor_type(leg["state_role"], particle)
    factor_id = f"factor:{prefix}:ext:{leg['slot']}:{spinor_type}"
    index_id = _add_index(local_indices, index_ids, "dirac", f"d_ext_{leg['slot']}", factor_id)
    return {"factor_id": factor_id, "leg_id": leg["leg_id"], "particle_id": leg["particle_id"], "state_role": leg["state_role"], "momentum_label": leg["momentum_label"], "factor_kind": "spinor_wavefunction", "spinor_type": spinor_type, "index_ids": [index_id]}


def _polarization_factor(prefix: str, leg: dict[str, Any], local_indices: dict[str, list[dict[str, str]]], index_ids: set[str]) -> dict[str, Any]:
    suffix = "eps_conj" if leg["state_role"] == "outgoing" else "eps"
    factor_id = f"factor:{prefix}:pol:{leg['slot']}:{suffix}"
    index_id = _add_index(local_indices, index_ids, "lorentz", f"l_pol_{leg['slot']}", factor_id)
    return {"factor_id": factor_id, "leg_id": leg["leg_id"], "particle_id": leg["particle_id"], "state_role": leg["state_role"], "momentum_label": leg["momentum_label"], "lorentz_index_id": index_id, "conjugation": "complex_conjugate" if leg["state_role"] == "outgoing" else "none", "transversality_status": "not_applied"}


def _vertex_factor(prefix: str, vertex: dict[str, Any], rule: dict[str, Any], order: int, local_indices: dict[str, list[dict[str, str]]], index_ids: set[str]) -> tuple[dict[str, Any], dict[tuple[str, int], str]]:
    factor_id = f"factor:{prefix}:vertex:{order}"
    fields_by_slot = {field["slot"]: field for field in rule["participating_fields"]}
    slot_indices: dict[tuple[str, int], str] = {}
    slot_factors = []
    lorentz_index_ids = []
    dirac_index_ids = []
    for binding in sorted(vertex["slot_bindings"], key=lambda item: item["rule_slot"]):
        field = fields_by_slot[binding["rule_slot"]]
        if field["field_role"] == "dirac_fermion":
            label = f"d_v{order}_{'bar' if field['quantum_field_role'] == 'psi_bar' else 'psi'}"
            index_id = _add_index(local_indices, index_ids, "dirac", label, factor_id)
            dirac_index_ids.append(index_id)
        else:
            label = f"l_v{order}_{field.get('index_label', 'slot' + str(binding['rule_slot']))}"
            index_id = _add_index(local_indices, index_ids, "lorentz", label, factor_id)
            lorentz_index_ids.append(index_id)
        slot_indices[(vertex["vertex_id"], binding["rule_slot"])] = index_id
        slot_factors.append({"rule_slot": binding["rule_slot"], "endpoint_id": binding["endpoint_id"], "field_id": binding["expected_field_id"], "momentum_substitution": binding["momentum_substitution"], "index_ids": [index_id]})
    return ({"factor_id": factor_id, "vertex_id": vertex["vertex_id"], "rule_id": vertex["rule_id"], "coefficient": _vertex_coefficient(rule), "lorentz_index_ids": lorentz_index_ids, "dirac_index_ids": dirac_index_ids, "slot_factors": slot_factors}, slot_indices)


def _propagator_factor(prefix: str, line: dict[str, Any], rule: dict[str, Any], order: int, local_indices: dict[str, list[dict[str, str]]], index_ids: set[str]) -> tuple[dict[str, Any], dict[tuple[str, str], str]]:
    factor_id = f"factor:{prefix}:prop:{order}"
    q = line["momentum"]["label"]
    fields = sorted(rule["participating_fields"], key=lambda field: field["slot"])
    if fields and fields[0]["field_role"] == "dirac_fermion":
        left = _add_index(local_indices, index_ids, "dirac", f"d_p{order}_l", factor_id)
        right = _add_index(local_indices, index_ids, "dirac", f"d_p{order}_r", factor_id)
        numerator = f"I (GS[{q}] + m)"
        denominator = f"SP[{q}, {q}] - m^2 + I epsilon"
    else:
        left = _add_index(local_indices, index_ids, "lorentz", f"l_p{order}_l", factor_id)
        right = _add_index(local_indices, index_ids, "lorentz", f"l_p{order}_r", factor_id)
        numerator = f"-I MT[{_index_label(local_indices, left)}, {_index_label(local_indices, right)}]"
        denominator = f"SP[{q}, {q}] + I epsilon"
    return ({"factor_id": factor_id, "line_id": line["line_id"], "rule_id": line["propagator_rule_id"], "particle_id": line["particle_id"], "momentum_label": q, "momentum_expression": line["momentum"]["expression"], "numerator": numerator, "denominator": denominator, "index_ids": [left, right]}, {(line["line_id"], "from"): left, (line["line_id"], "to"): right})


def _momentum_substitutions(prefix: str, diagram: dict[str, Any], rules_by_id: dict[str, dict[str, Any]], vertex_order: dict[str, int]) -> list[dict[str, Any]]:
    substitutions = []
    for vertex in diagram["vertex_instances"]:
        symbols = rules_by_id[vertex["rule_id"]]["momentum_labels_order"]
        v_order = vertex_order[vertex["vertex_id"]]
        factor_id = f"factor:{prefix}:vertex:{v_order}"
        for binding in sorted(vertex["slot_bindings"], key=lambda item: item["rule_slot"]):
            substitutions.append({"substitution_id": f"subst:{prefix}:v{v_order}:slot{binding['rule_slot']}", "source_factor_id": factor_id, "rule_slot": binding["rule_slot"], "symbol": symbols[binding["rule_slot"] - 1], "expression": binding["momentum_substitution"], "convention_conversion": dict(binding["convention_conversion"])})
    return substitutions


def _fermion_chains(prefix: str, diagram: dict[str, Any], rules_by_id: dict[str, dict[str, Any]], external_by_id: dict[str, dict[str, Any]], lines_by_id: dict[str, dict[str, Any]], vertex_by_id: dict[str, dict[str, Any]], vertex_order: dict[str, int], line_order: dict[str, int], vertex_slot_indices: dict[tuple[str, int], str], propagator_endpoint_indices: dict[tuple[str, str], str], external_factor_by_leg: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bindings_by_vertex = {vertex["vertex_id"]: vertex["slot_bindings"] for vertex in diagram["vertex_instances"]}
    vertex_for_external: dict[str, tuple[str, dict[str, Any]]] = {}
    for vertex in diagram["vertex_instances"]:
        for binding in vertex["slot_bindings"]:
            if binding["endpoint_kind"] == "external_leg" and _is_dirac_binding(binding):
                vertex_for_external[binding["endpoint_id"]] = (vertex["vertex_id"], binding)
    starts = sorted(((leg_id, vertex_id, binding) for leg_id, (vertex_id, binding) in vertex_for_external.items() if binding["fermion_flow"]["field_orientation"] == "psi_bar"), key=lambda item: external_by_id[item[0]]["slot"])
    chains = []
    contractions = []
    visited_starts: set[str] = set()
    for leg_id, vertex_id, entry_binding in starts:
        if leg_id in visited_starts:
            continue
        chain_index = len(chains) + 1
        chain_id = f"chain:{prefix}:fermion:{chain_index}"
        ordered = [external_factor_by_leg[leg_id]["factor_id"]]
        attached_bosonic: list[str] = []
        prev_factor = external_factor_by_leg[leg_id]["factor_id"]
        prev_index = external_factor_by_leg[leg_id]["index_ids"][0]
        current_vertex_id = vertex_id
        current_entry = entry_binding
        guard = 0
        while True:
            guard += 1
            if guard > len(diagram["vertex_instances"]) + len(diagram["internal_lines"]) + 4:
                raise AmplitudeBuildError(f"fermion chain traversal did not terminate in {diagram['diagram_id']}")
            v_order = vertex_order[current_vertex_id]
            vertex_factor_id = f"factor:{prefix}:vertex:{v_order}"
            ordered.append(vertex_factor_id)
            entry_index = vertex_slot_indices[(current_vertex_id, current_entry["rule_slot"])]
            contractions.append(_contraction(prefix, "dirac", len(contractions) + 1, prev_factor, prev_index, "right", vertex_factor_id, entry_index, "left"))
            exit_binding = _binding_with_orientation(bindings_by_vertex[current_vertex_id], "psi")
            exit_index = vertex_slot_indices[(current_vertex_id, exit_binding["rule_slot"])]
            for binding in bindings_by_vertex[current_vertex_id]:
                if binding["endpoint_kind"] == "external_leg" and binding["endpoint_id"] not in external_factor_by_leg:
                    attached_bosonic.append(_polarization_factor_id(prefix, external_by_id[binding["endpoint_id"]]))
                if binding["endpoint_kind"] == "internal_line" and not _is_dirac_binding(binding):
                    attached_bosonic.append(f"factor:{prefix}:prop:{line_order[binding['endpoint_id']]}")
            if exit_binding["endpoint_kind"] == "external_leg":
                end_factor = external_factor_by_leg[exit_binding["endpoint_id"]]
                contractions.append(_contraction(prefix, "dirac", len(contractions) + 1, vertex_factor_id, exit_index, "right", end_factor["factor_id"], end_factor["index_ids"][0], "left"))
                ordered.append(end_factor["factor_id"])
                visited_starts.add(leg_id)
                chains.append({"chain_id": chain_id, "ordered_factor_ids": ordered, "external_start_factor_id": external_factor_by_leg[leg_id]["factor_id"], "external_end_factor_id": end_factor["factor_id"], "attached_bosonic_factor_ids": _unique(attached_bosonic)})
                break
            if exit_binding["endpoint_kind"] != "internal_line":
                raise AmplitudeBuildError(f"unsupported fermion-chain endpoint {exit_binding['endpoint_kind']}")
            line = lines_by_id[exit_binding["endpoint_id"]]
            if not _line_is_dirac(line, rules_by_id):
                raise AmplitudeBuildError(f"fermion chain exits through non-fermion line: {line['line_id']}")
            line_factor_id = f"factor:{prefix}:prop:{line_order[line['line_id']]}"
            ordered.append(line_factor_id)
            side, other_side = _line_sides_for_vertex(line, current_vertex_id)
            contractions.append(_contraction(prefix, "dirac", len(contractions) + 1, vertex_factor_id, exit_index, "right", line_factor_id, propagator_endpoint_indices[(line["line_id"], side)], "left"))
            other_vertex_id = line[other_side]["id"]
            other_binding = _internal_binding(vertex_by_id[other_vertex_id], line["line_id"])
            if other_binding["fermion_flow"]["field_orientation"] != "psi_bar":
                raise AmplitudeBuildError(f"wrong fermion flow across internal line: {line['line_id']}")
            prev_factor = line_factor_id
            prev_index = propagator_endpoint_indices[(line["line_id"], other_side)]
            current_vertex_id = other_vertex_id
            current_entry = other_binding
    return chains, contractions


def _lorentz_contractions(prefix: str, diagram: dict[str, Any], rules_by_id: dict[str, dict[str, Any]], vertex_order: dict[str, int], line_order: dict[str, int], vertex_slot_indices: dict[tuple[str, int], str], propagator_endpoint_indices: dict[tuple[str, str], str], polarization_by_leg: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    contractions = []
    for vertex in diagram["vertex_instances"]:
        v_factor = f"factor:{prefix}:vertex:{vertex_order[vertex['vertex_id']]}"
        for binding in vertex["slot_bindings"]:
            if _is_dirac_binding(binding):
                continue
            v_index = vertex_slot_indices[(vertex["vertex_id"], binding["rule_slot"])]
            if binding["endpoint_kind"] == "external_leg":
                pol = polarization_by_leg[binding["endpoint_id"]]
                contractions.append(_contraction(prefix, "lorentz", len(contractions) + 1, v_factor, v_index, "lorentz", pol["factor_id"], pol["lorentz_index_id"], "lorentz"))
            elif binding["endpoint_kind"] == "internal_line":
                line_id = binding["endpoint_id"]
                line = next(line for line in diagram["internal_lines"] if line["line_id"] == line_id)
                if _line_is_dirac(line, rules_by_id):
                    continue
                side, _ = _line_sides_for_vertex(line, vertex["vertex_id"])
                prop_factor = f"factor:{prefix}:prop:{line_order[line_id]}"
                contractions.append(_contraction(prefix, "lorentz", len(contractions) + 1, v_factor, v_index, "lorentz", prop_factor, propagator_endpoint_indices[(line_id, side)], "lorentz"))
    return contractions


def _non_chain_factors(prefix: str, diagram: dict[str, Any], rules_by_id: dict[str, dict[str, Any]], line_order: dict[str, int], vertex_slot_indices: dict[tuple[str, int], str], fermion_chains: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chain_by_vertex_order = {}
    for chain in fermion_chains:
        for factor_id in chain["ordered_factor_ids"]:
            match = re.match(rf"factor:{re.escape(prefix)}:vertex:(\d+)$", factor_id)
            if match:
                chain_by_vertex_order[int(match.group(1))] = chain["chain_id"]
    factors = []
    for line in diagram["internal_lines"]:
        if _line_is_dirac(line, rules_by_id):
            continue
        from_order = _vertex_order_from_id(diagram, line["from"]["id"])
        to_order = _vertex_order_from_id(diagram, line["to"]["id"])
        connects = []
        if from_order in chain_by_vertex_order:
            connects.append({"chain_id": chain_by_vertex_order[from_order], "index_id": vertex_slot_indices[(line["from"]["id"], line["from"]["slot"])]})
        if to_order in chain_by_vertex_order:
            connects.append({"chain_id": chain_by_vertex_order[to_order], "index_id": vertex_slot_indices[(line["to"]["id"], line["to"]["slot"])]})
        factors.append({"factor_id": f"factor:{prefix}:nonchain:{line_order[line['line_id']]}", "factor_kind": "boson_propagator_between_currents", "source_factor_ids": [f"factor:{prefix}:prop:{line_order[line['line_id']]}"], "connects": connects})
    return factors


def _spinor_type(state_role: str, particle: dict[str, Any]) -> str:
    fermion_number = particle.get("fermion_number")
    if fermion_number == 1:
        return "u" if state_role == "incoming" else "ubar"
    if fermion_number == -1:
        return "vbar" if state_role == "incoming" else "v"
    raise AmplitudeBuildError(f"Dirac external particle needs fermion_number +/-1: {particle['particle_id']}")


def _vertex_coefficient(rule: dict[str, Any]) -> str:
    template = rule.get("feyncalc", {}).get("template", "")
    if "GA[" in template:
        return template.split("GA[", 1)[0].strip().rstrip("*").strip()
    return template


def _line_is_dirac(line: dict[str, Any], rules_by_id: dict[str, dict[str, Any]]) -> bool:
    rule = rules_by_id[line["propagator_rule_id"]]
    return any(field["field_role"] == "dirac_fermion" for field in rule["participating_fields"])


def _is_dirac_binding(binding: dict[str, Any]) -> bool:
    return binding["fermion_flow"]["field_orientation"] in {"psi", "psi_bar"}


def _binding_with_orientation(bindings: list[dict[str, Any]], orientation: str) -> dict[str, Any]:
    matches = [binding for binding in bindings if binding["fermion_flow"]["field_orientation"] == orientation]
    if len(matches) != 1:
        raise AmplitudeBuildError(f"expected exactly one {orientation} binding at a QED fermion vertex")
    return matches[0]


def _internal_binding(vertex: dict[str, Any], line_id: str) -> dict[str, Any]:
    matches = [binding for binding in vertex["slot_bindings"] if binding["endpoint_kind"] == "internal_line" and binding["endpoint_id"] == line_id]
    if len(matches) != 1:
        raise AmplitudeBuildError(f"expected one binding to internal line {line_id} at {vertex['vertex_id']}")
    return matches[0]


def _line_sides_for_vertex(line: dict[str, Any], vertex_id: str) -> tuple[str, str]:
    if line["from"]["id"] == vertex_id:
        return "from", "to"
    if line["to"]["id"] == vertex_id:
        return "to", "from"
    raise AmplitudeBuildError(f"vertex {vertex_id} is not an endpoint of {line['line_id']}")


def _vertex_order_from_id(diagram: dict[str, Any], vertex_id: str) -> int:
    for index, vertex in enumerate(diagram["vertex_instances"], start=1):
        if vertex["vertex_id"] == vertex_id:
            return index
    raise AmplitudeBuildError(f"unknown vertex id: {vertex_id}")


def _polarization_factor_id(prefix: str, leg: dict[str, Any]) -> str:
    suffix = "eps_conj" if leg["state_role"] == "outgoing" else "eps"
    return f"factor:{prefix}:pol:{leg['slot']}:{suffix}"


def _contraction(prefix: str, index_type: str, order: int, factor_a: str, index_a: str, role_a: str, factor_b: str, index_b: str, role_b: str) -> dict[str, Any]:
    return {"contraction_id": f"contract:{prefix}:{index_type}:{order}", "index_type": index_type, "factor_indices": [{"factor_id": factor_a, "index_id": index_a, "index_role": role_a}, {"factor_id": factor_b, "index_id": index_b, "index_role": role_b}]}


def _add_index(local_indices: dict[str, list[dict[str, str]]], index_ids: set[str], index_type: str, label: str, owner_id: str) -> str:
    sanitized_label = _sanitize_label(label)
    owner_parts = owner_id.split(":")
    owner_scope = ":".join(owner_parts[1:3])
    owner_tail = _sanitize_label(owner_parts[-1])
    index_id = f"idx:{owner_scope}:{owner_tail}:{sanitized_label}"
    counter = 2
    base = index_id
    while index_id in index_ids:
        index_id = f"{base}_{counter}"
        counter += 1
    index_ids.add(index_id)
    local_indices[index_type].append({"index_id": index_id, "label": sanitized_label, "index_type": index_type, "owner_id": owner_id})
    return index_id


def _index_label(local_indices: dict[str, list[dict[str, str]]], index_id: str) -> str:
    for group in ("lorentz", "dirac"):
        for index in local_indices[group]:
            if index["index_id"] == index_id:
                return index["label"]
    raise AmplitudeBuildError(f"unknown index id: {index_id}")


def _require_known_indices(ids: list[str], known: set[str], owner: str) -> None:
    missing = set(ids) - known
    if missing:
        raise AmplitudeBuildError(f"{owner} references unknown indices: {sorted(missing)}")


def _require_known_factors(ids: list[str], known: set[str], owner: str) -> None:
    missing = set(ids) - known
    if missing:
        raise AmplitudeBuildError(f"{owner} references unknown factors: {sorted(missing)}")


def _factor_ids(amplitude: dict[str, Any]) -> set[str]:
    ids = set()
    for key in ["external_state_factors", "vertex_factors", "propagator_factors", "bosonic_external_polarization_factors", "non_chain_factors"]:
        ids.update(factor["factor_id"] for factor in amplitude.get(key, []))
    return ids


def _rules_by_id(rule_registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {rule["rule_id"]: rule for rule in rule_registry.get("vertices", []) + rule_registry.get("propagators", [])}


def _internal_momentum_expression(slots: tuple[int, int], external_by_slot: dict[int, dict[str, Any]]) -> str:
    terms = []
    for slot in slots:
        endpoint = external_by_slot[slot]
        sign = "+" if endpoint["state_role"] == "incoming" else "-"
        terms.append((sign, endpoint["momentum_label"]))
    first_sign, first_label = terms[0]
    expression = first_label if first_sign == "+" else f"-{first_label}"
    for sign, label in terms[1:]:
        expression += f"{sign}{label}"
    return expression


def _stable_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _id_tail(object_id: str) -> str:
    return object_id.split(":")[-1].replace("-", "_")


def _sanitize_label(value: str) -> str:
    value = value.lower().replace("-", "m").replace("+", "p")
    value = re.sub(r"[^a-z0-9_]+", "_", value).strip("_") or "x"
    if not value[0].isalpha():
        value = f"x_{value}"
    return value


def _unique(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
