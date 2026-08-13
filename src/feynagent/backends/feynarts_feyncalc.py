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
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


class NativeBackendError(ValueError):
    """Raised when a PhysicsCard cannot be handled by the native backend."""


@dataclass(frozen=True)
class BackendConfig:
    """Configuration for the bounded Day-4 native QED backend."""

    backend_id: str = "feynarts_feyncalc_native"
    model: str = "SM"
    generic_model: str = "Lorentz"
    restrictions: str = "QEDOnly"
    insertion_level: str = "Classes"
    exclude_topologies: tuple[str, ...] = ("Tadpoles", "SelfEnergies", "WFCorrections")


PARTICLE_TO_FEYNARTS = {
    "e-": "F[2, {1}]",
    "e+": "-F[2, {1}]",
    "mu-": "F[2, {2}]",
    "mu+": "-F[2, {2}]",
    "gamma": "V[1]",
}

OUTPUT_FILES = (
    "native_amplitude.wl",
    "stdout.log",
    "stderr.log",
    "native_summary.json",
    "raw_feynarts_amplitude.m",
    "raw_feynarts_amplitude.inputform.txt",
    "feyncalc_amplitude.m",
    "feyncalc_amplitude.inputform.txt",
    "run_manifest.json",
)


def backend_config_from_dict(data: dict[str, Any]) -> BackendConfig:
    """Build BackendConfig from structured backend configuration YAML."""

    allowed = {"backend_id", "model", "generic_model", "restrictions", "insertion_level", "exclude_topologies"}
    unknown = sorted(set(data) - allowed - {"scope", "notes"})
    if unknown:
        raise NativeBackendError(f"unknown native backend config key(s): {unknown}")
    return BackendConfig(
        backend_id=data.get("backend_id", BackendConfig.backend_id),
        model=data.get("model", BackendConfig.model),
        generic_model=data.get("generic_model", BackendConfig.generic_model),
        restrictions=data.get("restrictions", BackendConfig.restrictions),
        insertion_level=data.get("insertion_level", BackendConfig.insertion_level),
        exclude_topologies=tuple(data.get("exclude_topologies", BackendConfig.exclude_topologies)),
    )


def validate_native_qed_request(physics_card: dict[str, Any], config: BackendConfig | None = None) -> None:
    """Validate the bounded Day-4 native backend request."""

    config = config or BackendConfig()
    if config.backend_id != "feynarts_feyncalc_native":
        raise NativeBackendError("backend_id must be feynarts_feyncalc_native")
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
    unsupported = [leg.get("particle_id") for leg in incoming + outgoing if leg.get("particle_id") not in PARTICLE_TO_FEYNARTS]
    if unsupported:
        raise NativeBackendError(f"unsupported native QED particle(s): {unsupported}")


