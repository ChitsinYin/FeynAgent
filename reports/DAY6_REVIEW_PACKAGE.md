# Day 6 Review Package

Status: PASS

## Purpose

`reports/FeynAgent_Day6_Review_Bundle.zip` is the self-contained Day 6 review bundle for Python validation and tests. It is intended for review of the standard-native release-candidate workflow, not as a public release artifact.

## Included Content

The bundle includes:

- repository root metadata: `README.md`, `LICENSE`, `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md`, `pyproject.toml`, `.gitignore`, `AGENTS.md` when present;
- source package under `src/`, including packaged runtime schemas;
- benchmark specifications and reference fixtures under `benchmarks/`;
- schemas under `schemas/`;
- backend profiles under `profiles/`;
- rules under `rules/`;
- scripts under `scripts/`;
- tests under `tests/`;
- docs under `docs/`;
- FeynAgent skill files under `skills/feynagent/`;
- Markdown reports under `reports/*.md`.

## Excluded Content

The bundle excludes:

- `.git/`;
- `.feynagent/` local machine state;
- generated `runs/` artifacts;
- build outputs such as `build/`, `dist/`, and `*.egg-info/`;
- Python caches and pytest caches;
- review ZIP binaries;
- large transient Mathematica/FeynCalc outputs.

## Self-Test

The final ZIP was extracted under `runs/day6_rc_qa/zip_selftest/extracted` and tested from the clean extraction with:

```powershell
python scripts\validate_examples.py
python -m pytest
python -m build --sdist --wheel --outdir _selftest_dist
```

Observed final ZIP self-test result:

```text
validate_examples: PASS
pytest: 89 passed
build: PASS
```

## Release Status

- Standard-native release candidate: PASS.
- Custom gravity/graviton readiness: NOT_READY.
- Public release/tag: not created.
- GitHub push: not performed.
