# FeynAgent

FeynAgent is a reproducible HEP workflow tool for the public v0.1 validated scope:

- standard native tree-level QED 2-to-2 workflows with external `e-`, `e+`, `mu-`, `mu+`, and `gamma`, using externally installed FeynArts/FeynCalc through `feynarts_feyncalc_native`;
- the single locked custom B04 benchmark `phi phi -> h h`, `model_id = reheating_scalar_gravity_v1`, through `direct_feyncalc_custom_audited`, requiring separately supplied audited external knowledge.

The unreleased v0.2 feature-spike surface adds exactly one native tree-level QED 2-to-3 benchmark, `e- mu- -> e- mu- gamma` (B05). It is not a general n-body route: it reuses the five standard-QED particle mappings, classifies the four external-leg bremsstrahlung diagrams, checks the total-amplitude Ward identity, performs a structural soft check against B03, and refuses automatic full 2-to-3 M2 simplification.

FeynAgent-owned code and documentation are licensed under Apache-2.0. FeynAgent does not vendor or relicense FeynCalc, FeynArts, Mathematica/Wolfram, their examples, their documentation, or the external B04 knowledge package.

## Support Matrix

| Area | v0.1 Status | Notes |
|---|---:|---|
| Tree-level QED 2-to-2 | Supported | Validated through B01, B02, and B03. |
| Bounded QED 2-to-3 spike | Feature-spike validated | Only B05 `e- mu- -> e- mu- gamma`; no general n-body claim. |
| External particles | Supported | `e-`, `e+`, `mu-`, `mu+`, `gamma`. |
| Native backend | Supported for standard QED scope | FeynArts/FeynCalc via `feynarts_feyncalc_native`. |
| Diagrams | Supported | Persistent FeynArts diagram source and `diagrams.pdf`. |
| Channel-separated amplitudes | Supported | Per-diagram/channel FeynCalc metadata and files. |
| LaTeX output | Supported | `amplitudes.tex` and compiled `amplitudes.pdf`. |
| Executable FeynCalc output | Supported | `native_amplitude.wl`, `feyncalc_amplitudes.m`, `compute_m2.wl`. |
| Bounded benchmark M2 | Supported with approval | Runs only when `ExecutionRequest` authorizes bounded benchmark-regression operations with fixed timeout. |
| Validation/provenance report | Supported | `validation_report.json`, `run_manifest.json`, logs, hashes. |
| Locked B04 `phi phi -> h h` | Supported only for the audited benchmark route | `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, requires the registered audited external knowledge package. |
| B04 squared amplitude / M2 | Not part of automatic public execution | Requires separate explicit authorization; do not infer it from topology or amplitude authorization. |
| Arbitrary Standard Model workflows | Not supported | Outside the validated v0.1 scope. |
| QCD production workflows | Not supported | Outside the validated v0.1 scope. |
| Custom BSM production workflows | Not supported | Outside the validated v0.1 scope. |
| Arbitrary gravity or graviton workflows | Not supported | Only the locked B04 route above is validated. |
| Loops and renormalization | Not supported | Tree level only. |
| Ungated production-heavy execution | Not supported | Requires explicit production-heavy authorization and future validation. |

## Validated Platform

Full physics E2E validation for the v0.1 release candidate was performed on Windows 11 with the tested Wolfram/FeynCalc/FeynArts toolchain. Python tests may pass on Linux or macOS, but that is not a claim that full physics E2E workflows are validated on those platforms.

## Requirements

- Python 3.10 or newer.
- Mathematica/Wolfram with `wolframscript` available on `PATH`, or supplied during initialization.
- FeynCalc installed in the Wolfram environment.
- FeynArts available through FeynCalc using `$LoadAddOns = {"FeynArts"}`.
- A LaTeX engine such as `lualatex` for amplitude PDF rendering.
- For the locked B04 route only: the separately supplied audited external knowledge package registered by `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.

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

For the release-candidate E2E, the wheel install was verified on the validated Windows 11 physics toolchain in a fresh venv without `PYTHONPATH=src` and without editable install.

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

