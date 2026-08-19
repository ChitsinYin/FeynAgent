# Day-7 B04 Backend Feasibility

## Scope

This is a bounded backend-feasibility decision for the locked B04 custom gravity model
`reheating_scalar_gravity_v1`, process `phi(p1) phi(p2) -> h(k1) h(k2)`.

No trusted rule, convention, benchmark gold file, or source-of-truth status was changed.
No full squared amplitude was computed. No final B04 amplitude pipeline was implemented.

## Authority And Lock Check

- Physics authority: externally locked gravity knowledge package registered by
  `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml`.
- Lock verifier: `python scripts/verify_knowledge_lock.py --model-id reheating_scalar_gravity_v1`.
- Result: `custom_model:reheating_scalar_gravity_v1 AVAILABLE`; `checked_hashes: 19`;
  readiness `KNOWLEDGE_READY_FOR_B04`; process `process:B04_phi_phi_to_h_h`.
- Required locked rules:
  - `propagator:phi`
  - `vertex:h_phi_phi`
  - `propagator:h`
  - `vertex:h_h_h`
  - `vertex:h_h_phi_phi`
  - `polarization_sum:massless_graviton_b04`
- Canonical normalization: `kappa = 2/M_P`, metric signature `+---`, weak-field expansion
  `g_mu_nu = eta_mu_nu + kappa h_mu_nu + ...`, de Donder graviton propagator.
- FeynGrav policy from the lock: helper/validator only; never an authority. The historical
  FeynGrav 3.0 scalar-scalar-graviton-graviton/contact candidate remains rejected as a
  source of truth.

`KNOWLEDGE_LOCK_MATCH = YES`

## Route A - DIRECT_FEYNCALC_CUSTOM

Status: `FEASIBLE_PRIMARY`

Architecture evaluated:

`structured custom RuleRegistry / DiagramIR + generic custom topology layer + deterministic Mathematica/FeynCalc tensor assembly`

Findings:

| Question | Decision |
| --- | --- |
| Required fields representable? | Yes. The existing RuleRegistry schema already admits `scalar` and `symmetric_rank_2_tensor`; `phi` is self-conjugate scalar and `h` is self-conjugate rank-2 tensor. |
| Every required vertex representable? | Yes as explicit audited tensor templates sourced from the lock: `h_phi_phi`, `h_h_h`, and `h_h_phi_phi`. The three-graviton rule should preserve the locked compact symmetrized form until deterministic expansion rules are explicitly implemented. |
| Exact gravity normalization preservable? | Yes. Use explicit symbolic `kappa` with locked substitution `kappa = 2/M_P`; do not import normalization from FeynGrav or FeynArts. |
| Momentum ordering preservable? | Yes. Existing DiagramIR slot bindings preserve physical external momenta, outgoing crossing to all-momenta-incoming vertices, and internal routing labels. B04 requires careful fixed maps for `k1-p1`, `k2-p1`, and `p1+p2`. |
| Topology generation possible? | Yes. FeynCalc need not enumerate diagrams. Use the existing generic custom 2-to-2 topology machinery and extend/adapt inputs through a custom gravity RuleRegistry, without hard-coding B04 topology into the core enumerator. |
| Per-diagram amplitude possible? | Yes. Assemble each DiagramIR instance into explicit FeynCalc expressions using `MTD`, `FVD`, `SPD`, denominator factors, and rank-2 index pairs. Keep per-diagram expressions separate before any total amplitude step. |
| Trusted gold comparison possible? | Yes, at the per-diagram/reduced-expression level against locked gold summaries and later against locked gold files by hash-gated access. Do not recompute full M2 in this phase. |
| New source-of-truth risk | Low if the RuleRegistry stores locked formulas/provenance and the FeynCalc assembler is only an algebra renderer. Risk rises if helper output is promoted into canonical rules. |
| Expected engineering complexity | Medium. Main work is a deterministic tensor-template assembler, index allocator, momentum substitution layer, and compact symmetry-expansion handling for `h_h_h`. |
| Expected failure modes | Sign/crossing mistakes, dummy-index collisions, premature manual expansion of the three-graviton vertex, contact-term normalization drift, accidental FeynGrav contact substitution, and current DiagramIR/object-id casing friction for external B04 process IDs. |
| Prototype evidence | FeynCalc 10.1.0 accepts explicit rank-2 graviton propagator structure built from metric tensors and scalar products; a tiny local probe contracted `MTD[mu,nu] FVD[p,mu]` to `Pair[LorentzIndex[nu,D], Momentum[p,D]]`. The project RuleRegistry schema includes `symmetric_rank_2_tensor`. |

Important architecture decision:

FeynCalc is selected for tensor/amplitude algebra only. It should not be treated as the
diagram-topology enumerator for B04. The preferred topology path is the existing generic
custom DiagramIR/topology machinery, with no B04-specific hard-code in the core enumerator.

Implementation caveat:

The current DiagramIR schema/generator path should be checked before persisting B04
DiagramIR because B04 imports an external process spelling with uppercase `B04`. This is
an engineering serialization concern, not a physics-convention change.

## Route B - CUSTOM_FEYNARTS_NATIVE

Status: `NOT_FEASIBLE_WITHIN_BOUNDED_SPIKE`

Bounded spike evidence:

- Installed FeynArts: 3.12, loaded through the FeynCalc add-on path.
- Installed model files include the standard `Lorentz`, `QED`, `SM`, MSSM/THDM/SQCD-style
  models, and related variants.
