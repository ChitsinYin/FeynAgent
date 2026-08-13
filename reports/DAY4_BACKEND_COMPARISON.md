# Day 4 Backend Comparison

Generated at: 2026-08-13T15:08:11.8609147+08:00
Comparison run root: runs/day4_backend_comparison/20260813_150031
Legacy structural summary SHA256: 4a10f21c4d05d7d0a903ec34f485079dd4045e9a18122913cb9461d576917892

## Executive status

PASS WITH WARNINGS

Native FeynArts/FeynCalc remains the primary standard-sector regression reference. The legacy custom backend agrees with B01/B02 at the physics-structure level, but direct squared-amplitude equality requires an explicit representation/convention map. B03 is not supported by the current legacy benchmark entry path without changing the B03 native-only card or adding benchmark-specific glue.

## Classification

| benchmark | classification | short reason |
| --- | --- | --- |
| B01 | CONVENTION_MAP_REQUIRED | Diagram/amplitude structure agrees; M2 agrees only after mapping legacy explicit denominators/coupling/regulator to FeynCalc benchmark conventions. |
| B02 | CONVENTION_MAP_REQUIRED | s/u structure, electron propagators, and photon conjugation agree; M2 agrees only after the same explicit map. |
| B03 | LEGACY_LIMITATION | Native backend supports and passes B03; legacy generation refuses the current B03 card because it is scoped to `native:feynarts_sm_qedonly`, and the legacy CLI only whitelists B01/B02. |

## Comparison Scope

Compared physics-level invariants only:

- diagram count
- channel assignment
- internal species
- internal momentum routing up to momentum-conservation/channel maps
- external fermion/antifermion wavefunction classes
- photon polarization conjugation
- number and relative structure of amplitude terms
- squared amplitude after the same averaging and kinematics convention

Ignored by design: dummy-index names, raw expression ordering, global phase, and formatting.

## Convention/Representation Map Used for M2

The native backend emits official `FCFAConvert` FeynCalc structures using `SMP["e"]`, `Spinor[...]`, `FeynAmpDenominator[...]`, and FeynCalc polarization objects. The legacy renderer emits explicit pedagogical structures using `e`, `SpinorU`/`SpinorUBar`/`SpinorV`/`SpinorVBar`, `SP[...]` denominators with an explicit `epsilon`, and `PolarizationVector` factors.

For the bounded M2 comparison, the following map was applied after the same spin/polarization averaging pattern:

- identify legacy `e` with native `SMP["e"]`;
- take the benchmark gold limit `epsilon -> 0`;
- map explicit legacy channel denominators to Mandelstam variables, e.g. B01 `Pair[Momentum[p1+p2], Momentum[p1+p2]] -> s`;
- B02 maps `Pair[Momentum[p1+k1], Momentum[p1+k1]] -> s` and `Pair[Momentum[k2-p1], Momentum[k2-p1]] -> u`, then applies the massless Compton relation `s+t+u=0` via `TrickMandelstam`.

No native backend code was patched to reproduce a legacy expression.

## B01: e- e+ -> mu- mu+

| invariant | native FeynArts/FeynCalc | legacy custom | result |
| --- | --- | --- | --- |
| diagram count | 1 | 1 | agree |
| channel assignment | s-channel annihilation | s-channel annihilation | agree |
| internal species | photon | photon | agree |
| internal momentum routing | FeynCalc route appears as final-pair momentum `p3+p4`; by conservation equals `p1+p2` | `q_s = p1+p2` | equivalent after channel map |
| external wavefunctions | incoming e-/e+ and outgoing mu-/mu+ spinors from FeynArts | `u(p1)`, `vbar(p2)`, `ubar(p3)`, `v(p4)` | agree |
| photon polarization conjugation | not applicable | not applicable | agree |
| amplitude terms | one term | one `amp_s` term with two currents linked by photon propagator | agree |
| M2 | native massless gold below | legacy mapped result below | agree after convention map |

Native/official massless M2:

~~~text
(2*(t^2 + u^2)*SMP["e"]^4)/s^2
~~~

Legacy mapped M2:

