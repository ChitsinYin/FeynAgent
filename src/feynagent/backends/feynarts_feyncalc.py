"""Minimal FeynArts/FeynCalc-native tree-level QED backend.

This module is intentionally separate from the legacy custom amplitude backend.
It renders and runs native FeynArts/FeynCalc scripts from structured PhysicsCard
content and backend configuration, without consulting the legacy QED RuleRegistry
or rewriting native amplitudes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


class NativeBackendError(ValueError):
    """Raised when a PhysicsCard cannot be handled by the native backend."""


@dataclass(frozen=True)
class BackendConfig:
    """Configuration resolved from a BackendProfile for native QED."""

    backend_profile_id: str = "backend_profile:feynarts_sm_qed"
    backend_id: str = "feynarts_feyncalc_native"
    model_id: str = "sm_qed"
    sector: str = "qed"
    model: str = "SM"
    generic_model: str = "Lorentz"
    restrictions: str = "QEDOnly"
    insertion_level: str = "Classes"
    exclude_topologies: tuple[str, ...] = ("Tadpoles", "SelfEnergies", "WFCorrections")
    particle_to_feynarts: dict[str, str] = field(default_factory=dict)
    particle_masses: dict[str, str] = field(default_factory=dict)
    particle_state_kinds: dict[str, str] = field(default_factory=dict)
    particle_spin_average_denominators: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class NativeChannel:
    """Metadata label for a native FeynArts diagram channel."""

    channel: str
    internal_particle: str
    routing: str


OUTPUT_FILES = (
    "native_amplitude.wl",
    "stdout.log",
    "stderr.log",
    "native_summary.json",
    "diagram_source.m",
    "diagram_source.inputform.txt",
    "diagram_source.paint.inputform.txt",
    "diagrams.pdf",
    "raw_feynarts_amplitude.m",
    "raw_feynarts_amplitude.inputform.txt",
    "raw_feynarts_amplitudes.m",
    "feyncalc_amplitude.m",
    "feyncalc_amplitude.inputform.txt",
    "feyncalc_amplitudes.m",
    "amplitudes.tex",
    "amplitudes.pdf",
    "amplitudes.json",
    "amplitudes.aux",
    "amplitudes.log",
    "run_manifest.json",
)


REQUIRED_NATIVE_ARTIFACTS = (
    "diagrams.pdf",
    "diagram_source.m",
    "diagram_source.inputform.txt",
    "amplitudes.tex",
    "amplitudes.pdf",
    "amplitudes.json",
    "feyncalc_amplitudes.m",
    "native_amplitude.wl",
    "stdout.log",
    "stderr.log",
)


def backend_config_from_dict(data: dict[str, Any]) -> BackendConfig:
    """Build BackendConfig from a structured BackendProfile YAML object."""

    if data.get("backend_kind") != "feynarts_feyncalc_native":
        raise NativeBackendError("backend profile must have backend_kind feynarts_feyncalc_native")
    resolves = data.get("resolves", {})
    native = data.get("native", {}).get("feynarts", {})
    mappings = native.get("particle_mappings", [])
    particle_to_feynarts = {
        item["particle_id"]: item["backend_identifier"]
        for item in mappings
    }
    particle_masses = {
        item["particle_id"]: item.get("mass", _default_particle_mass(item["particle_id"]))
        for item in mappings
    }
    particle_state_kinds = {
        item["particle_id"]: item.get("external_state_kind", _default_external_state_kind(item["particle_id"]))
        for item in mappings
    }
    particle_spin_average_denominators = {
        item["particle_id"]: int(item.get("spin_average_denominator", _default_spin_average_denominator(item["particle_id"])))
        for item in mappings
    }
    if not particle_to_feynarts:
        raise NativeBackendError("native backend profile must define particle_mappings")
    return BackendConfig(
        backend_profile_id=data.get("backend_profile_id", data.get("object_id", BackendConfig.backend_profile_id)),
        backend_id=data.get("backend_kind", BackendConfig.backend_id),
        model_id=resolves.get("model_id", BackendConfig.model_id),
        sector=resolves.get("sector", BackendConfig.sector),
        model=native.get("model", BackendConfig.model),
        generic_model=native.get("generic_model", BackendConfig.generic_model),
        restrictions=native.get("restrictions", BackendConfig.restrictions),
        insertion_level=native.get("insertion_level", BackendConfig.insertion_level),
        exclude_topologies=tuple(native.get("exclude_topologies", BackendConfig.exclude_topologies)),
        particle_to_feynarts=particle_to_feynarts,
        particle_masses=particle_masses,
        particle_state_kinds=particle_state_kinds,
        particle_spin_average_denominators=particle_spin_average_denominators,
    )


def validate_native_qed_request(physics_card: dict[str, Any], config: BackendConfig) -> None:
    """Validate the bounded native backend request against backend-neutral physics intent."""

    if config.backend_id != "feynarts_feyncalc_native":
        raise NativeBackendError("backend_id must be feynarts_feyncalc_native")
    if physics_card.get("model_id") != config.model_id or physics_card.get("sector") != config.sector:
        raise NativeBackendError("PhysicsCard model_id/sector does not match BackendProfile")
    if config.model != "SM" or config.generic_model != "Lorentz":
        raise NativeBackendError("Day-4 native backend supports only FeynArts SM/Lorentz")
    if config.restrictions != "QEDOnly":
        raise NativeBackendError("Day-4 native backend requires Restrictions -> QEDOnly")
    if config.insertion_level != "Classes":
        raise NativeBackendError("Day-4 native backend requires InsertionLevel -> Classes")
    if physics_card.get("process_type") != "scattering_2_to_2":
        raise NativeBackendError("Day-4 native backend supports only 2 -> 2 scattering")
    perturbative = physics_card.get("perturbative_order", {})
    if perturbative.get("loop_order") != 0 or perturbative.get("restriction") != "tree_level_only":
        raise NativeBackendError("Day-4 native backend supports only tree-level requests")
    orders = physics_card.get("coupling_order", {}).get("orders", [])
    if not orders or any(order.get("coupling") != "e" for order in orders):
        raise NativeBackendError("Day-4 native backend supports QED coupling order only")
    incoming = physics_card.get("particles", {}).get("incoming", [])
    outgoing = physics_card.get("particles", {}).get("outgoing", [])
    if len(incoming) != 2 or len(outgoing) != 2:
        raise NativeBackendError("Day-4 native backend requires exactly two incoming and two outgoing particles")
    if not config.particle_to_feynarts:
        raise NativeBackendError("native backend profile must define particle mappings")
    unsupported = [
        leg.get("particle_id")
        for leg in incoming + outgoing
        if leg.get("particle_id") not in config.particle_to_feynarts
    ]
    if unsupported:
        raise NativeBackendError(f"unsupported native QED particle(s): {unsupported}")
    native_qed_channel_plan(physics_card)


def native_qed_channel_plan(physics_card: dict[str, Any]) -> list[NativeChannel]:
    """Infer QED 2 -> 2 channel labels for metadata from external particles."""

    incoming = sorted(physics_card.get("particles", {}).get("incoming", []), key=lambda leg: leg["slot"])
    outgoing = sorted(physics_card.get("particles", {}).get("outgoing", []), key=lambda leg: leg["slot"])
    if len(incoming) != 2 or len(outgoing) != 2:
        raise NativeBackendError("native QED channel metadata requires a 2 -> 2 request")
    legs = [incoming[0], incoming[1], outgoing[0], outgoing[1]]
    candidates = [
        ("s", (0, 1), (2, 3), f"{legs[0]['momentum_label']}+{legs[1]['momentum_label']}"),
        ("t", (0, 2), (1, 3), f"{legs[0]['momentum_label']}-{legs[2]['momentum_label']}"),
        ("u", (0, 3), (1, 2), f"{legs[0]['momentum_label']}-{legs[3]['momentum_label']}"),
    ]
    channels: list[NativeChannel] = []
    for channel, left, right, routing in candidates:
        left_internal = _qed_internal_for_pair(legs[left[0]]["particle_id"], legs[left[1]]["particle_id"])
        right_internal = _qed_internal_for_pair(legs[right[0]]["particle_id"], legs[right[1]]["particle_id"])
        if left_internal is not None and left_internal == right_internal:
            channels.append(NativeChannel(channel=channel, internal_particle=left_internal, routing=routing))
    if not channels:
        raise NativeBackendError("no supported native QED tree channel found for request")
    return channels


def validate_native_qed_artifact_metadata(metadata: dict[str, Any], physics_card: dict[str, Any]) -> list[str]:
    """Return validation issues for native diagram/amplitude artifact metadata."""

    issues: list[str] = []
    expected_channels = native_qed_channel_plan(physics_card)
    expected_labels = [channel.channel for channel in expected_channels]
    diagrams = metadata.get("diagrams", [])
    if metadata.get("diagram_count") != len(expected_channels):
        issues.append("diagram_count does not match expected native QED channels")
    if metadata.get("channel_count") != len(expected_channels):
        issues.append("channel_count does not match expected native QED channels")
    if metadata.get("per_diagram_amplitude_count") != len(expected_channels):
        issues.append("per_diagram_amplitude_count does not match expected native QED channels")
    if len(diagrams) != len(expected_channels):
        issues.append("diagram metadata length does not match expected native QED channels")
    diagram_labels = [diagram.get("channel") for diagram in diagrams]
    if diagram_labels != expected_labels:
        issues.append(f"channel labels {diagram_labels} do not match expected {expected_labels}")
    expression_ids = [diagram.get("expression_id") for diagram in diagrams]
    if any(not expression_id for expression_id in expression_ids):
        issues.append("every diagram must record an expression_id")
    if any(diagram.get("amplitude_file") != "feyncalc_amplitudes.m" for diagram in diagrams):
        issues.append("every diagram must point to feyncalc_amplitudes.m")
    if any(diagram.get("latex_file") != "amplitudes.tex" for diagram in diagrams):
        issues.append("every diagram must point to amplitudes.tex")
    total = metadata.get("total_amplitude", {})
    if total.get("term_expression_ids") != expression_ids:
        issues.append("total amplitude terms do not match per-diagram expression IDs")
    if total.get("definition") != "Plus @@ per_diagram_amplitudes":
        issues.append("total amplitude definition must be the sum of per-diagram amplitudes")
    consistency = metadata.get("consistency", {})
    for key in (
        "diagram_count_matches_channel_plan",
        "diagram_count_matches_per_diagram_amplitudes",
        "total_is_sum_of_per_diagram_amplitudes",
    ):
        if consistency.get(key) is not True:
            issues.append(f"metadata consistency flag failed: {key}")
    if consistency.get("m2_computed") is not False:
        issues.append("native artifact generation must not compute M2")
    return issues


def validate_native_qed_artifacts(output_dir: str | Path, physics_card: dict[str, Any]) -> list[str]:
    """Validate persisted native artifact files and their structured metadata."""

    output_path = Path(output_dir)
    issues = []
    for name in REQUIRED_NATIVE_ARTIFACTS:
        if not (output_path / name).exists():
            issues.append(f"missing required artifact: {name}")
    metadata_path = output_path / "amplitudes.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        issues.extend(validate_native_qed_artifact_metadata(metadata, physics_card))
    return issues


def build_native_qed_script(physics_card: dict[str, Any], config: BackendConfig) -> str:
    """Build a Wolfram script for native FeynArts/FeynCalc artifact generation."""

    validate_native_qed_request(physics_card, config)
    incoming_legs = sorted(physics_card["particles"]["incoming"], key=lambda leg: leg["slot"])
    outgoing_legs = sorted(physics_card["particles"]["outgoing"], key=lambda leg: leg["slot"])
    incoming = [_map_particle(leg, config) for leg in incoming_legs]
    outgoing = [_map_particle(leg, config) for leg in outgoing_legs]
    incoming_momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs]
    outgoing_momenta = [_wl_symbol(leg["momentum_label"]) for leg in outgoing_legs]
    transverse_momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs + outgoing_legs if leg["particle_id"] == "gamma"]
    channel_plan = native_qed_channel_plan(physics_card)
    create_call = _create_topologies_call(config)
    insert_call = _insert_fields_call(config, incoming, outgoing)
    process_id = physics_card.get("process_id", "process:unknown")
    process_title = _latex_escape(_process_title(incoming_legs, outgoing_legs))
    backend_label = _latex_escape(config.backend_id)
    channel_plan_wl = _channel_plan_wl(channel_plan)
    transverse_option = ""
    if transverse_momenta:
        transverse_option = f",\n  TransversePolarizationVectors -> {{{', '.join(transverse_momenta)}}}"

    return f'''(* FeynAgent native FeynArts/FeynCalc QED backend. *)
(* Loading strategy validated by `python -m feynagent init`: $LoadAddOns = {{"FeynArts"}}; << FeynCalc`. *)
(* source_process_id = "{process_id}" *)
(* backend_profile_id = "{config.backend_profile_id}" *)
(* This script uses native FeynArts/FeynCalc amplitudes only. *)

$LoadAddOns = {{"FeynArts"}};
Quiet[Get["FeynCalc`"], FrontEndObject::notavail];

outputDir = DirectoryName[$InputFileName];
diagramsPdfPath = FileNameJoin[{{outputDir, "diagrams.pdf"}}];
diagramSourcePath = FileNameJoin[{{outputDir, "diagram_source.m"}}];
diagramSourceTextPath = FileNameJoin[{{outputDir, "diagram_source.inputform.txt"}}];
diagramPaintSourceTextPath = FileNameJoin[{{outputDir, "diagram_source.paint.inputform.txt"}}];
rawAmpPath = FileNameJoin[{{outputDir, "raw_feynarts_amplitude.m"}}];
rawTextPath = FileNameJoin[{{outputDir, "raw_feynarts_amplitude.inputform.txt"}}];
rawDiagramAmpPath = FileNameJoin[{{outputDir, "raw_feynarts_amplitudes.m"}}];
fcAmpPath = FileNameJoin[{{outputDir, "feyncalc_amplitude.m"}}];
fcTextPath = FileNameJoin[{{outputDir, "feyncalc_amplitude.inputform.txt"}}];
fcAmpsPath = FileNameJoin[{{outputDir, "feyncalc_amplitudes.m"}}];
amplitudesTexPath = FileNameJoin[{{outputDir, "amplitudes.tex"}}];
amplitudesJsonPath = FileNameJoin[{{outputDir, "amplitudes.json"}}];
summaryPath = FileNameJoin[{{outputDir, "native_summary.json"}}];

createTopologiesCall = "{_escape_wl_string(create_call)}";
insertFieldsCall = "{_escape_wl_string(insert_call)}";
channelPlan = {channel_plan_wl};

Print["FEYNAGENT_NATIVE_BACKEND_BEGIN"];
Print["WOLFRAM_VERSION=" <> $Version];
Print["FEYNARTS_VERSION=" <> ToString[Quiet[Check[FeynArts`$FeynArtsVersion, "unknown"]], InputForm]];
Print["FEYNCALC_VERSION=" <> ToString[Quiet[Check[FeynCalc`$FeynCalcVersion, "unknown"]], InputForm]];
Print["CREATE_TOPOLOGIES_CALL=" <> createTopologiesCall];
Print["INSERT_FIELDS_CALL=" <> insertFieldsCall];

topologies = {create_call};
inserted = {insert_call};
diagramCount = Length[List @@ inserted];
Print["DIAGRAM_COUNT=" <> ToString[diagramCount, InputForm]];

Put[inserted, diagramSourcePath];
Export[diagramSourceTextPath, ToString[inserted, InputForm], "Text"];
paintedDiagrams = Quiet[Check[
  Paint[
    inserted,
    PaintLevel -> {{{config.insertion_level}}},
    ColumnsXRows -> {{Max[1, diagramCount], 1}},
    SheetHeader -> None,
    Numbering -> Simple,
    DisplayFunction -> Identity
  ],
  $Failed
]];
diagramRenderingRoute = If[paintedDiagrams === $Failed, "feynarts_paint_failed", "feynarts_paint_export_pdf"];
If[paintedDiagrams =!= $Failed,
  Export[diagramPaintSourceTextPath, ToString[paintedDiagrams, InputForm], "Text"];
  Export[diagramsPdfPath, paintedDiagrams];
];
Print["DIAGRAM_RENDERING_ROUTE=" <> diagramRenderingRoute];
If[FileExistsQ[diagramsPdfPath], Print["DIAGRAMS_PDF_SAVED=" <> diagramsPdfPath]];

rawAmplitude = CreateFeynAmp[inserted, PreFactor -> 1];
rawDiagramAmplitudes = List @@ rawAmplitude;
Put[rawAmplitude, rawAmpPath];
Export[rawTextPath, ToString[rawAmplitude, InputForm], "Text"];
Put[rawDiagramAmplitudes, rawDiagramAmpPath];

feyncalcDiagramAmplitudes = FCFAConvert[
  rawAmplitude,
  IncomingMomenta -> {{{', '.join(incoming_momenta)}}},
  OutgoingMomenta -> {{{', '.join(outgoing_momenta)}}},
  LoopMomenta -> {{}},
  UndoChiralSplittings -> True,
  ChangeDimension -> 4{transverse_option},
  List -> True,
  SMP -> True
];
feyncalcTotalAmplitude = Plus @@ feyncalcDiagramAmplitudes;
expressionIds = Table["expr:{_escape_wl_string(process_id)}:diagram:" <> ToString[i], {{i, Length[feyncalcDiagramAmplitudes]}}];
totalExpressionId = "expr:{_escape_wl_string(process_id)}:total";
Put[feyncalcDiagramAmplitudes, fcAmpPath];
Export[fcTextPath, ToString[feyncalcDiagramAmplitudes, InputForm], "Text"];
Put[
  <|
    "per_diagram_expression_ids" -> expressionIds,
    "per_diagram_amplitudes" -> feyncalcDiagramAmplitudes,
    "total_expression_id" -> totalExpressionId,
    "total_amplitude" -> feyncalcTotalAmplitude
  |>,
  fcAmpsPath
];

extractPropagators[expr_] := Cases[
  expr,
  PropagatorDenominator[Momentum[mom_, ___], mass___] :> <|
    "momentum" -> ToString[Unevaluated[mom], InputForm],
    "mass" -> ToString[Unevaluated[{{mass}}], InputForm]
  |>,
  Infinity
];

texString[expr_] := StringReplace[ToString[TeXForm[expr]], "^*^{{" -> "^{{* "];

texSections = Table[
  "% expression-id: " <> expressionIds[[i]] <> "\\n" <>
  "\\\\subsection*{{Diagram " <> ToString[i] <> ": " <> channelPlan[[i, "channel"]] <> "-channel}}\\n" <>
  "\\\\begin{{align*}}\\n" <>
  "\\\\mathcal{{M}}_{{" <> channelPlan[[i, "channel"]] <> "}} &= " <> texString[feyncalcDiagramAmplitudes[[i]]] <> "\\n" <>
  "\\\\end{{align*}}\\n",
  {{i, Length[feyncalcDiagramAmplitudes]}}
];
amplitudesTex = StringJoin[
  "\\\\documentclass[11pt]{{article}}\\n",
  "\\\\usepackage{{amsmath}}\\n",
  "\\\\usepackage[margin=1in]{{geometry}}\\n",
  "\\\\begin{{document}}\\n",
  "\\\\section*{{Native FeynCalc Amplitudes}}\\n",
  "\\\\noindent Process: {process_title}\\\\\\\\\\n",
  "\\\\noindent Backend: {backend_label}\\\\\\\\\\n",
  "\\\\noindent Expression source: \\\\texttt{{feyncalc\\\\_amplitudes.m}}\\\\\\\\\\n\\n",
  StringRiffle[texSections, "\\n"],
  "% expression-id: " <> totalExpressionId <> "\\n",
  "\\\\subsection*{{Total amplitude}}\\n",
  "\\\\begin{{align*}}\\n",
  "\\\\mathcal{{M}}_{{\\\\mathrm{{total}}}} &= " <> texString[feyncalcTotalAmplitude] <> "\\n",
  "\\\\end{{align*}}\\n",
  "\\\\end{{document}}\\n"
];
Export[amplitudesTexPath, amplitudesTex, "Text"];

diagramRecords = Table[
  <|
    "diagram_id" -> ("native:diagram:" <> ToString[i]),
    "expression_id" -> expressionIds[[i]],
    "channel" -> channelPlan[[i, "channel"]],
    "internal_particle" -> channelPlan[[i, "internal_particle"]],
    "expected_routing" -> channelPlan[[i, "routing"]],
    "propagators" -> extractPropagators[feyncalcDiagramAmplitudes[[i]]],
    "amplitude_file" -> "feyncalc_amplitudes.m",
    "latex_file" -> "amplitudes.tex"
  |>,
  {{i, Length[feyncalcDiagramAmplitudes]}}
];

amplitudeMetadata = <|
  "backend_profile_id" -> "{config.backend_profile_id}",
  "backend_id" -> "{config.backend_id}",
  "process_id" -> "{process_id}",
  "diagram_count" -> diagramCount,
  "channel_count" -> Length[channelPlan],
  "per_diagram_amplitude_count" -> Length[feyncalcDiagramAmplitudes],
  "diagram_rendering_route" -> diagramRenderingRoute,
  "diagram_source" -> "diagram_source.m",
  "diagrams_pdf" -> If[FileExistsQ[diagramsPdfPath], "diagrams.pdf", Null],
  "feyncalc_amplitudes_file" -> "feyncalc_amplitudes.m",
  "latex_file" -> "amplitudes.tex",
  "latex_pdf" -> "amplitudes.pdf",
  "diagrams" -> diagramRecords,
  "total_amplitude" -> <|
    "expression_id" -> totalExpressionId,
    "definition" -> "Plus @@ per_diagram_amplitudes",
    "term_expression_ids" -> expressionIds,
    "amplitude_file" -> "feyncalc_amplitudes.m",
    "latex_file" -> "amplitudes.tex"
  |>,
  "consistency" -> <|
    "diagram_count_matches_channel_plan" -> (diagramCount == Length[channelPlan]),
    "diagram_count_matches_per_diagram_amplitudes" -> (diagramCount == Length[feyncalcDiagramAmplitudes]),
    "total_is_sum_of_per_diagram_amplitudes" -> True,
    "m2_computed" -> False
  |>
|>;
Export[amplitudesJsonPath, amplitudeMetadata, "JSON"];

summary = <|
  "backend_profile_id" -> "{config.backend_profile_id}",
  "backend_id" -> "{config.backend_id}",
  "process_id" -> "{process_id}",
  "model_id" -> "{config.model_id}",
  "sector" -> "{config.sector}",
  "wolfram_version" -> $Version,
  "feynarts_version" -> ToString[Quiet[Check[FeynArts`$FeynArtsVersion, "unknown"]], InputForm],
  "feyncalc_version" -> ToString[Quiet[Check[FeynCalc`$FeynCalcVersion, "unknown"]], InputForm],
  "create_topologies_call" -> createTopologiesCall,
  "insert_fields_call" -> insertFieldsCall,
  "diagram_count" -> diagramCount,
  "channel_plan" -> channelPlan,
  "diagram_rendering_route" -> diagramRenderingRoute,
  "model" -> "{config.model}",
  "generic_model" -> "{config.generic_model}",
  "restrictions" -> "{config.restrictions}",
  "insertion_level" -> "{config.insertion_level}",
  "m2_computed" -> False
|>;
Export[summaryPath, summary, "JSON"];
Print["DIAGRAM_SOURCE_SAVED=" <> diagramSourcePath];
Print["RAW_FEYNARTS_AMPLITUDE_SAVED=" <> rawAmpPath];
Print["FCFA_CONVERT_AMPLITUDES_SAVED=" <> fcAmpsPath];
Print["AMPLITUDES_TEX_SAVED=" <> amplitudesTexPath];
Print["AMPLITUDES_JSON_SAVED=" <> amplitudesJsonPath];
Print["FEYNAGENT_NATIVE_BACKEND_END"];
Quit[0];
'''


def run_native_qed_backend(
    physics_card: dict[str, Any],
    output_dir: str | Path,
    config: BackendConfig,
    *,
    wolframscript: str = "wolframscript",
    timeout_seconds: int = 60,
) -> dict[str, Any]:
    """Run the generated native Wolfram script and write a manifest."""

    validate_native_qed_request(physics_card, config)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    script_path = output_path / "native_amplitude.wl"
    stdout_path = output_path / "stdout.log"
    stderr_path = output_path / "stderr.log"
    manifest_path = output_path / "run_manifest.json"
    script_path.write_text(build_native_qed_script(physics_card, config), encoding="utf-8", newline="\n")

    started_at = datetime.now().astimezone().isoformat()
    completed = subprocess.run(
        [wolframscript, "-script", str(script_path.resolve())],
        cwd=output_path,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    completed_at = datetime.now().astimezone().isoformat()
    stdout_text = completed.stdout
    stderr_text = completed.stderr

    latex_completed = None
    amplitudes_tex_path = output_path / "amplitudes.tex"
    if completed.returncode == 0 and amplitudes_tex_path.exists():
        latex_completed = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "amplitudes.tex"],
            cwd=output_path,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
        stdout_text += "\nFEYNAGENT_AMPLITUDES_LATEX_BEGIN\n" + latex_completed.stdout + "\nFEYNAGENT_AMPLITUDES_LATEX_END\n"
        stderr_text += "\nFEYNAGENT_AMPLITUDES_LATEX_BEGIN\n" + latex_completed.stderr + "\nFEYNAGENT_AMPLITUDES_LATEX_END\n"

    stdout_path.write_text(stdout_text, encoding="utf-8", newline="\n")
    stderr_path.write_text(stderr_text, encoding="utf-8", newline="\n")

    summary_path = output_path / "native_summary.json"
    summary: dict[str, Any] = {}
    if summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    amplitudes_metadata_path = output_path / "amplitudes.json"
    amplitudes_metadata: dict[str, Any] = {}
    if amplitudes_metadata_path.exists():
        amplitudes_metadata = json.loads(amplitudes_metadata_path.read_text(encoding="utf-8"))
    artifact_validation = validate_native_qed_artifacts(output_path, physics_card)
    manifest = {
        "backend_profile_id": config.backend_profile_id,
        "backend_id": config.backend_id,
        "process_id": physics_card.get("process_id"),
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": completed.returncode,
        "script_path": str(script_path.name),
        "stdout_path": str(stdout_path.name),
        "stderr_path": str(stderr_path.name),
        "summary_path": str(summary_path.name) if summary_path.exists() else None,
        "amplitudes_metadata_path": str(amplitudes_metadata_path.name) if amplitudes_metadata_path.exists() else None,
        "native_summary": summary,
        "amplitudes": amplitudes_metadata,
        "latex_compile": None if latex_completed is None else {
            "command": ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "amplitudes.tex"],
            "exit_code": latex_completed.returncode,
            "pdf_path": "amplitudes.pdf" if (output_path / "amplitudes.pdf").exists() else None,
        },
        "artifact_validation": artifact_validation,
        "outputs": {},
        "notes": "Native FeynArts/FeynCalc amplitude generation only; no M2 calculation performed.",
    }
    for name in OUTPUT_FILES:
        path = output_path / name
        if path.exists():
            manifest["outputs"][name] = {"sha256": _sha256(path), "bytes": path.stat().st_size}
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    return manifest


def _map_particle(leg: dict[str, Any], config: BackendConfig) -> str:
    particle_id = leg.get("particle_id")
    if particle_id not in config.particle_to_feynarts:
        raise NativeBackendError(f"unsupported native QED particle: {particle_id}")
    return config.particle_to_feynarts[particle_id]


def _create_topologies_call(config: BackendConfig) -> str:
    excluded = ", ".join(config.exclude_topologies)
    return f"CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {{{excluded}}}]"


def _insert_fields_call(config: BackendConfig, incoming: list[str], outgoing: list[str]) -> str:
    return (
        f"InsertFields[topologies, {{{incoming[0]}, {incoming[1]}}} -> {{{outgoing[0]}, {outgoing[1]}}}, "
        f"Model -> \"{config.model}\", GenericModel -> \"{config.generic_model}\", "
        f"Restrictions -> {config.restrictions}, InsertionLevel -> {{{config.insertion_level}}}]"
    )


def _wl_symbol(label: str) -> str:
    return label.replace("_", "")


def _channel_plan_wl(channels: list[NativeChannel]) -> str:
    items = []
    for channel in channels:
        items.append(
            "<|"
            f'"channel" -> "{_escape_wl_string(channel.channel)}", '
            f'"internal_particle" -> "{_escape_wl_string(channel.internal_particle)}", '
            f'"routing" -> "{_escape_wl_string(channel.routing)}"'
            "|>"
        )
    return "{" + ", ".join(items) + "}"


def _qed_internal_for_pair(first: str, second: str) -> str | None:
    if first == "gamma" and _charged_fermion_family(second):
        return second
    if second == "gamma" and _charged_fermion_family(first):
        return first
    first_family = _charged_fermion_family(first)
    second_family = _charged_fermion_family(second)
    if first_family and second_family == first_family:
        return "gamma"
    return None


def _charged_fermion_family(particle_id: str) -> str | None:
    if particle_id in {"e-", "e+"}:
        return "e"
    if particle_id in {"mu-", "mu+"}:
        return "mu"
    return None


def _process_title(incoming_legs: list[dict[str, Any]], outgoing_legs: list[dict[str, Any]]) -> str:
    incoming = " + ".join(leg["particle_id"] for leg in incoming_legs)
    outgoing = " + ".join(leg["particle_id"] for leg in outgoing_legs)
    return f"{incoming} -> {outgoing}"


def _latex_escape(value: str) -> str:
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def _escape_wl_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


M2_OUTPUT_FILES = (
    "compute_m2.wl",
    "m2_raw.m",
    "m2_simplified.m",
    "m2_inputform.txt",
    "m2_manifest.json",
    "m2_stdout.log",
    "m2_stderr.log",
)


def build_native_qed_m2_script(
    physics_card: dict[str, Any],
    config: BackendConfig,
    *,
    gold_expression: str | None = None,
    simplify_timeout_seconds: int = 60,
) -> str:
    """Build a generic native FeynCalc script for standard-QED 2 -> 2 M2."""

    validate_native_qed_request(physics_card, config)
    incoming_legs = sorted(physics_card["particles"]["incoming"], key=lambda leg: leg["slot"])
    outgoing_legs = sorted(physics_card["particles"]["outgoing"], key=lambda leg: leg["slot"])
    incoming = [_map_particle(leg, config) for leg in incoming_legs]
    outgoing = [_map_particle(leg, config) for leg in outgoing_legs]
    incoming_momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs]
    outgoing_momenta = [_wl_symbol(leg["momentum_label"]) for leg in outgoing_legs]
    external_photons = _external_photon_momenta(physics_card)
    transverse_option = ""
    if external_photons:
        transverse_option = f",\n  TransversePolarizationVectors -> {{{', '.join(external_photons)}}}"
    create_call = _create_topologies_call(config)
    insert_call = _insert_fields_call(config, incoming, outgoing)
    set_mandelstam_call = _set_mandelstam_call(incoming_legs, outgoing_legs, config)
    mandelstam_mass_sum = _mandelstam_mass_sum(incoming_legs, outgoing_legs, config)
    spin_average_factor = _initial_spin_average_factor(incoming_legs, config)
    massless_replacements = _massless_replacements(incoming_legs + outgoing_legs, config)
    polarization_steps = _polarization_sum_steps(external_photons)
    photon_list = "{" + ", ".join(external_photons) + "}"
    fermion_list = "{" + ", ".join(_fermion_momenta(physics_card)) + "}"
    gold_assignment = "goldResult = Null;"
    comparison_block = 'comparison = <|"status" -> "NOT_REQUESTED"|>; status = "PASS";'
    if gold_expression:
        gold_assignment = f"goldResult = {gold_expression};"
        comparison_block = """
