# QED Convention Audit

Audit timestamp: 2026-08-12T19:34:29.0947130+08:00

Verdict: PASS WITH WARNINGS

This bounded audit checks the currently used QED rules in `rules/qed/qed_tree_v1.yaml`
before amplitude generation. No squared amplitudes were computed.

## Declared Project Convention

- Metric: `diag(+,-,-,-)`, recorded in cards as `metric_signature: +---`.
- Lagrangian:
  `L_QED = -1/4 F_mu_nu F^mu_nu + psi_bar (i slash(partial) - m) psi - e psi_bar gamma^mu A_mu psi`.
- Tree vertex: `-i e gamma^mu`.
- Fermion propagator: `i (slash(q)+m)/(q^2-m^2+i epsilon)`.
- Photon propagator in Feynman gauge: `-i g^mu nu/(q^2+i epsilon)`.

## Rule Audit Table

| rule_id | project formula | FeynCalc representation | audit status | notes |
|---|---|---|---|---|
| `rule:qed_tree_v1:e_e_gamma_vertex` | `-i e gamma^mu` | `-I e GA[mu]` | `AUDITED_EQUIVALENT_AFTER_CONVENTION_MAP` | Matches the declared project and stored FeynCalc convention directly. Bundled FeynArts QED uses `I FCGV["EL"]` for the lepton-photon classes coupling, and local FeynCalc `FeynArtsSigns.md` documents the FeynArts lepton-gauge vertex as `+i e gamma^mu`; using FeynArts amplitudes therefore requires an explicit vertex-sign map relative to this project. |
| `rule:qed_tree_v1:mu_mu_gamma_vertex` | `-i e gamma^mu` | `-I e GA[mu]` | `AUDITED_EQUIVALENT_AFTER_CONVENTION_MAP` | Same project/FeynCalc match and same FeynArts sign map as the electron vertex, with generation index selecting the muon class. |
| `rule:qed_tree_v1:electron_propagator` | `i (slash(q)+m)/(q^2-m^2+i epsilon)` | `I (GS[q] + m)/(SP[q, q] - m^2 + I epsilon)` | `AUDITED_EQUIVALENT_AFTER_CONVENTION_MAP` | Stored FeynCalc template matches the declared project line momentum `q`. Bundled FeynArts generic QED writes the internal fermion numerator as `FADiracSlash[-mom] + Mass[F[i]]` times `I FAPropagatorDenominator[mom, Mass[F[i]]]`; this is equivalent only after recording the FeynArts internal line momentum map `q_project = -mom_FA` for that oriented line. |
| `rule:qed_tree_v1:photon_propagator` | `-i g^mu nu/(q^2+i epsilon)` | `-I MT[mu, nu]/(SP[q, q] + I epsilon)` | `AUDITED_MATCH` | Stored FeynCalc template matches the declared Feynman-gauge propagator. Bundled FeynArts generic QED gives `-I FAPropagatorDenominator[mom, Mass[V[i]]]` times the covariant-gauge tensor; with photon mass zero and `FAGaugeXi[A] = 1`, this reduces to the project formula. |

No rule used in B01/B02 is marked `CONFLICT_REQUIRES_REVIEW`; the stop condition was not triggered.

## Local Backend Evidence

- FeynCalc syntax probe: `runs/qed_convention_audit/feyncalc_template_syntax_check.wl`.
- FeynCalc version from the probe: `10.1.0`.
- FeynArts symbols loaded through FeynCalc: `324`.
- FeynCalc metric signature from `FCGetMetricSignature[]`: `{1, -1}`, matching `diag(+,-,-,-)`.
- Local FeynCalc documentation `FCSetMetricSignature.md` states the default is `(1,-1,-1,-1)`.
- Local FeynCalc documentation `Extra/FeynArtsSigns.md` documents FeynArts' tree-level prefactor behavior and the lepton-photon vertex sign difference relative to Peskin-style `-i e gamma^mu`.
- Local FeynArts files inspected: bundled `FeynArts/Models/QED.mod` and `FeynArts/Models/QED.gen`.
- Local FeynCalc examples inspected but not run: `Examples/QED/Tree/Mathematica/ElAel-MuAmu.m` and `Examples/QED/Tree/Mathematica/ElGa-ElGa.m`.

