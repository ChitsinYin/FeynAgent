# FeynAgent Day 2 Review Package

## Repository Tree To Depth 4

```text
./
benchmarks/
  B00_environment/
    outputs/
      tikz_compile/
      .gitkeep
      commands_executed.txt
      tikz_compile.exitcode.txt
    README.md
    smoke_test.wl
    tikz_smoke_test.tex
  B01_ee_to_mumu/
    convention_card.yaml
    diagrams.yaml
    expected.yaml
    physics_card.yaml
    README.md
    rule_manifest.yaml
  B02_compton/
    convention_card.yaml
    diagrams.yaml
    expected.yaml
    physics_card.yaml
    README.md
    rule_manifest.yaml
  .gitkeep
  DAY2_BENCHMARK_SUMMARY.md
docs/
  ARCHITECTURE.md
  DESIGN_DECISIONS.md
  ENVIRONMENT_REPORT.md
  MIGRATION_0_1_0_TO_0_1_1.md
  SCOPE_V0_1.md
reports/
  .gitkeep
  DAY1_REPORT.md
  DAY1_REVIEW_PACKAGE.md
  DAY2_FEYNARTS_CROSSCHECK.md
  DAY2_REPORT.md
rules/
  qed/
    qed_tree_v1.yaml
  .gitkeep
runs/
  day2_benchmarks/
    20260812_141950/
      B01_ee_to_mumu/
      B02_compton/
      RUN_ID.txt
      SUMMARY.md
  day2_feynarts_crosscheck/
    20260812_154018/
      feynarts_crosscheck_day2.wl
      probe_b01.wl
      probe_b02_structure.wl
      probe_extract.wl
      probe_feynarts.wl
      probe_feynarts_via_feyncalc.wl
  day2_final_qa/
    20260812_155139/
      B01_ee_to_mumu/
      B02_compton/
      qa_summary.json
      RUN_ID.txt
  day2_render/
    20260812_151438/
      B01_ee_to_mumu/
    20260812_151557/
      B01_ee_to_mumu/
      B02_compton/
      RUN_ID.txt
      SUMMARY.md
  .gitkeep
schemas/
  .gitkeep
  convention_card.schema.json
  diagram_ir.schema.json
  physics_card.schema.json
  rule_registry.schema.json
scripts/
  .gitkeep
  generate_diagrams.py
  render_diagrams.py
  validate_examples.py
src/
  feynagent/
    diagrams/
      __init__.py
      topology.py
    render/
      __init__.py
      tikz.py
    __init__.py
tests/
  .gitkeep
  test_b02_compton.py
  test_day2_benchmarks.py
  test_schema_files.py
  test_tikz_renderer.py
  test_topology_generator.py
.gitignore
AGENTS.md
pyproject.toml
README.md
```

## Git Diff Summary From Day-1 Commit

Day-1 baseline commit: `ee10a679890cc367b2cc63ed8d9bc5a80c47610d`

```text
benchmarks/B02_compton/README.md            |  30 +-
 benchmarks/B02_compton/convention_card.yaml |   4 +-
 benchmarks/B02_compton/diagrams.yaml        | 212 +++++++++++--
 benchmarks/B02_compton/expected.yaml        |   2 +-
 benchmarks/B02_compton/physics_card.yaml    |  18 +-
 benchmarks/B02_compton/rule_manifest.yaml   | 128 +-------
 docs/ARCHITECTURE.md                        |   8 +-
 rules/qed/qed_tree_v1.yaml                  | 385 ++++++++++++++++-------
 schemas/convention_card.schema.json         | 102 ++++--
 schemas/diagram_ir.schema.json              | 452 +++++++++++++++++++++++----
 schemas/physics_card.schema.json            | 140 +++++++--
 schemas/rule_registry.schema.json           | 466 ++++++++++++++++++++++++----
 scripts/validate_examples.py                |   6 +-
 tests/test_b02_compton.py                   | 101 +++++-
 14 files changed, 1599 insertions(+), 455 deletions(-)
```

