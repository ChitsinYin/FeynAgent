# Day-3 Review Package

## Repository tree to depth 4

```text
.
  .gitignore
  AGENTS.md
  README.md
  pyproject.toml
  .benchmarks/
  benchmarks/
    .gitkeep
    DAY2_BENCHMARK_SUMMARY.md
    B00_environment/
      README.md
      smoke_test.wl
      tikz_smoke_test.tex
      outputs/
        .gitkeep
        commands_executed.txt
        lualatex_command.stderr.log
        lualatex_command.stdout.log
        lualatex_version.stderr.log
        lualatex_version.stdout.log
        os.stderr.log
        os.stdout.log
        pdflatex_command.stderr.log
        pdflatex_command.stdout.log
        pdflatex_version.stderr.log
        pdflatex_version.stdout.log
        python_version.stderr.log
        python_version.stdout.log
        tikz_compile.exitcode.txt
        tikz_compile.stderr.log
        tikz_compile.stdout.log
        wolframscript_command.stderr.log
        wolframscript_command.stdout.log
        wolframscript_file_smoke.stderr.log
        wolframscript_file_smoke.stdout.log
        wolframscript_version.stderr.log
        wolframscript_version.stdout.log
        tikz_compile/
    B01_ee_to_mumu/
      README.md
      amplitude_audit.md
      amplitude_ir.example.yaml
      amplitude_ir.yaml
      amplitude_smoke.wl
      amplitudes.pdf
      amplitudes.tex
      amplitudes.wl
      compute_m2.wl
      convention_card.yaml
      diagrams.yaml
      expected.yaml
      physics_card.yaml
      rule_manifest.yaml
    B02_compton/
      README.md
      amplitude_audit.md
      amplitude_ir.example.yaml
      amplitude_ir.yaml
      amplitude_smoke.wl
      amplitudes.pdf
      amplitudes.tex
      amplitudes.wl
      compute_m2.wl
      convention_card.yaml
      diagrams.yaml
      expected.yaml
      physics_card.yaml
      rule_manifest.yaml
      ward_check.wl
  docs/
    ARCHITECTURE.md
    DAY3_DESIGN_DECISIONS.md
    DESIGN_DECISIONS.md
    ENVIRONMENT_REPORT.md
    MIGRATION_0_1_0_TO_0_1_1.md
    MIGRATION_0_1_1_TO_0_1_2.md
    QED_CONVENTION_AUDIT.md
    SCOPE_V0_1.md
  reports/
    .gitkeep
    DAY1_REPORT.md
    DAY1_REVIEW_PACKAGE.md
    DAY2_FEYNARTS_CROSSCHECK.md
    DAY2_REPORT.md
    DAY2_REVIEW_PACKAGE.md
    FeynAgent_Day2_Review_Bundle.zip
  rules/
    .gitkeep
    qed/
      qed_tree_v1.yaml
  runs/
    .gitkeep
    day2_benchmarks/
      20260812_141950/
        RUN_ID.txt
        SUMMARY.md
        B01_ee_to_mumu/
        B02_compton/
    day2_feynarts_crosscheck/
      20260812_154018/
        feynarts_crosscheck.stderr.log
        feynarts_crosscheck.stdout.log
        feynarts_crosscheck_day2.wl
        probe.stderr.log
        probe.stdout.log
        probe_b01.stderr.log
        probe_b01.stdout.log
        probe_b01.wl
        probe_b02_structure.stderr.log
        probe_b02_structure.stdout.log
        probe_b02_structure.wl
        probe_extract.stderr.log
        probe_extract.stdout.log
        probe_extract.wl
        probe_feynarts.wl
        probe_feynarts_via_feyncalc.wl
        probe_via_feyncalc.stderr.log
        probe_via_feyncalc.stdout.log
    day2_final_qa/
      20260812_155139/
        RUN_ID.txt
        qa_summary.json
        B01_ee_to_mumu/
        B02_compton/
    day2_render/
      20260812_151438/
        B01_ee_to_mumu/
      20260812_151557/
        RUN_ID.txt
        SUMMARY.md
        B01_ee_to_mumu/
        B02_compton/
    day3_fermion_flow/
      20260812_192216/
        RUN_ID.txt
        B01_ee_to_mumu/
        B02_compton/
      20260812_192439/
        RUN_ID.txt
        B01_ee_to_mumu/
        B02_compton/
    day3_final_qa/
      20260812_220452/
        RUN_ID.txt
        amplitude_generation.log
        canonical_hygiene.log
        canonical_hygiene_review_relevant.log
        clean_diagram_compare.log
        clean_diagram_structural_compare.log
        physics_audit.log
        post_generation_schema.log
        pytest_all.log
        renderer_regression_tests.log
        review_inputs_summary.log
        schema_validate_amplitude_ir.log
        schema_validate_examples.log
        B01_ee_to_mumu/
        B02_compton/
    qed_convention_audit/
      feyncalc_amp_probe.wl
      feyncalc_spinor_probe.wl
      feyncalc_template_syntax_check.wl
  schemas/
    .gitkeep
    amplitude_ir.schema.json
    convention_card.schema.json
    diagram_ir.schema.json
    physics_card.schema.json
    rule_registry.schema.json
  scripts/
    .gitkeep
    generate_amplitudes.py
    generate_diagrams.py
    render_diagrams.py
    validate_examples.py
  src/
    feynagent/
      __init__.py
      amplitudes/
        __init__.py
        backends.py
        builder.py
      diagrams/
        __init__.py
        topology.py
      render/
        __init__.py
        tikz.py
  tests/
    .gitkeep
    test_amplitude_backends.py
    test_amplitude_builder.py
    test_amplitude_ir_schema.py
    test_b02_compton.py
    test_day2_benchmarks.py
    test_schema_files.py
    test_tikz_renderer.py
    test_topology_generator.py
```

## Git diff summary from Day-2 commit

