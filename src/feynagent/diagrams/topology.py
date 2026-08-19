"""Deterministic v0.1.2 tree-level 2->2 topology enumeration."""

from __future__ import annotations

from itertools import permutations
from typing import Any


class DiagramGenerationError(ValueError):
    """Raised when structured inputs are outside the supported generator scope."""


CHANNEL_PARTITIONS = {
    "s": ((1, 2), (3, 4)),
    "t": ((1, 3), (2, 4)),
    "u": ((1, 4), (2, 3)),
}


def generate_tree_2_to_2(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    rule_registry: dict[str, Any],
    backend_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate exchange/contact DiagramIR for supported tree-level 2->2 inputs."""

    _validate_supported_inputs(physics_card, convention_card, rule_registry, backend_profile)

    external_by_slot = _external_particles_by_slot(physics_card)
    selected_rule_sets = set(_selected_rule_set_ids(physics_card, backend_profile))
    vertices = [
        rule
        for rule in rule_registry.get("vertices", [])
        if rule.get("rule_set_id") in selected_rule_sets
    ]
    three_vertices = [rule for rule in vertices if len(rule["participating_fields"]) == 3]
    contact_vertices = [rule for rule in vertices if len(rule["participating_fields"]) == 4]
    propagators = [
        rule
        for rule in rule_registry.get("propagators", [])
        if rule.get("rule_set_id") in selected_rule_sets
    ]
    particle_catalog = {
        particle["particle_id"]: particle
        for particle in rule_registry.get("particle_catalog", [])
    }

    diagrams: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()

    for channel in ("s", "t", "u"):
        left_slots, right_slots = CHANNEL_PARTITIONS[channel]
        momentum_expression = _internal_momentum_expression(left_slots, external_by_slot)
        momentum_label = f"q_{channel}"
        internal_species = _allowed_internal_species(physics_card, propagators)

        for species in internal_species:
            propagator = _find_propagator_for_species(species, propagators, particle_catalog)
            if propagator is None:
                continue

            left_matches = _match_three_point_side(
                three_vertices,
                [external_by_slot[slot] for slot in left_slots],
                species,
                particle_catalog,
            )
            right_matches = _match_three_point_side(
                three_vertices,
                [external_by_slot[slot] for slot in right_slots],
                species,
                particle_catalog,
            )

            for left_match in left_matches:
                for right_match in right_matches:
                    if not _internal_fields_can_join(
                        left_match["internal_field"],
                        right_match["internal_field"],
                        species,
                        propagator,
                        particle_catalog,
                    ):
                        continue

                    diagram = _build_exchange_diagram(
                        physics_card,
                        channel,
                        external_by_slot,
                        species,
                        propagator,
                        left_match,
                        right_match,
                        momentum_label,
                        momentum_expression,
                    )
                    signature = diagram_signature(diagram)
                    if signature not in seen:
                        seen.add(signature)
                        diagrams.append(diagram)

    for match in _match_contact_vertices(contact_vertices, external_by_slot, particle_catalog):
        diagram = _build_contact_diagram(physics_card, external_by_slot, match)
        signature = diagram_signature(diagram)
        if signature not in seen:
            seen.add(signature)
            diagrams.append(diagram)

    return {
        "schema_version": "0.1.2",
        "object_id": f"diagram_ir:generated:{_id_tail(physics_card['process_id'])}",
        "status": "candidate",
        "process_id": physics_card["process_id"],
        "diagrams": diagrams,
        "metadata": {
            "notes": "Generated deterministic tree-level 2->2 DiagramIR; no amplitudes were calculated."
        },
    }


def diagram_signature(diagram: dict[str, Any]) -> tuple[Any, ...]:
    """Return a canonical structural signature used for deterministic deduplication."""

    internal = tuple(
        sorted(
            (
                line["particle_id"],
                line["momentum"]["expression"],
                line["propagator_rule_id"],
            )
            for line in diagram.get("internal_lines", [])
        )
    )
    vertices = []
    for vertex in diagram.get("vertex_instances", []):
        bindings = tuple(
            sorted(_binding_signature(binding) for binding in vertex["slot_bindings"])
        )
        vertices.append((vertex["rule_id"], bindings))
    return (
        diagram["channel"],
        tuple(
            sorted(
                (item["coupling"], item["power"])
                for item in diagram["coupling_order"]
            )
        ),
        internal,
        tuple(sorted(vertices)),
    )



def _binding_signature(binding: dict[str, Any]) -> tuple[Any, ...]:
    flow = binding["fermion_flow"]
    if flow["field_orientation"] in {"psi", "psi_bar"}:
        return (
            "fermion",
            binding["rule_slot"],
            binding["endpoint_kind"],
            binding["endpoint_particle_id"],
            binding["momentum_label"],
            binding["expected_particle_id"],
            binding["expected_field_id"],
            binding["crossing_treatment"],
            binding["momentum_substitution"],
            flow["field_orientation"],
            flow["flow_direction"],
        )
    return (
        "boson",
        binding["endpoint_kind"],
        binding["endpoint_particle_id"],
        binding["momentum_label"],
        binding["expected_particle_id"],
        binding["crossing_treatment"],
        binding["momentum_substitution"],
        flow["field_orientation"],
        flow["flow_direction"],
    )

def _validate_supported_inputs(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    rule_registry: dict[str, Any],
    backend_profile: dict[str, Any] | None = None,
) -> None:
    if physics_card.get("schema_version") != "0.2.0":
        raise DiagramGenerationError("PhysicsCard schema_version must be 0.2.0")
    if convention_card.get("schema_version") != "0.1.1":
        raise DiagramGenerationError("ConventionCard schema_version must be 0.1.1")
    if rule_registry.get("schema_version") != "0.1.1":
        raise DiagramGenerationError("RuleRegistry schema_version must be 0.1.1")
    if physics_card.get("process_type") != "scattering_2_to_2":
        raise DiagramGenerationError("only scattering_2_to_2 is supported")
    if physics_card.get("perturbative_order", {}).get("loop_order") != 0:
        raise DiagramGenerationError("only loop_order = 0 is supported")
    if convention_card.get("all_momenta_incoming_vertex_convention") is not True:
        raise DiagramGenerationError("all-momenta-incoming vertex convention is required")
    external = physics_card.get("particles", {})
    if len(external.get("incoming", [])) != 2 or len(external.get("outgoing", [])) != 2:
        raise DiagramGenerationError("exactly 2 incoming and 2 outgoing particles are required")
    if physics_card.get("model_id") is None or physics_card.get("sector") is None:
        raise DiagramGenerationError("PhysicsCard must declare backend-neutral model_id and sector")
    if backend_profile is not None:
        if backend_profile.get("backend_kind") != "legacy_custom_backend":
            raise DiagramGenerationError("legacy DiagramIR generation requires a legacy_custom_backend profile")
        resolves = backend_profile.get("resolves", {})
        if resolves.get("model_id") != physics_card.get("model_id") or resolves.get("sector") != physics_card.get("sector"):
            raise DiagramGenerationError("BackendProfile model_id/sector does not match PhysicsCard")
        registry = backend_profile.get("legacy", {}).get("rule_registry", {})
        if registry.get("registry_id") != rule_registry.get("registry_id"):
            raise DiagramGenerationError("BackendProfile registry_id does not match RuleRegistry")


def _selected_rule_set_ids(
    physics_card: dict[str, Any],
    backend_profile: dict[str, Any] | None,
) -> list[str]:
    if backend_profile is not None:
        rule_set_ids = backend_profile.get("legacy", {}).get("rule_registry", {}).get("rule_set_ids", [])
        if not rule_set_ids:
            raise DiagramGenerationError("legacy BackendProfile must provide rule_set_ids")
        return list(rule_set_ids)
    selected = physics_card.get("selected_rule_set", {})
    rule_set_ids = selected.get("rule_set_ids", [])
    if not rule_set_ids:
        raise DiagramGenerationError("legacy generation requires rule_set_ids from BackendProfile")
    return list(rule_set_ids)


def _external_particles_by_slot(physics_card: dict[str, Any]) -> dict[int, dict[str, Any]]:
    particles: dict[int, dict[str, Any]] = {}
    for state_role in ("incoming", "outgoing"):
        for entry in physics_card["particles"][state_role]:
            item = dict(entry)
            item["state_role"] = state_role
            particles[item["slot"]] = item
    if set(particles) != {1, 2, 3, 4}:
        raise DiagramGenerationError("2->2 external slots must be exactly 1, 2, 3, 4")
    return particles


def _allowed_internal_species(
    physics_card: dict[str, Any],
    propagators: list[dict[str, Any]],
) -> list[str]:
    available = sorted(
        {
            field["particle_id"]
            for propagator in propagators
            for field in propagator["participating_fields"]
        }
    )
    policy = physics_card.get("internal_species_policy", {})
    if "allowed_particle_ids" in policy:
        species = [particle for particle in policy["allowed_particle_ids"] if particle in available]
    else:
        species = available
    forbidden = set(policy.get("forbidden_particle_ids", []))
    return [particle for particle in species if particle not in forbidden]


def _find_propagator_for_species(
    species: str,
    propagators: list[dict[str, Any]],
    particle_catalog: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    for propagator in propagators:
        fields = propagator["participating_fields"]
        if all(_field_accepts_internal_species(field, species, particle_catalog) for field in fields):
            return propagator
    return None


def _match_three_point_side(
    vertex_rules: list[dict[str, Any]],
    external_endpoints: list[dict[str, Any]],
    internal_species: str,
    particle_catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for rule in sorted(vertex_rules, key=lambda item: item["rule_id"]):
        fields = sorted(rule["participating_fields"], key=lambda field: field["slot"])
        for internal_field in fields:
            if not _field_accepts_internal_species(internal_field, internal_species, particle_catalog):
                continue
            external_fields = [field for field in fields if field["slot"] != internal_field["slot"]]
            for field_perm in permutations(external_fields):
                bindings = []
                ok = True
                for endpoint, field in zip(external_endpoints, field_perm):
                    if not _field_accepts_external(field, endpoint, particle_catalog):
                        ok = False
                        break
                    bindings.append((field, endpoint))
                if ok:
                    matches.append(
                        {
                            "rule": rule,
                            "external_bindings": tuple(bindings),
                            "internal_field": internal_field,
                        }
                    )
    return matches


def _match_contact_vertices(
    vertex_rules: list[dict[str, Any]],
    external_by_slot: dict[int, dict[str, Any]],
    particle_catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    endpoints = [external_by_slot[slot] for slot in (1, 2, 3, 4)]
    matches: list[dict[str, Any]] = []
    for rule in sorted(vertex_rules, key=lambda item: item["rule_id"]):
        fields = sorted(rule["participating_fields"], key=lambda field: field["slot"])
        for field_perm in permutations(fields):
            bindings = []
            ok = True
            for endpoint, field in zip(endpoints, field_perm):
                if not _field_accepts_external(field, endpoint, particle_catalog):
                    ok = False
                    break
                bindings.append((field, endpoint))
            if ok:
                matches.append({"rule": rule, "external_bindings": tuple(bindings)})
    return matches


def _field_accepts_external(
    field: dict[str, Any],
    endpoint: dict[str, Any],
    particle_catalog: dict[str, dict[str, Any]],
) -> bool:
    particle = endpoint["particle_id"]
    expected = field["particle_id"]
    role = endpoint["state_role"]
    quantum_role = field.get("quantum_field_role")

    if field["field_role"] == "dirac_fermion":
        antiparticle = _antiparticle(expected, particle_catalog)
        if quantum_role == "psi":
            return (role == "incoming" and particle == expected) or (
                role == "outgoing" and particle == antiparticle
            )
        if quantum_role == "psi_bar":
            return (role == "outgoing" and particle == expected) or (
                role == "incoming" and particle == antiparticle
            )
        return False

    return particle == expected or (
        particle == _antiparticle(expected, particle_catalog)
        and particle_catalog.get(expected, {}).get("self_conjugate", False)
    )


def _field_accepts_internal_species(
    field: dict[str, Any],
    species: str,
    particle_catalog: dict[str, dict[str, Any]],
) -> bool:
    expected = field["particle_id"]
    return species == expected or species == _antiparticle(expected, particle_catalog)


def _internal_fields_can_join(
    left_field: dict[str, Any],
    right_field: dict[str, Any],
    species: str,
    propagator: dict[str, Any],
    particle_catalog: dict[str, dict[str, Any]],
) -> bool:
    if not _field_accepts_internal_species(left_field, species, particle_catalog):
        return False
    if not _field_accepts_internal_species(right_field, species, particle_catalog):
        return False

    prop_roles = {
        field.get("quantum_field_role")
        for field in propagator["participating_fields"]
        if field["field_role"] == "dirac_fermion"
    }
    if prop_roles:
        return {
            left_field.get("quantum_field_role"),
            right_field.get("quantum_field_role"),
        } == prop_roles
    return left_field["particle_id"] == right_field["particle_id"]


def _build_exchange_diagram(
    physics_card: dict[str, Any],
    channel: str,
    external_by_slot: dict[int, dict[str, Any]],
    internal_species: str,
    propagator: dict[str, Any],
    left_match: dict[str, Any],
    right_match: dict[str, Any],
    momentum_label: str,
    momentum_expression: str,
) -> dict[str, Any]:
    process_tail = _id_tail(physics_card["process_id"])
    line_id = f"line:generated:{process_tail}:{channel}:{internal_species}"
    left_vertex_id = f"vertex:generated:{process_tail}:{channel}:1"
    right_vertex_id = f"vertex:generated:{process_tail}:{channel}:2"

    external_legs = _external_legs_for_channel(process_tail, channel, external_by_slot)
    leg_ids = {leg["slot"]: leg["leg_id"] for leg in external_legs}

    left_bindings = _build_slot_bindings(
        left_match,
        leg_ids,
        line_id,
        internal_species,
        momentum_label,
        left_internal_sign="-",
    )
    right_bindings = _build_slot_bindings(
        right_match,
        leg_ids,
        line_id,
        internal_species,
        momentum_label,
        left_internal_sign="",
    )
    left_internal_slot = left_match["internal_field"]["slot"]
    right_internal_slot = right_match["internal_field"]["slot"]

    left_vertex_rule_id = left_match["rule"]["rule_id"]
    right_vertex_rule_id = right_match["rule"]["rule_id"]
    vertex_rule_refs = [
        {"rule_id": rule_id, "rule_type": "vertex"}
        for rule_id in sorted({left_vertex_rule_id, right_vertex_rule_id})
    ]
    coupling_order = _sum_coupling_orders([left_match["rule"], right_match["rule"]])

    return {
        "diagram_id": f"diagram:generated:{process_tail}:{channel}:{internal_species}",
        "process_id": physics_card["process_id"],
        "status": "candidate",
        "loop_order": 0,
        "channel": channel,
        "external_legs": external_legs,
        "vertex_instances": [
            {
                "vertex_id": left_vertex_id,
                "rule_id": left_vertex_rule_id,
                "slot_bindings": left_bindings,
            },
            {
                "vertex_id": right_vertex_id,
                "rule_id": right_match["rule"]["rule_id"],
                "slot_bindings": right_bindings,
            },
        ],
        "internal_lines": [
            {
                "line_id": line_id,
                "particle_id": internal_species,
                "propagator_rule_id": propagator["rule_id"],
                "from": {"kind": "vertex", "id": left_vertex_id, "slot": left_internal_slot},
                "to": {"kind": "vertex", "id": right_vertex_id, "slot": right_internal_slot},
                "momentum": {
                    "label": momentum_label,
                    "expression": momentum_expression,
                    "external_convention": "physical_external_momenta",
                },
            }
        ],
        "momentum_routing": [
            {
                "target_id": line_id,
                "momentum_label": momentum_label,
                "definition": momentum_expression,
            }
        ],
        "rule_references": vertex_rule_refs
        + [{"rule_id": propagator["rule_id"], "rule_type": "propagator"}],
        "coupling_order": coupling_order,
        "symmetry_factor": "1",
        "metadata": {
            "notes": "Generated exchange topology only; no amplitude expression is encoded."
        },
    }


def _build_contact_diagram(
    physics_card: dict[str, Any],
    external_by_slot: dict[int, dict[str, Any]],
    match: dict[str, Any],
) -> dict[str, Any]:
    process_tail = _id_tail(physics_card["process_id"])
    channel = "contact"
    external_legs = _external_legs_for_channel(process_tail, channel, external_by_slot)
    leg_ids = {leg["slot"]: leg["leg_id"] for leg in external_legs}
    vertex_id = f"vertex:generated:{process_tail}:contact:1"
    bindings = []
    for field, endpoint in sorted(match["external_bindings"], key=lambda item: item[0]["slot"]):
        bindings.append(_external_binding(field, endpoint, leg_ids[endpoint["slot"]]))
    rule = match["rule"]
    return {
        "diagram_id": f"diagram:generated:{process_tail}:contact:{rule['rule_id'].split(':')[-1]}",
        "process_id": physics_card["process_id"],
        "status": "candidate",
        "loop_order": 0,
        "channel": "contact",
        "external_legs": external_legs,
        "vertex_instances": [{"vertex_id": vertex_id, "rule_id": rule["rule_id"], "slot_bindings": bindings}],
        "internal_lines": [],
        "momentum_routing": [],
        "rule_references": [{"rule_id": rule["rule_id"], "rule_type": "vertex"}],
        "coupling_order": _sum_coupling_orders([rule]),
        "symmetry_factor": "1",
        "metadata": {"notes": "Generated contact topology only; no amplitude expression is encoded."},
    }


def _build_slot_bindings(
    match: dict[str, Any],
    leg_ids: dict[int, str],
    line_id: str,
    internal_species: str,
    momentum_label: str,
    left_internal_sign: str,
) -> list[dict[str, Any]]:
    bindings = []
    for field, endpoint in match["external_bindings"]:
        bindings.append(_external_binding(field, endpoint, leg_ids[endpoint["slot"]]))
    internal_field = match["internal_field"]
    bindings.append(
        {
            "rule_slot": internal_field["slot"],
            "endpoint_id": line_id,
            "endpoint_kind": "internal_line",
            "expected_particle_id": internal_field["particle_id"],
            "expected_field_id": internal_field["field_id"],
            "endpoint_particle_id": internal_species,
            "momentum_label": momentum_label,
            "momentum_substitution": f"{left_internal_sign}{momentum_label}",
            "crossing_treatment": "internal_line_orientation",
            "convention_conversion": {
                "source": "internal_routing",
                "target": "all_momenta_incoming_vertex",
            },
            "fermion_flow": {
                "field_orientation": _field_orientation(internal_field),
                "flow_direction": _fermion_flow_direction(internal_field),
            },
        }
    )
    return sorted(bindings, key=lambda binding: binding["rule_slot"])


def _external_binding(
    field: dict[str, Any],
    endpoint: dict[str, Any],
    endpoint_id: str,
) -> dict[str, Any]:
    incoming = endpoint["state_role"] == "incoming"
    return {
        "rule_slot": field["slot"],
        "endpoint_id": endpoint_id,
        "endpoint_kind": "external_leg",
        "expected_particle_id": field["particle_id"],
        "expected_field_id": field["field_id"],
        "endpoint_particle_id": endpoint["particle_id"],
        "momentum_label": endpoint["momentum_label"],
        "momentum_substitution": endpoint["momentum_label"]
        if incoming
        else f"-{endpoint['momentum_label']}",
        "crossing_treatment": "external_incoming_as_rule_incoming"
        if incoming
        else "external_outgoing_crossed_to_rule_incoming",
        "convention_conversion": {
            "source": "physical_external_momenta",
            "target": "all_momenta_incoming_vertex",
        },
        "fermion_flow": {
            "field_orientation": _field_orientation(field),
            "flow_direction": _fermion_flow_direction(field),
        },
    }


def _fermion_flow_direction(field: dict[str, Any]) -> str:
    if field["field_role"] != "dirac_fermion":
        return "not_applicable"
    orientation = field["quantum_field_role"]
    if orientation == "psi":
        return "into_vertex"
    if orientation == "psi_bar":
        return "out_of_vertex"
    raise DiagramGenerationError(f"unsupported Dirac quantum_field_role: {orientation}")


def _field_orientation(field: dict[str, Any]) -> str:
    if field["field_role"] == "dirac_fermion":
        return field["quantum_field_role"]
    return "not_applicable"


def _external_legs_for_channel(
    process_tail: str,
    channel: str,
    external_by_slot: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "leg_id": f"leg:generated:{process_tail}:{channel}:{slot}",
            "slot": slot,
            "particle_id": external_by_slot[slot]["particle_id"],
            "state_role": external_by_slot[slot]["state_role"],
            "momentum_label": external_by_slot[slot]["momentum_label"],
        }
        for slot in (1, 2, 3, 4)
    ]


def _internal_momentum_expression(
    slots: tuple[int, int],
    external_by_slot: dict[int, dict[str, Any]],
) -> str:
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


def _sum_coupling_orders(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: dict[str, int] = {}
    for rule in rules:
        for item in rule.get("coupling_order", []):
            totals[item["coupling"]] = totals.get(item["coupling"], 0) + item["power"]
    return [
        {"coupling": coupling, "power": totals[coupling]}
        for coupling in sorted(totals)
    ]


def _antiparticle(
    particle_id: str,
    particle_catalog: dict[str, dict[str, Any]],
) -> str:
    return particle_catalog.get(particle_id, {}).get("antiparticle_id", particle_id)


def _id_tail(object_id: str) -> str:
    return object_id.split(":")[-1].replace("_", "-").lower()


def _endpoint_slot_from_id(endpoint_id: str) -> str:
    return endpoint_id.split(":")[-1]


