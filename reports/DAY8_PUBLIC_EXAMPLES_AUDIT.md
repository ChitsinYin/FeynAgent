# Day 8 Public Examples Audit

Date: 2026-08-26
Branch: `release/v0.1.0`

## Result

Status: PASS

A minimal public examples/gallery layer was created without copying generated runs wholesale, adding physics code, rerunning B04 M2, altering the external gravity knowledge package, tagging, or releasing.

## Created Example Layer

### A. Reproducible Standard Example

Directory: `examples/B02_compton/`

Files:

- `README.md`
- `physics_card.yaml`
- `backend_profile.yaml`
- `execution_request.benchmark_regression.yaml`
- `expected_results.yaml`

Scope recorded:

- Process: `e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)`.
- Route: `standard_native`.
- Backend: `feynarts_feyncalc_native`.
- Expected channels: `s`, `u`.
- Expected massless M2: `(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)`.
- ExecutionRequest mode: bounded `benchmark_regression` with fixed 180 s timeout.
- Production-heavy execution: not authorized.

Input hashes:

| file | sha256 |
| --- | --- |
| `examples/B02_compton/physics_card.yaml` | `9494fe31e53a952ff667057401288a10509c5dad870a6ead0bd41ddff2d837ec` |
| `examples/B02_compton/backend_profile.yaml` | `30ceaf474e40b56ef08aa22e3da5408ba5fb7ace8116707200daedcee0cbfe85` |
| `examples/B02_compton/execution_request.benchmark_regression.yaml` | `0a28a69430a58a37ed801f1346b37a735b56f1e731834cef70b7c823bb9a22f1` |
| `examples/B02_compton/expected_results.yaml` | `f403d05420c38c35b73bdb228a1d8a0e4094c7537805317a87dfa96166e349e9` |

### B. Locked Custom Example

Directory: `examples/B04_locked_scalar_gravity/`

Files:

- `README.md`
- `manifest.yaml`

Scope recorded:

- Process: `phi phi -> h h`.
- Process ID: `process:B04_phi_phi_to_h_h`.
- Model ID: `reheating_scalar_gravity_v1`.
- Backend route: `direct_feyncalc_custom_audited`.
- External knowledge: separately supplied audited package required; not bundled.
- Required rules: `propagator:phi`, `vertex:h_phi_phi`, `propagator:h`, `vertex:h_h_h`, `vertex:h_h_phi_phi`.
- Expected topology classes: scalar exchange `a`, scalar exchange `b`, s-channel graviton exchange `c`, contact `d`.
- Per-diagram classifications: `a`/`b` match after explicit representation map; `c`/`d` match directly.
- Reduced benchmark M2 summary: raw polarization-summed total `2 M^4/M_P^4`; rate-convention result `M^4/(2 M_P^4)` after the two locked identical-particle factors.
- Explicit non-support: arbitrary gravity, arbitrary BSM, arbitrary SM, QCD production, loops, renormalization, and ungated production-heavy execution.

Manifest hash:

| file | sha256 |
| --- | --- |
| `examples/B04_locked_scalar_gravity/manifest.yaml` | `99440ff3c419176016f9fd57fac6e3cd31f29439231da4fd1cb6bc2851d5c11d` |

### C. Gallery

Directory: `examples/gallery/`

Included only small PDFs with clear publication provenance:

| artifact | provenance | sha256 |
| --- | --- | --- |
| `examples/gallery/B02_compton_diagrams.pdf` | Day-6 public deterministic B02 runner, `runs/day6_public_runner/20260815_105021_b02_compton_e117f8e7/run_manifest.json`, status `PASS`. | `7dafcc0171d688457d468e589ad42a7f8c9917bf57df46de6d14084eeedbf6b6` |
| `examples/gallery/B02_compton_amplitudes.pdf` | Day-6 public deterministic B02 runner, `runs/day6_public_runner/20260815_105021_b02_compton_e117f8e7/run_manifest.json`, status `PASS`. | `905a2237830107a48e9946059c94fe2739f470a0bd132680881f89a0a2e89cc4` |
| `examples/gallery/B04_locked_scalar_gravity_topology.pdf` | Day-7 final B04 topology render, `runs/day7_final_b04_diagram_labels_20260819/run_manifest.json`, topology comparison `PASS`, rule usage audit `PASS`. | `ea59ae5f9e87bae9ed7bb80dfa0dc9e6a28c9af798d689030eb71b75d715701e` |

Omitted by policy:

- Full generated run directories.
- Private/source external B04 knowledge package.
- Private source PDFs.
- Private notebooks.
- Raw gold files.
- Absolute local paths.
- Unapproved third-party content.
- Any artifact with unclear publication provenance.

## README Update

`README.md` now includes a short Examples section pointing to:

- `examples/B02_compton/`;
- `examples/B04_locked_scalar_gravity/`;
- `examples/gallery/`.

## Validation

- New B02 example `physics_card.yaml`, `backend_profile.yaml`, and `execution_request.benchmark_regression.yaml` validate against existing schemas.
- B04 example forbidden-content scan found no absolute local paths, no `source_material` paths, and no bundled notebook/PDF paths; mentions of private PDFs/notebooks are explicit exclusion statements only.
- Gallery includes only the three listed curated PDFs; no generated run directory was copied.

Validation commands completed after creation:

```text
python -c example schema validation -> PASS
python scripts/validate_examples.py -> PASS
python -m pytest -> PASS (122 passed in 22.01s)
git diff --check -> PASS (line-ending normalization warnings only)
new example trailing-whitespace scan -> PASS
```
