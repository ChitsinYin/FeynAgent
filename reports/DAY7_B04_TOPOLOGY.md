# Day-7 B04 Topology Closure

- Knowledge lock hash: `19cfb8a8de198a104c23909148aa577889c50212277bae2c0887ffe265c7c1c6`
- Primary backend: `DIRECT_FEYNCALC_CUSTOM`
- Scope: topology generation, structural gold comparison, and diagram rendering only.
- Amplitudes: not calculated.
- M2: not calculated.
- Reheating/nonrelativistic approximations: not applied.

## Gold Topology

- `a`: scalar_exchange, internal=phi, momentum=k1-p1
- `b`: scalar_exchange, internal=phi, momentum=k2-p1
- `c`: s_channel_graviton_exchange, internal=h, momentum=p1+p2
- `d`: contact_h_h_phi_phi, internal=None, momentum=None

## Generated Topology

- `diagram:generated:b04-phi-phi-to-h-h:s:h`: channel=s, internal=h, momentum=p1+p2, order=kappa^2, rules=vertex:h_h_h, vertex:h_phi_phi, propagator:h
- `diagram:generated:b04-phi-phi-to-h-h:t:phi`: channel=t, internal=phi, momentum=p1-k1, order=kappa^2, rules=vertex:h_phi_phi, propagator:phi
- `diagram:generated:b04-phi-phi-to-h-h:u:phi`: channel=u, internal=phi, momentum=p1-k2, order=kappa^2, rules=vertex:h_phi_phi, propagator:phi
- `diagram:generated:b04-phi-phi-to-h-h:contact:h_h_phi_phi`: channel=contact, internal=None, momentum=None, order=kappa^2, rules=vertex:h_h_phi_phi

## Structural Comparison

| Gold | Generated | Classification | Representation Map |
| --- | --- | --- | --- |
| a | diagram:generated:b04-phi-phi-to-h-h:t:phi | MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP | internal momentum differs by internal-line orientation sign |
| b | diagram:generated:b04-phi-phi-to-h-h:u:phi | MATCH_AFTER_EXPLICIT_REPRESENTATION_MAP | internal momentum differs by internal-line orientation sign |
| c | diagram:generated:b04-phi-phi-to-h-h:s:h | MATCH |  |
| d | diagram:generated:b04-phi-phi-to-h-h:contact:h_h_phi_phi | MATCH |  |

## Rule Usage

- Audit: `PASS`
- Used rules: `propagator:h`, `propagator:phi`, `vertex:h_h_h`, `vertex:h_h_phi_phi`, `vertex:h_phi_phi`
- Unexpected rules: none

## Diagram Artifact

- PDF: `E:/003hep-ph-research/Agent/FeynAgent/runs/day7_final_b04_diagram_labels_20260819/diagrams/diagrams.pdf`
- PDF sha256: `ea59ae5f9e87bae9ed7bb80dfa0dc9e6a28c9af798d689030eb71b75d715701e`

## Representation Maps

- Scalar-exchange internal momenta are compared up to internal-line orientation: `p1-k1` maps to `-(k1-p1)` and `p1-k2` maps to `-(k2-p1)`.
- External outgoing gravitons are crossed to all-momenta-incoming vertex bindings by the existing DiagramIR convention conversion.
- FeynCalc is reserved for the later amplitude algebra phase and is not used as a topology enumerator here.

## Tests

- Focused label regression: `python -m pytest tests\test_b04_topology_phase5.py -k b04_tex -q` -> PASS, `1 passed, 8 deselected`. Final repository regression: `python -m pytest` -> PASS, `122 passed`.

## Warnings

- Scalar-exchange gold momenta match generated routing only after explicit internal-line orientation mapping.
- Diagram rendering is presentation-only and does not modify DiagramIR physics.
- FeynCalc is intentionally unused in Phase 5 except as the selected future algebra backend.