```text
benchmarks/B01_ee_to_mumu/diagrams.yaml      |  10 +-
 benchmarks/B01_ee_to_mumu/expected.yaml      |   2 +-
 benchmarks/B01_ee_to_mumu/physics_card.yaml  |  28 +-
 benchmarks/B01_ee_to_mumu/rule_manifest.yaml |   2 +-
 benchmarks/B02_compton/README.md             |   6 +-
 benchmarks/B02_compton/diagrams.yaml         | 621 ++++++++++++++-------------
 benchmarks/B02_compton/expected.yaml         |  21 +-
 benchmarks/B02_compton/physics_card.yaml     |  87 ++--
 benchmarks/B02_compton/rule_manifest.yaml    |   2 +-
 docs/ARCHITECTURE.md                         |   2 +-
 rules/qed/qed_tree_v1.yaml                   |  47 +-
 schemas/diagram_ir.schema.json               |   4 +-
 schemas/physics_card.schema.json             |  38 +-
 src/feynagent/diagrams/topology.py           |  24 +-
 src/feynagent/render/tikz.py                 | 124 ++++--
 tests/test_b02_compton.py                    |  34 +-
 tests/test_schema_files.py                   |   1 +
 tests/test_tikz_renderer.py                  |  25 +-
 tests/test_topology_generator.py             |  34 +-
 19 files changed, 675 insertions(+), 437 deletions(-)
warning: in the working copy of 'rules/qed/qed_tree_v1.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_b02_compton.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_schema_files.py', LF will be replaced by CRLF the next time Git touches it
```

```text
M	benchmarks/B01_ee_to_mumu/diagrams.yaml
M	benchmarks/B01_ee_to_mumu/expected.yaml
M	benchmarks/B01_ee_to_mumu/physics_card.yaml
M	benchmarks/B01_ee_to_mumu/rule_manifest.yaml
M	benchmarks/B02_compton/README.md
M	benchmarks/B02_compton/diagrams.yaml
M	benchmarks/B02_compton/expected.yaml
M	benchmarks/B02_compton/physics_card.yaml
M	benchmarks/B02_compton/rule_manifest.yaml
M	docs/ARCHITECTURE.md
M	rules/qed/qed_tree_v1.yaml
M	schemas/diagram_ir.schema.json
M	schemas/physics_card.schema.json
M	src/feynagent/diagrams/topology.py
M	src/feynagent/render/tikz.py
M	tests/test_b02_compton.py
M	tests/test_schema_files.py
M	tests/test_tikz_renderer.py
M	tests/test_topology_generator.py
warning: in the working copy of 'rules/qed/qed_tree_v1.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_b02_compton.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tests/test_schema_files.py', LF will be replaced by CRLF the next time Git touches it
```

## Migration summary

- DiagramIR migrated to fermion-flow/binding semantics sufficient for Day-3 amplitude assembly.
- PhysicsCard approvals now separate topology, amplitude generation, and heavy calculation.
- AmplitudeIR schema added as derived structure, not canonical user input.
- Backend files are generated from AmplitudeIR only.

## QED audit summary

- rule:qed_tree_v1:e_e_gamma_vertex: trust_status=validated; formula=-i e \gamma^{\mu}_{ij}; feyncalc=-I e GA[mu]
- rule:qed_tree_v1:mu_mu_gamma_vertex: trust_status=validated; formula=-i e \gamma^{\mu}_{ij}; feyncalc=-I e GA[mu]
- rule:qed_tree_v1:electron_propagator: trust_status=validated; formula=i(\slashed{q}+m)/(q^2-m^2+i\epsilon); feyncalc=I (GS[q] + m)/(SP[q, q] - m^2 + I epsilon)
- rule:qed_tree_v1:photon_propagator: trust_status=validated; formula=-i g^{\mu\nu}/(q^2+i\epsilon); feyncalc=-I MT[mu, nu]/(SP[q, q] + I epsilon)

## External wavefunction truth table

| external state | generated factor |
|---|---|
| incoming fermion | `u(p)` |
| outgoing fermion | `ubar(p)` |
| incoming antifermion | `vbar(p)` |
| outgoing antifermion | `v(p)` |

## Representative corrected B01 DiagramIR bindings

```text
- vertex:generated:b01-ee-to-mumu:s:1 slot 1: endpoint=leg:generated:b01-ee-to-mumu:s:2 particle=e+ field=field:qed:e:psi_bar momentum_substitution=p2 orientation=psi_bar flow=out_of_vertex
- vertex:generated:b01-ee-to-mumu:s:1 slot 2: endpoint=leg:generated:b01-ee-to-mumu:s:1 particle=e- field=field:qed:e:psi momentum_substitution=p1 orientation=psi flow=into_vertex
- vertex:generated:b01-ee-to-mumu:s:1 slot 3: endpoint=line:generated:b01-ee-to-mumu:s:gamma particle=gamma field=field:qed:gamma:a momentum_substitution=-q_s orientation=not_applicable flow=not_applicable
- vertex:generated:b01-ee-to-mumu:s:2 slot 1: endpoint=leg:generated:b01-ee-to-mumu:s:3 particle=mu- field=field:qed:mu:psi_bar momentum_substitution=-p3 orientation=psi_bar flow=out_of_vertex
- vertex:generated:b01-ee-to-mumu:s:2 slot 2: endpoint=leg:generated:b01-ee-to-mumu:s:4 particle=mu+ field=field:qed:mu:psi momentum_substitution=-p4 orientation=psi flow=into_vertex
- vertex:generated:b01-ee-to-mumu:s:2 slot 3: endpoint=line:generated:b01-ee-to-mumu:s:gamma particle=gamma field=field:qed:gamma:a momentum_substitution=q_s orientation=not_applicable flow=not_applicable
```

## B01 AmplitudeIR

