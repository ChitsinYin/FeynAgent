# Quick Start

This guide assumes you are a HEP student who has not used FeynArts or FeynCalc before. FeynAgent will orchestrate them, but you must have the external tools installed and working locally.

## 1. What FeynAgent Can Do In v0.1

FeynAgent v0.1 supports a narrow public workflow:

- tree-level QED 2-to-2 scattering;
- external `e-`, `e+`, `mu-`, `mu+`, and `gamma` states;
- FeynArts/FeynCalc native backend;
- diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output;
- bounded benchmark M2 execution when an `ExecutionRequest` authorizes it;
- validation and provenance reports.

It does not yet support arbitrary Standard Model, QCD, custom BSM, or custom graviton production workflows.

## 2. Install Prerequisites

Install these outside FeynAgent:

1. Python 3.10 or newer.
2. Mathematica/Wolfram with `wolframscript` available on `PATH`.
3. FeynCalc in your Wolfram installation.
4. FeynArts available through FeynCalc with this Wolfram loading pattern:

```wolfram
$LoadAddOns = {"FeynArts"};
<< FeynCalc`
```

5. A LaTeX engine such as `lualatex` if you want `amplitudes.pdf`.

FeynAgent does not install or relicense Mathematica/Wolfram, FeynCalc, FeynArts, LaTeX, or their documentation/examples.

## 3. Install FeynAgent

From a cloned repository:

```powershell
git clone <your-feynagent-repository-url>
cd FeynAgent
python -m pip install -e .[dev]
```

From a wheel:

```powershell
python -m pip install dist\feynagent-0.1.0-py3-none-any.whl
```

The Day-6 release-candidate wheel was tested in a fresh venv with no editable install and no `PYTHONPATH=src`.

## 4. Initialize And Doctor

Run:

```powershell
python -m feynagent init --timeout 60
python -m feynagent doctor --timeout 60
```

Expected successful shape:

```text
FeynAgent init: PASS
- wolfram: PASS
- feyncalc: PASS
- feynarts: PASS
- native_qed_tree_capability: PASS
- latex: PASS
```

`init` writes machine-local files under `.feynagent/`. Do not commit those files.

## 5. Install The Codex Skill

The Day-6 tested Codex surface discovered user skills from the local skills directory. On that Windows client, the validated method was:

```powershell
Copy-Item -Path skills\feynagent -Destination C:\Users\lenovo\.codex\skills\feynagent -Recurse
python C:\Users\lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\lenovo\.codex\skills\feynagent
```

If your Codex home is elsewhere, install to:

```text
$CODEX_HOME\skills\feynagent
```

or, when `CODEX_HOME` is unset on Windows:

```text
C:\Users\<you>\.codex\skills\feynagent
```

## 6. First Compton Request In Codex

Open a fresh Codex task in the FeynAgent project and ask:

```text
Generate the standard tree-level Compton scattering artifact bundle for e- gamma -> e- gamma, including diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output, bounded M2 regression if authorized, and validation/provenance. Report the run directory and whether it passed.
```

Do not ask Codex to hand-write Feynman rules for this standard QED process. The native FeynArts/FeynCalc backend owns standard QED diagrams and amplitudes.

## 7. Run The Public CLI Directly

Create or reuse an approved `ExecutionRequest` for bounded benchmark regression, then run:

```powershell
python -m feynagent run `
  --physics-card benchmarks\B02_compton\physics_card.yaml `
  --backend-profile profiles\backends\feynarts_sm_qed.yaml `
  --execution-request runs\requests\b02_execution_request.yaml `
  --run-root runs
```

For B02 benchmark M2 execution, the request must include:

```yaml
execution_mode: benchmark_regression
timeout_policy:
  kind: fixed_seconds
  seconds: 180
allowed_operations:
  - schema_validation
  - diagram_generation
  - amplitude_generation
  - latex_render
  - feyncalc_smoke
  - m2_regression
  - spin_sums
  - polarization_sums
  - heavy_simplification
```

## 8. Find Your Outputs

The runner prints a run directory such as:

```text
runs/20260815_114653_b02_compton_7dff0c3c
```

Important files include:

```text
inputs/physics_card.yaml
inputs/backend_profile.yaml
inputs/execution_request.yaml
diagrams.pdf
diagram_source.m
amplitudes.tex
amplitudes.pdf
amplitudes.json
feyncalc_amplitudes.m
native_amplitude.wl
compute_m2.wl
m2_raw.m
m2_simplified.m
m2_inputform.txt
m2_manifest.json
validation_report.json
run_manifest.json
stdout.log
stderr.log
```

For B02, `amplitudes.json` should report two channels: `s` and `u`.

## 9. Heavy-Computation Approval Behavior

FeynAgent separates artifact generation from heavy execution:

- `amplitude_only`: generate scripts/artifacts but do not execute M2.
- `benchmark_regression`: execute bounded M2 only with approved `ExecutionRequest`, fixed timeout, and required operation permissions.
- `production_heavy`: refused unless explicitly authorized as production-heavy.

Benchmark-regression approval is not production-heavy approval.

## 10. Cite And Respect Third-Party Licenses

FeynAgent is Apache-2.0. External packages remain under their own terms. Cite FeynAgent and also cite the exact FeynCalc, FeynArts, Mathematica/Wolfram, and backend versions used to produce your artifacts.
