# FeynAgent Day-7 Review Package

## Purpose

This review package closes the audited B04 custom gravity benchmark for Day 7. It is intentionally bounded: it includes source/spec/test/docs/report material needed to review the locked B04 route and sanitized Day-7 evidence, but it excludes raw external gravity source material, private PDFs/notebooks, generated caches, build products, and nested review archives.

## Review ZIP

Archive path: `reports/FeynAgent_Day7_Review_Bundle.zip`

ZIP status: PASS. The ZIP is generated for review but is not staged for the Git commit.

## Included Source And Specs

- `pyproject.toml`, `README.md`, `CHANGELOG.md`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`
- `benchmarks/B04_phi_phi_to_hh/` sanitized benchmark metadata, manifests, cards, and expected topology
- `profiles/backends/b04_custom_gravity_audited.yaml`
- `schemas/*.schema.json` and `src/feynagent/schemas/*.schema.json`
- B04 source modules: `src/feynagent/b04_topology.py`, `src/feynagent/b04_amplitudes.py`, `src/feynagent/b04_phase7_closure.py`, `src/feynagent/backends/b04_custom.py`, `src/feynagent/dispatch.py`, plus shared initialized runner/knowledge modules needed by tests
- Day-7 scripts: `scripts/day7_b04_topology.py`, `scripts/day7_b04_amplitudes.py`, `scripts/day7_b04_phase7_closure.py`, `scripts/validate_examples.py`, `scripts/verify_knowledge_lock.py`
- FeynAgent skill source: `skills/feynagent/SKILL.md`, `skills/feynagent/evals/smoke_cases.json`, `skills/feynagent/references/*.md`, `skills/feynagent/scripts/*.py`
- Tests needed for Day-7 review and regression, including B04 topology/amplitude/phase7/skill dispatch tests and standard regression tests
- Reports: Day-7 phase reports, this review package, and `reports/DAY7_REPORT.md`

## Curated Evidence

The review bundle may include the sanitized topology-only diagram evidence from `runs/day7_final_b04_diagram_labels_20260819/`:

- `diagrams/diagrams.tex`
- `diagrams/diagrams.pdf`
- `diagrams/diagram_source.json`
- `diagrams/diagrams.json`
- `diagrams/render_manifest.json`
- `run_manifest.json`
- `rule_usage.json`
- `validation/topology_report.md`

This evidence contains no raw private external gravity package material and no B04 M2 rerun artifacts.

## Exclusions

The archive excludes:

- `.git/`
- `.feynagent/`
- `runs/` except the curated small topology evidence listed above
- `dist/`
- `build/`
- `__pycache__/`
- `.pytest_cache/`
- private external gravity source material
- private PDFs/notebooks
- nested review ZIPs
- temporary patch/work files such as `*.patch`, `runner_work.py`, `Get-Service ssh-agent*`, `chemas`, and `rc`

## QA Results

- `python scripts\validate_examples.py` -> PASS
- `python -m pytest` -> PASS, `122 passed in 19.00s`
- `python -m build --sdist --wheel` -> PASS
- `git diff --check` -> PASS
- deterministic skill eval -> PASS, `7/7`
- clean-extraction review ZIP self-test -> PASS, `validate_examples` exit 0 and extracted `python -m pytest` -> `121 passed, 1 skipped`

## Readiness

B04_CUSTOM_GRAVITY_BENCHMARK = PASS
B04_LOCKED_PRODUCTION_PATH = PASS
GENERAL_CUSTOM_GRAVITY_PRODUCTION_READY = NO
PUBLIC_V0_1_READY = NO
READY_FOR_DAY8 = YES
