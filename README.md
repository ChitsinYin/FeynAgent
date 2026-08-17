# FeynAgent

FeynAgent is a reproducible HEP workflow tool for the public v0.1 standard-native scope: tree-level QED 2-to-2 benchmarks with electrons, muons, and photons, using externally installed FeynArts/FeynCalc as the native diagram and algebra backend.

FeynAgent-owned code and documentation are licensed under Apache-2.0. FeynAgent does not vendor or relicense FeynCalc, FeynArts, Mathematica/Wolfram, their examples, their documentation, or any future external backend.

## Support Matrix

| Area | v0.1 Status | Notes |
|---|---:|---|
| Tree-level QED 2-to-2 | Supported | Validated through B01, B02, and B03. |
| External particles | Supported | `e-`, `e+`, `mu-`, `mu+`, `gamma`. |
| Native backend | Supported | FeynArts/FeynCalc via `feynarts_feyncalc_native`. |
| Diagrams | Supported | Persistent FeynArts diagram source and `diagrams.pdf`. |
| Channel-separated amplitudes | Supported | Per-diagram/channel FeynCalc metadata and files. |
| LaTeX output | Supported | `amplitudes.tex` and compiled `amplitudes.pdf`. |
| Executable FeynCalc output | Supported | `native_amplitude.wl`, `feyncalc_amplitudes.m`, `compute_m2.wl`. |
| Bounded benchmark M2 | Supported with approval | Runs only when `ExecutionRequest` authorizes bounded benchmark-regression operations with fixed timeout. |
| Validation/provenance report | Supported | `validation_report.json`, `run_manifest.json`, logs, hashes. |
| Arbitrary Standard Model workflows | Not supported yet | Do not claim until benchmarks pass. |
| QCD production workflows | Not supported yet | Do not claim until benchmarks pass. |
| Custom BSM production workflows | Not supported yet | Requires audited model/rule provenance and benchmarks. |
| Custom graviton/gravity workflows | Not supported | No gravity benchmark support in v0.1. |
| Ungated production-heavy execution | Not supported | Requires explicit production-heavy authorization and future validation. |

## Requirements

- Python 3.10 or newer.
- Mathematica/Wolfram with `wolframscript` available on `PATH`, or supplied during initialization.
- FeynCalc installed in the Wolfram environment.
- FeynArts available through FeynCalc using `$LoadAddOns = {"FeynArts"}`.
- A LaTeX engine such as `lualatex` for amplitude PDF rendering.

FeynAgent interfaces with these external tools. It does not install them for you.

## Install

From a cloned repository for development:

```powershell
python -m pip install -e .[dev]
```

From a built wheel:

```powershell
python -m build --sdist --wheel
python -m pip install dist\feynagent-0.1.0-py3-none-any.whl
```

For the Day-6 release-candidate E2E, the wheel install was verified in a fresh venv without `PYTHONPATH=src` and without editable install.

## Initialize And Check The Local Physics Toolchain

```powershell
python -m feynagent init --timeout 60
python -m feynagent doctor --timeout 60
```

`init` writes local machine state under `.feynagent/`:

```text
.feynagent/environment.yaml
.feynagent/capability_report.json
.feynagent/reference_index.json
```

## Install The Codex Skill

Codex loads user skills from `$HOME/.agents/skills`. Install the canonical repository skill source to `$HOME/.agents/skills/feynagent`:

```powershell
$skillTarget = Join-Path $HOME ".agents\skills\feynagent"
New-Item -ItemType Directory -Path $skillTarget -Force
Copy-Item -Path skills\feynagent\* -Destination $skillTarget -Recurse -Force
python C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py $skillTarget
```

Do not keep a duplicate FeynAgent skill under an obsolete legacy location such as `$HOME/.codex/skills/feynagent`; duplicate skill names can both appear in Codex selectors and make validation ambiguous.

## First Compton Request

In a fresh Codex task after installing the skill, a natural-language request can be:

```text
Generate the standard tree-level Compton scattering artifact bundle for e- gamma -> e- gamma, including diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output, bounded M2 regression if authorized, and validation/provenance. Report the run directory and whether it passed.
```

The Day-6 discovery test confirmed that Codex used the FeynAgent skill and invoked the deterministic public runner rather than a direct helper script.

## Direct CLI Runner

The public deterministic runner is:

```powershell
python -m feynagent run `
  --physics-card benchmarks\B02_compton\physics_card.yaml `
  --backend-profile profiles\backends\feynarts_sm_qed.yaml `
  --execution-request runs\requests\b02_execution_request.yaml `
  --run-root runs
```

The execution request must be an approved structured file. For bounded B02 M2 regression, it must authorize `benchmark_regression`, fixed timeout, and the required operations. Production-heavy execution is refused unless explicitly authorized as production-heavy.

## Where Outputs Appear

Generated artifacts belong under `runs/<run_id>/`, for example:

```text
diagrams.pdf
diagram_source.m
amplitudes.tex
amplitudes.pdf
amplitudes.json
feyncalc_amplitudes.m
native_amplitude.wl
compute_m2.wl
m2_manifest.json
validation_report.json
run_manifest.json
stdout.log
stderr.log
```

The runner also snapshots input files under `runs/<run_id>/inputs/` and records hashes in `run_manifest.json`.

## Third-Party Dependency And Citation Notice

FeynAgent relies on externally installed FeynCalc, FeynArts, Mathematica/Wolfram, LaTeX, and any future external backend. Those tools remain subject to their own licenses, installation terms, and citation requirements. When publishing results, cite FeynAgent if used, and also cite the exact external packages and versions that performed the diagram generation, algebra, rendering, or execution.

See [CITATION.cff](CITATION.cff), [docs/QUICKSTART.md](docs/QUICKSTART.md), and [docs/RELEASE_SCOPE_V0_1.md](docs/RELEASE_SCOPE_V0_1.md).
