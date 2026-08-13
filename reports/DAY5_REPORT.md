# Day 5 Final QA Report

Generated at: 2026-08-13T19:58:32.5692163+08:00

## Executive status

DAY5_PASS

FeynAgent Day 5 separates backend-neutral physics intent, backend implementation, and runtime authorization while adding portable local initialization and a reusable Codex skill. No new physics models were added.

## Repository QA

| check | status | evidence |
| --- | --- | --- |
| no caches | PASS | cache scan run before packaging; final cleanup repeated after self-test |
| no machine-local `.feynagent` files tracked | PASS | `.feynagent/` is ignored; `git ls-files .feynagent` is empty |
| no generated runs staged | PASS | `runs/*` ignored except `runs/.gitkeep`; generated Day-5 QA run remains untracked |
| no tracked review ZIP binaries | PASS | tracked Day-4 ZIP removed; Day-5 ZIP is handoff artifact and is not staged |
| no duplicate native backend profile | PASS | one shared native profile: `profiles/backends/feynarts_sm_qed.yaml` |
| no benchmark-local machine paths | PASS | backend paths live in `.feynagent/`; benchmark cards use relative/shared profile references |
| no EOL-only diff noise | PASS | `.gitattributes` normalizes text to LF; `git diff --check` passed |

## Architecture QA

| requirement | status | evidence |
| --- | --- | --- |
| PhysicsCard backend-neutral | PASS | B01/B02/B03 use `schema_version: 0.2.0`, `model_id: sm_qed`, `sector: qed` |
| BackendProfile resolves implementation | PASS | native and legacy profiles resolve `sm_qed/qed` differently |
| ExecutionRequest separates authorization | PASS | `schemas/execution_request.schema.json` supports `structural`, `amplitude_only`, `benchmark_regression`, `production_heavy` |
| native backend primary for standard QED | PASS | docs and skill classify standard QED as `standard_native` |
| legacy backend fallback/reference | PASS | `profiles/backends/legacy_sm_qed.yaml` and legacy tests retained |
| custom RuleRegistry available | PASS | `rules/qed/qed_tree_v1.yaml` retained for legacy/custom audited path |

## Initialization QA

| check | status | evidence |
| --- | --- | --- |
| init | PASS | `$env:PYTHONPATH='src'; python -m feynagent init --timeout 60` |
| doctor | PASS | `$env:PYTHONPATH='src'; python -m feynagent doctor --timeout 60` |
| Wolfram | PASS | 15.0.1 for Microsoft Windows |
| FeynCalc | PASS | 10.1.0 detected |
| FeynArts | PASS | FeynArts 3.12 loaded through FeynCalc add-on path |
| reference index | PASS | `.feynagent/reference_index.json`, 200 metadata/hash/path entries |
| no package source copied | PASS | index records external paths and hashes only |

## Skill QA

| check | status | evidence |
| --- | --- | --- |
| `SKILL.md` exists | PASS | `skills/feynagent/SKILL.md`, 15 lines |
| standard/custom decision tree tested | PASS | skill eval 5/5 |
| missing-init behavior tested | PASS | eval case returns actionable initialization request |
| no large docs duplication | PASS | concise skill plus three short reference files; no copied FeynCalc/FeynArts docs |
| clean E2E | PASS | `reports/DAY5_SKILL_E2E.md`: Test A `standard_native`, Test B `custom_audited` |

## Physics Regression

| benchmark | native structural status | diagram count | official M2 regression |
| --- | --- | ---: | --- |
| B01 e- e+ -> mu- mu+ | PASS | 1 | PASS, Day-4 bounded regression |
| B02 e- gamma -> e- gamma | PASS | 2 | PASS, Day-4 bounded regression plus Day-5 skill E2E Compton check |
| B03 e- mu- -> e- mu- | PASS | 1 | PASS, Day-4 bounded regression |

Fresh native structural QA run: `runs/day5_final_qa_native/20260813_195330`.

Heavy production calculation remains separated from benchmark regression by `ExecutionRequest`. Day-4 M2 was user-authorized benchmark regression evidence, not production-heavy approval.

## Tests

| command | status | result |
| --- | --- | --- |
| `python scripts/validate_examples.py` | PASS | schemas/profiles/benchmark fixtures validated |
| `python -m pytest` | PASS | 75 passed |
| skill eval | PASS | 5/5 passed |
| ZIP clean extraction test | PASS | see `reports/DAY5_ZIP_SELFTEST.md` |

## Review Bundle

Bundle path: `reports/FeynAgent_Day5_Review_Bundle.zip`.

The bundle excludes `.git`, caches, `runs/`, `.feynagent/`, review ZIP binaries, and machine-local absolute-path diagnostics. It includes source, schemas, profiles, benchmark specs/gold/reference fixtures, rules, tests, skill files, docs, and sanitized Day-5 reports.

## Known Warnings

- Direct `python -m feynagent` fails in this development shell unless the project is installed or `PYTHONPATH=src` is set. The clean skill E2E installed the copied source with `pip install -e . --no-deps` and passed initialization.
- Headless FeynCalc examples can emit `FrontEndObject::notavail`; Day-4 M2 comparisons still passed with empty stderr.

## Recommendation

READY_FOR_CUSTOM_GRAVITY