```text
M	benchmarks/B02_compton/README.md
M	benchmarks/B02_compton/convention_card.yaml
M	benchmarks/B02_compton/diagrams.yaml
M	benchmarks/B02_compton/expected.yaml
M	benchmarks/B02_compton/physics_card.yaml
M	benchmarks/B02_compton/rule_manifest.yaml
M	docs/ARCHITECTURE.md
M	rules/qed/qed_tree_v1.yaml
M	schemas/convention_card.schema.json
M	schemas/diagram_ir.schema.json
M	schemas/physics_card.schema.json
M	schemas/rule_registry.schema.json
M	scripts/validate_examples.py
M	tests/test_b02_compton.py
```

## Migration Summary

Schema/artifact version `0.1.1` closes the Day-1 semantic gaps required before generation/rendering: explicit vertex rule-slot bindings, particle/conjugation metadata in the RuleRegistry, benchmark manifests referencing one canonical QED registry, and separated approval scopes for topology, amplitude generation, and heavy calculation.

## Exact B01 PhysicsCard

```yaml
schema_version: 0.1.1
object_id: physics_card:b01_ee_to_mumu
status: approved
process_id: process:b01_ee_to_mumu
process_type: scattering_2_to_2
perturbative_order:
  loop_order: 0
  restriction: tree_level_only
coupling_order:
  mode: explicit
  orders:
  - coupling: e
    power: 2
particles:
  incoming:
  - slot: 1
    particle_id: e-
    display_name: electron
    state_role: incoming
    momentum_label: p1
  - slot: 2
    particle_id: e+
    display_name: positron
    state_role: incoming
    momentum_label: p2
  outgoing:
  - slot: 3
    particle_id: mu-
    display_name: muon
    state_role: outgoing
    momentum_label: p3
  - slot: 4
    particle_id: mu+
    display_name: antimuon
    state_role: outgoing
    momentum_label: p4
selected_rule_set:
  registry_id: registry:qed_tree_v1
  rule_set_ids:
  - ruleset:qed_tree_v1
internal_species_policy:
  allowed_particle_ids:
  - gamma
requested_outputs:
- diagram_ir
- validation_report
approval:
  topology:
    status: approved
    approved_by: user
    approved_at: '2026-08-12T14:17:36+08:00'
    notes: Approved only for B01 tree topology representation.
  amplitude_generation:
    status: not_requested
    notes: No amplitude generation in this benchmark phase.
  heavy_calculation:
    status: not_requested
    notes: No heavy calculation in this benchmark phase.
metadata:
  notes: B01 e- e+ -> mu- mu+ topology benchmark only; no amplitudes are calculated.

```

## Exact B02 PhysicsCard

```yaml
schema_version: "0.1.1"
object_id: physics_card:b02_compton
status: approved
process_id: process:b02_compton
process_type: scattering_2_to_2
perturbative_order:
  loop_order: 0
  restriction: tree_level_only
coupling_order:
  mode: explicit
  orders:
    - coupling: e
      power: 2
particles:
  incoming:
    - slot: 1
      particle_id: e-
      display_name: electron
      state_role: incoming
      momentum_label: p1
    - slot: 2
      particle_id: gamma
      display_name: photon
      state_role: incoming
      momentum_label: k1
  outgoing:
    - slot: 3
      particle_id: e-
      display_name: electron
      state_role: outgoing
      momentum_label: p2
    - slot: 4
      particle_id: gamma
      display_name: photon
      state_role: outgoing
      momentum_label: k2
selected_rule_set:
  registry_id: registry:qed_tree_v1
  rule_set_ids:
    - ruleset:qed_tree_v1
internal_species_policy:
  allowed_particle_ids:
    - e-
requested_outputs:
  - diagram_ir
  - tikz_feynman
  - latex_amplitude
  - feyncalc_code
  - validation_report
approval:
  topology:
    status: approved
    approved_by: user
    approved_at: "2026-08-12T13:53:39+08:00"
    notes: Approved only for the B02 tree topology representation during the 0.1.1 migration.
  amplitude_generation:
    status: not_requested
    notes: Day 2 semantic closure explicitly forbids amplitude generation.
  heavy_calculation:
    status: not_requested
    notes: Heavy Mathematica/FeynCalc calculations remain outside the live agent loop.
metadata:
  notes: B02 Compton scattering specification benchmark only; amplitudes, traces, polarization sums, and Ward identity checks are out of scope for this migration.

```

## Relevant Canonical QED Rules

