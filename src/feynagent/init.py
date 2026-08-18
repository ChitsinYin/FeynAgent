"""Local initialization and capability probing for FeynAgent."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


LOCAL_DIR = Path(".feynagent")
ENVIRONMENT_YAML = LOCAL_DIR / "environment.yaml"
CAPABILITY_REPORT_JSON = LOCAL_DIR / "capability_report.json"
REFERENCE_INDEX_JSON = LOCAL_DIR / "reference_index.json"
SUPPORTED_POLICY = {
    "wolfram": "Record detected version. Newer compatible Wolfram versions are warnings only unless the probe fails.",
    "feyncalc": "Tested with FeynCalc 10.1.x. Compatible newer versions are accepted with recorded provenance.",
    "feynarts": "FeynArts must be loaded through FeynCalc using $LoadAddOns = {\"FeynArts\"}; << FeynCalc`.",
    "latex": "LaTeX is optional for non-rendering workflows; missing LaTeX is a WARNING, not a FAIL.",
}


@dataclass(frozen=True)
class ProbeResult:
    status: str
    environment: dict[str, Any]
    capabilities: dict[str, Any]
    reference_index: dict[str, Any]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m feynagent")
    sub = parser.add_subparsers(dest="command", required=True)
    init_parser = sub.add_parser("init", help="Probe local Wolfram/FeynCalc/FeynArts/LaTeX capabilities")
    _add_probe_options(init_parser)
    doctor_parser = sub.add_parser("doctor", help="Re-probe local capabilities and print PASS/WARNING/FAIL")
    _add_probe_options(doctor_parser)
    run_parser = sub.add_parser("run", help="Run the deterministic native standard-QED pipeline")
    run_parser.add_argument("--physics-card", required=True, help="PhysicsCard YAML/JSON file")
    run_parser.add_argument("--backend-profile", required=True, help="BackendProfile YAML/JSON file")
    run_parser.add_argument("--execution-request", required=True, help="ExecutionRequest YAML/JSON file")
    run_parser.add_argument("--run-root", default="runs", help="Run artifact root directory")
    args = parser.parse_args(argv)
    if args.command == "init":
        result = run_init(args)
        print(_summary_text(result, include_files=True))
        return 0 if result.status in {"PASS", "WARNING"} else 1
    if args.command == "doctor":
        result = probe_environment(args)
        print(_doctor_text(result))
        return 0 if result.status in {"PASS", "WARNING"} else 1
    if args.command == "run":
        from .runner import run_cli

        return run_cli(args)
    parser.error(f"unknown command: {args.command}")
    return 2


def _add_probe_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--wolframscript", help="Explicit wolframscript executable path")
    parser.add_argument("--feyncalc-dir", help="Explicit FeynCalc directory hint; no installation is attempted")
    parser.add_argument("--timeout", type=int, default=60, help="Probe timeout in seconds")


def run_init(args: argparse.Namespace) -> ProbeResult:
    result = probe_environment(args)
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    _write_yaml(ENVIRONMENT_YAML, result.environment)
    CAPABILITY_REPORT_JSON.write_text(json.dumps(result.capabilities, indent=2, sort_keys=True), encoding="utf-8")
    REFERENCE_INDEX_JSON.write_text(json.dumps(result.reference_index, indent=2, sort_keys=True), encoding="utf-8")
    return result


def probe_environment(args: argparse.Namespace) -> ProbeResult:
    detected_at = datetime.now().astimezone().isoformat()
    wolframscript = _detect_wolframscript(args.wolframscript)
    latex = _detect_latex_engine()
    wolfram_probe = _probe_wolfram(wolframscript, args.timeout, args.feyncalc_dir)
    reference_index = _build_reference_index(wolfram_probe)
    checks = _capability_checks(wolframscript, wolfram_probe, latex)
    status = _overall_status(checks)
    custom_models = _custom_model_capabilities()
    environment = {
        "schema_version": "0.1.0",
        "generated_at": detected_at,
        "wolframscript": wolframscript,
        "feyncalc_dir_hint": args.feyncalc_dir,
        "wolfram": wolfram_probe.get("wolfram", {}),
        "feyncalc": wolfram_probe.get("feyncalc", {}),
        "feynarts": wolfram_probe.get("feynarts", {}),
        "latex": latex,
        "supported_version_policy": SUPPORTED_POLICY,
        "notes": "Machine-local FeynAgent initialization state. Do not commit .feynagent/.",
    }
    capabilities = {
        "schema_version": "0.1.0",
        "generated_at": detected_at,
        "status": status,
        "checks": checks,
        "wolfram_probe": wolfram_probe,
        "latex": latex,
        "native_qed_tree_capability": checks["native_qed_tree_capability"],
        "custom_models": custom_models,
    }
    return ProbeResult(status=status, environment=environment, capabilities=capabilities, reference_index=reference_index)


def _detect_wolframscript(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    return shutil.which("wolframscript")


def _probe_wolfram(wolframscript: str | None, timeout: int, feyncalc_dir: str | None) -> dict[str, Any]:
    if not wolframscript:
        return {"status": "FAIL", "error": "wolframscript not found on PATH and --wolframscript not provided"}
    script = _wolfram_probe_script(feyncalc_dir)
    with tempfile.TemporaryDirectory(prefix="feynagent_probe_") as tmp:
        script_path = Path(tmp) / "probe.wl"
        script_path.write_text(script, encoding="utf-8")
        try:
            completed = subprocess.run(
                [wolframscript, "-script", str(script_path)],
                text=True,
                capture_output=True,
                timeout=timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"status": "FAIL", "error": str(exc), "wolframscript": wolframscript}
    parsed = _parse_probe_stdout(completed.stdout)
    parsed["status"] = "PASS" if completed.returncode == 0 and parsed.get("feyncalc", {}).get("loaded") else "FAIL"
    parsed["exit_code"] = completed.returncode
    parsed["wolframscript"] = wolframscript
    parsed["stderr"] = completed.stderr.strip()
    return parsed


def _wolfram_probe_script(feyncalc_dir: str | None) -> str:
    dir_hint = ""
    if feyncalc_dir:
        escaped = feyncalc_dir.replace("\\", "\\\\").replace('"', '\\"')
        dir_hint = f'AppendTo[$Path, "{escaped}"];\n'
    return f"""{dir_hint}$LoadAddOns = {{"FeynArts"}};
