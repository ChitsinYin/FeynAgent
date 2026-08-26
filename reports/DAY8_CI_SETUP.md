# Day 8 CI Setup Report

Status: LOCAL_PASS_PENDING_PUSH

Branch: `release/v0.1.0`
Remote: `https://github.com/ChitsinYin/FeynAgent.git`

## Scope

Minimal public GitHub CI was added for the open-source Python/package layer only. The workflow does not install or run Mathematica, WolframScript, FeynCalc, or FeynArts, and it does not bundle or resolve the private B04 external knowledge package.

No physics code was changed for this phase, no new physics was added, no B04 M2 calculation was rerun, and no release tag or GitHub release was created.

## Files added

- `.github/workflows/ci.yml`
- `scripts/check_release_invariants.py`
- `tests/test_release_invariants.py`
- `docs/CI_AND_RELEASE_GATES.md`
- `reports/DAY8_CI_SETUP.md`

## CI workflow

The workflow runs on GitHub-hosted `ubuntu-latest` runners with Python `3.10` and `3.11`.

Commands:

```bash
python -m pip install .[dev]
python scripts/check_release_invariants.py
python scripts/validate_examples.py
python -m pytest
python -m build --sdist --wheel
```

## Release invariants

`scripts/check_release_invariants.py` checks:

- package version consistency;
- FeynAgent skill metadata and required references;
- no tracked `.feynagent/` files;
- tracked `runs/` content limited to `runs/.gitkeep`;
- no private external-knowledge source-material path markers in the public release surface, excluding the committed hash-only B04 knowledge manifest.

## Local validation

PASS:

- `python -m pip install .[dev]`
- `python scripts/check_release_invariants.py`
- `python scripts/validate_examples.py`
- `python -m pytest` (`123 passed`)
- `python -m build --sdist --wheel`
- `git diff --check` (exit 0; CRLF normalization warnings only)

## Push and GitHub Actions observation

Pending push and remote workflow observation.