```yaml
- rule_id: rule:qed_tree_v1:e_e_gamma_vertex
  rule_type: vertex
  rule_set_id: ruleset:qed_tree_v1
  participating_fields:
  - slot: 1
    field_id: field:qed:e:psi_bar
    particle_id: e-
    field_role: dirac_fermion
    quantum_field_role: psi_bar
    fermion_flow_role: fermion_flow_out_of_vertex
    arrow_flow: against_momentum
    index_label: i
  - slot: 2
    field_id: field:qed:e:psi
    particle_id: e-
    field_role: dirac_fermion
    quantum_field_role: psi
    fermion_flow_role: fermion_flow_into_vertex
    arrow_flow: with_momentum
    index_label: j
  - slot: 3
    field_id: field:qed:gamma:a
    particle_id: gamma
    field_role: vector
    quantum_field_role: vector_field
    fermion_flow_role: not_applicable
    arrow_flow: none
    index_label: mu
  momentum_labels_order:
  - p_bar
  - p_psi
  - k
  lorentz_index_structure:
    form: template
    expression: gamma(mu) with Dirac indices i,j
    indices:
    - label: mu
      index_type: lorentz
    - label: i
      index_type: dirac
    - label: j
      index_type: dirac
  latex: -i e \gamma^{\mu}_{ij}
  feyncalc:
    template: -I e GA[mu]
    required_symbols:
    - e
    - mu
  coupling_order:
  - coupling: e
    power: 1
  mass_dimension: 0
  symmetries:
  - charge_conjugate_related
  provenance:
  - source_type: standard_convention
    citation: Standard QED electron-electron-photon vertex under the explicitly stated
      FeynAgent Day 1 convention card.
    section: QED tree-level Feynman rules
    page: not_applicable
    notes: Uses metric signature +---, natural units, all momenta incoming at vertices,
      and vertex factor -i e gamma^mu. Marked pending convention review because no
      independent source check was performed during Day 1.
    checked_by: codex
    checked_at: '2026-08-12T13:00:00+08:00'
  trust_status: validated_pending_convention_review
- rule_id: rule:qed_tree_v1:mu_mu_gamma_vertex
  rule_type: vertex
  rule_set_id: ruleset:qed_tree_v1
  participating_fields:
  - slot: 1
    field_id: field:qed:mu:psi_bar
    particle_id: mu-
    field_role: dirac_fermion
    quantum_field_role: psi_bar
    fermion_flow_role: fermion_flow_out_of_vertex
    arrow_flow: against_momentum
    index_label: i
  - slot: 2
    field_id: field:qed:mu:psi
    particle_id: mu-
    field_role: dirac_fermion
    quantum_field_role: psi
    fermion_flow_role: fermion_flow_into_vertex
    arrow_flow: with_momentum
    index_label: j
  - slot: 3
    field_id: field:qed:gamma:a
    particle_id: gamma
    field_role: vector
    quantum_field_role: vector_field
    fermion_flow_role: not_applicable
    arrow_flow: none
    index_label: mu
  momentum_labels_order:
  - p_bar
  - p_psi
  - k
  lorentz_index_structure:
    form: template
    expression: gamma(mu) with muon Dirac indices i,j
    indices:
    - label: mu
      index_type: lorentz
    - label: i
      index_type: dirac
    - label: j
      index_type: dirac
  latex: -i e \gamma^{\mu}_{ij}
  feyncalc:
    template: -I e GA[mu]
    required_symbols:
    - e
    - mu
  coupling_order:
  - coupling: e
    power: 1
  mass_dimension: 0
  symmetries:
  - charge_conjugate_related
  provenance:
  - source_type: standard_convention
    citation: Standard QED muon-muon-photon vertex under the explicitly stated FeynAgent
      0.1.1 convention card.
    section: QED tree-level Feynman rules
    page: not_applicable
    notes: Uses the same explicit metric/sign/all-momenta-incoming convention as the
      electron QED vertex. Pending independent convention review.
    checked_by: codex
    checked_at: '2026-08-12T14:17:36+08:00'
  trust_status: validated_pending_convention_review
- rule_id: rule:qed_tree_v1:electron_propagator
  rule_type: propagator
  rule_set_id: ruleset:qed_tree_v1
  participating_fields:
  - slot: 1
    field_id: field:qed:e:psi
    particle_id: e-
    field_role: dirac_fermion
    quantum_field_role: psi
    fermion_flow_role: fermion_flow_into_vertex
    arrow_flow: with_momentum
    index_label: i
  - slot: 2
    field_id: field:qed:e:psi_bar
    particle_id: e-
    field_role: dirac_fermion
    quantum_field_role: psi_bar
    fermion_flow_role: fermion_flow_out_of_vertex
    arrow_flow: against_momentum
    index_label: j
  momentum_labels_order:
  - q
  lorentz_index_structure:
    form: template
    expression: Dirac numerator slash(q)+m over q^2-m^2+i epsilon
    indices:
    - label: i
      index_type: dirac
    - label: j
      index_type: dirac
  latex: i(\slashed{q}+m)/(q^2-m^2+i\epsilon)
  feyncalc:
    template: I (GS[q] + m)/(SP[q, q] - m^2 + I epsilon)
    required_symbols:
    - q
    - m
    - epsilon
  coupling_order:
  - coupling: e
    power: 0
  mass_dimension: -1
  symmetries:
  - none
  provenance:
  - source_type: standard_convention
    citation: Standard QED electron propagator under the explicitly stated FeynAgent
      Day 1 convention card.
    section: QED tree-level Feynman rules
    page: not_applicable
    notes: Uses metric signature +--- and propagator factor i(slash(q)+m)/(q^2-m^2+i
      epsilon). Marked pending convention review because no independent source check
      was performed during Day 1.
    checked_by: codex
    checked_at: '2026-08-12T13:00:00+08:00'
  trust_status: validated_pending_convention_review
- rule_id: rule:qed_tree_v1:photon_propagator
  rule_type: propagator
  rule_set_id: ruleset:qed_tree_v1
  participating_fields:
  - slot: 1
    field_id: field:qed:gamma:a
    particle_id: gamma
    field_role: vector
    quantum_field_role: vector_field
    fermion_flow_role: not_applicable
    arrow_flow: none
    index_label: mu
  - slot: 2
    field_id: field:qed:gamma:a
    particle_id: gamma
    field_role: vector
    quantum_field_role: vector_field
    fermion_flow_role: not_applicable
    arrow_flow: none
    index_label: nu
  momentum_labels_order:
  - q
  lorentz_index_structure:
    form: template
    expression: metric tensor numerator over photon quadratic denominator
    indices:
    - label: mu
      index_type: lorentz
    - label: nu
      index_type: lorentz
  latex: -i g^{\mu\nu}/(q^2+i\epsilon)
  feyncalc:
    template: -I MT[mu, nu]/(SP[q, q] + I epsilon)
    required_symbols:
    - q
    - mu
    - nu
    - epsilon
  coupling_order:
  - coupling: e
    power: 0
  mass_dimension: -2
  symmetries:
  - field_exchange_symmetric
  provenance:
  - source_type: standard_convention
    citation: Standard QED photon propagator under the explicitly stated FeynAgent
      0.1.1 convention card.
    section: QED tree-level Feynman rules
    page: not_applicable
    notes: Uses metric signature +--- and a conventional covariant photon propagator
      template. Pending independent convention review.
    checked_by: codex
    checked_at: '2026-08-12T14:17:36+08:00'
  trust_status: validated_pending_convention_review

```