Quiet[Get["FeynCalc`"], FrontEndObject::notavail];
faDir = Quiet[Check[FeynArts`$FeynArtsDirectory, "unknown"]];
If[!StringQ[faDir] || faDir === "unknown", faDir = FileNameJoin[{{FeynCalc`$FeynCalcDirectory, "FeynArts"}}]];
examplesRoot = FileNameJoin[{{FeynCalc`$FeynCalcDirectory, "Examples"}}];
modelsRoot = FileNameJoin[{{faDir, "Models"}}];
faLoaded = TrueQ[ValueQ[FeynArts`$FeynArtsVersion]];
json = <|
  "wolfram" -> <|"version" -> $Version|>,
  "feyncalc" -> <|
    "loaded" -> TrueQ[ValueQ[FeynCalc`$FeynCalcVersion]],
    "version" -> Quiet[Check[FeynCalc`$FeynCalcVersion, "unknown"]],
    "directory" -> Quiet[Check[FeynCalc`$FeynCalcDirectory, "unknown"]]
  |>,
  "feynarts" -> <|
    "loaded" -> faLoaded,
    "version" -> Quiet[Check[FeynArts`$FeynArtsVersion, "unknown"]],
    "directory" -> faDir,
    "addon_load_requested" -> True,
    "loaded_via_feyncalc_addon" -> faLoaded
  |>,
  "paths" -> <|
    "feyncalc_examples_root" -> examplesRoot,
    "feynarts_models_root" -> modelsRoot
  |>
|>;
Print["FEYNAGENT_PROBE_JSON_BEGIN"];
Print[ExportString[json, "RawJSON"]];
Print["FEYNAGENT_PROBE_JSON_END"];
Quit[0];
"""


def _parse_probe_stdout(stdout: str) -> dict[str, Any]:
    begin = "FEYNAGENT_PROBE_JSON_BEGIN"
    end = "FEYNAGENT_PROBE_JSON_END"
    if begin not in stdout or end not in stdout:
        return {"status": "FAIL", "error": "probe JSON markers not found", "stdout_excerpt": stdout[-1000:]}
    payload = stdout.split(begin, 1)[1].split(end, 1)[0].strip()
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return {"status": "FAIL", "error": f"invalid probe JSON: {exc}", "stdout_excerpt": payload[:1000]}
    return data


def _detect_latex_engine() -> dict[str, Any]:
    for engine in ("lualatex", "pdflatex", "xelatex"):
        path = shutil.which(engine)
        if not path:
            continue
        version = "unknown"
        try:
            completed = subprocess.run([path, "--version"], text=True, capture_output=True, timeout=10)
            version = (completed.stdout or completed.stderr).splitlines()[0] if (completed.stdout or completed.stderr) else "unknown"
        except (OSError, subprocess.TimeoutExpired):
            pass
        return {"status": "PASS", "engine": engine, "path": path, "version": version}
    return {"status": "WARNING", "engine": None, "path": None, "version": None, "notes": "No LaTeX engine found on PATH"}


def _capability_checks(wolframscript: str | None, probe: dict[str, Any], latex: dict[str, Any]) -> dict[str, dict[str, Any]]:
    wolfram_ok = bool(wolframscript) and probe.get("status") == "PASS"
    feyncalc = probe.get("feyncalc", {})
    feynarts = probe.get("feynarts", {})
    feyncalc_ok = wolfram_ok and bool(feyncalc.get("loaded"))
    feynarts_ok = feyncalc_ok and bool(feynarts.get("loaded")) and bool(feynarts.get("loaded_via_feyncalc_addon"))
    native_ok = feynarts_ok and bool(probe.get("paths", {}).get("feynarts_models_root"))
    return {
        "wolfram": {"status": "PASS" if wolfram_ok else "FAIL", "details": probe.get("wolfram", probe.get("error"))},
        "feyncalc": {"status": "PASS" if feyncalc_ok else "FAIL", "details": feyncalc or probe.get("error")},
        "feynarts": {"status": "PASS" if feynarts_ok else "FAIL", "details": feynarts or probe.get("error")},
        "native_qed_tree_capability": {"status": "PASS" if native_ok else "FAIL", "details": "FeynArts loaded through FeynCalc add-on path" if native_ok else "Native QED tree backend requires Wolfram + FeynCalc + FeynArts"},
        "latex": {"status": latex.get("status", "WARNING"), "details": latex},
    }


def _custom_model_capabilities() -> list[dict[str, Any]]:
    try:
        from .custom_knowledge import custom_model_statuses
    except Exception as exc:  # pragma: no cover
        return [{"model_id": "unknown", "status": "CONFLICT_REQUIRES_REVIEW", "issues": [str(exc)]}]
    return [status.as_capability() for status in custom_model_statuses()]


def _overall_status(checks: dict[str, dict[str, Any]]) -> str:
    statuses = {item["status"] for item in checks.values()}
    if "FAIL" in statuses:
        return "FAIL"
    if "WARNING" in statuses:
        return "WARNING"
    return "PASS"


def _build_reference_index(probe: dict[str, Any]) -> dict[str, Any]:
    paths = probe.get("paths", {})
    root_text = _strip_wl_string(paths.get("feyncalc_examples_root"))
    examples_root = Path(root_text) if root_text and root_text != "unknown" else None
    entries = []
    if examples_root and examples_root.exists():
        for file in sorted(examples_root.rglob("*")):
            if file.is_file() and file.suffix.lower() in {".m", ".md", ".wl", ".nb"}:
                entries.append({
                    "path": str(file),
                    "relative_path": str(file.relative_to(examples_root)).replace("\\", "/"),
                    "sha256": _sha256(file),
                    "bytes": file.stat().st_size,
                    "title": _example_title(file),
                })
    return {
        "schema_version": "0.1.0",
        "generated_at": datetime.now().astimezone().isoformat(),
        "examples_root": str(examples_root) if examples_root else None,
        "entry_count": len(entries),
        "entries": entries,
        "notes": "Metadata/hash/path only; official examples are not copied into the repository.",
    }


def _strip_wl_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    return text


def _example_title(path: Path) -> str | None:
    if path.suffix.lower() not in {".md", ".m", ".wl"}:
        return None
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]:
            stripped = line.strip().strip("(* ").strip("*) ").strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip() or None
            if stripped and not stripped.startswith(("(*", "*)", "$", "<<")):
                return stripped[:160]
    except OSError:
        return None
    return None


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    if yaml is None:
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        return
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _summary_text(result: ProbeResult, *, include_files: bool) -> str:
    lines = [f"FeynAgent init: {result.status}"]
    for key, check in result.capabilities["checks"].items():
        lines.append(f"- {key}: {check['status']}")
    if include_files:
        lines.extend([
            f"wrote {ENVIRONMENT_YAML}",
            f"wrote {CAPABILITY_REPORT_JSON}",
            f"wrote {REFERENCE_INDEX_JSON}",
        ])
    return "\n".join(lines)


def _doctor_text(result: ProbeResult) -> str:
    lines = [f"FeynAgent doctor: {result.status}"]
    for key in ("wolfram", "feyncalc", "feynarts", "native_qed_tree_capability", "latex"):
        check = result.capabilities["checks"][key]
        lines.append(f"{check['status']:7} {key}")
    for custom in result.capabilities.get("custom_models", []):
        lines.append(f"{custom.get('status', 'UNKNOWN'):24} custom_model:{custom.get('model_id', 'unknown')}")
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
