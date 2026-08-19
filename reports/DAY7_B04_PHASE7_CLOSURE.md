# Day-7 B04 Phase-7 Closure

- Overall status: `PASS`
- Closure: `CLOSED`
- Workflow classification: `custom_audited` (not arbitrary-gravity production support).
- Process: `process:B04_phi_phi_to_h_h`
- Amplitude run: `day7_b04_amplitude_closure_20260819T000000Z`
- M2 run: `day7_b04_m2_manual_20260819T000000Z`
- Layer order preserved: `EXACT_RAW` amplitudes, then `REDUCED_NR_TT`, then reduced-layer M2.

## Gate Results

- Knowledge lock and M2 gold: `PASS`
- Diagram/amplitude prerequisite gate: `PASS`
- Manual M2 manifest: `PASS`
- Deterministic Wolfram script structure: `PASS`
- No amplitude diagram is classified `CONFLICT_REQUIRES_REVIEW`.

## M2 Gold Comparison

| Quantity | Generated | Locked gold | Status |
| --- | --- | --- | --- |
| `Mc2` | `(18*M^4)/MP^4` | `18 M^4/MP^4` | `PASS` |
| `Md2` | `(32*M^4)/MP^4` | `32 M^4/MP^4` | `PASS` |
| `interference` | `(-48*M^4)/MP^4` | `-48 M^4/MP^4` | `PASS` |
| `raw_total` | `(2*M^4)/MP^4` | `2 M^4/MP^4` | `PASS` |
| `rate_convention` | `M^4/(2*MP^4)` | `M^4/(2 MP^4)` | `PASS` |

The raw polarization-summed reduced-layer result is `2 M^4/MP^4`. Applying the locked initial identical factor `1/2` and final identical-particle phase-space factor `1/2` gives the published rate-convention result `M^4/(2 MP^4)`.

`Ma = Mb = 0` is used only in `REDUCED_NR_TT`; the exact t/u-channel assemblies remain preserved and hashed in the amplitude run.

## Provenance

- Knowledge lock sha256: `19cfb8a8de198a104c23909148aa577889c50212277bae2c0887ffe265c7c1c6`
- Locked `gold/m2_reference.m` sha256: `739e480db50fa4d34d63948f0c32517238cbb216bdb74f8947653ee0205c4eaf`
- Knowledge hashes rechecked: `19`
- Contact authority: locked corrected manual `TauLocked` rule.
- Historical FeynGrav 3.0 `ssgg` remains rejected as an authority.
- No rule was changed to force agreement and no disagreement was averaged.

## Runtime

- Wolfram: `15.0.1 for Microsoft Windows (64-bit) (July 2, 2026)`
- FeynCalc: `10.1.0`
- FeynArts: `FeynArts 3.12 (27 Mar 2025)`
- Headless `FrontEndObject::notavail` notices do not alter the successful exported checks.

## Input Artifacts

| Artifact | SHA-256 |
| --- | --- |
| `runs/day7_b04_amplitude_closure_20260819T000000Z/run_manifest.json` | `31c18351d1599a920d3ea7780cfdb927858e61774837d07a528c92d21a54e5aa` |
| `runs/day7_b04_amplitude_closure_20260819T000000Z/validation/amplitude_validation.json` | `3c0b2b8fbe021ac6bc5172dcaf00051099c5808fe8db47a1d65631f40f71212a` |
| `runs/day7_b04_m2_manual_20260819T000000Z/m2/M2_manifest.json` | `d8c692d87f29a5b809a5678e6a3dcd0af1f696977cdd6268b2365c90aef7ed2c` |
| `runs/day7_b04_m2_manual_20260819T000000Z/m2/M2_results.m` | `be317f3fa2a488d2034b941f2ece77027c873935f61329a0ece7a13f88760700` |
| `runs/day7_b04_m2_manual_20260819T000000Z/m2/run_b04_m2_reduced.wl` | `41e6f81a5e111b40155279c93f3f025b6bf928ddf1c3fec52240ca2aa2292be1` |

## Closure Decision

All required Phase-7 B04 amplitude and reduced-M2 checks pass. The B04 Phase-7 workflow is `CLOSED` for the locked audited rules and approved `REDUCED_NR_TT` comparison layer.