## Representative Explicit Vertex Bindings

```yaml
B01 first vertex:
  vertex_id: vertex:generated:b01-ee-to-mumu:s:1
  rule_id: rule:qed_tree_v1:e_e_gamma_vertex
  slot_bindings:
  - rule_slot: 1
    endpoint_id: leg:generated:b01-ee-to-mumu:s:2
    endpoint_kind: external_leg
    expected_particle_id: e-
    expected_field_id: field:qed:e:psi_bar
    endpoint_particle_id: e+
    momentum_label: p2
    momentum_substitution: p2
    crossing_treatment: external_incoming_as_rule_incoming
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: psi_bar
      flow_direction: into_vertex
  - rule_slot: 2
    endpoint_id: leg:generated:b01-ee-to-mumu:s:1
    endpoint_kind: external_leg
    expected_particle_id: e-
    expected_field_id: field:qed:e:psi
    endpoint_particle_id: e-
    momentum_label: p1
    momentum_substitution: p1
    crossing_treatment: external_incoming_as_rule_incoming
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: psi
      flow_direction: into_vertex
  - rule_slot: 3
    endpoint_id: line:generated:b01-ee-to-mumu:s:gamma
    endpoint_kind: internal_line
    expected_particle_id: gamma
    expected_field_id: field:qed:gamma:a
    endpoint_particle_id: gamma
    momentum_label: q_s
    momentum_substitution: -q_s
    crossing_treatment: internal_line_orientation
    convention_conversion:
      source: internal_routing
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: not_applicable
      flow_direction: not_applicable
B02 s-channel first vertex:
  vertex_id: vertex:generated:b02-compton:s:1
  rule_id: rule:qed_tree_v1:e_e_gamma_vertex
  slot_bindings:
  - rule_slot: 1
    endpoint_id: line:generated:b02-compton:s:e-
    endpoint_kind: internal_line
    expected_particle_id: e-
    expected_field_id: field:qed:e:psi_bar
    endpoint_particle_id: e-
    momentum_label: q_s
    momentum_substitution: -q_s
    crossing_treatment: internal_line_orientation
    convention_conversion:
      source: internal_routing
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: psi_bar
      flow_direction: through_internal_line
  - rule_slot: 2
    endpoint_id: leg:generated:b02-compton:s:1
    endpoint_kind: external_leg
    expected_particle_id: e-
    expected_field_id: field:qed:e:psi
    endpoint_particle_id: e-
    momentum_label: p1
    momentum_substitution: p1
    crossing_treatment: external_incoming_as_rule_incoming
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: psi
      flow_direction: into_vertex
  - rule_slot: 3
    endpoint_id: leg:generated:b02-compton:s:2
    endpoint_kind: external_leg
    expected_particle_id: gamma
    expected_field_id: field:qed:gamma:a
    endpoint_particle_id: gamma
    momentum_label: k1
    momentum_substitution: k1
    crossing_treatment: external_incoming_as_rule_incoming
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
    fermion_flow:
      field_orientation: not_applicable
      flow_direction: not_applicable

```