```yaml
schema_version: 0.1.0
object_id: amplitude_ir:b01_ee_to_mumu:generated
ir_type: derived_amplitude_ir
status: derived_candidate
process_id: process:b01_ee_to_mumu
source:
  physics_card_id: physics_card:b01_ee_to_mumu
  convention_card_id: convention_card:b01_qed_plusminus
  rule_registry_id: registry:qed_tree_v1
  rule_registry_sha256: e55c688d3343c43099ca25c0c7ceab13685fe1a94e9f2e9f46e36108babb7399
  diagram_ir_id: diagram_ir:b01_ee_to_mumu_gold_topology
  diagram_ir_sha256: ebe8813a8630f87b27c36562dcd44f2081fda3894851f013838c0bceabe4d637
total_amplitude:
  term_amplitude_ids:
  - amplitude:b01_ee_to_mumu:amp_s
  sum_kind: ordered_symbolic_sum
  notes: Symbolic sum of accepted diagram amplitudes; no simplification performed.
audit_metadata:
  convention_audit_path: docs/QED_CONVENTION_AUDIT.md
  approved_for_amplitude_generation: true
  heavy_calculation_approved: false
  notes: Derived after topology and amplitude-generation gates; heavy calculation
    not required.
amplitudes:
- amplitude_id: amplitude:b01_ee_to_mumu:amp_s
  diagram_id: diagram:generated:b01-ee-to-mumu:s:gamma
  process_id: process:b01_ee_to_mumu
  source_rule_ids:
  - rule:qed_tree_v1:e_e_gamma_vertex
  - rule:qed_tree_v1:mu_mu_gamma_vertex
  - rule:qed_tree_v1:photon_propagator
  external_state_factors:
  - factor_id: factor:b01_ee_to_mumu:s:ext:1:u
    leg_id: leg:generated:b01-ee-to-mumu:s:1
    particle_id: e-
    state_role: incoming
    momentum_label: p1
    factor_kind: spinor_wavefunction
    spinor_type: u
    index_ids:
    - idx:b01_ee_to_mumu:s:u:d_ext_1
  - factor_id: factor:b01_ee_to_mumu:s:ext:2:vbar
    leg_id: leg:generated:b01-ee-to-mumu:s:2
    particle_id: e+
    state_role: incoming
    momentum_label: p2
    factor_kind: spinor_wavefunction
    spinor_type: vbar
    index_ids:
    - idx:b01_ee_to_mumu:s:vbar:d_ext_2
  - factor_id: factor:b01_ee_to_mumu:s:ext:3:ubar
    leg_id: leg:generated:b01-ee-to-mumu:s:3
    particle_id: mu-
    state_role: outgoing
    momentum_label: p3
    factor_kind: spinor_wavefunction
    spinor_type: ubar
    index_ids:
    - idx:b01_ee_to_mumu:s:ubar:d_ext_3
  - factor_id: factor:b01_ee_to_mumu:s:ext:4:v
    leg_id: leg:generated:b01-ee-to-mumu:s:4
    particle_id: mu+
    state_role: outgoing
    momentum_label: p4
    factor_kind: spinor_wavefunction
    spinor_type: v
    index_ids:
    - idx:b01_ee_to_mumu:s:v:d_ext_4
  vertex_factors:
  - factor_id: factor:b01_ee_to_mumu:s:vertex:1
    vertex_id: vertex:generated:b01-ee-to-mumu:s:1
    rule_id: rule:qed_tree_v1:e_e_gamma_vertex
    coefficient: -I e
    lorentz_index_ids:
    - idx:b01_ee_to_mumu:s:x_1:l_v1_mu
    dirac_index_ids:
    - idx:b01_ee_to_mumu:s:x_1:d_v1_bar
    - idx:b01_ee_to_mumu:s:x_1:d_v1_psi
    slot_factors:
    - rule_slot: 1
      endpoint_id: leg:generated:b01-ee-to-mumu:s:2
      field_id: field:qed:e:psi_bar
      momentum_substitution: p2
      index_ids:
      - idx:b01_ee_to_mumu:s:x_1:d_v1_bar
    - rule_slot: 2
      endpoint_id: leg:generated:b01-ee-to-mumu:s:1
      field_id: field:qed:e:psi
      momentum_substitution: p1
      index_ids:
      - idx:b01_ee_to_mumu:s:x_1:d_v1_psi
    - rule_slot: 3
      endpoint_id: line:generated:b01-ee-to-mumu:s:gamma
      field_id: field:qed:gamma:a
      momentum_substitution: -q_s
      index_ids:
      - idx:b01_ee_to_mumu:s:x_1:l_v1_mu
  - factor_id: factor:b01_ee_to_mumu:s:vertex:2
    vertex_id: vertex:generated:b01-ee-to-mumu:s:2
    rule_id: rule:qed_tree_v1:mu_mu_gamma_vertex
    coefficient: -I e
    lorentz_index_ids:
    - idx:b01_ee_to_mumu:s:x_2:l_v2_mu
    dirac_index_ids:
    - idx:b01_ee_to_mumu:s:x_2:d_v2_bar
    - idx:b01_ee_to_mumu:s:x_2:d_v2_psi
    slot_factors:
    - rule_slot: 1
      endpoint_id: leg:generated:b01-ee-to-mumu:s:3
      field_id: field:qed:mu:psi_bar
      momentum_substitution: -p3
      index_ids:
      - idx:b01_ee_to_mumu:s:x_2:d_v2_bar
    - rule_slot: 2
      endpoint_id: leg:generated:b01-ee-to-mumu:s:4
      field_id: field:qed:mu:psi
      momentum_substitution: -p4
      index_ids:
      - idx:b01_ee_to_mumu:s:x_2:d_v2_psi
    - rule_slot: 3
      endpoint_id: line:generated:b01-ee-to-mumu:s:gamma
      field_id: field:qed:gamma:a
      momentum_substitution: q_s
      index_ids:
      - idx:b01_ee_to_mumu:s:x_2:l_v2_mu
  propagator_factors:
  - factor_id: factor:b01_ee_to_mumu:s:prop:1
    line_id: line:generated:b01-ee-to-mumu:s:gamma
    rule_id: rule:qed_tree_v1:photon_propagator
    particle_id: gamma
    momentum_label: q_s
    momentum_expression: p1+p2
    numerator: -I MT[l_p1_l, l_p1_r]
    denominator: SP[q_s, q_s] + I epsilon
    index_ids:
    - idx:b01_ee_to_mumu:s:x_1:l_p1_l
    - idx:b01_ee_to_mumu:s:x_1:l_p1_r
  local_indices:
    lorentz:
    - index_id: idx:b01_ee_to_mumu:s:x_1:l_v1_mu
      label: l_v1_mu
      index_type: lorentz
      owner_id: factor:b01_ee_to_mumu:s:vertex:1
    - index_id: idx:b01_ee_to_mumu:s:x_2:l_v2_mu
      label: l_v2_mu
      index_type: lorentz
      owner_id: factor:b01_ee_to_mumu:s:vertex:2
    - index_id: idx:b01_ee_to_mumu:s:x_1:l_p1_l
      label: l_p1_l
      index_type: lorentz
      owner_id: factor:b01_ee_to_mumu:s:prop:1
    - index_id: idx:b01_ee_to_mumu:s:x_1:l_p1_r
      label: l_p1_r
      index_type: lorentz
      owner_id: factor:b01_ee_to_mumu:s:prop:1
    dirac:
    - index_id: idx:b01_ee_to_mumu:s:u:d_ext_1
      label: d_ext_1
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:ext:1:u
    - index_id: idx:b01_ee_to_mumu:s:vbar:d_ext_2
      label: d_ext_2
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:ext:2:vbar
    - index_id: idx:b01_ee_to_mumu:s:ubar:d_ext_3
      label: d_ext_3
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:ext:3:ubar
    - index_id: idx:b01_ee_to_mumu:s:v:d_ext_4
      label: d_ext_4
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:ext:4:v
    - index_id: idx:b01_ee_to_mumu:s:x_1:d_v1_bar
      label: d_v1_bar
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:vertex:1
    - index_id: idx:b01_ee_to_mumu:s:x_1:d_v1_psi
      label: d_v1_psi
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:vertex:1
    - index_id: idx:b01_ee_to_mumu:s:x_2:d_v2_bar
      label: d_v2_bar
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:vertex:2
    - index_id: idx:b01_ee_to_mumu:s:x_2:d_v2_psi
      label: d_v2_psi
      index_type: dirac
      owner_id: factor:b01_ee_to_mumu:s:vertex:2
  momentum_substitutions:
  - substitution_id: subst:b01_ee_to_mumu:s:v1:slot1
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:1
    rule_slot: 1
    symbol: p_bar
    expression: p2
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
  - substitution_id: subst:b01_ee_to_mumu:s:v1:slot2
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:1
    rule_slot: 2
    symbol: p_psi
    expression: p1
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
  - substitution_id: subst:b01_ee_to_mumu:s:v1:slot3
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:1
    rule_slot: 3
    symbol: k
    expression: -q_s
    convention_conversion:
      source: internal_routing
      target: all_momenta_incoming_vertex
  - substitution_id: subst:b01_ee_to_mumu:s:v2:slot1
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:2
    rule_slot: 1
    symbol: p_bar
    expression: -p3
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
  - substitution_id: subst:b01_ee_to_mumu:s:v2:slot2
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:2
    rule_slot: 2
    symbol: p_psi
    expression: -p4
    convention_conversion:
      source: physical_external_momenta
      target: all_momenta_incoming_vertex
  - substitution_id: subst:b01_ee_to_mumu:s:v2:slot3
    source_factor_id: factor:b01_ee_to_mumu:s:vertex:2
    rule_slot: 3
    symbol: k
    expression: q_s
    convention_conversion:
      source: internal_routing
      target: all_momenta_incoming_vertex
  fermion_chains:
  - chain_id: chain:b01_ee_to_mumu:s:fermion:1
    ordered_factor_ids:
    - factor:b01_ee_to_mumu:s:ext:2:vbar
    - factor:b01_ee_to_mumu:s:vertex:1
    - factor:b01_ee_to_mumu:s:ext:1:u
    external_start_factor_id: factor:b01_ee_to_mumu:s:ext:2:vbar
    external_end_factor_id: factor:b01_ee_to_mumu:s:ext:1:u
    attached_bosonic_factor_ids:
    - factor:b01_ee_to_mumu:s:prop:1
  - chain_id: chain:b01_ee_to_mumu:s:fermion:2
    ordered_factor_ids:
    - factor:b01_ee_to_mumu:s:ext:3:ubar
    - factor:b01_ee_to_mumu:s:vertex:2
    - factor:b01_ee_to_mumu:s:ext:4:v
    external_start_factor_id: factor:b01_ee_to_mumu:s:ext:3:ubar
    external_end_factor_id: factor:b01_ee_to_mumu:s:ext:4:v
    attached_bosonic_factor_ids:
    - factor:b01_ee_to_mumu:s:prop:1
  bosonic_external_polarization_factors: []
  non_chain_factors:
  - factor_id: factor:b01_ee_to_mumu:s:nonchain:1
    factor_kind: boson_propagator_between_currents
    source_factor_ids:
    - factor:b01_ee_to_mumu:s:prop:1
    connects:
    - chain_id: chain:b01_ee_to_mumu:s:fermion:1
      index_id: idx:b01_ee_to_mumu:s:x_1:l_v1_mu
    - chain_id: chain:b01_ee_to_mumu:s:fermion:2
      index_id: idx:b01_ee_to_mumu:s:x_2:l_v2_mu
  index_contractions:
  - contraction_id: contract:b01_ee_to_mumu:s:dirac:1
    index_type: dirac
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:ext:2:vbar
      index_id: idx:b01_ee_to_mumu:s:vbar:d_ext_2
      index_role: right
    - factor_id: factor:b01_ee_to_mumu:s:vertex:1
      index_id: idx:b01_ee_to_mumu:s:x_1:d_v1_bar
      index_role: left
  - contraction_id: contract:b01_ee_to_mumu:s:dirac:2
    index_type: dirac
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:vertex:1
      index_id: idx:b01_ee_to_mumu:s:x_1:d_v1_psi
      index_role: right
    - factor_id: factor:b01_ee_to_mumu:s:ext:1:u
      index_id: idx:b01_ee_to_mumu:s:u:d_ext_1
      index_role: left
  - contraction_id: contract:b01_ee_to_mumu:s:dirac:3
    index_type: dirac
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:ext:3:ubar
      index_id: idx:b01_ee_to_mumu:s:ubar:d_ext_3
      index_role: right
    - factor_id: factor:b01_ee_to_mumu:s:vertex:2
      index_id: idx:b01_ee_to_mumu:s:x_2:d_v2_bar
      index_role: left
  - contraction_id: contract:b01_ee_to_mumu:s:dirac:4
    index_type: dirac
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:vertex:2
      index_id: idx:b01_ee_to_mumu:s:x_2:d_v2_psi
      index_role: right
    - factor_id: factor:b01_ee_to_mumu:s:ext:4:v
      index_id: idx:b01_ee_to_mumu:s:v:d_ext_4
      index_role: left
  - contraction_id: contract:b01_ee_to_mumu:s:lorentz:1
    index_type: lorentz
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:vertex:1
      index_id: idx:b01_ee_to_mumu:s:x_1:l_v1_mu
      index_role: lorentz
    - factor_id: factor:b01_ee_to_mumu:s:prop:1
      index_id: idx:b01_ee_to_mumu:s:x_1:l_p1_l
      index_role: lorentz
  - contraction_id: contract:b01_ee_to_mumu:s:lorentz:2
    index_type: lorentz
    factor_indices:
    - factor_id: factor:b01_ee_to_mumu:s:vertex:2
      index_id: idx:b01_ee_to_mumu:s:x_2:l_v2_mu
      index_role: lorentz
    - factor_id: factor:b01_ee_to_mumu:s:prop:1
      index_id: idx:b01_ee_to_mumu:s:x_1:l_p1_r
      index_role: lorentz
  overall_factor:
    scalar_prefactor: '1'
    relative_sign: '+1'
    sign_source: diagram_ir_symmetry_and_fermion_ordering
    notes: No gamma-chain simplification, spin sums, polarization sums, or squaring
      performed.
  generation_status:
    status: derived_candidate
    generated_by: feynagent.amplitudes.builder
    notes: Deterministically derived from approved structured inputs.
  audit_metadata:
    convention_audit_path: docs/QED_CONVENTION_AUDIT.md
    approved_for_amplitude_generation: true
    heavy_calculation_approved: false
    notes: Rule factors reference audited canonical rule IDs; heavy calculation approval
      not required.
  metadata:
    notes: Per-diagram derived amplitude structure; not a final rendered amplitude.
metadata:
  notes: Derived AmplitudeIR; not a canonical user-input physics source.

```

