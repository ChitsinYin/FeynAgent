# Quick Start

This guide assumes you are a HEP student who has not used FeynArts or FeynCalc before. FeynAgent will orchestrate them, but you must have the external tools installed and working locally.

## 1. What FeynAgent Can Do In v0.1

FeynAgent v0.1 supports two validated public routes:

- standard native tree-level QED 2-to-2 scattering with external `e-`, `e+`, `mu-`, `mu+`, and `gamma` states;
- FeynArts/FeynCalc native backend `feynarts_feyncalc_native` for that standard QED scope;
- diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output;
- bounded benchmark M2 execution when an `ExecutionRequest` authorizes it;
- validation and provenance reports;
- the single locked custom B04 route `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, requiring separately supplied audited external knowledge.

It does not support arbitrary Standard Model workflows, arbitrary gravity, arbitrary BSM, QCD production, loops, renormalization, or ungated production-heavy execution.

## 2. Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Passing Python tests on Linux or macOS are not a claim that full physics E2E workflows are validated on those platforms.

## 3. Install Prerequisites

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
6. For B04 only, the audited external knowledge package registered by `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.

FeynAgent does not install or relicense Mathematica/Wolfram, FeynCalc, FeynArts, LaTeX, their documentation/examples, or the B04 external knowledge package.

## 4. Install FeynAgent

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

The release-candidate wheel was tested in a fresh Windows 11 physics-toolchain venv with no editable install and no `PYTHONPATH=src`.

## 5. Initialize And Doctor

Run:

```powershell
python -m feynagent init --timeout 60
python -m feynagent doctor --timeout 60
```

Expected successful shape for the standard native QED route:

```text
FeynAgent init: PASS
- wolfram: PASS
- feyncalc: PASS
- feynarts: PASS
- native_qed_tree_capability: PASS
- latex: PASS
```

For B04, the capability report must also show `custom_model:reheating_scalar_gravity_v1 AVAILABLE`. If it is missing, the locked B04 route is unavailable on that machine.

`init` writes machine-local files under `.feynagent/`. Do not commit those files.

## 6. Install The Codex Skill

Codex loads user skills from `$HOME/.agents/skills`. Install the canonical repository skill source to `$HOME/.agents/skills/feynagent`:

```powershell
$skillTarget = Join-Path $HOME ".agents\skills\feynagent"
New-Item -ItemType Directory -Path $skillTarget -Force
Copy-Item -Path skills\feynagent\* -Destination $skillTarget -Recurse -Force
python <path-to-skill-creator>\scripts\quick_validate.py $skillTarget
```

The user skill should end up at:

```text
$HOME/.agents/skills/feynagent
```

Do not keep a duplicate FeynAgent skill under an obsolete legacy location such as `$HOME/.codex/skills/feynagent`; duplicate skill names can both appear in Codex selectors and make validation ambiguous.

## 7. First Compton Request In Codex

Open a fresh Codex task in the FeynAgent project and ask:

```text
Generate the standard tree-level Compton scattering artifact bundle for e- gamma -> e- gamma, including diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output, bounded M2 regression if authorized, and validation/provenance. Report the run directory and whether it passed.
```

Do not ask Codex to hand-write Feynman rules for this standard QED process. The native FeynArts/FeynCalc backend owns standard QED diagrams and amplitudes.

## 8. Run The Standard Native Public CLI Directly

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

## 9. Locked B04 Route

The only validated custom route is B04:

```text
phi phi -> h h
model_id = reheating_scalar_gravity_v1
backend = direct_feyncalc_custom_audited
```

It uses the repository B04 PhysicsCard and backend profile:

```text
benchmarks/B04_phi_phi_to_hh/physics_card.yaml
profiles/backends/b04_custom_gravity_audited.yaml
```

This route requires the separately supplied audited external knowledge package. It is not support for arbitrary gravity or arbitrary BSM models. B04 topology and amplitude authorization do not authorize a B04 M2 calculation; M2 requires separate explicit operations and remains outside automatic public execution.

## 10. Find Your Outputs

The runner prints a run directory such as:

```text
runs/20260815_114653_b02_compton_7dff0c3c
```

Important files can include:

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

## 11. Heavy-Computation Approval Behavior

FeynAgent separates artifact generation from heavy execution:

- `amplitude_only`: generate scripts/artifacts but do not execute M2.
- `benchmark_regression`: execute bounded M2 only with approved `ExecutionRequest`, fixed timeout, and required operation permissions.
- `production_heavy`: refused unless explicitly authorized as production-heavy.

Benchmark-regression approval is not production-heavy approval. B04 M2 is not implied by B04 topology or amplitude authorization.

## 12. Cite And Respect Third-Party Licenses

FeynAgent is Apache-2.0. External packages remain under their own terms. Cite FeynAgent and also cite the exact FeynCalc, FeynArts, Mathematica/Wolfram, external knowledge package, and backend versions used to produce your artifacts.
