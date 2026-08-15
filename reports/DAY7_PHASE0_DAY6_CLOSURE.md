# Day 7 Phase 0 - Day 6 Closure

Status: PASS.

## Scope Hygiene

- Updated the FeynAgent skill metadata and body to state the validated public v0.1 standard-native scope: tree-level QED 2->2 with external `e-`, `e+`, `mu-`, `mu+`, `gamma` through the FeynArts/FeynCalc native backend.
- Retained `custom_audited` only as custom-rule intake, convention/provenance review, and backend-feasibility assessment.
- Removed wording that implied arbitrary SM/QCD/custom BSM/gravity production support in the current release.

## Backend Strategy Hygiene

- Clarified `docs/BACKEND_STRATEGY.md` so current validated support is distinct from future architecture targets.
- Preserved the future architecture for SM/QCD/custom-model support, with benchmark gates required before production claims.

## Contributor Tooling

- Updated `[project.optional-dependencies].dev` so `pip install .[dev]` includes local QA/build tools:
  - `build>=1`
  - `pytest>=7`
- Kept `build` and `pytest` out of runtime dependencies.
- Added `tool.pytest.ini_options.testpaths = ["tests"]` so local QA does not collect ignored generated run-bundle extractions under `runs/`.

## Readiness Semantics

- Added `docs/READINESS_LEVELS.md`.
- Defined `STANDARD_NATIVE_RC_PASS`, `READY_TO_START_CUSTOM_GRAVITY_DEVELOPMENT`, `CUSTOM_GRAVITY_BENCHMARK_PASS`, `CUSTOM_GRAVITY_PRODUCTION_READY`, and `PUBLIC_V0_1_READY`.
- Explained why Day 6 could pass standard-native RC while custom-gravity production readiness remained false.

## Verification

- `python scripts/validate_examples.py`: PASS.
- `python -m pytest`: PASS, 89 passed.
- `python -m build --sdist --wheel`: PASS, built `feynagent-0.1.0.tar.gz` and `feynagent-0.1.0-py3-none-any.whl`.
- `git diff --check`: PASS.

## Notes

The first `python -m pytest` attempt collected copied tests from ignored Day-6 ZIP self-test extraction directories under `runs/`, producing import-mismatch collection errors. The repository now scopes pytest discovery to the tracked `tests/` directory, which matches documented local QA and prevents generated run artifacts from contaminating contributor test runs.

No gravity physics, gravity rules, or new physics models were added.