## FeynCalc Syntax Check Result

Command:

```text
wolframscript -file runs\qed_convention_audit\feyncalc_template_syntax_check.wl
```

Result: `PASS`, exit code `0`.

Output summary:

```text
FEYNCALC_VERSION="10.1.0"
FEYNARTS_SYMBOLS=324
FEYNCALC_METRIC_SIGNATURE={1, -1}
LOCAL_TIMESTAMP=2026-08-12T19:34:02
TEMPLATE_CHECK|rule:qed_tree_v1:e_e_gamma_vertex|PASS|syntax=True|parsed_head=HoldComplete|fci_head=Times
TEMPLATE_CHECK|rule:qed_tree_v1:mu_mu_gamma_vertex|PASS|syntax=True|parsed_head=HoldComplete|fci_head=Times
TEMPLATE_CHECK|rule:qed_tree_v1:electron_propagator|PASS|syntax=True|parsed_head=HoldComplete|fci_head=Times
TEMPLATE_CHECK|rule:qed_tree_v1:photon_propagator|PASS|syntax=True|parsed_head=HoldComplete|fci_head=Times
OVERALL_TEMPLATE_SYNTAX_STATUS=PASS
```

Warnings observed during package startup:

```text
FrontEndObject::notavail: A front end is not available; certain operations require a front end.
```

These did not affect the batch syntax check result.

## Momentum and External-State Conventions

B01 and B02 convention cards explicitly set:

- `all_momenta_incoming_vertex_convention: true`
- physical incoming momenta for incoming particles
- physical outgoing momenta for outgoing particles
- `propagator_momentum_flow: explicit_per_line`

DiagramIR slot bindings implement the conversion as:

- incoming physical external leg: `momentum_substitution = p`
- outgoing physical external leg: `momentum_substitution = -p`
- internal line: explicit oriented `q` with each vertex slot recording `q` or `-q`

The generator implementation in `src/feynagent/diagrams/topology.py` matches this convention:
`_external_binding` keeps incoming labels unchanged and negates outgoing labels.

External Dirac state mapping is verified at the topology/field-orientation level:

| physical state | project spinor | stored field orientation | flow direction |
|---|---|---|---|
| incoming fermion | `u` | `psi` | `into_vertex` |
| outgoing fermion | `ubar` | `psi_bar` | `out_of_vertex` |
| incoming antifermion | `vbar` | `psi_bar` | `out_of_vertex` |
| outgoing antifermion | `v` | `psi` | `into_vertex` |

The regression test `test_external_dirac_fermion_flow_truth_table` checks these four cases for B01.

## Trust and Provenance

No rule was promoted to fully trusted. After user review and approval at `2026-08-12T19:48:05.9409820+08:00`, the four QED rules used by B01/B02 were promoted from `validated_pending_convention_review` to `validated`.

The existing registry provenance still contains historical `source_type: standard_convention` entries. Each promoted rule now also preserves that provenance and appends a `local_file` provenance entry pointing to this audit report.

## Post-Audit Approval

User approval was recorded at `2026-08-12T19:48:05.9409820+08:00`. Amplitude generation is approved for B01 and B02 only. Heavy calculation remains unapproved.

Remaining implementation constraints:

1. FeynArts-derived amplitude builders must apply the documented vertex-sign, prefactor, and momentum maps explicitly.
2. Future FeynArts use must set or assert Feynman gauge with `FAGaugeXi[A] = 1` before relying on the photon-propagator match.
3. This approval does not extend the QED registry beyond the B01/B02 tree-level use cases audited here.
