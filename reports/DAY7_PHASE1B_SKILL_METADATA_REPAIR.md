# Day 7 Phase 1B Skill Metadata Repair

## Root Cause

The clean GitHub-clone smoke test reached `skills/feynagent/SKILL.md` and failed on YAML frontmatter parsing. The `description` field was an unquoted plain scalar containing colon-bearing text, which made the frontmatter invalid YAML for the validator path used by Codex skill packaging.

No physics behavior was changed. The repair is limited to skill metadata, a repository-level metadata regression test, current user-facing install documentation, and this report.

## Old Invalid Frontmatter

```yaml
---
name: feynagent
description: Use for FeynAgent public v0.1 standard-native workflows: tree-level QED 2-to-2 with external e-, e+, mu-, mu+, gamma through the FeynArts/FeynCalc native backend; deterministic `python -m feynagent run`; validation/provenance; or local init/doctor checks. Use custom_audited only for custom-rule intake, convention/provenance review, and backend-feasibility assessment, not arbitrary custom BSM/gravity production.
---
```

## Corrected Frontmatter

```yaml
---
name: feynagent
description: "Use FeynAgent for validated tree-level QED 2-to-2 workflows with e-, e+, mu-, mu+, and gamma through FeynArts/FeynCalc; local init/doctor checks; and audited custom-rule intake. Do not treat arbitrary SM, QCD, BSM, or gravity as validated production support."
---
```

## Repository Regression Test Result

Added `tests/test_skill_metadata.py` to parse the YAML frontmatter from `skills/feynagent/SKILL.md` and assert:

- `name` exists and is a nonempty string;
- `description` exists and is a nonempty string;
- `name == "feynagent"`;
- the skill body is nonempty.

Result:

```text
python -m pytest tests\test_skill_metadata.py
1 passed in 0.07s
```

Direct parser check:

```text
frontmatter parse: PASS
```

## quick_validate Result

The local Codex skill validator was available at `C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py`.

```text
python C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\feynagent
Skill is valid!
```

Result: PASS.

## User Skill Location Policy

Current user-facing installation documentation now uses `$HOME/.agents/skills/feynagent` as the supported manual user skill install target. The repository continues to keep `skills/feynagent/` as the canonical source tree for this project.

The old `$HOME/.codex/skills/feynagent` location is documented only as an obsolete/legacy duplicate location that should not coexist with the new installed copy. Historical Day-6 reports were not rewritten.

The system validator path under `C:\Users\lenovo\.codex\skills\.system\skill-creator\...` remains documented only for local validation.

## Full Pytest Result

```text
python -m pytest
90 passed in 36.90s
```

Result: PASS.

## Example Validation Result

```text
python scripts\validate_examples.py
PASS rules/qed/qed_tree_v1.yaml
PASS profiles/backends/feynarts_sm_qed.yaml
PASS profiles/backends/legacy_sm_qed.yaml
PASS benchmarks/B01_ee_to_mumu/physics_card.yaml
PASS benchmarks/B01_ee_to_mumu/convention_card.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/diagrams.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/amplitude_ir.example.yaml
PASS benchmarks/B02_compton/physics_card.yaml
PASS benchmarks/B02_compton/convention_card.yaml
PASS benchmarks/B02_compton/legacy/diagrams.yaml
PASS benchmarks/B02_compton/legacy/amplitude_ir.example.yaml
PASS benchmarks/B03_emu_to_emu/physics_card.yaml
PASS benchmarks/B03_emu_to_emu/convention_card.yaml
PASS profiles/backends/feynarts_sm_qed.yaml
PASS profiles/backends/legacy_sm_qed.yaml
PASS benchmarks/B01_ee_to_mumu/native_expected.yaml
PASS benchmarks/B01_ee_to_mumu/legacy/rule_manifest.yaml
PASS benchmarks/B02_compton/native_expected.yaml
PASS benchmarks/B02_compton/legacy/rule_manifest.yaml
PASS benchmarks/B03_emu_to_emu/native_expected.yaml
```

Result: PASS.

## Wheel-Build Result

```text
python -m build --sdist --wheel
Successfully built feynagent-0.1.0.tar.gz and feynagent-0.1.0-py3-none-any.whl
```

Result: PASS.

## Diff Check Result

```text
git diff --check
```

Result: PASS.

## Commit Hash

The final commit hash is reported in the task handoff as `NEW_COMMIT`. A committed report cannot embed its own final commit hash without changing that hash.

## Push Result

The push result is reported in the task handoff as `PUSHED_TO_ORIGIN_MAIN` after `git push` completes.
