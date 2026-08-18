"""External custom knowledge mapping and lock verification helpers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


AVAILABLE = "AVAILABLE"
MISSING_KNOWLEDGE = "MISSING_KNOWLEDGE"
CONFLICT_REQUIRES_REVIEW = "CONFLICT_REQUIRES_REVIEW"
STANDARD_NATIVE = "standard_native"
CUSTOM_AUDITED = "custom_audited"
UNSUPPORTED_REQUIRES_REVIEW = "unsupported_requires_review"

DEFAULT_MAPPING_PATH = Path(".feynagent") / "knowledge_roots.yaml"
DEFAULT_BENCHMARK_ROOT = Path("benchmarks")
DEFAULT_B04_MANIFEST = DEFAULT_BENCHMARK_ROOT / "B04_phi_phi_to_hh" / "knowledge_manifest.yaml"
STANDARD_QED_PARTICLES = {"e-", "e+", "mu-", "mu+", "gamma"}


@dataclass(frozen=True)
class KnowledgeVerification:
    model_id: str
    status: str
    readiness: str | None = None
    process_id: str | None = None
    checked_hashes: int = 0
    issues: tuple[str, ...] = ()

    def as_capability(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"model_id": self.model_id, "status": self.status}
        if self.readiness:
            payload["readiness"] = self.readiness
        if self.process_id:
            payload["process_id"] = self.process_id
        if self.checked_hashes:
            payload["checked_hashes"] = self.checked_hashes
        if self.issues:
            payload["issues"] = list(self.issues)
        return payload


def verify_knowledge_lock(
    *,
    model_id: str,
    benchmark_manifest_path: Path = DEFAULT_B04_MANIFEST,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
) -> KnowledgeVerification:
    """Compare the local external package against the registered benchmark lock."""

    try:
        manifest = _load_yaml(benchmark_manifest_path)
    except OSError as exc:
        return KnowledgeVerification(model_id=model_id, status=MISSING_KNOWLEDGE, issues=(f"benchmark manifest missing: {exc}",))

    manifest_model = manifest.get("model_id")
    if manifest_model != model_id:
        return KnowledgeVerification(
            model_id=model_id,
            status=CONFLICT_REQUIRES_REVIEW,
            issues=(f"manifest model_id {manifest_model!r} does not match requested {model_id!r}",),
        )

    root = registered_root_for_model(model_id, mapping_path=mapping_path)
    if root is None:
        return KnowledgeVerification(
            model_id=model_id,
            status=MISSING_KNOWLEDGE,
            readiness=manifest.get("readiness"),
            process_id=manifest.get("process_id"),
            issues=("local knowledge root is not registered",),
        )
    if not root.exists():
        return KnowledgeVerification(
            model_id=model_id,
            status=MISSING_KNOWLEDGE,
            readiness=manifest.get("readiness"),
            process_id=manifest.get("process_id"),
            issues=("registered local knowledge root does not exist",),
        )

    lock_path = root / "KNOWLEDGE_LOCK.json"
    if not lock_path.exists():
        return KnowledgeVerification(
            model_id=model_id,
            status=MISSING_KNOWLEDGE,
            readiness=manifest.get("readiness"),
            process_id=manifest.get("process_id"),
            issues=("registered local knowledge root has no KNOWLEDGE_LOCK.json",),
        )

    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return KnowledgeVerification(model_id=model_id, status=CONFLICT_REQUIRES_REVIEW, issues=(f"invalid KNOWLEDGE_LOCK.json: {exc}",))

    issues: list[str] = []
    for key in ("readiness", "model_id", "process_id", "convention_id"):
        expected = manifest.get(key)
        actual = lock.get(key)
        if expected is not None and actual != expected:
            issues.append(f"lock {key} {actual!r} does not match registered {expected!r}")

    if lock.get("unresolved_conflicts"):
        issues.append("lock reports unresolved conflicts")

    expected_groups = manifest.get("registered_lock", {})
    checked = 0
    for group_name in ("canonical_input_hashes", "locked_source_gold_file_sha256"):
        expected_hashes = expected_groups.get(group_name, {})
        actual_hashes = lock.get(group_name, {})
        if not isinstance(expected_hashes, dict):
            issues.append(f"registered {group_name} is not a mapping")
            continue
        if not isinstance(actual_hashes, dict):
            issues.append(f"lock {group_name} is not a mapping")
            continue
        for relative_path, expected_sha in sorted(expected_hashes.items()):
            checked += 1
            lock_sha = actual_hashes.get(relative_path)
            if lock_sha != expected_sha:
                issues.append(f"lock hash mismatch for {relative_path}")
            file_path = root / relative_path
            if not file_path.exists():
                issues.append(f"external file missing for {relative_path}")
                continue
            actual_sha = sha256_file(file_path)
            if actual_sha != expected_sha:
                issues.append(f"current hash mismatch for {relative_path}")

    status = CONFLICT_REQUIRES_REVIEW if issues else AVAILABLE
    return KnowledgeVerification(
        model_id=model_id,
        status=status,
        readiness=manifest.get("readiness"),
        process_id=manifest.get("process_id"),
        checked_hashes=checked,
        issues=tuple(issues),
    )


def custom_model_statuses(
    *,
    benchmark_root: Path = DEFAULT_BENCHMARK_ROOT,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
) -> list[KnowledgeVerification]:
    statuses = []
    for manifest_path in discover_knowledge_manifests(benchmark_root):
        try:
            manifest = _load_yaml(manifest_path)
        except OSError:
            continue
        model_id = manifest.get("model_id")
        if isinstance(model_id, str) and model_id:
            statuses.append(verify_knowledge_lock(model_id=model_id, benchmark_manifest_path=manifest_path, mapping_path=mapping_path))
    return statuses


def discover_knowledge_manifests(benchmark_root: Path = DEFAULT_BENCHMARK_ROOT) -> list[Path]:
    if not benchmark_root.exists():
        return []
    return sorted(path for path in benchmark_root.glob("B*/knowledge_manifest.yaml") if path.is_file())


def discover_custom_model_ids(benchmark_root: Path = DEFAULT_BENCHMARK_ROOT) -> set[str]:
    model_ids: set[str] = set()
    for manifest_path in discover_knowledge_manifests(benchmark_root):
        try:
            manifest = _load_yaml(manifest_path)
        except OSError:
            continue
        model_id = manifest.get("model_id")
        if isinstance(model_id, str) and model_id:
            model_ids.add(model_id)
    return model_ids


def classify_physics_card(physics_card: dict[str, Any], *, custom_model_ids: set[str] | None = None) -> str:
    particles = _particle_ids(physics_card)
    if (
        physics_card.get("model_id") == "sm_qed"
        and physics_card.get("sector") == "qed"
        and physics_card.get("process_type") == "scattering_2_to_2"
        and particles.issubset(STANDARD_QED_PARTICLES)
        and physics_card.get("perturbative_order", {}).get("loop_order") == 0
    ):
        return STANDARD_NATIVE
    if custom_model_ids and physics_card.get("model_id") in custom_model_ids:
        return CUSTOM_AUDITED
    return UNSUPPORTED_REQUIRES_REVIEW


def registered_root_for_model(model_id: str, *, mapping_path: Path = DEFAULT_MAPPING_PATH) -> Path | None:
    try:
        mapping = _load_yaml(mapping_path)
    except OSError:
        return None
    for entry in _mapping_entries(mapping):
        if entry.get("model_id") == model_id and entry.get("root"):
            return Path(str(entry["root"])).expanduser()
    return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _mapping_entries(mapping: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("roots", "knowledge_roots", "models"):
        entries = mapping.get(key)
        if isinstance(entries, list):
            return [entry for entry in entries if isinstance(entry, dict)]
    return []


def _particle_ids(physics_card: dict[str, Any]) -> set[str]:
    particles: set[str] = set()
    for state in ("incoming", "outgoing"):
        for item in physics_card.get("particles", {}).get(state, []):
            particle_id = item.get("particle_id")
            if isinstance(particle_id, str):
                particles.add(particle_id)
    return particles


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:  # pragma: no cover
        raise OSError("PyYAML is not installed")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise OSError(f"expected mapping in {path}")
    return data