## Generated B01 Canonical Topology Signature

```text
('s', (('e', 2),), (('gamma', 'p1+p2', 'rule:qed_tree_v1:photon_propagator'),), (('rule:qed_tree_v1:e_e_gamma_vertex', ((1, 'external_leg', 'e+', 'p2', 'e-', 'field:qed:e:psi_bar', 'external_incoming_as_rule_incoming', 'p2', 'psi_bar'), (2, 'external_leg', 'e-', 'p1', 'e-', 'field:qed:e:psi', 'external_incoming_as_rule_incoming', 'p1', 'psi'), (3, 'internal_line', 'gamma', 'q_s', 'gamma', 'field:qed:gamma:a', 'internal_line_orientation', '-q_s', 'not_applicable'))), ('rule:qed_tree_v1:mu_mu_gamma_vertex', ((1, 'external_leg', 'mu-', 'p3', 'mu-', 'field:qed:mu:psi_bar', 'external_outgoing_crossed_to_rule_incoming', '-p3', 'psi_bar'), (2, 'external_leg', 'mu+', 'p4', 'mu-', 'field:qed:mu:psi', 'external_outgoing_crossed_to_rule_incoming', '-p4', 'psi'), (3, 'internal_line', 'gamma', 'q_s', 'gamma', 'field:qed:gamma:a', 'internal_line_orientation', 'q_s', 'not_applicable')))))
```

## Generated B02 Canonical Topology Signatures