comparisonStatus = True;
FCCompareResults[m2Simplified, goldResult, Text -> {"native M2 vs gold", "CORRECT.", "WRONG!"}, Interrupt -> {Hold[comparisonStatus = False], Automatic}];
equivalence = TimeConstrained[FullSimplify[m2Simplified == goldResult], 30, $Failed];
status = If[comparisonStatus === True && equivalence === True, "PASS", "FAIL"];
comparison = <|"fc_compare_status" -> ToString[comparisonStatus, InputForm], "equivalence" -> ToString[equivalence, InputForm], "status" -> status|>;
""".strip()
    process_id = physics_card.get("process_id", "process:unknown")
    return f'''(* FeynAgent generic native standard-QED 2 -> 2 M2 generator. *)
(* source_process_id = "{process_id}" *)
(* backend_profile_id = "{config.backend_profile_id}" *)
(* This script uses native FeynArts/FeynCalc amplitudes only. *)

If[$FrontEnd === Null, $FeynCalcStartupMessages = False];
If[$Notebooks === False, $FeynCalcStartupMessages = False];
$LoadAddOns = {{"FeynArts"}};
Quiet[Get["FeynCalc`"], FrontEndObject::notavail];
$FAVerbose = 0;

outDir = DirectoryName[$InputFileName];
writeText[name_, expr_] := Export[FileNameJoin[{{outDir, name}}], ToString[InputForm[expr]], "Text"];
startTime = AbsoluteTime[];
status = "FAIL";

createTopologiesCall = "{_escape_wl_string(create_call)}";
insertFieldsCall = "{_escape_wl_string(insert_call)}";
setMandelstamCall = "{_escape_wl_string(set_mandelstam_call)}";
externalPhotonMomenta = {photon_list};
externalFermionMomenta = {fermion_list};
initialSpinAverageFactor = {spin_average_factor};
Print["FEYNAGENT_NATIVE_M2_BEGIN"];
Print["CREATE_TOPOLOGIES_CALL=" <> createTopologiesCall];
Print["INSERT_FIELDS_CALL=" <> insertFieldsCall];
Print["SET_MANDELSTAM_CALL=" <> setMandelstamCall];
Print["EXTERNAL_PHOTON_MOMENTA=" <> ToString[externalPhotonMomenta, InputForm]];
Print["EXTERNAL_FERMION_MOMENTA=" <> ToString[externalFermionMomenta, InputForm]];
Print["INITIAL_SPIN_AVERAGE_FACTOR=" <> ToString[initialSpinAverageFactor, InputForm]];

topologies = {create_call};
diags = {insert_call};
diagramCount = Length[List @@ diags];
rawAmplitude = CreateFeynAmp[diags, PreFactor -> 1];
ampTotal = FCFAConvert[
  rawAmplitude,
  IncomingMomenta -> {{{', '.join(incoming_momenta)}}},
  OutgoingMomenta -> {{{', '.join(outgoing_momenta)}}},
  LoopMomenta -> {{}},
  UndoChiralSplittings -> True,
  ChangeDimension -> 4{transverse_option},
  List -> False,
  SMP -> True,
  Contract -> True
];

FCClearScalarProducts[];
{set_mandelstam_call};
m2Product = ampTotal * ComplexConjugate[ampTotal];
m2DenExplicit = FeynAmpDenominatorExplicit[m2Product];
m2AfterPolarization = m2DenExplicit;
{polarization_steps}
m2Raw = FermionSpinSum[m2AfterPolarization, ExtraFactor -> initialSpinAverageFactor];
Put[m2Raw, FileNameJoin[{{outDir, "m2_raw.m"}}]];
writeText["m2_raw.inputform.txt", m2Raw];

m2Dirac = TimeConstrained[DiracSimplify[m2Raw], {simplify_timeout_seconds}, $Failed];
If[m2Dirac === $Failed, status = "TIMEOUT_DIRAC_SIMPLIFY"; Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], <|"status" -> status|>, "JSON"]; Quit[2]];
m2Mandelstam = TimeConstrained[TrickMandelstam[m2Dirac, {{s, t, u, {mandelstam_mass_sum}}}], {simplify_timeout_seconds}, $Failed];
If[m2Mandelstam === $Failed, status = "TIMEOUT_TRICK_MANDELSTAM"; Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], <|"status" -> status|>, "JSON"]; Quit[2]];
m2FullSimplified = TimeConstrained[Simplify[m2Mandelstam], {simplify_timeout_seconds}, $Failed];
If[m2FullSimplified === $Failed, status = "TIMEOUT_SIMPLIFY"; Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], <|"status" -> status|>, "JSON"]; Quit[2]];
m2Massless = TimeConstrained[Simplify[m2FullSimplified /. {{{massless_replacements}}}], {simplify_timeout_seconds}, $Failed];
If[m2Massless === $Failed, status = "TIMEOUT_MASSLESS_SIMPLIFY"; Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], <|"status" -> status|>, "JSON"]; Quit[2]];
m2Simplified = TimeConstrained[Simplify[TrickMandelstam[m2Massless, {{s, t, u, 0}}]], {simplify_timeout_seconds}, $Failed];
If[m2Simplified === $Failed, status = "TIMEOUT_MASSLESS_MANDELSTAM"; Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], <|"status" -> status|>, "JSON"]; Quit[2]];
Put[m2Simplified, FileNameJoin[{{outDir, "m2_simplified.m"}}]];
writeText["m2_inputform.txt", m2Simplified];
writeText["m2_simplified.inputform.txt", m2Simplified];
{gold_assignment}
{comparison_block}
runtime = AbsoluteTime[] - startTime;
manifest = <|
  "backend_profile_id" -> "{config.backend_profile_id}",
  "backend_id" -> "{config.backend_id}",
  "process_id" -> "{process_id}",
  "diagram_count" -> diagramCount,
  "m2_product_definition" -> "ampTotal * ComplexConjugate[ampTotal]",
  "used_feyn_amp_denominator_explicit" -> True,
  "external_photon_momenta" -> ToString[externalPhotonMomenta, InputForm],
  "external_fermion_momenta" -> ToString[externalFermionMomenta, InputForm],
  "polarization_sums_only_external_photons" -> True,
  "fermion_spin_sum_applied" -> True,
  "initial_spin_average_factor" -> ToString[initialSpinAverageFactor, InputForm],
  "set_mandelstam_call" -> setMandelstamCall,
  "massless_replacements" -> ToString[{{{massless_replacements}}}, InputForm],
  "gold_expression" -> If[goldResult === Null, Null, ToString[InputForm[goldResult]]],
  "comparison" -> comparison,
  "status" -> status,
  "runtime_seconds" -> runtime
|>;
Export[FileNameJoin[{{outDir, "m2_manifest.json"}}], manifest, "JSON"];
Print["FEYNAGENT_NATIVE_M2_STATUS=" <> status];
Print["FEYNAGENT_NATIVE_M2_RUNTIME=" <> ToString[NumberForm[runtime, {{Infinity, 3}}]]];
Print["FEYNAGENT_NATIVE_M2_END"];
Quit[If[status === "PASS", 0, 1]];
'''


def run_native_qed_m2_generator(
    physics_card: dict[str, Any],
    output_dir: str | Path,
    config: BackendConfig,
    execution_request: dict[str, Any],
    *,
    wolframscript: str = "wolframscript",
    gold_expression: str | None = None,
) -> dict[str, Any]:
    """Generate, and when authorized execute, the generic native QED M2 script."""

    validate_native_qed_request(physics_card, config)
    policy = _m2_execution_policy(physics_card, config, execution_request)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    script_path = output_path / "compute_m2.wl"
    stdout_path = output_path / "m2_stdout.log"
    stderr_path = output_path / "m2_stderr.log"
    manifest_path = output_path / "m2_manifest.json"
    timeout_seconds = policy.get("timeout_seconds") or 60
    script_path.write_text(
        build_native_qed_m2_script(
            physics_card,
            config,
            gold_expression=gold_expression,
            simplify_timeout_seconds=min(timeout_seconds, 90),
        ),
        encoding="utf-8",
        newline="\n",
    )
    result: dict[str, Any] = {
        "backend_profile_id": config.backend_profile_id,
        "backend_id": config.backend_id,
        "process_id": physics_card.get("process_id"),
        "script_path": script_path.name,
        "script_sha256": _sha256(script_path),
        "authorization": policy,
        "executed": False,
        "exit_code": None,
        "outputs": {"compute_m2.wl": {"sha256": _sha256(script_path), "bytes": script_path.stat().st_size}},
    }
    if not policy["execute"]:
        result["status"] = "SCRIPT_GENERATED_ONLY"
        manifest_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
        return result

    started_at = datetime.now().astimezone().isoformat()
    completed = subprocess.run(
        [wolframscript, "-script", str(script_path.resolve())],
        cwd=output_path,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    completed_at = datetime.now().astimezone().isoformat()
    stdout_path.write_text(completed.stdout, encoding="utf-8", newline="\n")
    stderr_path.write_text(completed.stderr, encoding="utf-8", newline="\n")
    script_manifest: dict[str, Any] = {}
    if manifest_path.exists():
        script_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    result.update(
        {
            "executed": True,
            "started_at": started_at,
            "completed_at": completed_at,
            "exit_code": completed.returncode,
            "stdout_path": stdout_path.name,
            "stderr_path": stderr_path.name,
            "script_manifest": script_manifest,
            "status": script_manifest.get("status", "FAIL" if completed.returncode else "PASS"),
        }
    )
    for name in M2_OUTPUT_FILES:
        path = output_path / name
        if path.exists():
            result["outputs"][name] = {"sha256": _sha256(path), "bytes": path.stat().st_size}
    manifest_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    return result


def _m2_execution_policy(physics_card: dict[str, Any], config: BackendConfig, request: dict[str, Any]) -> dict[str, Any]:
    mode = request.get("execution_mode")
    status = request.get("status")
    timeout = request.get("timeout_policy", {})
    allowed = set(request.get("allowed_operations", []))
    required = {"m2_regression", "spin_sums", "heavy_simplification"}
    if _external_photon_momenta(physics_card):
        required.add("polarization_sums")
    base = {
        "execution_mode": mode,
        "request_status": status,
        "required_operations": sorted(required),
        "allowed_operations": sorted(allowed),
        "timeout_policy": timeout,
        "execute": False,
        "path": "script_only",
    }
    if mode == "amplitude_only":
        base["reason"] = "amplitude_only generates compute_m2.wl but does not execute M2"
        return base
    if status != "approved":
        raise NativeBackendError("M2 execution requires an approved ExecutionRequest")
    if timeout.get("kind") != "fixed_seconds" or not timeout.get("seconds"):
        raise NativeBackendError("M2 execution requires a fixed_seconds timeout policy")
    missing = sorted(required - allowed)
    if missing:
        raise NativeBackendError(f"M2 execution request is missing required operation(s): {missing}")
    if mode == "benchmark_regression":
        base.update({"execute": True, "path": "benchmark_regression", "timeout_seconds": timeout["seconds"]})
        return base
    if mode == "production_heavy":
        if "heavy_simplification" not in allowed:
            raise NativeBackendError("production_heavy M2 requires explicit heavy_simplification authorization")
        base.update({"execute": True, "path": "production_heavy", "timeout_seconds": timeout["seconds"]})
        return base
    raise NativeBackendError(f"unsupported M2 execution mode: {mode}")


def _external_photon_momenta(physics_card: dict[str, Any]) -> list[str]:
    legs = sorted(
        physics_card.get("particles", {}).get("incoming", []) + physics_card.get("particles", {}).get("outgoing", []),
        key=lambda leg: leg["slot"],
    )
    return [_wl_symbol(leg["momentum_label"]) for leg in legs if leg.get("particle_id") == "gamma"]


def _fermion_momenta(physics_card: dict[str, Any]) -> list[str]:
    legs = sorted(
        physics_card.get("particles", {}).get("incoming", []) + physics_card.get("particles", {}).get("outgoing", []),
        key=lambda leg: leg["slot"],
    )
    return [_wl_symbol(leg["momentum_label"]) for leg in legs if _charged_fermion_family(leg.get("particle_id", ""))]


def _set_mandelstam_call(incoming_legs: list[dict[str, Any]], outgoing_legs: list[dict[str, Any]], config: BackendConfig) -> str:
    momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs]
    momenta += ["-" + _wl_symbol(leg["momentum_label"]) for leg in outgoing_legs]
    masses = [_particle_mass(leg["particle_id"], config) for leg in incoming_legs + outgoing_legs]
    return f"SetMandelstam[s, t, u, {', '.join(momenta + masses)}]"


def _mandelstam_mass_sum(incoming_legs: list[dict[str, Any]], outgoing_legs: list[dict[str, Any]], config: BackendConfig) -> str:
    terms = []
    for leg in incoming_legs + outgoing_legs:
        mass = _particle_mass(leg["particle_id"], config)
        if mass != "0":
            terms.append(f"({mass})^2")
    return "0" if not terms else " + ".join(terms)


def _initial_spin_average_factor(incoming_legs: list[dict[str, Any]], config: BackendConfig) -> str:
    denominators = [_spin_average_denominator(leg["particle_id"], config) for leg in incoming_legs]
    return "1/(" + "*".join(str(value) for value in denominators) + ")"


def _massless_replacements(legs: list[dict[str, Any]], config: BackendConfig) -> str:
    masses = sorted({_particle_mass(leg["particle_id"], config) for leg in legs if _particle_mass(leg["particle_id"], config) != "0"})
    return ", ".join(f"{mass} -> 0" for mass in masses)


def _polarization_sum_steps(external_photons: list[str]) -> str:
    return "\n".join(
        f"m2AfterPolarization = DoPolarizationSums[m2AfterPolarization, {momentum}, 0];"
        for momentum in external_photons
    ) or "(* no external photon polarization sums required *)"


def _particle_mass(particle_id: str, config: BackendConfig) -> str:
    return config.particle_masses.get(particle_id, _default_particle_mass(particle_id))


def _spin_average_denominator(particle_id: str, config: BackendConfig) -> int:
    return config.particle_spin_average_denominators.get(particle_id, _default_spin_average_denominator(particle_id))


def _default_particle_mass(particle_id: str) -> str:
    if particle_id in {"e-", "e+"}:
        return 'SMP["m_e"]'
    if particle_id in {"mu-", "mu+"}:
        return 'SMP["m_mu"]'
    if particle_id == "gamma":
        return "0"
    return "0"


def _default_external_state_kind(particle_id: str) -> str:
    if particle_id == "gamma":
        return "massless_vector"
    if _charged_fermion_family(particle_id):
        return "dirac_spin_half"
    return "unknown"


def _default_spin_average_denominator(particle_id: str) -> int:
    kind = _default_external_state_kind(particle_id)
    if kind in {"dirac_spin_half", "massless_vector"}:
        return 2
    raise NativeBackendError(f"unsupported spin average metadata for particle: {particle_id}")
