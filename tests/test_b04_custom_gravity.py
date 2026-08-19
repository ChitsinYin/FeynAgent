import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.custom_knowledge import (
    AVAILABLE,
    CONFLICT_REQUIRES_REVIEW,
    CUSTOM_AUDITED,
    MISSING_KNOWLEDGE,
    STANDARD_NATIVE,
    classify_physics_card,
    discover_custom_model_ids,
    verify_knowledge_lock,
)

try:
    import jsonschema
    import yaml
except ImportError:  # pragma: no cover
    jsonschema = None
    yaml = None


B04 = ROOT / "benchmarks" / "B04_phi_phi_to_hh"


class B04CustomGravityRegistrationTests(unittest.TestCase):
    def setUp(self):
        if yaml is None or jsonschema is None:
            raise unittest.SkipTest("PyYAML/jsonschema are required")

    def test_b04_physics_card_validates(self):
        card = _load_yaml(B04 / "physics_card.yaml")
        schema = json.loads((ROOT / "schemas" / "physics_card.schema.json").read_text(encoding="utf-8"))
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        errors = sorted(validator_cls(schema).iter_errors(card), key=lambda error: list(error.path))
        self.assertEqual(errors, [])
        self.assertEqual(card["model_id"], "reheating_scalar_gravity_v1")
        self.assertEqual(card["process_id"], "process:B04_phi_phi_to_h_h")
        self.assertEqual(card["approval"]["amplitude_generation"]["status"], "not_requested")
        self.assertEqual(card["approval"]["heavy_calculation"]["status"], "not_requested")

    def test_no_committed_absolute_external_path_or_private_payloads(self):
        blocked_tokens = [
            "E:" + "\\",
            "FeynAgent" + "_external" + "_knowledge",
            "_external" + "_knowledge",
            "source_material" + "\\",
            "gold" + "\\",
        ]
        for path in list(B04.rglob("*")) + [ROOT / "src" / "feynagent" / "custom_knowledge.py", ROOT / "scripts" / "verify_knowledge_lock.py"]:
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            self.assertNotIn(path.suffix.lower(), {".pdf", ".nb", ".wl", ".m"}, rel)
            text = path.read_text(encoding="utf-8")
            for token in blocked_tokens:
                self.assertNotIn(token, text, f"{rel} contains {token}")

    def test_knowledge_lock_mismatch_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root, manifest, mapping = _write_external_fixture(base)
            result = verify_knowledge_lock(
                model_id="fixture_model",
                benchmark_manifest_path=manifest,
                mapping_path=mapping,
            )
            self.assertEqual(result.status, AVAILABLE)
            (root / "CONVENTIONS.yaml").write_text("changed\n", encoding="utf-8")
            result = verify_knowledge_lock(
                model_id="fixture_model",
                benchmark_manifest_path=manifest,
                mapping_path=mapping,
            )
            self.assertEqual(result.status, CONFLICT_REQUIRES_REVIEW)
            self.assertTrue(any("current hash mismatch" in issue for issue in result.issues))

    def test_missing_knowledge_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _, manifest, _ = _write_external_fixture(base)
            result = verify_knowledge_lock(
                model_id="fixture_model",
                benchmark_manifest_path=manifest,
                mapping_path=base / "missing_mapping.yaml",
            )
            self.assertEqual(result.status, MISSING_KNOWLEDGE)

    def test_custom_audited_classification_and_standard_qed_unchanged(self):
        custom_ids = discover_custom_model_ids(ROOT / "benchmarks")
        b04 = _load_yaml(B04 / "physics_card.yaml")
        b01 = _load_yaml(ROOT / "benchmarks" / "B01_ee_to_mumu" / "physics_card.yaml")
        self.assertEqual(classify_physics_card(b04, custom_model_ids=custom_ids), CUSTOM_AUDITED)
        self.assertEqual(classify_physics_card(b01, custom_model_ids=custom_ids), STANDARD_NATIVE)

    def test_local_mapping_is_gitignored(self):
        if not (ROOT / ".git").exists():
            raise unittest.SkipTest("Git metadata is excluded from review archives")
        completed = subprocess.run(
            ["git", "check-ignore", ".feynagent/knowledge_roots.yaml"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


def _load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_external_fixture(base):
    root = base / "external"
    root.mkdir()
    files = {
        "CONVENTIONS.yaml": "conventions\n",
        "FEYNMAN_RULES.yaml": "rules\n",
        "gold/reference.txt": "gold\n",
    }
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    canonical = {"CONVENTIONS.yaml": _sha(files["CONVENTIONS.yaml"]), "FEYNMAN_RULES.yaml": _sha(files["FEYNMAN_RULES.yaml"])}
    source_gold = {"gold/reference.txt": _sha(files["gold/reference.txt"])}
    lock = {
        "readiness": "KNOWLEDGE_READY_FOR_B04",
        "model_id": "fixture_model",
        "process_id": "process:Fixture",
        "convention_id": "conventions:fixture",
        "canonical_input_hashes": canonical,
        "locked_source_gold_file_sha256": source_gold,
        "unresolved_conflicts": [],
    }
    (root / "KNOWLEDGE_LOCK.json").write_text(json.dumps(lock, indent=2), encoding="utf-8", newline="\n")
    manifest_data = {
        "model_id": "fixture_model",
        "readiness": "KNOWLEDGE_READY_FOR_B04",
        "process_id": "process:Fixture",
        "convention_id": "conventions:fixture",
        "registered_lock": {
            "canonical_input_hashes": canonical,
            "locked_source_gold_file_sha256": source_gold,
        },
    }
    manifest = base / "knowledge_manifest.yaml"
    manifest.write_text(yaml.safe_dump(manifest_data, sort_keys=False), encoding="utf-8", newline="\n")
    mapping = base / "knowledge_roots.yaml"
    mapping.write_text(
        yaml.safe_dump({"schema_version": "0.1.0", "roots": [{"model_id": "fixture_model", "root": str(root)}]}, sort_keys=False),
        encoding="utf-8",
    )
    return root, manifest, mapping


if __name__ == "__main__":
    unittest.main()
