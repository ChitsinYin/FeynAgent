# Day 2 FeynArts Topology Cross-Check

## Executive Status

PASS WITH WARNINGS

This is a bounded independent topology/field-content cross-check only. FeynArts is not the canonical physics source for FeynAgent, and no DiagramIR, rule registry, benchmark gold file, or amplitude object was modified from FeynArts output.

## Raw Artifacts

Run directory:

```text
runs/day2_feynarts_crosscheck/20260812_154018/
```

Preserved final script and logs:

```text
runs/day2_feynarts_crosscheck/20260812_154018/feynarts_crosscheck_day2.wl
runs/day2_feynarts_crosscheck/20260812_154018/feynarts_crosscheck.stdout.log
runs/day2_feynarts_crosscheck/20260812_154018/feynarts_crosscheck.stderr.log
```

Additional bounded probe logs from setup discovery are preserved in the same run directory.

## Exact FeynArts Configuration

```text
Fresh process command:
wolframscript -file runs/day2_feynarts_crosscheck/20260812_154018/feynarts_crosscheck_day2.wl

Load method:
$LoadFeynArts = True;
<< FeynCalc`

FeynArts source:
C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\FeynArts

FeynCalc version:
10.1.0

FeynArts version:
3.12 (27 Mar 2025), patched for use with FeynCalc

Model:
Model -> "SM"
GenericModel -> "Lorentz"
InsertionLevel -> {Particles}

Topology:
CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]
```

No custom FeynArts model was built. No amplitudes were generated.

## B02 Compton Target

FeynAgent benchmark:

```text
e-(p1) + gamma(k1) -> e-(p2) + gamma(k2)
```

FeynArts field/model mapping:

```text
e-    -> F[2, {1}]
gamma -> V[1]
outgoing e- appears in particle insertion rules as -F[2, {1}]
```

FeynArts insertion command:

```text
InsertFields[
  top,
  {F[2, {1}], V[1]} -> {F[2, {1}], V[1]},
  Model -> "SM",
  GenericModel -> "Lorentz",
  InsertionLevel -> {Particles}
]
```

Result:

```text
B02_PARTICLE_INSERTION_COUNT=2
B02_CHANNELS={"s", "u"}
B02_FIELD_CONTENT={F[2, {1}], V[1], -F[2, {1}]}
B02_INTERNAL_FIELDS={F[2, {1}], F[2, {1}]}
B02_NON_QED_FIELD_CONTENT={}
B02_CROSSCHECK_STATUS=PASS
```

Comparison to FeynAgent B02 expectation:

```text
Expected diagram count: 2
FeynArts particle insertion count: 2
Expected channels: s, u
FeynArts classified channels: s, u
Expected internal field: electron
FeynArts internal fields: F[2, {1}], F[2, {1}]
Mismatch: none
```

## Optional B01 Probe

FeynAgent benchmark:

```text
e-(p1) + e+(p2) -> mu-(p3) + mu+(p4)
```

FeynArts field/model mapping:

```text
e-  -> F[2, {1}]
e+  -> -F[2, {1}]
mu- -> F[2, {2}]
mu+ -> -F[2, {2}]
```

Result:

```text
B01_ALL_SM_PARTICLE_INSERTION_COUNT=4
B01_INTERNAL_FIELDS_ALL_SM={S[1], S[2], V[1], V[2]}
B01_PHOTON_ONLY_PARTICLE_INSERTION_COUNT=1
```

Interpretation:

The installed SM model includes non-QED s-channel insertions for this process. The photon-only subset contains exactly one insertion with internal `V[1]`, matching the FeynAgent B01 QED topology expectation. This optional check is recorded as a field-content subset observation, not as a canonical source.

## Warnings

- `Needs["FeynArts`"]` did not load FeynArts directly in the first probe. FeynArts loaded successfully through the locally installed FeynCalc setup with `$LoadFeynArts = True`.
- FeynCalc emitted front-end availability messages in the fresh `wolframscript` process. These did not block FeynArts topology insertion.
- For B01, the SM model also produced non-QED internal fields. Only the photon-only subset was compared to FeynAgent's pure-QED B01 benchmark.
- FeynArts formatting and field sign conventions were not used to modify FeynAgent canonical artifacts.

## Scope Guard

No amplitude generation, Dirac traces, polarization sums, Ward identity checks, FeynRules integration, loop calculations, or custom FeynArts model construction were performed.