## B02 s/u AmplitudeIR factor-chain summaries

```text
- amplitude:b02_compton:amp_s from diagram:generated:b02-compton:s:e-
  chain: factor:b02_compton:s:ext:3:ubar -> factor:b02_compton:s:vertex:2 -> factor:b02_compton:s:prop:1 -> factor:b02_compton:s:vertex:1 -> factor:b02_compton:s:ext:1:u
  propagator: factor:b02_compton:s:prop:1 e- q_s=p1+k1
  polarizations: factor:b02_compton:s:pol:2:eps k1 none; factor:b02_compton:s:pol:4:eps_conj k2 complex_conjugate
- amplitude:b02_compton:amp_u from diagram:generated:b02-compton:u:e-
  chain: factor:b02_compton:u:ext:3:ubar -> factor:b02_compton:u:vertex:2 -> factor:b02_compton:u:prop:1 -> factor:b02_compton:u:vertex:1 -> factor:b02_compton:u:ext:1:u
  propagator: factor:b02_compton:u:prop:1 e- q_u=p1-k2
  polarizations: factor:b02_compton:u:pol:2:eps k1 none; factor:b02_compton:u:pol:4:eps_conj k2 complex_conjugate
```

## Exact rendered LaTeX amplitudes

### B01

```tex
q_{s} = p_{1}+p_{2}
\mathcal{M}_{s} = \bar v(p_{2})_{a_{2}}\left(-i e \gamma^{\mu_{1}}\right)u(p_{1})_{a_{1}} \, \frac{-i g^{\mu_{1}\mu_{2}}}{q_{s}^2+i\epsilon} \, \bar u(p_{3})_{a_{3}}\left(-i e \gamma^{\mu_{2}}\right)v(p_{4})_{a_{4}}
\mathcal{M} = \mathcal{M}_{s}
```