- Installed generic-model declarations expose `S`, `F`, `V`, `SV`, and `U` kinematic
  field classes; no clean shipped rank-2/spin-2 generic field class was found.

Findings:

| Question | Decision |
| --- | --- |
| Required fields representable? | Partially. `phi` as a scalar is clean. The required graviton/spin-2 field is not cleanly represented by the installed generic FeynArts model layer within this spike. |
| Every required vertex representable? | Not cleanly. Scalar and scalar-vector-style patterns exist, but the rank-2 graviton, three-graviton vertex, and `hh_phi_phi` contact rule would require substantial custom generic/classes-model work. |
| Exact gravity normalization preservable? | Theoretically possible in a custom model, but not demonstrated within the bounded spike. |
| Momentum ordering preservable? | Risky. FeynArts generic coupling permutation/flipping machinery would need careful custom closure rules for high-rank tensor expressions. |
| Topology generation possible? | Generic graph topology is possible, but native field insertion for the required spin-2 model is not cleanly supported by the installed model set. |
| Per-diagram amplitude possible? | Not cleanly within the bounded spike. |
| Trusted gold comparison possible? | Only after a substantial custom spin-2 model/adapter exists and has its own audit trail. |
| New source-of-truth risk | Medium to high. A new FeynArts gravity model could silently become a competing rule source unless tightly generated from the locked RuleRegistry. |
| Expected engineering complexity | High. This becomes a custom spin-2 FeynArts framework, not a bounded backend adapter. |
| Expected failure modes | Missing spin-2 field semantics, wrong symmetrization under field permutations, FCFAConvert incompatibilities, normalization drift, and opaque model-file debugging. |
| Prototype evidence | File-level spike found no installed rank-2 generic model declaration such as a tensor `KinematicIndices`/propagator/coupling family. |

Conclusion:

Do not select FeynArts-native as the primary B04 backend now. It may be revisited only if a
separate reviewed spin-2 FeynArts model project is explicitly authorized.

## Route C - FEYNGRAV_ASSISTED

Status: `AVAILABLE_LIMITED_VALIDATOR`

Bounded inspection:

- Local FeynGrav 3.0 package is present.
- It exposes scalar propagator, graviton propagator, graviton-scalar vertices, graviton
  self-interaction vertices, and polarization-tensor helpers.
- The locked B04 package explicitly rejects historical FeynGrav 3.0 scalar-scalar-graviton-
  graviton/contact output as authority due to the recorded factor conflict.

Findings:

| Question | Decision |
| --- | --- |
| Required fields representable? | Yes as helper functions, not as FeynAgent canonical fields. |
| Every required vertex representable? | Partially. Several required structures are available as helper functions, but the contact rule has an explicit locked conflict and must not be imported as authority. |
| Exact gravity normalization preservable? | Only if all FeynGrav output is wrapped by locked normalization checks. FeynGrav must not define `kappa` for B04. |
| Momentum ordering preservable? | Possible only with explicit locked momentum maps. |
| Topology generation possible? | No. FeynGrav is not selected as topology enumerator. |
| Per-diagram amplitude possible? | Possible as an independent tensor cross-check for selected vertices, not as the canonical assembly path. |
| Trusted gold comparison possible? | Yes as secondary comparison evidence for non-conflicting rules; no for the rejected contact candidate as authority. |
| New source-of-truth risk | High if used directly; acceptable only as a labeled validator/helper behind the locked RuleRegistry. |
| Expected engineering complexity | Low to medium for targeted probes; high if promoted into backend generation. |
| Expected failure modes | Contact-rule factor mismatch, hidden convention differences, gauge/normalization assumptions, and accidental replacement of locked formulas. |
| Prototype evidence | Local package inspection found FeynGrav 3.0 and relevant symbols including `GravitonScalarVertex`, `GravitonPropagator`, `GravitonVertex`, and polarization helpers. |

Conclusion:

Use FeynGrav only as an optional secondary validator for selected tensor/rule cross-checks.
It must never override the locked project rules.

## Decision

`PRIMARY_BACKEND = DIRECT_FEYNCALC_CUSTOM`

`SECONDARY_VALIDATOR = FEYNGRAV_ASSISTED_LIMITED`

Rationale:

Route A matches the project boundary: custom audited rules remain the authority, generic
DiagramIR/topology handles enumeration, and FeynCalc performs deterministic tensor algebra.
Route B would require a larger spin-2 FeynArts-native framework than this bounded phase
permits. Route C is available but carries explicit source-of-truth risk and one known
rejected historical candidate.

`READY_FOR_B04_TOPOLOGY = YES`

Meaning: ready to proceed with a B04 topology-generation implementation using the generic
custom topology/DiagramIR path, not with final amplitude or M2 construction. Before
persisted B04 DiagramIR artifacts, resolve the external-process-ID serialization caveat in
a schema-compatible way and record that migration explicitly.

## Return Summary

```text
KNOWLEDGE_LOCK_MATCH = YES
ROUTE_A = FEASIBLE_PRIMARY
ROUTE_B = NOT_FEASIBLE_WITHIN_BOUNDED_SPIKE
ROUTE_C = AVAILABLE_LIMITED_VALIDATOR
PRIMARY_BACKEND = DIRECT_FEYNCALC_CUSTOM
SECONDARY_VALIDATOR = FEYNGRAV_ASSISTED_LIMITED
READY_FOR_B04_TOPOLOGY = YES
```

## Regression Addendum

```text
STANDARD_QED_REGRESSION = PASS
```

Regression command: `python -m pytest`

Regression result: 96 passed in 10.84 seconds.
