# CI and Release Gates

This document records the minimal public CI and release gates for FeynAgent v0.1.

## GitHub CI purpose

GitHub Actions validates the open-source Python/package layer on GitHub-hosted runners. It does not install, configure, or run Mathematica, WolframScript, FeynCalc, or FeynArts.

Full physics E2E validation for the v0.1 release candidate remains the separately recorded Windows 11 workflow with the tested Wolfram/FeynCalc/FeynArts toolchain. Passing CI on Linux is not a full physics E2E validation claim.

## CI matrix

The public workflow runs on `ubuntu-latest` with Python `3.10` and `3.11`.

The project metadata keeps `requires-python = ">=3.10"` and version `0.1.0`. The matrix is intentionally small for the v0.1 public-release gate.

## CI commands

The workflow in `.github/workflows/ci.yml` performs:

```bash
python -m pip install .[dev]
python scripts/check_release_invariants.py
python scripts/validate_examples.py
python -m pytest
python -m build --sdist --wheel
```

Any tests that need a real Wolfram/FeynCalc/FeynArts runtime must skip cleanly when that runtime is absent. CI must not silently install external physics runtimes or private knowledge packages.

## Release invariants

`scripts/check_release_invariants.py` checks:

- package version consistency across `pyproject.toml`, `src/feynagent/__init__.py`, and installed package metadata;
- FeynAgent skill frontmatter and required skill references;
- no tracked `.feynagent/` files;
- no tracked `runs/` outputs except `runs/.gitkeep`;
- no private external-knowledge source-material paths in the public release surface, excluding the committed B04 hash-only knowledge manifest.

## Human release gates

Before final public release, a human reviewer must confirm:

- the final release date is assigned only at the release gate;
- no release tag or GitHub release is created before approval;
- the validated public scope still matches `docs/RELEASE_SCOPE_V0_1.md`;
- no B04 M2 calculation is rerun as part of CI or automated release checks;
- full physics E2E evidence remains Windows 11 plus the tested Wolfram/FeynCalc/FeynArts toolchain, not GitHub-hosted Linux CI.