### B02

```tex
q_{s} = p_{1}+k_{1}
q_{u} = p_{1}-k_{2}
\mathcal{M}_{s} = \bar u(p_{2})_{a_{2}}\left(-i e \gamma^{\mu_{4}}\right)\epsilon^{*}_{\mu_{4}}(k_{2})\frac{i(\not{q_{s}}+m_e)}{q_{s}^2-m_e^2+i\epsilon}\left(-i e \gamma^{\mu_{3}}\right)\epsilon_{\mu_{3}}(k_{1})u(p_{1})_{a_{1}}
\mathcal{M}_{u} = \bar u(p_{2})_{a_{2}}\left(-i e \gamma^{\mu_{4}}\right)\epsilon_{\mu_{4}}(k_{1})\frac{i(\not{q_{u}}+m_e)}{q_{u}^2-m_e^2+i\epsilon}\left(-i e \gamma^{\mu_{3}}\right)\epsilon^{*}_{\mu_{3}}(k_{2})u(p_{1})_{a_{1}}
\mathcal{M} = \mathcal{M}_{s} + \mathcal{M}_{u}
```

## Relevant generated FeynCalc snippets

### B01

```wolfram
qDefinitions = <|"q_s" -> HoldForm[qS == p1 + p2]|>;
qSubstitutions = {qS -> p1 + p2};
ampS = (SpinorVBar[p2, me] . ((-I e) GA[mu1]) . SpinorU[p1, me]) * ((-I MT[mu1, mu2])/(SP[qS, qS] + I epsilon)) * (SpinorUBar[p3, mmu] . ((-I e) GA[mu2]) . SpinorV[p4, mmu]);
diagramAmplitudes = <|"amp_s" -> ampS|>;
ampTotal = ampS;
```

### B02

```wolfram
qDefinitions = <|"q_s" -> HoldForm[qS == p1 + k1], "q_u" -> HoldForm[qU == p1 - k2]|>;
qSubstitutions = {qS -> p1 + k1, qU -> p1 - k2};
ampS = (SpinorUBar[p2, me] . ((-I e) GA[mu4]) . (I (GS[qS] + me)/(SP[qS, qS] - me^2 + I epsilon)) . ((-I e) GA[mu3]) . SpinorU[p1, me]) * ComplexConjugate[PolarizationVector[k2, mu4]] * PolarizationVector[k1, mu3];
ampU = (SpinorUBar[p2, me] . ((-I e) GA[mu4]) . (I (GS[qU] + me)/(SP[qU, qU] - me^2 + I epsilon)) . ((-I e) GA[mu3]) . SpinorU[p1, me]) * PolarizationVector[k1, mu4] * ComplexConjugate[PolarizationVector[k2, mu3]];
diagramAmplitudes = <|"amp_s" -> ampS, "amp_u" -> ampU|>;
ampTotal = ampS + ampU;
```

## Lightweight smoke-test output

### B01

```text
��L o a d i n g   F e y n C a l c   f r o m   C : \ U s e r s \ l e n o v o \ A p p D a t a \ R o a m i n g \ W o l f r a m \ A p p l i c a t i o n s \ F e y n C a l c \ 
 
 $ P r e P r i n t   i s   s e t   t o   F e y n C a l c F o r m .   U s e   F I   a n d   F C   t o   c h a n g e   t h e   d i s p l a y   f o r m a t . 
 
 F e y n C a l c   1 0 . 1 . 0   ( s t a b l e   v e r s i o n ) .   F o r   h e l p ,   u s e   t h e   D i s p l a y F o r m [ B u t t o n B o x [ o n l i n e   d o c u m e n t a t i o n , ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / f e y n c a l c . g i t h u b . i o / r e f e r e n c e D e v ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / f e y n c a l c . g i t h u b . i o / r e f e r e n c e D e v ] ]   v i s i t   t h e   D i s p l a y F o r m [ B u t t o n B o x [ f o r u m ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c / d i s c u s s i o n s ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c / d i s c u s s i o n s / ] ]   a n d   h a v e   a   l o o k   a t   t h e   s u p p l i e d   D i s p l a y F o r m [ B u t t o n B o x [ e x a m p l e s . ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n F u n c t i o n   : >   S y s t e m O p e n [ F i l e N a m e J o i n [ { $ F e y n C a l c D i r e c t o r y ,   E x a m p l e s } ] ] ,   E v a l u a t o r   - >   A u t o m a t i c ,   M e t h o d   - >   P r e e m p t i v e ] ]   T h e   P D F - v e r s i o n   o f   t h e   m a n u a l   c a n   b e   d o w n l o a d e d   D i s p l a y F o r m [ B u t t o n B o x [ h e r e . ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c - m a n u a l / r e l e a s e s / d o w n l o a d / d e v - m a n u a l / F e y n C a l c M a n u a l . p d f ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c - m a n u a l / r e l e a s e s / d o w n l o a d / d e v - m a n u a l / F e y n C a l c M a n u a l . p d f ] ] 
 
 I f   y o u   u s e   F e y n C a l c   i n   y o u r   r e s e a r c h ,   p l e a s e   e v a l u a t e   F e y n C a l c H o w T o C i t e [ ]   t o   l e a r n   h o w   t o   c i t e   t h i s   s o f t w a r e . 
 
 P l e a s e   k e e p   i n   m i n d   t h a t   t h e   p r o p e r   a c a d e m i c   a t t r i b u t i o n   o f   o u r   w o r k   i s   c r u c i a l   t o   e n s u r e   t h e   f u t u r e   d e v e l o p m e n t   o f   t h i s   p a c k a g e ! 
 
 L o a d e d   g e n e r a t e d   a m p l i t u d e s   f o r   B 0 1 _ e e _ t o _ m u m u 
 
 S M O K E   s t r u c t u r a l   s u m m a r y :   d i a g r a m s = 1 ;   k e y s = { a m p _ s } ;   q = { q _ s } 
 
 B 0 1 _ E X I T _ C O D E = 0 
 
 B 0 1 _ R U N T I M E _ S E C O N D S = 1 0 . 2 0 5 
 
 
```

