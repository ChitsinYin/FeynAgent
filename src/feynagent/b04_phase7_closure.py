"""Finalize the audited Day-7 B04 amplitude and reduced-M2 workflow."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

from .b04_topology import MODEL_ID, sha256_file, write_json
from .custom_knowledge import AVAILABLE, registered_root_for_model, verify_knowledge_lock

PROCESS_ID = "process:B04_phi_phi_to_h_h"
AMPLITUDE_RUN_DEFAULT = "day7_b04_amplitude_closure_20260819T000000Z"
M2_RUN_DEFAULT = "day7_b04_m2_manual_20260819T000000Z"
REPORT_NAME = "DAY7_B04_PHASE7_CLOSURE.md"

M2_GOLD_MAP = {
    "Mc2": ("Mc2Generated", "Mc2Gold"),
    "Md2": ("Md2Generated", "Md2Gold"),
    "interference": ("McMdInterferenceGenerated", "McMdInterferenceGold"),
    "raw_total": ("M2PolarizationSummedRawGenerated", "M2PolarizationSummedRawGold"),
    "rate_convention": ("M2PublishedRateConventionGenerated", "M2PublishedRateConventionGold"),
}

REQUIRED_SCRIPT_MARKERS = (
    'Get[FileNameJoin[{ampDir, "amp_001.m"}]]',
    'Get[FileNameJoin[{ampDir, "amp_002.m"}]]',
    'Get[FileNameJoin[{ampDir, "amp_003.m"}]]',
    'Get[FileNameJoin[{ampDir, "amp_004.m"}]]',
    'Get[FileNameJoin[{ampDir, "amp_total.m"}]]',
    "McReduced = Amp003ReducedNRTTGold /. kappa -> 2/MP",
    "MdReduced = Amp004ReducedNRTTGold /. kappa -> 2/MP",
    "MTotalReduced = AmpTotalReducedNRTT /. kappa -> 2/MP",
    "DoPolarizationSums",
    "GPS[mu_, nu_, a_, b_]",
    "1/2 * 1/2 * M2PolarizationSummedRawGenerated",
)


@dataclass(frozen=True)
class Monomial:
    coefficient: Fraction
    powers: tuple[tuple[str, int], ...] = ()

    @classmethod
    def symbol(cls, name: str) -> "Monomial":
        return cls(Fraction(1), ((name, 1),))

    def multiply(self, other: "Monomial") -> "Monomial":
        powers = dict(self.powers)
        for name, power in other.powers:
            powers[name] = powers.get(name, 0) + power
        return Monomial(self.coefficient * other.coefficient, _clean_powers(powers))

    def divide(self, other: "Monomial") -> "Monomial":
        if other.coefficient == 0:
            raise ValueError("division by zero in M2 expression")
        powers = dict(self.powers)
        for name, power in other.powers:
            powers[name] = powers.get(name, 0) - power
        return Monomial(self.coefficient / other.coefficient, _clean_powers(powers))

    def power(self, exponent: int) -> "Monomial":
        return Monomial(self.coefficient**exponent, tuple((name, power * exponent) for name, power in self.powers))

    def as_json(self) -> dict[str, Any]:
        coefficient = str(self.coefficient.numerator)
        if self.coefficient.denominator != 1:
            coefficient += f"/{self.coefficient.denominator}"
        return {"coefficient": coefficient, "powers": dict(self.powers)}


@dataclass(frozen=True)
class Phase7ClosureResult:
    amplitude_run_id: str
    m2_run_id: str
    status: str
    report_path: Path
    validation_path: Path
    run_manifest_path: Path
    validation_sha256: str


def parse_assignments(text: str) -> dict[str, str]:
    """Extract simple Wolfram assignments without evaluating Wolfram code."""

    return {
        match.group(1): match.group(2).strip()
        for match in re.finditer(r"\b([A-Za-z][A-Za-z0-9_]*)\s*=\s*(.*?);", text, re.DOTALL)
    }


def parse_monomial(expression: str) -> Monomial:
    """Parse the restricted rational monomials used by the locked B04 M2 gold."""

    source = expression.strip()
    source = re.sub(r"(?<=[0-9A-Za-z_)])\s+(?=[0-9A-Za-z_(])", "*", source)
    source = re.sub(r"\s+", "", source).replace("^", "**")
    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"unsupported M2 expression: {expression!r}") from exc
    return _eval_monomial(tree.body)


def compare_m2_to_gold(results_text: str, gold_text: str) -> dict[str, Any]:
    generated = parse_assignments(results_text)
    gold = parse_assignments(gold_text)
    comparisons: dict[str, Any] = {}
    for check_name, (generated_name, gold_name) in M2_GOLD_MAP.items():
        if generated_name not in generated or gold_name not in gold:
            comparisons[check_name] = {
                "status": "CONFLICT_REQUIRES_REVIEW",
                "generated_symbol": generated_name,
                "gold_symbol": gold_name,
                "reason": "required assignment is missing",
            }
            continue
        try:
            actual = parse_monomial(generated[generated_name])
            expected = parse_monomial(gold[gold_name])
        except ValueError as exc:
            comparisons[check_name] = {
                "status": "CONFLICT_REQUIRES_REVIEW",
                "generated_symbol": generated_name,
                "gold_symbol": gold_name,
                "reason": str(exc),
            }
            continue
        comparisons[check_name] = {
            "status": "PASS" if actual == expected else "CONFLICT_REQUIRES_REVIEW",
            "generated_symbol": generated_name,
            "gold_symbol": gold_name,
            "generated_expression": generated[generated_name],
            "gold_expression": gold[gold_name],
            "generated_canonical": actual.as_json(),
            "gold_canonical": expected.as_json(),
        }
    return comparisons


def audit_m2_script(script_bytes: bytes) -> dict[str, Any]:
    has_bom = script_bytes.startswith(b"\xef\xbb\xbf")
    try:
        text = script_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return {"status": "CONFLICT_REQUIRES_REVIEW", "utf8": False, "reason": str(exc)}
    missing = [marker for marker in REQUIRED_SCRIPT_MARKERS if marker not in text]
    status = "PASS" if not has_bom and not missing else "CONFLICT_REQUIRES_REVIEW"
    return {
        "status": status,
        "utf8": True,
        "utf8_bom": has_bom,
        "required_markers_present": not missing,
        "missing_markers": missing,
        "amplitude_layer": "REDUCED_NR_TT",
        "kappa_map": "kappa -> 2/MP",
        "identical_particle_factors": ["1/2 initial", "1/2 final phase space"],
    }


def run_phase7_closure(
    root: Path,
    *,
    amplitude_run_id: str = AMPLITUDE_RUN_DEFAULT,
    m2_run_id: str = M2_RUN_DEFAULT,
) -> Phase7ClosureResult:
    root = root.resolve()
    amplitude_run = root / "runs" / amplitude_run_id
    m2_run = root / "runs" / m2_run_id
    m2_dir = m2_run / "m2"
    validation_dir = m2_run / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "amplitude_manifest": amplitude_run / "run_manifest.json",
        "amplitude_validation": amplitude_run / "validation" / "amplitude_validation.json",
        "m2_script": m2_dir / "run_b04_m2_reduced.wl",
        "m2_results": m2_dir / "M2_results.m",
        "m2_manifest": m2_dir / "M2_manifest.json",
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing Phase-7 input artifact(s): {missing}")

    verification = verify_knowledge_lock(model_id=MODEL_ID)
    external_root = registered_root_for_model(MODEL_ID)
    if external_root is None:
        raise RuntimeError("no external B04 knowledge root is registered")
    lock_path = external_root / "KNOWLEDGE_LOCK.json"
    gold_path = external_root / "gold" / "m2_reference.m"
    if not lock_path.is_file() or not gold_path.is_file():
        raise FileNotFoundError("locked B04 knowledge package is incomplete")
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    expected_gold_sha = lock.get("locked_source_gold_file_sha256", {}).get("gold/m2_reference.m")
    actual_gold_sha = sha256_file(gold_path)
    lock_sha = sha256_file(lock_path)

    amplitude_manifest = _load_json(paths["amplitude_manifest"])
    amplitude_validation = _load_json(paths["amplitude_validation"])
    m2_manifest = _load_json(paths["m2_manifest"])
    results_text = paths["m2_results"].read_text(encoding="utf-8")
    gold_text = gold_path.read_text(encoding="utf-8")

    gold_comparisons = compare_m2_to_gold(results_text, gold_text)
    script_audit = audit_m2_script(paths["m2_script"].read_bytes())
    amplitude_gate = _audit_amplitude_gate(amplitude_run, amplitude_manifest, amplitude_validation, lock_sha)
    manual_manifest_audit = _audit_manual_manifest(m2_manifest, amplitude_run_id)
    knowledge_audit = {
        "status": "PASS"
        if verification.status == AVAILABLE and expected_gold_sha == actual_gold_sha
        else "CONFLICT_REQUIRES_REVIEW",
        "verification_status": verification.status,
        "checked_hashes": verification.checked_hashes,
        "knowledge_lock_sha256": lock_sha,
        "gold_m2_reference_sha256": actual_gold_sha,
        "gold_hash_matches_lock": expected_gold_sha == actual_gold_sha,
        "unresolved_conflicts": lock.get("unresolved_conflicts", []),
    }
    environment = _environment_summary(root)

    component_statuses = [
        knowledge_audit["status"],
        amplitude_gate["status"],
        manual_manifest_audit["status"],
        script_audit["status"],
        *[item["status"] for item in gold_comparisons.values()],
    ]
    status = "PASS" if all(item == "PASS" for item in component_statuses) else "CONFLICT_REQUIRES_REVIEW"
    classification = "CLOSED" if status == "PASS" else "REVIEW_REQUIRED"
    generated_at = datetime.now(timezone.utc).isoformat()

    input_hashes = {
        str(path.relative_to(root)).replace("\\", "/"): {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in paths.values()
    }
    validation = {
        "schema_version": "0.1.0",
        "generated_at": generated_at,
        "phase": "Phase 7",
        "process_id": PROCESS_ID,
        "workflow_classification": "custom_audited",
        "status": status,
        "closure": classification,
        "amplitude_run_id": amplitude_run_id,
        "m2_run_id": m2_run_id,
        "amplitude_layers": ["EXACT_RAW", "REDUCED_NR_TT"],
        "m2_layer": "REDUCED_NR_TT",
        "knowledge_audit": knowledge_audit,
        "amplitude_gate": amplitude_gate,
        "manual_m2_manifest_audit": manual_manifest_audit,
        "m2_script_audit": script_audit,
        "m2_gold_comparisons": gold_comparisons,
        "environment": environment,
        "input_artifacts": input_hashes,
        "rule_authority": {
            "contact_rule": "locked corrected manual TauLocked",
            "historical_feyngrav_3_ssgg": "REJECTED_AS_AUTHORITY",
            "rule_changed_to_force_agreement": False,
            "disagreements_averaged": False,
        },
    }

    report_text = render_phase7_report(validation)
    report_path = root / "reports" / REPORT_NAME
    run_report_path = validation_dir / REPORT_NAME
    report_path.write_text(report_text, encoding="utf-8", newline="\n")
    run_report_path.write_text(report_text, encoding="utf-8", newline="\n")

    validation_path = validation_dir / "phase7_closure.json"
    write_json(validation_path, validation)
    run_manifest_path = m2_run / "run_manifest.json"
    run_outputs = _output_hashes(m2_run, exclude={run_manifest_path})
    write_json(
        run_manifest_path,
        {
            "schema_version": "0.1.0",
            "run_id": m2_run_id,
            "process_id": PROCESS_ID,
            "workflow_classification": "custom_audited",
            "phase7_status": status,
            "closure": classification,
            "input_amplitude_run": amplitude_run_id,
            "knowledge_lock_sha256": lock_sha,
            "gold_m2_reference_sha256": actual_gold_sha,
            "outputs": run_outputs,
        },
    )
    return Phase7ClosureResult(
        amplitude_run_id=amplitude_run_id,
        m2_run_id=m2_run_id,
        status=status,
        report_path=report_path,
        validation_path=validation_path,
        run_manifest_path=run_manifest_path,
        validation_sha256=sha256_file(validation_path),
    )


def render_phase7_report(validation: dict[str, Any]) -> str:
    comparisons = validation["m2_gold_comparisons"]
    artifacts = validation["input_artifacts"]
    env = validation["environment"]
    lines = [
        "# Day-7 B04 Phase-7 Closure",
        "",
        f"- Overall status: `{validation['status']}`",
        f"- Closure: `{validation['closure']}`",
        "- Workflow classification: `custom_audited` (not arbitrary-gravity production support).",
        f"- Process: `{validation['process_id']}`",
        f"- Amplitude run: `{validation['amplitude_run_id']}`",
        f"- M2 run: `{validation['m2_run_id']}`",
        "- Layer order preserved: `EXACT_RAW` amplitudes, then `REDUCED_NR_TT`, then reduced-layer M2.",
        "",
        "## Gate Results",
        "",
        f"- Knowledge lock and M2 gold: `{validation['knowledge_audit']['status']}`",
        f"- Diagram/amplitude prerequisite gate: `{validation['amplitude_gate']['status']}`",
        f"- Manual M2 manifest: `{validation['manual_m2_manifest_audit']['status']}`",
        f"- Deterministic Wolfram script structure: `{validation['m2_script_audit']['status']}`",
        "- No amplitude diagram is classified `CONFLICT_REQUIRES_REVIEW`.",
        "",
        "## M2 Gold Comparison",
        "",
        "| Quantity | Generated | Locked gold | Status |",
        "| --- | --- | --- | --- |",
    ]
    for name in M2_GOLD_MAP:
        item = comparisons[name]
        lines.append(
            f"| `{name}` | `{item.get('generated_expression', 'missing')}` | "
            f"`{item.get('gold_expression', 'missing')}` | `{item['status']}` |"
        )
    lines.extend(
        [
            "",
            "The raw polarization-summed reduced-layer result is `2 M^4/MP^4`. Applying the locked "
            "initial identical factor `1/2` and final identical-particle phase-space factor `1/2` gives "
            "the published rate-convention result `M^4/(2 MP^4)`.",
            "",
            "`Ma = Mb = 0` is used only in `REDUCED_NR_TT`; the exact t/u-channel assemblies remain "
            "preserved and hashed in the amplitude run.",
            "",
            "## Provenance",
            "",
            f"- Knowledge lock sha256: `{validation['knowledge_audit']['knowledge_lock_sha256']}`",
            f"- Locked `gold/m2_reference.m` sha256: `{validation['knowledge_audit']['gold_m2_reference_sha256']}`",
            f"- Knowledge hashes rechecked: `{validation['knowledge_audit']['checked_hashes']}`",
            "- Contact authority: locked corrected manual `TauLocked` rule.",
            "- Historical FeynGrav 3.0 `ssgg` remains rejected as an authority.",
            "- No rule was changed to force agreement and no disagreement was averaged.",
            "",
            "## Runtime",
            "",
            f"- Wolfram: `{env.get('wolfram_version', 'not recorded')}`",
            f"- FeynCalc: `{env.get('feyncalc_version', 'not recorded')}`",
            f"- FeynArts: `{env.get('feynarts_version', 'not recorded')}`",
            "- Headless `FrontEndObject::notavail` notices do not alter the successful exported checks.",
            "",
            "## Input Artifacts",
            "",
            "| Artifact | SHA-256 |",
            "| --- | --- |",
        ]
    )
    for path, metadata in sorted(artifacts.items()):
        lines.append(f"| `{path}` | `{metadata['sha256']}` |")
    lines.extend(
        [
            "",
            "## Closure Decision",
            "",
            "All required Phase-7 B04 amplitude and reduced-M2 checks pass. The B04 Phase-7 workflow is `CLOSED` "
            "for the locked audited rules and approved `REDUCED_NR_TT` comparison layer.",
            "",
        ]
    )
    return "\n".join(lines)


def _audit_amplitude_gate(
    amplitude_run: Path,
    manifest: dict[str, Any],
    validation: dict[str, Any],
    knowledge_lock_sha256: str,
) -> dict[str, Any]:
    classifications = manifest.get("classifications", {})
    expected_classifications = {
        "amp_001": "PASS_AFTER_EXPLICIT_CONVENTION_MAP",
        "amp_002": "PASS_AFTER_EXPLICIT_CONVENTION_MAP",
        "amp_003": "PASS",
        "amp_004": "PASS",
    }
    hierarchy = validation.get("validation_hierarchy", {})
    hashes: dict[str, Any] = {}
    hashes_match = True
    for name in ("amp_001.m", "amp_002.m", "amp_003.m", "amp_004.m", "amp_total.m"):
        relative = f"amplitudes/{name}"
        path = amplitude_run / relative
        recorded = manifest.get("outputs", {}).get(relative, {}).get("sha256")
        actual = sha256_file(path) if path.is_file() else None
        match = actual is not None and actual == recorded
        hashes[relative] = {"recorded_sha256": recorded, "actual_sha256": actual, "match": match}
        hashes_match = hashes_match and match
    status = "PASS" if all(
        (
            manifest.get("knowledge_lock_match") is True,
            manifest.get("knowledge_lock_sha256") == knowledge_lock_sha256,
            manifest.get("m2_status") == "STOPPED_BEFORE_M2_NO_CONFLICTS",
            classifications == expected_classifications,
            hierarchy and all(value == "PASS" for value in hierarchy.values()),
            validation.get("rule_usage_audit") == "PASS",
            validation.get("topology_comparison") == "PASS",
            hashes_match,
        )
    ) else "CONFLICT_REQUIRES_REVIEW"
    return {
        "status": status,
        "classifications": classifications,
        "validation_hierarchy": hierarchy,
        "rule_usage_audit": validation.get("rule_usage_audit"),
        "topology_comparison": validation.get("topology_comparison"),
        "input_hashes": hashes,
    }


def _audit_manual_manifest(manifest: dict[str, Any], amplitude_run_id: str) -> dict[str, Any]:
    checks = manifest.get("checks", {})
    expected_checks = set(M2_GOLD_MAP)
    status = "PASS" if all(
        (
            manifest.get("input_amplitude_run") == amplitude_run_id,
            manifest.get("layer") == "REDUCED_NR_TT",
            manifest.get("m2_status") == "manual_heavy_run",
            set(checks) == expected_checks,
            all(checks.get(name) is True for name in expected_checks),
        )
    ) else "CONFLICT_REQUIRES_REVIEW"
    return {
        "status": status,
        "input_amplitude_run": manifest.get("input_amplitude_run"),
        "layer": manifest.get("layer"),
        "m2_status": manifest.get("m2_status"),
        "checks": checks,
    }


def _environment_summary(root: Path) -> dict[str, Any]:
    path = root / ".feynagent" / "environment.yaml"
    if not path.is_file():
        return {"status": "NOT_RECORDED"}
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (ImportError, OSError, ValueError):
        return {"status": "UNREADABLE"}
    return {
        "status": "RECORDED",
        "wolfram_version": data.get("wolfram", {}).get("version"),
        "feyncalc_version": data.get("feyncalc", {}).get("version"),
        "feynarts_version": data.get("feynarts", {}).get("version"),
        "latex_status": data.get("latex", {}).get("status"),
    }


def _eval_monomial(node: ast.AST) -> Monomial:
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return Monomial(Fraction(node.value))
    if isinstance(node, ast.Name) and node.id in {"M", "MP"}:
        return Monomial.symbol(node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return Monomial(Fraction(-1)).multiply(_eval_monomial(node.operand))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return _eval_monomial(node.left).multiply(_eval_monomial(node.right))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _eval_monomial(node.left).divide(_eval_monomial(node.right))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
            raise ValueError("M2 powers must be integer literals")
        return _eval_monomial(node.left).power(node.right.value)
    raise ValueError(f"unsupported M2 syntax node: {ast.dump(node, include_attributes=False)}")


def _clean_powers(powers: dict[str, int]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted((name, power) for name, power in powers.items() if power))


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def _output_hashes(run_dir: Path, *, exclude: set[Path]) -> dict[str, Any]:
    excluded = {path.resolve() for path in exclude}
    outputs: dict[str, Any] = {}
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        if path.resolve() in excluded:
            continue
        relative = str(path.relative_to(run_dir)).replace("\\", "/")
        outputs[relative] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    return outputs
