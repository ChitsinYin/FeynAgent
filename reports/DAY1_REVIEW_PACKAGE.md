# FeynAgent Day 1 Review Package

## Repository Tree To Depth 4

~~~text
.
|-- benchmarks
|   |-- B00_environment
|   |   |-- outputs
|   |   |   |-- tikz_compile
|   |   |   |-- .gitkeep
|   |   |   |-- commands_executed.txt
|   |   |   |-- lualatex_command.stderr.log
|   |   |   |-- lualatex_command.stdout.log
|   |   |   |-- lualatex_version.stderr.log
|   |   |   |-- lualatex_version.stdout.log
|   |   |   |-- os.stderr.log
|   |   |   |-- os.stdout.log
|   |   |   |-- pdflatex_command.stderr.log
|   |   |   |-- pdflatex_command.stdout.log
|   |   |   |-- pdflatex_version.stderr.log
|   |   |   |-- pdflatex_version.stdout.log
|   |   |   |-- python_version.stderr.log
|   |   |   |-- python_version.stdout.log
|   |   |   |-- tikz_compile.exitcode.txt
|   |   |   |-- tikz_compile.stderr.log
|   |   |   |-- tikz_compile.stdout.log
|   |   |   |-- wolframscript_command.stderr.log
|   |   |   |-- wolframscript_command.stdout.log
|   |   |   |-- wolframscript_file_smoke.stderr.log
|   |   |   |-- wolframscript_file_smoke.stdout.log
|   |   |   |-- wolframscript_version.stderr.log
|   |   |   `-- wolframscript_version.stdout.log
|   |   |-- README.md
|   |   |-- smoke_test.wl
|   |   `-- tikz_smoke_test.tex
|   |-- B02_compton
|   |   |-- convention_card.yaml
|   |   |-- diagrams.yaml
|   |   |-- expected.yaml
|   |   |-- physics_card.yaml
|   |   |-- README.md
|   |   `-- rule_manifest.yaml
|   `-- .gitkeep
|-- docs
|   |-- ARCHITECTURE.md
|   |-- DESIGN_DECISIONS.md
|   |-- ENVIRONMENT_REPORT.md
|   `-- SCOPE_V0_1.md
|-- reports
|   |-- .gitkeep
|   |-- DAY1_REPORT.md
|   `-- DAY1_REVIEW_PACKAGE.md
|-- rules
|   |-- qed
|   |   `-- qed_tree_v1.yaml
|   `-- .gitkeep
|-- runs
|   `-- .gitkeep
|-- schemas
|   |-- .gitkeep
|   |-- convention_card.schema.json
|   |-- diagram_ir.schema.json
|   |-- physics_card.schema.json
|   `-- rule_registry.schema.json
|-- scripts
|   |-- .gitkeep
|   `-- validate_examples.py
|-- src
|   `-- feynagent
|       `-- __init__.py
|-- tests
|   |-- .gitkeep
|   |-- test_b02_compton.py
|   `-- test_schema_files.py
|-- .gitignore
|-- AGENTS.md
|-- pyproject.toml
`-- README.md
~~~

## Git Commit Hash

No prior Git commit existed when this review package was generated. The final Day 1 commit hash is reported in the QA completion summary.

## Concise v0.1 Scope

Supported in v0.1: tree-level processes only; 1->n decays and 2->2 scattering with initial benchmark focus on 2->2; scalar, Dirac fermion, vector, and symmetric rank-2 tensor fields at representation level; rules-first workflows; user-supplied or pre-registered Feynman rules; standard QED as the first built-in rule set; explicit conventions; DiagramIR; later derived TikZ-Feynman, LaTeX amplitude, and FeynCalc code.

Not supported in v0.1: loops, automatic renormalization, arbitrary Feynman-rule derivation from arbitrary Lagrangians, full FeynRules integration, thermal field theory, phase-space integration, Boltzmann equations, paper writing, autonomous long-running Mathematica calculations, remote/HPC workflows, GUI/web apps, and arbitrary model discovery.

## Architecture Diagram

~~~text
Natural language
-> PhysicsCard
-> ConventionCard
-> RuleRegistry
-> candidate/approved process
-> DiagramIR
-> renderers/builders
-> LaTeX / FeynCalc artifacts
-> human-controlled heavy calculation
-> validators
~~~

## Four Schema Summary

- PhysicsCard: process identifier, external particles, process type, tree-level restriction, coupling order, selected rule set, internal species policy, requested outputs, and approval status.
- ConventionCard: spacetime dimension, metric signature, momentum conventions, all-momenta-incoming vertex convention, external-state convention, natural units, spin/polarization policy, and optional gravity conventions.
- RuleRegistry: provenance-aware vertex and propagator records with participating fields, momentum order, Lorentz/index structure, LaTeX representation, FeynCalc template, coupling order, mass dimension, symmetries, and trust status.
- DiagramIR: tree-level diagram collection with diagram IDs, channels, external legs, vertex instances, internal lines, momentum routing, rule references, coupling order, symmetry factor, and diagram status.

## Exact Compton PhysicsCard

~~~yaml
schema_version: "0.1.0"
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
  status: approved
  approved_by: user
  approved_at: "2026-08-12T13:00:00+08:00"
metadata:
  notes: B02 Compton scattering specification benchmark only; amplitudes, traces, polarization sums, and Ward identity checks are out of scope for Day 1.

~~~

## Exact Compton ConventionCard

~~~yaml
schema_version: "0.1.0"
object_id: convention_card:b02_compton_qed_plusminus
status: approved
spacetime_dimension:
  symbol: D
  value: 4
metric_signature: +---
momentum_convention:
  fourier_phase: exp_minus_i_p_x
  propagator_momentum_flow: explicit_per_line
all_momenta_incoming_vertex_convention: true
external_state_momentum_convention:
  incoming_particles: physical_incoming_momenta
  outgoing_particles: physical_outgoing_momenta
natural_units:
  hbar: "1"
  c: "1"
spin_polarization_policy:
  spin_sum: do_not_sum
  polarization_sum: do_not_sum
  initial_state_average: do_not_average
metadata:
  notes: External momenta p1,k1 are incoming and p2,k2 are outgoing. Vertex rules still use all momenta incoming, so outgoing external legs are crossed only at the vertex-rule binding stage, not by changing the external process convention.

~~~

## Exact QED Rules Used

~~~yaml
schema_version: "0.1.0"
object_id: rule_registry:qed_tree_v1
status: draft
registry_id: registry:qed_tree_v1
rule_sets:
  - rule_set_id: ruleset:qed_tree_v1
    display_name: QED tree v1 minimal rules
    status: draft
    convention_card_id: convention_card:b02_compton_qed_plusminus
vertices:
  - rule_id: rule:qed_tree_v1:e_e_gamma_vertex
    rule_type: vertex
    rule_set_id: ruleset:qed_tree_v1
    participating_fields:
      - slot: 1
        particle_id: e-
        field_role: dirac_fermion
        arrow_flow: with_momentum
        index_label: i
      - slot: 2
        particle_id: e+
        field_role: dirac_fermion
        arrow_flow: against_momentum
        index_label: j
      - slot: 3
        particle_id: gamma
        field_role: vector
        arrow_flow: none
        index_label: mu
    momentum_labels_order:
      - p_in
      - p_out
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
    latex: "-i e \\gamma^{\\mu}_{ij}"
    feyncalc:
      template: "-I e GA[mu]"
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
        citation: Standard QED electron-electron-photon vertex under the explicitly stated FeynAgent Day 1 convention card.
        section: QED tree-level Feynman rules
        page: not_applicable
        notes: Uses metric signature +---, natural units, all momenta incoming at vertices, and vertex factor -i e gamma^mu. Marked pending convention review because no independent source check was performed during Day 1.
        checked_by: codex
        checked_at: "2026-08-12T13:00:00+08:00"
    trust_status: validated_pending_convention_review
propagators:
  - rule_id: rule:qed_tree_v1:electron_propagator
    rule_type: propagator
    rule_set_id: ruleset:qed_tree_v1
    participating_fields:
      - slot: 1
        particle_id: e-
        field_role: dirac_fermion
        arrow_flow: with_momentum
        index_label: i
      - slot: 2
        particle_id: e-
        field_role: dirac_fermion
        arrow_flow: with_momentum
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
    latex: "i(\\slashed{q}+m)/(q^2-m^2+i\\epsilon)"
    feyncalc:
      template: "I (GS[q] + m)/(SP[q, q] - m^2 + I epsilon)"
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
        citation: Standard QED electron propagator under the explicitly stated FeynAgent Day 1 convention card.
        section: QED tree-level Feynman rules
        page: not_applicable
        notes: Uses metric signature +--- and propagator factor i(slash(q)+m)/(q^2-m^2+i epsilon). Marked pending convention review because no independent source check was performed during Day 1.
        checked_by: codex
        checked_at: "2026-08-12T13:00:00+08:00"
    trust_status: validated_pending_convention_review
metadata:
  notes: Minimal QED tree-level rule registry sufficient for the B02 Compton topology benchmark only; not a full QED model file.

~~~

## Exact Two DiagramIR Entries

~~~yaml
schema_version: "0.1.0"
object_id: diagram_ir:b02_compton_tree_topologies
status: approved
process_id: process:b02_compton
diagrams:
  - diagram_id: diagram:b02_compton:s_channel
    process_id: process:b02_compton
    status: approved
    loop_order: 0
    channel: s
    external_legs:
      - leg_id: leg:b02:s:1
        slot: 1
        particle_id: e-
        state_role: incoming
        momentum_label: p1
      - leg_id: leg:b02:s:2
        slot: 2
        particle_id: gamma
        state_role: incoming
        momentum_label: k1
      - leg_id: leg:b02:s:3
        slot: 3
        particle_id: e-
        state_role: outgoing
        momentum_label: p2
      - leg_id: leg:b02:s:4
        slot: 4
        particle_id: gamma
        state_role: outgoing
        momentum_label: k2
    vertex_instances:
      - vertex_id: vertex:b02:s:1
        rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        attached_endpoint_ids:
          - leg:b02:s:1
          - leg:b02:s:2
          - line:b02:s:electron
      - vertex_id: vertex:b02:s:2
        rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        attached_endpoint_ids:
          - line:b02:s:electron
          - leg:b02:s:3
          - leg:b02:s:4
    internal_lines:
      - line_id: line:b02:s:electron
        particle_id: e-
        propagator_rule_id: rule:qed_tree_v1:electron_propagator
        from:
          kind: vertex
          id: vertex:b02:s:1
          slot: 3
        to:
          kind: vertex
          id: vertex:b02:s:2
          slot: 1
        momentum:
          label: q_s
          expression: p1+k1
          external_convention: physical_external_momenta
    momentum_routing:
      - target_id: line:b02:s:electron
        momentum_label: q_s
        definition: p1+k1
    rule_references:
      - rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        rule_type: vertex
      - rule_id: rule:qed_tree_v1:electron_propagator
        rule_type: propagator
    coupling_order:
      - coupling: e
        power: 2
    symmetry_factor: "1"
    metadata:
      notes: S-channel electron exchange topology only; no amplitude expression is encoded.
  - diagram_id: diagram:b02_compton:u_channel
    process_id: process:b02_compton
    status: approved
    loop_order: 0
    channel: u
    external_legs:
      - leg_id: leg:b02:u:1
        slot: 1
        particle_id: e-
        state_role: incoming
        momentum_label: p1
      - leg_id: leg:b02:u:2
        slot: 2
        particle_id: gamma
        state_role: incoming
        momentum_label: k1
      - leg_id: leg:b02:u:3
        slot: 3
        particle_id: e-
        state_role: outgoing
        momentum_label: p2
      - leg_id: leg:b02:u:4
        slot: 4
        particle_id: gamma
        state_role: outgoing
        momentum_label: k2
    vertex_instances:
      - vertex_id: vertex:b02:u:1
        rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        attached_endpoint_ids:
          - leg:b02:u:1
          - leg:b02:u:4
          - line:b02:u:electron
      - vertex_id: vertex:b02:u:2
        rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        attached_endpoint_ids:
          - line:b02:u:electron
          - leg:b02:u:3
          - leg:b02:u:2
    internal_lines:
      - line_id: line:b02:u:electron
        particle_id: e-
        propagator_rule_id: rule:qed_tree_v1:electron_propagator
        from:
          kind: vertex
          id: vertex:b02:u:1
          slot: 3
        to:
          kind: vertex
          id: vertex:b02:u:2
          slot: 1
        momentum:
          label: q_u
          expression: p1-k2
          external_convention: physical_external_momenta
    momentum_routing:
      - target_id: line:b02:u:electron
        momentum_label: q_u
        definition: p1-k2
    rule_references:
      - rule_id: rule:qed_tree_v1:e_e_gamma_vertex
        rule_type: vertex
      - rule_id: rule:qed_tree_v1:electron_propagator
        rule_type: propagator
    coupling_order:
      - coupling: e
        power: 2
    symmetry_factor: "1"
    metadata:
      notes: U-channel electron exchange topology only; no amplitude expression is encoded.
metadata:
  notes: Gold tree topology representation for e- gamma -> e- gamma in QED. This is not an amplitude file.

~~~

## Environment Status Table

| tool | status | version | notes |
| --- | --- | --- | --- |
| OS | PASS | Windows 11 build 26200, 64-bit | Local smoke log captured. |
| Python | PASS | 3.10.9 | Executable path recorded only in environment logs/report. |
| WolframScript | PASS | 1.14.0 | `wolframscript -file` works. |
| Wolfram Engine | PASS | 15.0.1 | Fresh process smoke completed. |
| FeynCalc | PASS | 10.1.0 | Fresh process loaded package and evaluated `FCI[SP[p,p]]`. |
| FeynArts | PASS WITH WARNINGS | unknown | Fresh process exposed FeynArts symbols; version symbol not detected. |
| LaTeX | PASS WITH WARNINGS | MiKTeX 25.12 | `pdflatex` and `lualatex` available; MiKTeX warns updates have not been checked. |
| TikZ-Feynman | PASS WITH WARNINGS | package available | Minimal two-vertex PDF compiled; stderr includes MiKTeX update warning. |
| FeynGrav | PASS, MANUAL | 3.0 | User screenshot shows notebook startup works; not part of fresh `wolframscript -file` smoke. |

See `docs/ENVIRONMENT_REPORT.md` and `benchmarks/B00_environment/outputs/` for raw logs.

## Test Summary

~~~text
python scripts\validate_examples.py
PASS benchmarks/B02_compton/physics_card.yaml
PASS benchmarks/B02_compton/convention_card.yaml
PASS benchmarks/B02_compton/rule_manifest.yaml
PASS benchmarks/B02_compton/diagrams.yaml
PASS rules/qed/qed_tree_v1.yaml

python -m unittest discover -s tests
Ran 9 tests in about 0.2 seconds
OK

B00 repeatable smoke checks
Wolfram/FeynCalc/FeynArts smoke passed; TikZ-Feynman PDF compile exit code 0.
~~~

## Warnings

- QED rules are `validated_pending_convention_review`, not fully trusted.
- FeynArts version was not detected, although availability smoke passed.
- MiKTeX emitted an update-check warning while still producing the TikZ-Feynman PDF.
- `rg` execution was denied in this Windows environment; PowerShell fallback scans were used for hygiene checks.

## Unresolved Ambiguities

- Human approval is still required for the exact QED sign/convention package before changing rule trust status to `trusted`.
- The Day 1 DiagramIR encodes topology and rule references, not a complete amplitude ordering convention for spinor chains.
- Outgoing external momenta remain physical outgoing momenta; all-momenta-incoming applies at vertex-rule binding time and still needs careful Day 2 assembly tests.

## Files For Reviewer To Inspect

- `docs/SCOPE_V0_1.md`
- `docs/ARCHITECTURE.md`
- `docs/DESIGN_DECISIONS.md`
- `docs/ENVIRONMENT_REPORT.md`
- `schemas/physics_card.schema.json`
- `schemas/convention_card.schema.json`
- `schemas/rule_registry.schema.json`
- `schemas/diagram_ir.schema.json`
- `rules/qed/qed_tree_v1.yaml`
- `benchmarks/B02_compton/physics_card.yaml`
- `benchmarks/B02_compton/convention_card.yaml`
- `benchmarks/B02_compton/rule_manifest.yaml`
- `benchmarks/B02_compton/diagrams.yaml`
- `benchmarks/B02_compton/expected.yaml`
- `benchmarks/B02_compton/README.md`
- `tests/test_b02_compton.py`
- `scripts/validate_examples.py`