### B02

```text
��L o a d i n g   F e y n C a l c   f r o m   C : \ U s e r s \ l e n o v o \ A p p D a t a \ R o a m i n g \ W o l f r a m \ A p p l i c a t i o n s \ F e y n C a l c \ 
 
 $ P r e P r i n t   i s   s e t   t o   F e y n C a l c F o r m .   U s e   F I   a n d   F C   t o   c h a n g e   t h e   d i s p l a y   f o r m a t . 
 
 F e y n C a l c   1 0 . 1 . 0   ( s t a b l e   v e r s i o n ) .   F o r   h e l p ,   u s e   t h e   D i s p l a y F o r m [ B u t t o n B o x [ o n l i n e   d o c u m e n t a t i o n , ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / f e y n c a l c . g i t h u b . i o / r e f e r e n c e D e v ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / f e y n c a l c . g i t h u b . i o / r e f e r e n c e D e v ] ]   v i s i t   t h e   D i s p l a y F o r m [ B u t t o n B o x [ f o r u m ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c / d i s c u s s i o n s ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c / d i s c u s s i o n s / ] ]   a n d   h a v e   a   l o o k   a t   t h e   s u p p l i e d   D i s p l a y F o r m [ B u t t o n B o x [ e x a m p l e s . ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n F u n c t i o n   : >   S y s t e m O p e n [ F i l e N a m e J o i n [ { $ F e y n C a l c D i r e c t o r y ,   E x a m p l e s } ] ] ,   E v a l u a t o r   - >   A u t o m a t i c ,   M e t h o d   - >   P r e e m p t i v e ] ]   T h e   P D F - v e r s i o n   o f   t h e   m a n u a l   c a n   b e   d o w n l o a d e d   D i s p l a y F o r m [ B u t t o n B o x [ h e r e . ,   B u t t o n D a t a   : >   { U R L [ h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c - m a n u a l / r e l e a s e s / d o w n l o a d / d e v - m a n u a l / F e y n C a l c M a n u a l . p d f ] ,   N o n e } ,   B a s e S t y l e   - >   H y p e r l i n k ,   B u t t o n N o t e   - >   h t t p s : / / g i t h u b . c o m / F e y n C a l c / f e y n c a l c - m a n u a l / r e l e a s e s / d o w n l o a d / d e v - m a n u a l / F e y n C a l c M a n u a l . p d f ] ] 
 
 I f   y o u   u s e   F e y n C a l c   i n   y o u r   r e s e a r c h ,   p l e a s e   e v a l u a t e   F e y n C a l c H o w T o C i t e [ ]   t o   l e a r n   h o w   t o   c i t e   t h i s   s o f t w a r e . 
 
 P l e a s e   k e e p   i n   m i n d   t h a t   t h e   p r o p e r   a c a d e m i c   a t t r i b u t i o n   o f   o u r   w o r k   i s   c r u c i a l   t o   e n s u r e   t h e   f u t u r e   d e v e l o p m e n t   o f   t h i s   p a c k a g e ! 
 
 L o a d e d   g e n e r a t e d   a m p l i t u d e s   f o r   B 0 2 _ c o m p t o n 
 
 S M O K E   s t r u c t u r a l   s u m m a r y :   d i a g r a m s = 2 ;   k e y s = { a m p _ s ,   a m p _ u } ;   q = { q _ s ,   q _ u } 
 
 B 0 2 _ E X I T _ C O D E = 0 
 
 B 0 2 _ R U N T I M E _ S E C O N D S = 5 . 9 8 2 
 
 
```

## Hashes/paths of amplitudes.pdf

- `benchmarks/B01_ee_to_mumu/amplitudes.pdf`: sha256 `6cfeb020077742eff79455989579e51341abe09ec1817c9f57177148678c2f46`
- `benchmarks/B02_compton/amplitudes.pdf`: sha256 `99c35187b9f93b3386ce93272087a5a06599c50937eb91d89eb82c43a5de9c86`

## Names/hashes of compute_m2.wl and ward_check.wl

- `benchmarks/B01_ee_to_mumu/compute_m2.wl`: sha256 `95f6f9a55225aaf38d564e28039d8caea246f483c705385976c119da5c89ef90`
- `benchmarks/B02_compton/compute_m2.wl`: sha256 `ac4b0386731dd66c808fa96061f64819be510d9f7af100e10b070f01f3cacc65`
- `benchmarks/B02_compton/ward_check.wl`: sha256 `858cd3b73f8e55781cfb436ee57ee6ce7f7a7522e52c7f87538a4c0418d257f6`

## Proof that compute_m2.wl was not executed

```text

```

## All test results

### Schema validators