For B04, the doctor/capability report must include `custom_model:reheating_scalar_gravity_v1 AVAILABLE`; otherwise the locked custom route is not executable.

## Install The Codex Skill

Codex loads user skills from `$HOME/.agents/skills`. Install the canonical repository skill source to `$HOME/.agents/skills/feynagent`:

```powershell
$skillTarget = Join-Path $HOME ".agents\skills\feynagent"
New-Item -ItemType Directory -Path $skillTarget -Force
Copy-Item -Path skills\feynagent\* -Destination $skillTarget -Recurse -Force
python <path-to-skill-creator>\scripts\quick_validate.py $skillTarget
```

Do not keep a duplicate FeynAgent skill under an obsolete legacy location such as `$HOME/.codex/skills/feynagent`; duplicate skill names can both appear in Codex selectors and make validation ambiguous.

## First Compton Request

In a fresh Codex task after installing the skill, a natural-language request can be:

```text
Generate the standard tree-level Compton scattering artifact bundle for e- gamma -> e- gamma, including diagrams, channel-separated amplitudes, LaTeX/PDF, executable FeynCalc output, bounded M2 regression if authorized, and validation/provenance. Report the run directory and whether it passed.
```

The release-candidate discovery test confirmed that Codex used the FeynAgent skill and invoked the deterministic public runner rather than a direct helper script.

## Direct CLI Runner

The public deterministic runner for the standard native QED route is:

```powershell
python -m feynagent run `
  --physics-card benchmarks\B02_compton\physics_card.yaml `
  --backend-profile profiles\backends\feynarts_sm_qed.yaml `
  --execution-request runs\requests\b02_execution_request.yaml `
  --run-root runs
```

The execution request must be an approved structured file. For bounded B02 M2 regression, it must authorize `benchmark_regression`, fixed timeout, and the required operations. Production-heavy execution is refused unless explicitly authorized as production-heavy.

The locked B04 route uses `benchmarks\B04_phi_phi_to_hh\physics_card.yaml` with `profiles\backends\b04_custom_gravity_audited.yaml`. It is valid only for `phi phi -> h h` with `model_id = reheating_scalar_gravity_v1`, backend `direct_feyncalc_custom_audited`, and the separately supplied audited external knowledge. B04 M2 is not authorized by topology or amplitude generation alone.

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
ward_identity.json
soft_limit.json
validation_report.json
run_manifest.json
stdout.log
stderr.log
```

The runner also snapshots input files under `runs/<run_id>/inputs/` and records hashes in `run_manifest.json`.

## Examples

- `examples/B02_compton/`: reproducible public Compton example for users who have already passed `feynagent doctor`, including public inputs, a bounded benchmark-regression `ExecutionRequest`, expected `s`/`u` channels, and the expected massless M2.
- `examples/B04_locked_scalar_gravity/`: public documentation manifest for the locked B04 `phi phi -> h h` custom audited route. It records IDs, required rules, topology classes, diagram classifications, and reduced benchmark M2 summary without bundling private/source external knowledge.
- `examples/gallery/`: small curated PDFs with clear publication provenance and SHA256 hashes. It does not copy generated runs wholesale.
- `benchmarks/B05_emu_to_emu_gamma/`: bounded v0.2 feature-spike inputs and structural expectations; generated amplitudes and PDFs remain under `runs/`.

## Third-Party Dependency And Citation Notice

FeynAgent relies on externally installed FeynCalc, FeynArts, Mathematica/Wolfram, LaTeX, and the separately supplied B04 external knowledge package when that locked route is used. Those tools and materials remain subject to their own licenses, installation terms, access controls, and citation requirements. When publishing results, cite FeynAgent if used, and also cite the exact external packages and versions that performed the diagram generation, algebra, rendering, or execution.

See [CITATION.cff](CITATION.cff), [SECURITY.md](SECURITY.md), [docs/QUICKSTART.md](docs/QUICKSTART.md), [docs/RELEASE_SCOPE_V0_1.md](docs/RELEASE_SCOPE_V0_1.md), and [docs/CUSTOM_KNOWLEDGE_TRUST.md](docs/CUSTOM_KNOWLEDGE_TRUST.md).
