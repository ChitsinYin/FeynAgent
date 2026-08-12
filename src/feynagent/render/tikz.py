"""Deterministic TikZ-Feynman rendering for DiagramIR 0.1.1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RenderError(ValueError):
    """Raised when DiagramIR lacks data required for deterministic rendering."""


CHANNEL_ORDER = {"s": 0, "t": 1, "u": 2, "contact": 3}


def render_tikz_feynman(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    diagram_ir: dict[str, Any],
    output_dir: Path,
    latex_command: str = "lualatex",
) -> dict[str, Any]:
    """Write diagrams.tex, compile diagrams.pdf, and write render_manifest.json."""

    _validate_inputs(physics_card, convention_card, diagram_ir)
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    tex = build_tikz_document(physics_card, diagram_ir)
    tex_path = output_dir / "diagrams.tex"
    tex_path.write_text(tex, encoding="utf-8")

    compile_cmd = [
        latex_command,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory",
        str(output_dir),
        str(tex_path),
    ]
    completed = subprocess.run(
        compile_cmd,
        text=True,
        capture_output=True,
        cwd=output_dir,
        timeout=60,
    )

    stdout_path = output_dir / "latex.stdout.log"
    stderr_path = output_dir / "latex.stderr.log"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    pdf_path = output_dir / "diagrams.pdf"
    manifest = {
        "schema_version": "0.1.0",
        "renderer": "tikz-feynman",
        "renderer_role": "derived_artifact_backend",
        "physics_source": {
            "physics_card_id": physics_card["object_id"],
            "convention_card_id": convention_card["object_id"],
            "diagram_ir_id": diagram_ir["object_id"],
            "process_id": diagram_ir["process_id"],
        },
        "outputs": {
            "tex": str(tex_path),
            "pdf": str(pdf_path),
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        },
        "compile": {
            "command": compile_cmd,
            "exit_code": completed.returncode,
            "stdout_log": str(stdout_path),
            "stderr_log": str(stderr_path),
        },
        "diagram_count": len(diagram_ir["diagrams"]),
        "channels": [diagram["channel"] for diagram in _ordered_diagrams(diagram_ir)],
        "tex_sha256": hashlib.sha256(tex.encode("utf-8")).hexdigest(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "physics_state_modified": False,
        "notes": "TikZ layout is derived and is not encoded back into DiagramIR.",
    }
    if completed.returncode == 0 and not pdf_path.exists():
        manifest["compile"]["exit_code"] = 1
        manifest["compile"]["notes"] = "LaTeX returned success but diagrams.pdf was not found."

    manifest_path = output_dir / "render_manifest.json"
    manifest["outputs"]["manifest"] = str(manifest_path)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if manifest["compile"]["exit_code"] != 0:
        raise RenderError(f"LaTeX compile failed with exit code {manifest['compile']['exit_code']}")
    return manifest


def build_tikz_document(physics_card: dict[str, Any], diagram_ir: dict[str, Any]) -> str:
    """Return deterministic TeX for all diagrams in a DiagramIR object."""

    display_labels = _display_labels(physics_card)
    diagrams = [_render_diagram(diagram, display_labels) for diagram in _ordered_diagrams(diagram_ir)]
    body = "\n\n\\bigskip\n\n".join(diagrams)
    return "\n".join(
        [
            r"\documentclass[tikz,border=6pt]{standalone}",
            r"\usepackage[compat=1.1.0]{tikz-feynman}",
            r"\begin{document}",
            body,
            r"\end{document}",
            "",
        ]
    )


def _render_diagram(diagram: dict[str, Any], display_labels: dict[int, str]) -> str:
    _require_renderable(diagram)
    channel = diagram["channel"]
    vertices = diagram["vertex_instances"]
    internal_lines = diagram["internal_lines"]

    lines = [
        r"\begin{tikzpicture}",
        rf"  \node at (2.6,1.85) {{\(\mathrm{{{_tex_escape(channel)}}}-channel\)}};",
        r"  \begin{feynman}",
    ]

    for leg in sorted(diagram["external_legs"], key=lambda item: item["slot"]):
        name = _leg_node(leg["slot"])
        x, y = _leg_position(leg["slot"])
        label = _external_label(leg, display_labels)
        lines.append(rf"    \vertex ({name}) at ({x},{y}) {{\({_tex_escape(label)}\)}};")

    if channel == "contact":
        lines.append(r"    \vertex (v1) at (2.6,0);")
    else:
        lines.append(r"    \vertex (v1) at (1.8,0);")
        lines.append(r"    \vertex (v2) at (3.4,0);")

    edges = []
    if channel == "contact":
        vertex = vertices[0]
        for binding in sorted(vertex["slot_bindings"], key=lambda item: item["rule_slot"]):
            if binding["endpoint_kind"] != "external_leg":
                raise RenderError("contact diagram slot bindings must attach only external legs")
            leg = _external_leg_by_id(diagram, binding["endpoint_id"])
            edges.append(_edge_for_binding(_leg_node(leg["slot"]), "v1", binding, None))
    else:
        vertex_ids = [vertex["vertex_id"] for vertex in vertices]
        vertex_names = {vertex_ids[0]: "v1", vertex_ids[1]: "v2"}
        internal = internal_lines[0]
        for vertex in vertices:
            vertex_name = vertex_names[vertex["vertex_id"]]
            for binding in sorted(vertex["slot_bindings"], key=lambda item: item["rule_slot"]):
                if binding["endpoint_kind"] == "external_leg":
                    leg = _external_leg_by_id(diagram, binding["endpoint_id"])
                    edges.append(_edge_for_binding(_leg_node(leg["slot"]), vertex_name, binding, None))
        internal_label = _internal_label(internal)
        internal_style = _internal_edge_style(diagram, internal, vertex_names)
        edges.append(rf"      (v1) -- [{internal_style}, edge label={{\({_tex_escape(internal_label)}\)}}] (v2)")

    lines.append(r"    \diagram* {")
    for index, edge in enumerate(edges):
        comma = "," if index < len(edges) - 1 else ""
        lines.append(edge + comma)
    lines.append(r"    };")
    lines.append(r"  \end{feynman}")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _require_renderable(diagram: dict[str, Any]) -> None:
    if diagram.get("loop_order") != 0:
        raise RenderError("renderer supports only loop_order = 0")
    if diagram.get("channel") not in CHANNEL_ORDER:
        raise RenderError(f"unsupported channel: {diagram.get('channel')}")
    if diagram["channel"] == "contact":
        if len(diagram.get("vertex_instances", [])) != 1:
            raise RenderError("contact rendering requires exactly one vertex")
        if diagram.get("internal_lines"):
            raise RenderError("contact rendering expects no internal lines")
    else:
        if len(diagram.get("vertex_instances", [])) != 2:
            raise RenderError("exchange rendering requires exactly two vertices")
        if len(diagram.get("internal_lines", [])) != 1:
            raise RenderError("exchange rendering requires exactly one internal line")

    endpoint_ids = {leg["leg_id"] for leg in diagram["external_legs"]}
    endpoint_ids.update(line["line_id"] for line in diagram["internal_lines"])
    for vertex in diagram["vertex_instances"]:
        if "slot_bindings" not in vertex:
            raise RenderError(f"missing slot_bindings for {vertex.get('vertex_id')}")
        slots = [binding.get("rule_slot") for binding in vertex["slot_bindings"]]
        if None in slots or len(slots) != len(set(slots)):
            raise RenderError(f"incomplete or duplicate rule slots for {vertex.get('vertex_id')}")
        for binding in vertex["slot_bindings"]:
            for key in ("endpoint_id", "endpoint_kind", "momentum_label", "fermion_flow"):
                if key not in binding:
                    raise RenderError(f"missing {key} in slot binding for {vertex.get('vertex_id')}")
            if binding["endpoint_id"] not in endpoint_ids:
                raise RenderError(f"slot binding references unknown endpoint {binding['endpoint_id']}")
            flow = binding["fermion_flow"]
            if "field_orientation" not in flow or "flow_direction" not in flow:
                raise RenderError("fermion_flow must include field_orientation and flow_direction")
            if _is_fermion_binding(binding) and flow["flow_direction"] == "not_applicable":
                raise RenderError("fermion binding requires explicit flow direction")


def _edge_for_binding(
    leg_node: str,
    vertex_node: str,
    binding: dict[str, Any],
    label: str | None,
) -> str:
    style = _external_edge_style(binding)
    label_part = "" if label is None else rf", edge label={{\({_tex_escape(label)}\)}}"
    flow = binding["fermion_flow"]["flow_direction"]
    if _is_fermion_binding(binding) and flow == "out_of_vertex":
        return rf"      ({vertex_node}) -- [{style}{label_part}] ({leg_node})"
    return rf"      ({leg_node}) -- [{style}{label_part}] ({vertex_node})"


def _external_edge_style(binding: dict[str, Any]) -> str:
    if _is_fermion_binding(binding):
        return "fermion"
    if binding["fermion_flow"]["field_orientation"] != "not_applicable":
        raise RenderError("non-fermion line has inconsistent fermion_flow")
    return _boson_style(binding["endpoint_particle_id"])


def _internal_edge_style(
    diagram: dict[str, Any],
    internal: dict[str, Any],
    vertex_names: dict[str, str],
) -> str:
    from_vertex = internal["from"]["id"]
    to_vertex = internal["to"]["id"]
    from_binding = _internal_binding_for_vertex(diagram, from_vertex, internal["line_id"])
    to_binding = _internal_binding_for_vertex(diagram, to_vertex, internal["line_id"])
    fermion_bindings = [binding for binding in (from_binding, to_binding) if _is_fermion_binding(binding)]
    if not fermion_bindings:
        return _boson_style(internal["particle_id"])
    if len(fermion_bindings) != 2:
        raise RenderError("fermion internal line requires flow data at both vertices")
    orientations = {binding["fermion_flow"]["field_orientation"] for binding in fermion_bindings}
    if orientations != {"psi", "psi_bar"}:
        raise RenderError("fermion internal line requires psi and psi_bar endpoint orientations")
    if vertex_names[from_vertex] != "v1" or vertex_names[to_vertex] != "v2":
        raise RenderError("unexpected internal vertex ordering")
    return "fermion"


def _internal_binding_for_vertex(
    diagram: dict[str, Any],
    vertex_id: str,
    line_id: str,
) -> dict[str, Any]:
    for vertex in diagram["vertex_instances"]:
        if vertex["vertex_id"] != vertex_id:
            continue
        for binding in vertex["slot_bindings"]:
            if binding["endpoint_id"] == line_id:
                return binding
    raise RenderError(f"missing internal slot binding for {line_id} at {vertex_id}")


def _is_fermion_binding(binding: dict[str, Any]) -> bool:
    return binding["fermion_flow"]["field_orientation"] in {"psi", "psi_bar"}


def _boson_style(particle_id: str) -> str:
    if particle_id == "gamma":
        return "photon"
    return "scalar"


def _ordered_diagrams(diagram_ir: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        diagram_ir["diagrams"],
        key=lambda item: (CHANNEL_ORDER.get(item["channel"], 99), item["diagram_id"]),
    )


def _display_labels(physics_card: dict[str, Any]) -> dict[int, str]:
    labels = {}
    for role in ("incoming", "outgoing"):
        for particle in physics_card["particles"][role]:
            labels[particle["slot"]] = particle.get("display_name") or particle["particle_id"]
    return labels


def _external_label(leg: dict[str, Any], display_labels: dict[int, str]) -> str:
    particle = display_labels.get(leg["slot"], leg["particle_id"])
    return f"{particle}\\;({leg['momentum_label']})"


def _internal_label(internal: dict[str, Any]) -> str:
    momentum = internal["momentum"]
    return f"{internal['particle_id']}\\;({momentum['label']}={momentum['expression']})"


def _external_leg_by_id(diagram: dict[str, Any], leg_id: str) -> dict[str, Any]:
    for leg in diagram["external_legs"]:
        if leg["leg_id"] == leg_id:
            return leg
    raise RenderError(f"unknown external leg {leg_id}")


def _leg_node(slot: int) -> str:
    return f"l{slot}"


def _leg_position(slot: int) -> tuple[str, str]:
    positions = {
        1: ("0", "-1.0"),
        2: ("0", "1.0"),
        3: ("5.2", "-1.0"),
        4: ("5.2", "1.0"),
    }
    if slot not in positions:
        raise RenderError(f"unsupported external slot for Day-2 renderer: {slot}")
    return positions[slot]


def _tex_escape(value: str) -> str:
    return (
        str(value)
        .replace("_", r"\_")
        .replace("#", r"\#")
        .replace("&", r"\&")
        .replace("%", r"\%")
    )


def _validate_inputs(
    physics_card: dict[str, Any],
    convention_card: dict[str, Any],
    diagram_ir: dict[str, Any],
) -> None:
    if physics_card.get("schema_version") != "0.1.1":
        raise RenderError("PhysicsCard schema_version must be 0.1.1")
    if convention_card.get("schema_version") != "0.1.1":
        raise RenderError("ConventionCard schema_version must be 0.1.1")
    if diagram_ir.get("schema_version") != "0.1.1":
        raise RenderError("DiagramIR schema_version must be 0.1.1")
    if physics_card.get("process_id") != diagram_ir.get("process_id"):
        raise RenderError("PhysicsCard process_id does not match DiagramIR")
    if not convention_card.get("all_momenta_incoming_vertex_convention"):
        raise RenderError("renderer requires explicit all-momenta-incoming convention")




