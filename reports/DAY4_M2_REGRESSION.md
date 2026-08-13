# Day 4 Native M2 Regression

Generated at: 2026-08-13T14:55:56.8510608+08:00
Run root: runs/day4_native/20260813_145016
Execution policy: bounded Wolfram processes, 180 s timeout per benchmark. No timeout occurred.

## Executive status

PASS

| benchmark | status | runtime s | DONE sentinel | comparison |
| --- | --- | ---: | --- | --- |
| B01 e- e+ -> mu- mu+ | PASS | 10.165 | yes | FCCompareResults CORRECT; equivalence True |
| B02 e- gamma -> e- gamma | PASS | 7.734 | yes | FCCompareResults CORRECT; equivalence True |
| B03 e- mu- -> e- mu- | PASS | 5.956 | yes | FCCompareResults CORRECT; equivalence True |

## Official Example Patterns Used

| benchmark | installed example | pattern notes |
| --- | --- | --- |
| B01 | ElAel-MuAmu.m | FCClearScalarProducts[]; SetMandelstam[s,t,u,p1,p2,-k1,-k2,me,me,mmu,mmu]; FeynAmpDenominatorExplicit; FermionSpinSum[..., ExtraFactor -> 1/2^2]; DiracSimplify; bounded Simplify; FCCompareResults. |
| B02 | ElGa-ElGa.m | Same native Compton pattern with TransversePolarizationVectors -> {k1,k2} and DoPolarizationSums[..., k1, 0], DoPolarizationSums[..., k2, 0] only. No fermion momenta were passed to polarization sums. |
| B03 | ElMu-ElMu.m | FCClearScalarProducts[]; process-correct electron-muon SetMandelstam; FeynAmpDenominatorExplicit; FermionSpinSum[..., ExtraFactor -> 1/2^2]; DiracSimplify; bounded Simplify; FCCompareResults. |

## B01 Result

Massless M2:

~~~text
(2*(t^2 + u^2)*SMP["e"]^4)/s^2
~~~

Gold target:

~~~text
(2*(t^2 + u^2)*SMP["e"]^4)/s^2
~~~

Comparison:

~~~text
<|"fc_compare_status" -> True, "equivalence" -> True, "status" -> "PASS"|>
~~~

Artifacts: runs/day4_native/20260813_145016/B01_ee_to_mumu/
Script SHA256: e808f1e2d6563b61f8c6328c9586f30bbe2a7f3f2f227c56c08a2bd2cf6d9205

## B02 Result

Massive simplified M2:

~~~text
(2*SMP["e"]^4*(-(s*u*(s^2 + u^2)) + (s^3 + 7*s^2*u + 7*s*u^2 + u^3)*SMP["m_e"]^2 - (3*s^2 + 14*s*u + 3*u^2)*SMP["m_e"]^4 + 6*SMP["m_e"]^8))/((s - SMP["m_e"]^2)^2*(u - SMP["m_e"]^2)^2)
~~~

Official known result expression:

~~~text
2*SMP["e"]^4*((s/2 - SMP["m_e"]^2/2)/(-1/2*u + SMP["m_e"]^2/2) + (-1/2*u + SMP["m_e"]^2/2)/(s/2 - SMP["m_e"]^2/2) + 2*SMP["m_e"]^2*((s/2 - SMP["m_e"]^2/2)^(-1) - (-1/2*u + SMP["m_e"]^2/2)^(-1)) + SMP["m_e"]^4*((s/2 - SMP["m_e"]^2/2)^(-1) - (-1/2*u + SMP["m_e"]^2/2)^(-1))^2)
~~~

Massless limit recorded:

~~~text
(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
~~~

Official known massless limit:

~~~text
(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)
~~~

Comparison:

~~~text
<|"fc_compare_status" -> True, "equivalence" -> True, "status" -> "PASS"|>
~~~

Artifacts: runs/day4_native/20260813_145016/B02_compton/
Script SHA256: 631e83279bb8548431177d411e36223cf634040cd02f2f52e931d0a50ce19533

## B03 Result

Massless M2:

~~~text
(2*(s^2 + u^2)*SMP["e"]^4)/t^2
~~~

Gold target:

~~~text
(2*(s^2 + u^2)*SMP["e"]^4)/t^2
~~~

Comparison:

~~~text
<|"fc_compare_status" -> True, "equivalence" -> True, "status" -> "PASS"|>
~~~

Artifacts: runs/day4_native/20260813_145016/B03_emu_to_emu/
Script SHA256: 0b31cf851b6d88acfbae67176e34886383b8b412583651a5c61193a221046a3c

## Saved Outputs

Each benchmark directory contains:

- m2_regression.wl
- m2_raw.m and m2_raw.inputform.txt
- m2_simplified.m and m2_simplified.inputform.txt
- known_result.m and known_result.inputform.txt
- comparison_result.inputform.txt
- runtime_seconds.txt
- stdout.log and stderr.log
- SHA256SUMS.txt
- DONE only because the benchmark passed

B01 and B03 also contain m2_massless.*. B02 contains m2_massless.* and known_massless.*.

## Warnings

FeynCalc emitted FrontEndObject::notavail in stdout for all three headless runs. This is consistent with loading/printing in a front-end-free wolframscript process and did not affect comparison results. All stderr.log files are empty.

## Guardrails Confirmed

- FCClearScalarProducts[] used in all benchmarks.
- Process-correct SetMandelstam used in all benchmarks.
- FeynAmpDenominatorExplicit applied before spin and polarization sums.
- FermionSpinSum used with ExtraFactor -> 1/2^2 for initial-state averaging.
- Massless photon polarization sums used only for B02 photon momenta k1 and k2 via DoPolarizationSums[..., k, 0].
- No polarization sums were called on fermion momenta.
- DiracSimplify used and final simplification was wrapped in TimeConstrained.
- Raw M2 was saved before final simplification.
- FCCompareResults and an explicit equivalence check both passed.
- All outputs were saved under runs/day4_native/20260813_145016/.
