# Day 9: bounded QED bremsstrahlung spike

## Outcome

The v0.2 feature spike passes its real Windows FeynArts/FeynCalc execution for

```text
e-(p1) mu-(p2) -> e-(p3) mu-(p4) gamma(k).
```

This is a single bounded `scattering_2_to_3` route, not a general n-body implementation. It reuses the existing backend-profile mappings `e- -> F[2,{1}]`, `mu- -> F[2,{2}]`, and `gamma -> V[1]`. No QED rule was added to Python or to a local rule registry; FeynArts `SM`/`Lorentz` with `Restrictions -> QEDOnly` remains the diagram and amplitude authority.

The locked B04 dispatch, knowledge gate, topology/amplitude implementation, and M2 policy were not changed.

## Structured path and backend calls

- PhysicsCard: `benchmarks/B05_emu_to_emu_gamma/physics_card.yaml`
- Process type: `scattering_2_to_3`
- Schema cardinality: exactly two incoming and exactly three outgoing particles
- Execution mode: approved `amplitude_only`
- FeynArts topology call: `CreateTopologies[0, 2 -> 3, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]`
- FeynArts insertion call: `InsertFields[..., {F[2,{1}], F[2,{2}]} -> {F[2,{1}], F[2,{2}], V[1]}, Model -> "SM", GenericModel -> "Lorentz", Restrictions -> QEDOnly, InsertionLevel -> {Classes}]`

The local reference index was searched before implementation. It contains the official FeynCalc tree example `QED/Tree/Mathematica/ElMu-ElMu.m` (SHA256 `08b5435b2b80bd349086e241ff2a2d5f1a23edbb20e424e84e1aaacdfe276578`) for the B03 hard process, but no exact installed 2-to-3 example. The B05 soft structural check therefore references the validated B03 external state without claiming an official 2-to-3 example.

## Topology result

FeynArts generated **4** class-level tree diagrams. The structural comparison against four external charged-leg bremsstrahlung attachments is `PASS`.

Actual FeynArts order and classification:

| Diagram | Emission leg | Radiating propagator routing | Exchanged virtual particle | Exchange routing |
|---|---|---|---|---|
| 1 | incoming `mu-` (slot 2) | `p2-k` | `gamma` | `p1-p3` |
| 2 | outgoing `mu-` (slot 4) | `p4+k` | `gamma` | `p1-p3` |
| 3 | incoming `e-` (slot 1) | `p1-k` | `gamma` | `p2-p4` |
| 4 | outgoing `e-` (slot 3) | `p3+k` | `gamma` | `p2-p4` |

This metadata is derived by classifying the propagators in the generated FeynCalc expressions. The existing 2-to-2 s/t/u planner is not called for B05, and no four amplitude formulas are hard-coded in core code.

## Amplitude preservation

`FCFAConvert[..., List -> True]` preserves all four generated diagram amplitudes. The persistent `feyncalc_amplitudes.m` association records their expression IDs and objects, then defines the total as

```text
Plus @@ per_diagram_amplitudes
```

The same four objects are rendered as separate sections in `amplitudes.tex`; the total section is generated from their sum. Metadata validation confirms that the total term IDs exactly match the four per-diagram expression IDs.

## Ward identity

Result: **PASS**.

The emitted-photon polarization in the total amplitude is replaced deterministically by `k`. The implementation verifies that this total is the sum of the persisted per-diagram terms, applies on-shell Dirac reduction, canonicalizes the single exchanged-photon dummy Lorentz index, and checks the two external-line cancellation pairs:

- electron-emission pair: `0`
- muon-emission pair: `0`
- total: `0`

The full global simplifier is intentionally avoided; the pairwise reduction is deterministic and bounded while still operating on the total amplitude assembled from the generated objects.

## Soft-photon check

Result: **PASS (structural)**.

Against the B03 hard external state `e- mu- -> e- mu-`, the generated B05 topology contains exactly one emitted-photon attachment on each charged external leg: incoming/outgoing electron and incoming/outgoing muon. The exchanged virtual particle remains a photon in all four classifications.

This is not a numerical Low-theorem coefficient test. A numerical or symbolic leading-soft-factor comparison should be a separate follow-up before widening the route beyond feature-spike status.

## M2 policy

`compute_m2.wl` is generated and records the exact persisted per-diagram/total amplitude relationship. Its status is `SCRIPT_GENERATED_ONLY`; it is not executed. It performs no amplitude squaring, spin sums, polarization sums, full simplification, phase-space integration, or cross-section calculation.

## Passing run and artifacts

Run directory:

`runs/day9_bremsstrahlung_spike/20260831_095025_b05_emu_to_emu_gamma_42b14ce4/`

Key artifacts:

- `diagrams.pdf` — persistent FeynArts diagram PDF
- `diagram_source.m` — persistent inserted FeynArts diagrams
- `feyncalc_amplitudes.m` — four FeynCalc objects plus their total
- `amplitudes.tex` and `amplitudes.pdf` — separate diagram amplitudes and total
- `amplitudes.json` — classifications, propagators, expression IDs, and topology comparison
- `ward_identity.json` and `ward_replaced_total.m` — deterministic total-amplitude Ward result
- `soft_limit.json` — structural B03 soft-emission coverage result
- `compute_m2.wl` and `m2_manifest.json` — non-executed M2 policy artifact
- `validation_report.json` and `run_manifest.json` — passing gates, hashes, package versions, and provenance

Recorded backend versions are Wolfram `15.0.1`, FeynCalc `10.1.0`, and FeynArts `3.12`.

Poppler visual QA of the final one-page `diagrams.pdf` confirmed four numbered diagrams with visible external labels and photon lines, with no clipping, overlap, or missing glyphs.

## Regression closeout

The full suite was run once at final closeout, as requested. It reported `130 passed` and one B04 renderer failure caused by Python decoding MiKTeX UTF-8 output with the Windows GBK default. The subprocess boundary was corrected to use UTF-8 with replacement handling (the same fix required by WolframScript on this host). The single failed B04 renderer test was then rerun in isolation with access to the installed MiKTeX user configuration and passed (`1 passed`).

Thus every one of the 131 collected tests has passing evidence, including B01/B02/B03 and the locked B04 regressions; the full suite was not run a second time.

## Recommendation for v0.2

Accept B05 as an **experimental, benchmark-scoped v0.2 feature** behind its exact particle-pattern and `amplitude_only` gates. Do not advertise general QED 2-to-3 or n-body support yet.

Before promotion to a general 2-to-3 route, add at least one independent bremsstrahlung benchmark, replace benchmark-specific routing normalization with a generic graph/fermion-line classifier, validate a leading-soft factor numerically at fixed physical phase-space points, and design a separately authorized bounded M2 strategy. Phase-space integration and cross sections should remain out of scope until those steps are complete.
