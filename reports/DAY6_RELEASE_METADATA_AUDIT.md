# Day 6 Release Metadata Audit

Status: PASS

## License Decision

The user explicitly selected:

```text
Apache-2.0
```

Copyright holder:

```text
Chitsin Yin
```

Copyright year:

```text
2026
```

A repository-root `LICENSE` file was created with the full Apache License 2.0 text and the project copyright notice.

No license was chosen silently.

## Files Created Or Updated

```text
LICENSE
CITATION.cff
CHANGELOG.md
CONTRIBUTING.md
README.md
docs/QUICKSTART.md
pyproject.toml
reports/DAY6_RELEASE_METADATA_AUDIT.md
```

## Pyproject Metadata

`pyproject.toml` now identifies the project license as Apache-2.0 and records the author:

```toml
license = "Apache-2.0"
license-files = ["LICENSE"]
authors = [{ name = "Chitsin Yin" }]
```

It also uses the current SPDX license string form and keeps the previously audited runtime dependencies:

```text
jsonschema>=4
PyYAML>=6
```

## README / Quick Start Coverage

The README and `docs/QUICKSTART.md` include:

- Python requirement: Python 3.10 or newer.
- Mathematica/Wolfram requirement: `wolframscript` available on `PATH` or supplied during initialization.
- FeynCalc/FeynArts setup expectation: FeynCalc installed and FeynArts loaded through `$LoadAddOns = {"FeynArts"}`.
- pip install from cloned repository and from built wheel.
- `python -m feynagent init --timeout 60`.
- `python -m feynagent doctor --timeout 60`.
- Actual Codex skill installation method validated on this Day-6 surface: filesystem installation into `C:\Users\lenovo\.codex\skills\feynagent`, followed by `quick_validate.py`.
- First natural-language Compton request.
- Output location under `runs/<run_id>/`.
- Heavy-computation approval behavior through `ExecutionRequest`.

## Support Matrix

README now includes a support matrix with the public v0.1 boundary:

Supported:

- tree-level QED 2-to-2;
- external `e-`, `e+`, `mu-`, `mu+`, `gamma`;
- FeynArts/FeynCalc native backend;
- diagrams;
- channel-separated amplitudes;
- LaTeX output;
- executable FeynCalc output;
- bounded benchmark M2 when authorized;
- validation/provenance reports.

Explicitly not supported in v0.1:

- arbitrary Standard Model workflows;
- QCD production workflows;
- custom BSM production workflows;
- custom graviton/gravity workflows;
- ungated production-heavy execution.

## Overclaim Audit

The prior README sentence:

```text
Use `feynarts_feyncalc_native` for standard QED/SM/QCD sectors supported by installed FeynArts/FeynCalc model files.
```

was replaced with a validated v0.1 support statement limited to tree-level QED 2-to-2 benchmarks.

The new release metadata does not claim:

- arbitrary SM support;
- arbitrary BSM support;
- custom graviton support;
- arbitrary QCD production support.

## Third-Party Dependency / Citation Notice

README, `docs/QUICKSTART.md`, `CONTRIBUTING.md`, and `CITATION.cff` now state that FeynAgent only interfaces with external FeynCalc, FeynArts, Mathematica/Wolfram, LaTeX, and future external backends.

This update does not modify or relicense:

- FeynCalc;
- FeynArts;
- Mathematica/Wolfram;
- upstream examples;
- upstream documentation;
- any future external backend.

Those dependencies remain subject to their own licenses and citation requirements.

## No Per-Source Headers

No per-source-file license headers were added in this phase, because no existing packaging standard in this repository required them.

## Validation

Validation commands should pass after this metadata update:

```powershell
python scripts\validate_examples.py
python -m pytest
git diff --check
```

Results observed in this phase:

```text
python scripts\validate_examples.py  -> PASS
python -m pytest                     -> 89 passed
python -m build --sdist --wheel       -> PASS after SPDX cleanup
git diff --check                     -> PASS
```