```text
��P A S S   b e n c h m a r k s / B 0 1 _ e e _ t o _ m u m u / p h y s i c s _ c a r d . y a m l   - >   s c h e m a s / p h y s i c s _ c a r d . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 1 _ e e _ t o _ m u m u / c o n v e n t i o n _ c a r d . y a m l   - >   s c h e m a s / c o n v e n t i o n _ c a r d . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 1 _ e e _ t o _ m u m u / d i a g r a m s . y a m l   - >   s c h e m a s / d i a g r a m _ i r . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 1 _ e e _ t o _ m u m u / a m p l i t u d e _ i r . y a m l   - >   s c h e m a s / a m p l i t u d e _ i r . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 2 _ c o m p t o n / p h y s i c s _ c a r d . y a m l   - >   s c h e m a s / p h y s i c s _ c a r d . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 2 _ c o m p t o n / c o n v e n t i o n _ c a r d . y a m l   - >   s c h e m a s / c o n v e n t i o n _ c a r d . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 2 _ c o m p t o n / d i a g r a m s . y a m l   - >   s c h e m a s / d i a g r a m _ i r . s c h e m a . j s o n 
 
 P A S S   b e n c h m a r k s / B 0 2 _ c o m p t o n / a m p l i t u d e _ i r . y a m l   - >   s c h e m a s / a m p l i t u d e _ i r . s c h e m a . j s o n 
 
 P A S S   r u l e s / q e d / q e d _ t r e e _ v 1 . y a m l   - >   s c h e m a s / r u l e _ r e g i s t r y . s c h e m a . j s o n 
 
 
```

### Full Python tests

```text
��= = = = = = = = = = = = = = = = = = = = = = = = = = = = =   t e s t   s e s s i o n   s t a r t s   = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
 
 p l a t f o r m   w i n 3 2   - -   P y t h o n   3 . 1 0 . 9 ,   p y t e s t - 7 . 3 . 1 ,   p l u g g y - 1 . 0 . 0 
 
 b e n c h m a r k :   4 . 0 . 0   ( d e f a u l t s :   t i m e r = t i m e . p e r f _ c o u n t e r   d i s a b l e _ g c = F a l s e   m i n _ r o u n d s = 5   m i n _ t i m e = 0 . 0 0 0 0 0 5   m a x _ t i m e = 1 . 0   c a l i b r a t i o n _ p r e c i s i o n = 1 0   w a r m u p = F a l s e   w a r m u p _ i t e r a t i o n s = 1 0 0 0 0 0 ) 
 
 r o o t d i r :   E : \ 0 0 3 h e p - p h - r e s e a r c h \ A g e n t \ F e y n A g e n t 
 
 p l u g i n s :   a n y i o - 3 . 5 . 0 ,   a s y n c i o - 0 . 2 1 . 0 ,   b e n c h m a r k - 4 . 0 . 0 ,   c o v - 4 . 0 . 0 ,   i n t e g r a t i o n - 0 . 2 . 3 ,   m o c k - 3 . 1 0 . 0 
 
 a s y n c i o :   m o d e = s t r i c t 
 
 c o l l e c t e d   5 9   i t e m s 
 
 
 
 t e s t s \ t e s t _ a m p l i t u d e _ b a c k e n d s . p y   . . . . .                                                                       [     8 % ] 
 
 t e s t s \ t e s t _ a m p l i t u d e _ b u i l d e r . p y   . . . . . . . . .                                                                 [   2 3 % ] 
 
 t e s t s \ t e s t _ a m p l i t u d e _ i r _ s c h e m a . p y   . . . . .                                                                     [   3 2 % ] 
 
 t e s t s \ t e s t _ b 0 2 _ c o m p t o n . p y   . . . . . . . . . . . .                                                                       [   5 2 % ] 
 
 t e s t s \ t e s t _ d a y 2 _ b e n c h m a r k s . p y   . . . . . . . .                                                                       [   6 6 % ] 
 
 t e s t s \ t e s t _ s c h e m a _ f i l e s . p y   . . .                                                                                       [   7 1 % ] 
 
 t e s t s \ t e s t _ t i k z _ r e n d e r e r . p y   . . . . . .                                                                               [   8 1 % ] 
 
 t e s t s \ t e s t _ t o p o l o g y _ g e n e r a t o r . p y   . . . . . . . . . . .                                                           [ 1 0 0 % ] 
 
 
 
 = = = = = = = = = = = = = = = = = = = = = = = = = = = = =   5 9   p a s s e d   i n   6 . 3 5 s   = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
 
 
```

### Renderer regression tests

```text
��= = = = = = = = = = = = = = = = = = = = = = = = = = = = =   t e s t   s e s s i o n   s t a r t s   = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
 
 p l a t f o r m   w i n 3 2   - -   P y t h o n   3 . 1 0 . 9 ,   p y t e s t - 7 . 3 . 1 ,   p l u g g y - 1 . 0 . 0 
 
 b e n c h m a r k :   4 . 0 . 0   ( d e f a u l t s :   t i m e r = t i m e . p e r f _ c o u n t e r   d i s a b l e _ g c = F a l s e   m i n _ r o u n d s = 5   m i n _ t i m e = 0 . 0 0 0 0 0 5   m a x _ t i m e = 1 . 0   c a l i b r a t i o n _ p r e c i s i o n = 1 0   w a r m u p = F a l s e   w a r m u p _ i t e r a t i o n s = 1 0 0 0 0 0 ) 
 
 r o o t d i r :   E : \ 0 0 3 h e p - p h - r e s e a r c h \ A g e n t \ F e y n A g e n t 
 
 p l u g i n s :   a n y i o - 3 . 5 . 0 ,   a s y n c i o - 0 . 2 1 . 0 ,   b e n c h m a r k - 4 . 0 . 0 ,   c o v - 4 . 0 . 0 ,   i n t e g r a t i o n - 0 . 2 . 3 ,   m o c k - 3 . 1 0 . 0 
 
 a s y n c i o :   m o d e = s t r i c t 
 
 c o l l e c t e d   5   i t e m s 
 
 
 
 t e s t s \ t e s t _ a m p l i t u d e _ b a c k e n d s . p y   . . . . .                                                                       [ 1 0 0 % ] 
 
 
 
 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =   5   p a s s e d   i n   0 . 8 0 s   = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
 
 
```

### Clean diagram generation

```text
��g e n e r a t e d   1   d i a g r a m ( s ) :   s 
 
 w r o t e   r u n s \ d a y 3 _ f i n a l _ q a \ 2 0 2 6 0 8 1 2 _ 2 2 0 4 5 2 \ B 0 1 _ e e _ t o _ m u m u \ g e n e r a t e d _ d i a g r a m s . y a m l 
 
 
��g e n e r a t e d   2   d i a g r a m ( s ) :   s ,   u 
 
 w r o t e   r u n s \ d a y 3 _ f i n a l _ q a \ 2 0 2 6 0 8 1 2 _ 2 2 0 4 5 2 \ B 0 2 _ c o m p t o n \ g e n e r a t e d _ d i a g r a m s . y a m l 
 
 
```

### Diagram comparison

