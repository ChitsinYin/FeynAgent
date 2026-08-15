# Contributing

Thank you for helping improve FeynAgent. This project is currently a small, release-candidate HEP workflow focused on reproducibility and explicit physics/backend boundaries.

## Ground Rules

- Do not invent trusted Feynman rules.
- Do not silently change conventions, channel definitions, benchmark gold files, or approximation assumptions.
- Keep generated amplitudes, PDFs, Wolfram logs, M2 outputs, and run manifests under `runs/`.
- Keep benchmark directories for input specs, gold/reference fixtures, and explicitly marked historical artifacts.
- Do not claim arbitrary SM, QCD, BSM, or graviton support until corresponding benchmarks pass and the support matrix is updated.
- Treat FeynArts, FeynCalc, Mathematica/Wolfram, and future external backends as separately licensed external dependencies.

## Development Setup

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

On Unix-like shells, activate the venv with your usual shell-specific command and run the same `pip install -e .[dev]` inside it.

## Required External Tools For Native Workflows

FeynAgent does not vendor or install Mathematica, FeynCalc, or FeynArts. Native workflows require:

- Mathematica/Wolfram with `wolframscript` on `PATH` or passed during initialization.
- FeynCalc installed so Wolfram can load `FeynCalc``.
- FeynArts loaded through FeynCalc with `$LoadAddOns = {"FeynArts"}`.
- A LaTeX engine such as `lualatex` for PDF amplitude rendering.

Check local readiness:

```powershell
python -m feynagent init --timeout 60
python -m feynagent doctor --timeout 60
```

## Tests

Run the current Python suite:

```powershell
python -m pytest
python scripts\validate_examples.py
```

For native release-candidate checks, use run-scoped artifacts under `runs/` and record exact commands, runtime, output paths, and failures.

## Pull Requests

A useful pull request should include:

- A clear description of changed behavior.
- The support-matrix impact, if any.
- New or updated tests for behavioral changes.
- Provenance for any physics rule, convention, benchmark, or external reference.
- Confirmation that generated artifacts were not committed outside approved locations.

## License

FeynAgent-owned code and documentation are licensed under Apache-2.0. Contributions intentionally submitted to this repository are expected to be licensed under Apache-2.0 unless separately agreed in writing.

This does not relicense FeynCalc, FeynArts, Mathematica/Wolfram, their examples, their documentation, or any future external backend.