```text
('s', (('e', 2),), (('e-', 'p1+k1', 'rule:qed_tree_v1:electron_propagator'),), (('rule:qed_tree_v1:e_e_gamma_vertex', ((1, 'external_leg', 'e-', 'p2', 'e-', 'field:qed:e:psi_bar', 'external_outgoing_crossed_to_rule_incoming', '-p2', 'psi_bar'), (2, 'internal_line', 'e-', 'q_s', 'e-', 'field:qed:e:psi', 'internal_line_orientation', 'q_s', 'psi'), (3, 'external_leg', 'gamma', 'k2', 'gamma', 'field:qed:gamma:a', 'external_outgoing_crossed_to_rule_incoming', '-k2', 'not_applicable'))), ('rule:qed_tree_v1:e_e_gamma_vertex', ((1, 'internal_line', 'e-', 'q_s', 'e-', 'field:qed:e:psi_bar', 'internal_line_orientation', '-q_s', 'psi_bar'), (2, 'external_leg', 'e-', 'p1', 'e-', 'field:qed:e:psi', 'external_incoming_as_rule_incoming', 'p1', 'psi'), (3, 'external_leg', 'gamma', 'k1', 'gamma', 'field:qed:gamma:a', 'external_incoming_as_rule_incoming', 'k1', 'not_applicable')))))
('u', (('e', 2),), (('e-', 'p1-k2', 'rule:qed_tree_v1:electron_propagator'),), (('rule:qed_tree_v1:e_e_gamma_vertex', ((1, 'external_leg', 'e-', 'p2', 'e-', 'field:qed:e:psi_bar', 'external_outgoing_crossed_to_rule_incoming', '-p2', 'psi_bar'), (2, 'internal_line', 'e-', 'q_u', 'e-', 'field:qed:e:psi', 'internal_line_orientation', 'q_u', 'psi'), (3, 'external_leg', 'gamma', 'k1', 'gamma', 'field:qed:gamma:a', 'external_incoming_as_rule_incoming', 'k1', 'not_applicable'))), ('rule:qed_tree_v1:e_e_gamma_vertex', ((1, 'internal_line', 'e-', 'q_u', 'e-', 'field:qed:e:psi_bar', 'internal_line_orientation', '-q_u', 'psi_bar'), (2, 'external_leg', 'e-', 'p1', 'e-', 'field:qed:e:psi', 'external_incoming_as_rule_incoming', 'p1', 'psi'), (3, 'external_leg', 'gamma', 'k2', 'gamma', 'field:qed:gamma:a', 'external_outgoing_crossed_to_rule_incoming', '-k2', 'not_applicable')))))
```

## Generated-vs-Gold Result

```text
B01 generated == gold by canonical structural signature: True
B02 generated == gold by canonical structural signature: True
B01 repeated run equivalent: True
B02 repeated run equivalent: True
```

## Rendered PDFs

```text
B01: runs/day2_final_qa/20260812_155139/B01_ee_to_mumu/diagrams.pdf
B01 sha256: 60bd44251ac354f22faaf0928669a5451882e4f040263119a5fba8b01d37968d
B01 bytes: 33372

B02: runs/day2_final_qa/20260812_155139/B02_compton/diagrams.pdf
B02 sha256: 831d1feaccdadb882d26f0b8826c4e55bc3b46f48e3ec5243fb5d6e7e926ab1d
B02 bytes: 37446
```

## Test Summary

```text
schema validation: PASS
unit/regression tests: PASS, 36 tests
generator clean run: PASS for B01 and B02
render clean run: PASS for B01 and B02
generated-vs-gold comparison: PASS
slot binding completeness: PASS
rule reference resolution: PASS
approval scope: topology-only for B01/B02
```

## FeynArts Result

FeynArts was attempted in a bounded fresh Wolfram process. B02 produced exactly two particle insertions classified as `s` and `u`, with internal electron field `F[2,{1}]` in both diagrams and no non-QED field content. Optional B01 photon-only subset count was one, while the full SM model also produced non-QED insertions.

## All Warnings

- QED convention-dependent rule signs/templates remain validated_pending_convention_review pending independent human convention review.
- LaTeX rendering succeeds, but lualatex stderr contains the MiKTeX update-check warning.
- Direct Needs["FeynArts`"] did not load; FeynArts loaded through local FeynCalc with $LoadFeynArts=True.
- Optional B01 FeynArts probe used the photon-only subset because the installed SM model also contains non-QED s-channel insertions.
- rg.exe was unavailable due Windows access denial during QA; equivalent PowerShell scans were used.

## Files For External Review

```text
docs/SCOPE_V0_1.md
docs/ARCHITECTURE.md
docs/MIGRATION_0_1_0_TO_0_1_1.md
schemas/physics_card.schema.json
schemas/convention_card.schema.json
schemas/rule_registry.schema.json
schemas/diagram_ir.schema.json
rules/qed/qed_tree_v1.yaml
src/feynagent/diagrams/topology.py
src/feynagent/render/tikz.py
scripts/generate_diagrams.py
scripts/render_diagrams.py
scripts/validate_examples.py
benchmarks/B01_ee_to_mumu/
benchmarks/B02_compton/
tests/test_topology_generator.py
tests/test_day2_benchmarks.py
tests/test_tikz_renderer.py
reports/DAY2_FEYNARTS_CROSSCHECK.md
runs/day2_final_qa/20260812_155139/qa_summary.json
```