~~~text
(2*(t^2 + u^2)*SMP["e"]^4)/s^2
~~~

Legacy equivalence record:

~~~text
<|"mapped" -> (2*(t^2 + u^2)*SMP["e"]^4)/s^2, "known" -> (2*(t^2 + u^2)*SMP["e"]^4)/s^2, "equivalence" -> True|>
~~~

Classification: CONVENTION_MAP_REQUIRED.

## B02: e- gamma -> e- gamma

| invariant | native FeynArts/FeynCalc | legacy custom | result |
| --- | --- | --- | --- |
| diagram count | 2 | 2 | agree |
| channel assignment | s-like and u-like Compton electron-exchange terms | `amp_s`, `amp_u` | agree |
| internal species | electron | electron | agree |
| internal momentum routing | FeynCalc routes equivalent to s/u electron denominators under external conservation | `q_s=p1+k1`, `q_u=p1-k2` | equivalent after channel map |
| external wavefunctions | incoming/outgoing electron spinors | `u(p1)`, `ubar(p2)` | agree |
| photon polarization conjugation | incoming photon ordinary, outgoing photon conjugate | incoming `none`, outgoing `complex_conjugate` | agree |
| amplitude terms | two terms | `amp_s + amp_u` | agree |
| M2 | native massless Compton gold below | legacy mapped result below | agree after convention map |

Native/official massless M2:

~~~text
(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
~~~

Legacy mapped M2:

~~~text
(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
~~~

Legacy equivalence record:

~~~text
<|"mapped" -> (-2*(s^2 + u^2)*SMP["e"]^4)/(s*u), "known" -> (-2*(s^2 + u^2)*SMP["e"]^4)/(s*u), "equivalence" -> True|>
~~~

Classification: CONVENTION_MAP_REQUIRED.

## B03: e- mu- -> e- mu-

| invariant | native FeynArts/FeynCalc | legacy custom | result |
| --- | --- | --- | --- |
| diagram count | 1 | not generated | legacy limitation |
| channel assignment | t-channel photon exchange | not generated | legacy limitation |
| internal species | photon | not generated | legacy limitation |
| internal momentum routing | native denominator equivalent to t-channel transfer | not generated | legacy limitation |
| external wavefunctions | electron and muon spinor currents | not generated | legacy limitation |
| photon polarization conjugation | not applicable | not applicable | not applicable |
| amplitude terms | one term | not generated | legacy limitation |
| M2 | native massless gold below | not generated | legacy limitation |

Native/official massless M2:

~~~text
(2*(s^2 + u^2)*SMP["e"]^4)/t^2
~~~

Legacy refusal probe:

~~~text
ERROR: PhysicsCard selected registry_id does not match RuleRegistry
~~~

Classification: LEGACY_LIMITATION.

## Diagnostics

Generated comparison artifacts:

- `runs/day4_backend_comparison/20260813_150031/legacy_structural_summary.json`
- B01/B02 fresh legacy `generated_diagrams.yaml`
- B01/B02 fresh legacy `legacy_amplitude_ir.yaml`
- B01/B02 `legacy_amplitudes.wl` and `legacy_amplitudes.tex`
- B01/B02 bounded `legacy_m2_probe.wl` and `legacy_m2_map_compare.wl` logs
- B03 clean legacy refusal logs

The legacy M2 probes emitted only FeynCalc headless `FrontEndObject::notavail` messages, matching the native smoke/M2 runs. No B03 legacy M2 was attempted because no legacy B03 amplitude was generated.

## Recommendation

Recommendation: keep the legacy backend as custom/fallback and regression/pedagogy reference, not as the production standard QED backend. Before relying on it for future custom models beyond structural AmplitudeIR generation, repair or formalize the executable FeynCalc convention map so squared-amplitude checks do not depend on ad hoc renderer-head and denominator substitutions.

Operationally:

- Standard QED/SM production should continue to use `feynarts_feyncalc_native`.
- Legacy custom backend should remain available for reference, fallback, and future nonstandard-rule prototyping.
- Future custom-model work should either implement a FeynArts-compatible model/adapter or make the legacy-to-FeynCalc map explicit and tested before using M2 results as validation evidence.
