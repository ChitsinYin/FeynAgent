# Contributing

Thank you for helping improve FeynAgent. This project is currently a small, release-candidate HEP workflow focused on reproducibility and explicit physics/backend boundaries.

## Validated Public Scope

v0.1 public claims are limited to:

- standard native tree-level QED 2->2 workflows with external `e-`, `e+`, `mu-`, `mu+`, and `gamma` through `feynarts_feyncalc_native`;
- the single locked B04 `phi phi -> h h` route with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and separately supplied audited external knowledge.

Do not describe arbitrary SM, arbitrary gravity, arbitrary BSM, QCD production, loops, renormalization, or ungated production-heavy execution as supported in v0.1.

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Passing Python tests on Linux or macOS are not a claim of full physics E2E validation on those platforms.

## Ground Rules

- Do not invent trusted Feynman rules.
- Do not silently change conventions, channel definitions, benchmark gold files, or approximation assumptions.
- Keep generated amplitudes, PDFs, Wolfram logs, M2 outputs, and run manifests under `runs/`.
- Keep benchmark directories for input specs, gold/reference fixtures, and explicitly marked historical artifacts.
- Do not claim arbitrary SM, QCD, BSM, or gravity support until corresponding benchmarks pass and the support matrix is updated. Locked B04 is the only current custom exception.
- Do not treat B04 topology or amplitude authorization as B04 M2 authorization.
- Treat FeynArts, FeynCalc, Mathematica/Wolfram, LaTeX, and external knowledge packages as separately licensed external dependencies.
- Keep project version `0.1.0` during release-candidate hardening and do not assign a final release date until the human release gate.

## Development Setup

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

On Unix-like shells, activate the venv with your usual shell-specific command and run the same `pip install -e .[dev]` inside it. That can validate Python behavior, but it is not full physics E2E validation for Linux or macOS.

## Required External Tools For Native Workflows

FeynAgent does not vendor or install Mathematica, FeynCalc, or FeynArts. Native workflows require:

- Mathematica/Wolfram with `wolframscript` on `PATH` or passed during initialization.
- FeynCalc installed so Wolfram can load `FeynCalc``.
- FeynArts loaded through FeynCalc with `$LoadAddOns = {"FeynArts"}`.
- A LaTeX engine such as `lualatex` for PDF amplitude rendering.

The locked B04 route additionally requires the separately supplied audited external knowledge package registered by `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.

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
- Confirmation that public release wording still matches `docs/RELEASE_SCOPE_V0_1.md`.

## License

FeynAgent-owned code and documentation are licensed under Apache-2.0. Contributions intentionally submitted to this repository are expected to be licensed under Apache-2.0 unless separately agreed in writing.

This does not relicense FeynCalc, FeynArts, Mathematica/Wolfram, LaTeX, their examples, their documentation, or external knowledge packages.