Strict comparison warning:

```text
��p y t h o n   :   F A I L   B 0 1 _ e e _ t o _ m u m u :   c l e a n   g e n e r a t e d   D i a g r a m I R   d i f f e r s   f r o m   s t o r e d   D i a g r a m I R 
 
 A t   l i n e : 1 7   c h a r : 6 
 
 +   ' @   |   p y t h o n   -   2 > & 1   |   T e e - O b j e c t   - F i l e P a t h   $ l o g 
 
 +             ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
 
         +   C a t e g o r y I n f o                     :   N o t S p e c i f i e d :   ( F A I L   B 0 1 _ e e _ t o _ . . . t o r e d   D i a g r a m I R : S t r i n g )   [ ] ,   R e m o t e E x c e p t i o n 
 
         +   F u l l y Q u a l i f i e d E r r o r I d   :   N a t i v e C o m m a n d E r r o r 
 
   
 
 
```

Normalized structural comparison:

```text
��P A S S   B 0 1 _ e e _ t o _ m u m u :   n o r m a l i z e d   c l e a n   D i a g r a m I R   s t r u c t u r e   m a t c h e s   s t o r e d   D i a g r a m I R 
 
 P A S S   B 0 2 _ c o m p t o n :   n o r m a l i z e d   c l e a n   D i a g r a m I R   s t r u c t u r e   m a t c h e s   s t o r e d   D i a g r a m I R 
 
 
```

### Physics audit

```text
��P A S S   Q E D   a u d i t   s t a t u s   r u l e : q e d _ t r e e _ v 1 : e _ e _ g a m m a _ v e r t e x :   v a l i d a t e d 
 
 P A S S   Q E D   a u d i t   s t a t u s   r u l e : q e d _ t r e e _ v 1 : m u _ m u _ g a m m a _ v e r t e x :   v a l i d a t e d 
 
 P A S S   Q E D   a u d i t   s t a t u s   r u l e : q e d _ t r e e _ v 1 : e l e c t r o n _ p r o p a g a t o r :   v a l i d a t e d 
 
 P A S S   Q E D   a u d i t   s t a t u s   r u l e : q e d _ t r e e _ v 1 : p h o t o n _ p r o p a g a t o r :   v a l i d a t e d 
 
 P A S S   a p p r o v a l s   B 0 1 _ e e _ t o _ m u m u :   a m p l i t u d e _ g e n e r a t i o n   a p p r o v e d ;   h e a v y _ c a l c u l a t i o n   n o t _ r e q u e s t e d 
 
 P A S S   a p p r o v a l s   B 0 2 _ c o m p t o n :   a m p l i t u d e _ g e n e r a t i o n   a p p r o v e d ;   h e a v y _ c a l c u l a t i o n   n o t _ r e q u e s t e d 
 
 P A S S   p r o v e n a n c e   B 0 1 _ e e _ t o _ m u m u :   d i a g r a m _ i r : b 0 1 _ e e _ t o _ m u m u _ g o l d _ t o p o l o g y   s h a 2 5 6 = e b e 8 8 1 3 a 8 6 3 0 f 8 7 b 2 7 c 3 6 5 6 2 d c d 4 4 f 2 0 8 1 f d a 3 8 9 4 8 5 1 f 0 1 3 8 3 8 c 0 b c e a b e 4 d 6 3 7 
 
 P A S S   u n i q u e   i n d i c e s   a m p l i t u d e : b 0 1 _ e e _ t o _ m u m u : a m p _ s :   1 2   l o c a l   i n d i c e s 
 
 P A S S   p r o v e n a n c e   B 0 2 _ c o m p t o n :   d i a g r a m _ i r : b 0 2 _ c o m p t o n _ t r e e _ t o p o l o g i e s   s h a 2 5 6 = b 8 c 1 4 3 2 9 a a d f 0 3 0 7 8 0 6 1 e d 8 2 8 4 e 7 0 d d e d 2 d 1 5 f f d c c f 8 4 e 8 5 8 0 e e 5 c e c 9 a 5 0 b 2 b 4 
 
 P A S S   u n i q u e   i n d i c e s   a m p l i t u d e : b 0 2 _ c o m p t o n : a m p _ s :   1 2   l o c a l   i n d i c e s 
 
 P A S S   u n i q u e   i n d i c e s   a m p l i t u d e : b 0 2 _ c o m p t o n : a m p _ u :   1 2   l o c a l   i n d i c e s 
 
 P A S S   w a v e f u n c t i o n   i n c o m i n g   f e r m i o n   - >   u 
 
 P A S S   w a v e f u n c t i o n   o u t g o i n g   f e r m i o n   - >   u b a r 
 
 P A S S   w a v e f u n c t i o n   i n c o m i n g   a n t i f e r m i o n   - >   v b a r 
 
 P A S S   w a v e f u n c t i o n   o u t g o i n g   a n t i f e r m i o n   - >   v 
 
 P A S S   B 0 1   t w o - c u r r e n t   s t r u c t u r e ,   q _ s = p 1 + p 2 ,   a m p T o t a l = a m p _ s 
 
 P A S S   B 0 2   s / u   c h a i n   o r d e r ,   o u t g o i n g   p h o t o n   c o n j u g a t i o n ,   q _ s / q _ u ,   a m p T o t a l = a m p _ s + a m p _ u 
 
 P A S S   i n t e r n a l   f e r m i o n   a r r o w   d i r e c t i o n :   B 0 2   i n t e r n a l   e -   l i n e   f r o m   p s i _ b a r   s l o t   t o   p s i   s l o t 
 
 P A S S   a n t i p a r t i c l e   a r r o w   d i r e c t i o n :   i n c o m i n g   e +   b i n d s   p s i _ b a r ;   o u t g o i n g   m u +   b i n d s   p s i 
 
 P A S S   c o m p u t e _ m 2   n o t   e x e c u t e d   f o r   B 0 1 _ e e _ t o _ m u m u :   n o   m 2 _ o u t p u t s   d i r e c t o r y 
 
 P A S S   c o m p u t e _ m 2   n o t   e x e c u t e d   f o r   B 0 2 _ c o m p t o n :   n o   m 2 _ o u t p u t s   d i r e c t o r y 
 
 
```

## All warnings

- Metadata-only strict DiagramIR comparison difference: generated candidate status/object IDs versus stored approved gold metadata.
- LaTeX overfull boxes for long rule/audit identifiers.
- MiKTeX update reminder emitted during PDF compilation.
- Broader absolute-path scan found pre-existing paths in B00 environment outputs and `docs/ENVIRONMENT_REPORT.md`; excluded from review-relevant canonical package.
