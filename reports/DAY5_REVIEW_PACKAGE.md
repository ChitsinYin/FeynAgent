# Day 5 Review Package

Generated at: 2026-08-13T19:58:32.5692163+08:00

## Scope

Day 5 repaired the FeynAgent contract boundary and packaged the project as a reusable Codex skill. It did not add gravity, new physics models, loops, phase-space integration, FeynRules, HPC, or multi-agent orchestration.

## Meaningful Source Changes

- `PhysicsCard` 0.2.0 is backend-neutral.
- `BackendProfile` schemas and profiles now resolve `sm_qed/qed` to either native FeynArts/FeynCalc or legacy RuleRegistry implementation.
- `ExecutionRequest` schema separates structural/amplitude-only/benchmark-regression/production-heavy authorization.
- Native backend consumes profile-local particle mappings and uses the FeynCalc add-on loading pattern documented in `docs/INITIALIZATION.md`.
- Legacy topology path remains available and accepts the legacy backend profile.
- Local initialization writes only `.feynagent/` machine state and builds a metadata-only reference index.
- Codex skill files were added under `skills/feynagent/`.

## Backend Roles

| role | status | authority |
| --- | --- | --- |
| standard supported QED | `feynarts_feyncalc_native` primary | FeynArts/FeynCalc native packages and official examples |
| legacy custom backend | fallback/reference | audited legacy RuleRegistry snapshot |
| custom rules | custom audited path | explicit convention/provenance review; RuleRegistry remains authority |

## Migrated Benchmarks

| benchmark | PhysicsCard theory intent | native profile | legacy support |
| --- | --- | --- | --- |
| B01 | `model_id: sm_qed`, `sector: qed` | PASS, 1 diagram | PASS |
| B02 | `model_id: sm_qed`, `sector: qed` | PASS, 2 diagrams | PASS |
| B03 | `model_id: sm_qed`, `sector: qed` | PASS, 1 diagram | PASS; old limitation resolved as configuration coupling |

## Initialization Evidence

- `init`: PASS from source tree with `PYTHONPATH=src`.
- `doctor`: PASS from source tree with `PYTHONPATH=src`.
- Wolfram: 15.0.1 for Microsoft Windows.
- FeynCalc: 10.1.0.
- FeynArts: 3.12, loaded through FeynCalc add-on path.
- Reference index: 200 entries; external package paths and hashes only.

## Skill Evidence

- `skills/feynagent/SKILL.md` exists and is concise.
- References: `BACKEND_POLICY.md`, `CUSTOM_RULE_PROTOCOL.md`, `OUTPUT_CONTRACT.md`.
- Scripts: `ensure_initialized.py`, `run_feynagent.py`.
- Eval set: `skills/feynagent/evals/smoke_cases.json`.
- Eval result: 5/5 PASS.
- Clean E2E result: PASS. Standard Compton selected `standard_native`; toy Yukawa selected `custom_audited`.

## Physics Evidence

Native structural QA run: `runs/day5_final_qa_native/20260813_195330`.

| benchmark | status | diagram count |
| --- | --- | ---: |
| B01 | PASS | 1 |
| B02 | PASS | 2 |
| B03 | PASS | 1 |

Official M2 regression evidence remains the Day-4 bounded run `runs/day4_native/20260813_145016`, recorded in `reports/DAY4_M2_REGRESSION.md`, with B01/B02/B03 all PASS. No new production-heavy calculation was performed during final QA.

## Tests

- `python scripts/validate_examples.py`: PASS.
- `python -m pytest`: PASS, 75 passed.
- `python skills/feynagent/scripts/run_feynagent.py eval --cases skills/feynagent/evals/smoke_cases.json`: PASS, 5/5.
- ZIP clean extraction: PASS.

## Repository Hygiene

- `.feynagent/` ignored and untracked.
- `runs/` ignored except `runs/.gitkeep`.
- Review ZIP binaries are not staged; the old tracked Day-4 ZIP is removed.
- Benchmark-local native backend profile duplication removed; shared profile is `profiles/backends/feynarts_sm_qed.yaml`.
- No benchmark-local machine paths are required for validation.
- `.gitattributes` normalizes text to LF.

## Files Expected In Commit

Source/docs/spec/report changes only, including the tracked deletion of `reports/FeynAgent_Day4_Review_Bundle.zip`. Generated runs, `.feynagent/`, caches, and `reports/FeynAgent_Day5_Review_Bundle.zip` remain unstaged.

## Day 6 Readiness

READY_FOR_CUSTOM_GRAVITY, subject to preserving the Day-5 contracts: standard native backend first, custom audited rules only with provenance, and production-heavy execution only through an explicit `ExecutionRequest`.