def build_native_qed_script(physics_card: dict[str, Any], config: BackendConfig | None = None) -> str:
    """Build a Wolfram script for native FeynArts/FeynCalc amplitude generation."""

    config = config or BackendConfig()
    validate_native_qed_request(physics_card, config)
    incoming = [_map_particle(leg) for leg in sorted(physics_card["particles"]["incoming"], key=lambda leg: leg["slot"])]
    outgoing = [_map_particle(leg) for leg in sorted(physics_card["particles"]["outgoing"], key=lambda leg: leg["slot"])]
    incoming_legs = sorted(physics_card["particles"]["incoming"], key=lambda leg: leg["slot"])
    outgoing_legs = sorted(physics_card["particles"]["outgoing"], key=lambda leg: leg["slot"])
    incoming_momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs]
    outgoing_momenta = [_wl_symbol(leg["momentum_label"]) for leg in outgoing_legs]
    transverse_momenta = [_wl_symbol(leg["momentum_label"]) for leg in incoming_legs + outgoing_legs if leg["particle_id"] == "gamma"]
    create_call = _create_topologies_call(config)
    insert_call = _insert_fields_call(config, incoming, outgoing)
    process_id = physics_card.get("process_id", "process:unknown")
    transverse_option = ""
    if transverse_momenta:
        transverse_option = f",\n  TransversePolarizationVectors -> {{{', '.join(transverse_momenta)}}}"

    return f'''(* FeynAgent Day-4 native FeynArts/FeynCalc QED backend. *)
(* source_process_id = "{process_id}" *)
(* This script uses native FeynArts/FeynCalc amplitudes only. *)

$LoadFeynArts = True;
Quiet[Get["FeynCalc`"], FrontEndObject::notavail];

outputDir = DirectoryName[$InputFileName];
rawAmpPath = FileNameJoin[{{outputDir, "raw_feynarts_amplitude.m"}}];
rawTextPath = FileNameJoin[{{outputDir, "raw_feynarts_amplitude.inputform.txt"}}];
fcAmpPath = FileNameJoin[{{outputDir, "feyncalc_amplitude.m"}}];
fcTextPath = FileNameJoin[{{outputDir, "feyncalc_amplitude.inputform.txt"}}];
summaryPath = FileNameJoin[{{outputDir, "native_summary.json"}}];

createTopologiesCall = "{_escape_wl_string(create_call)}";
insertFieldsCall = "{_escape_wl_string(insert_call)}";

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

rawAmplitude = CreateFeynAmp[inserted, PreFactor -> 1];
Put[rawAmplitude, rawAmpPath];
Export[rawTextPath, ToString[rawAmplitude, InputForm], "Text"];

feyncalcAmplitude = FCFAConvert[
  rawAmplitude,
  IncomingMomenta -> {{{', '.join(incoming_momenta)}}},
  OutgoingMomenta -> {{{', '.join(outgoing_momenta)}}},
  LoopMomenta -> {{}},
  UndoChiralSplittings -> True,
  ChangeDimension -> 4{transverse_option},
  List -> True,
  SMP -> True
];
Put[feyncalcAmplitude, fcAmpPath];
Export[fcTextPath, ToString[feyncalcAmplitude, InputForm], "Text"];

summary = <|
  "backend_id" -> "{config.backend_id}",
  "process_id" -> "{process_id}",
  "wolfram_version" -> $Version,
  "feynarts_version" -> ToString[Quiet[Check[FeynArts`$FeynArtsVersion, "unknown"]], InputForm],
  "feyncalc_version" -> ToString[Quiet[Check[FeynCalc`$FeynCalcVersion, "unknown"]], InputForm],
  "create_topologies_call" -> createTopologiesCall,
  "insert_fields_call" -> insertFieldsCall,
  "diagram_count" -> diagramCount,
  "model" -> "{config.model}",
  "generic_model" -> "{config.generic_model}",
  "restrictions" -> "{config.restrictions}",
  "insertion_level" -> "{config.insertion_level}"
|>;
Export[summaryPath, summary, "JSON"];
Print["RAW_FEYNARTS_AMPLITUDE_SAVED=" <> rawAmpPath];
Print["FCFA_CONVERT_AMPLITUDE_SAVED=" <> fcAmpPath];
Print["FEYNAGENT_NATIVE_BACKEND_END"];
Quit[0];
'''


def run_native_qed_backend(
    physics_card: dict[str, Any],
    output_dir: str | Path,
    config: BackendConfig | None = None,
    *,
    wolframscript: str = "wolframscript",
    timeout_seconds: int = 60,
) -> dict[str, Any]:
    """Run the generated native Wolfram script and write a manifest."""

    config = config or BackendConfig()
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
        [wolframscript, "-script", str(script_path)],
        cwd=output_path,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    completed_at = datetime.now().astimezone().isoformat()
    stdout_path.write_text(completed.stdout, encoding="utf-8", newline="\n")
    stderr_path.write_text(completed.stderr, encoding="utf-8", newline="\n")

    summary_path = output_path / "native_summary.json"
    summary: dict[str, Any] = {}
    if summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    manifest = {
        "backend_id": config.backend_id,
        "process_id": physics_card.get("process_id"),
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": completed.returncode,
        "script_path": str(script_path.name),
        "stdout_path": str(stdout_path.name),
        "stderr_path": str(stderr_path.name),
        "summary_path": str(summary_path.name) if summary_path.exists() else None,
        "native_summary": summary,
        "outputs": {},
        "notes": "Native FeynArts/FeynCalc amplitude generation only; no M2 calculation performed.",
    }
    for name in OUTPUT_FILES:
        path = output_path / name
        if path.exists():
            manifest["outputs"][name] = {"sha256": _sha256(path), "bytes": path.stat().st_size}
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    return manifest


def _map_particle(leg: dict[str, Any]) -> str:
    particle_id = leg.get("particle_id")
    if particle_id not in PARTICLE_TO_FEYNARTS:
        raise NativeBackendError(f"unsupported native QED particle: {particle_id}")
    return PARTICLE_TO_FEYNARTS[particle_id]


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


def _escape_wl_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
