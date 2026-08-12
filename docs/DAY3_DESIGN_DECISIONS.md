# Day 3 Design Decisions

## AmplitudeIR Is Derived

`AmplitudeIR` is a deterministic derived artifact. It is not a new canonical user-input physics source and must not be edited to change the physics of a process. Its inputs are, in order:

- `PhysicsCard`
- `ConventionCard`
- `RuleRegistry`
- generated `DiagramIR`

A future amplitude builder may emit `AmplitudeIR` only after the relevant amplitude-generation approval gate is approved. Heavy calculation approval remains separate and is not implied by `AmplitudeIR` generation.

## Scope

The Day-3 schema is intentionally limited to tree-level amplitudes. It has no loop momentum, integration measure, counterterm, renormalization, tensor reduction, spin sum, polarization sum, or squared-amplitude structure.

The first contract version is `schema_version: 0.1.0` because this is the initial AmplitudeIR schema, even though it consumes existing `PhysicsCard` and `DiagramIR` 0.1.2 artifacts.

## Structure

An `AmplitudeIR` document contains source identity and hashes, then one or more amplitude records. Each amplitude records:

- the amplitude ID, diagram ID, and process ID;
- source rule IDs;
- external spinor factors;
- instantiated vertex factors;
- instantiated propagator factors;
- local Lorentz and Dirac indices;
- momentum substitutions inherited from DiagramIR slot bindings;
- zero or more ordered fermion chains;
- external bosonic polarization factors;
- non-chain factors, such as a photon propagator linking two separate fermion currents;
- explicit index contractions;
- overall scalar prefactor and relative sign source;
- generation status and audit metadata.

The schema allows small formula fragments on individual factors, such as a vertex coefficient or propagator denominator, but it does not allow a single opaque final LaTeX or FeynCalc string to replace the factor graph.

## Preventing Renderer Divergence

LaTeX and FeynCalc builders should consume the same `AmplitudeIR` factor graph:

- Spinor ordering comes from `fermion_chains[].ordered_factor_ids`.
- Momentum signs come from `momentum_substitutions`, which are copied from DiagramIR convention-conversion bindings.
- Lorentz and Dirac contractions come from `index_contractions`, not renderer-local naming assumptions.
- Non-chain factors keep current-current structures explicit, so B01 cannot be flattened into one fake fermion chain.
- Backend-specific convention maps remain audit metadata and implementation constraints, not hidden edits to rendered strings.

This gives LaTeX and FeynCalc two renderings of one derived structure instead of two independent amplitude constructions.

## B01 Representability

The B01 fixture `benchmarks/B01_ee_to_mumu/amplitude_ir.example.yaml` represents
`e- e+ -> mu- mu+` as one s-channel amplitude with:

- an electron current chain, `vbar(p2) ... u(p1)`;
- a muon current chain, `ubar(p3) ... v(p4)`;
- a non-chain photon propagator factor linking the two currents;
- explicit Lorentz contractions between each current vertex and the photon propagator;
- explicit Dirac contractions inside each current.

This avoids pretending the photon propagator is part of either open fermion chain.

## B02 Representability

The B02 fixture `benchmarks/B02_compton/amplitude_ir.example.yaml` represents s- and u-channel Compton amplitudes. Each amplitude has:

- one ordered electron fermion chain from outgoing `ubar(p2)` to incoming `u(p1)`;
- one internal electron propagator factor;
- two electron-photon vertex factors;
- one incoming photon polarization vector;
- one outgoing conjugated photon polarization vector;
- explicit Lorentz contractions between polarization factors and their vertex factors.

## Index Collision Prevention

Every local Lorentz or Dirac index occurrence gets a unique `index_id` scoped to the amplitude, e.g. `idx:b02:s:mu_v1`. Reusing display labels is therefore unnecessary. A renderer may rename labels for presentation, but the identity and contractions come from `index_id` references.

The schema requires index records to be grouped by Lorentz or Dirac type and referenced by factors and contractions. The tests add semantic checks that all fixture index IDs are unique and that every referenced index exists in the local index table.

## Current Non-Goals

- No amplitude builder is implemented in Day 3 design work.
- No final LaTeX or FeynCalc amplitude strings are generated here.
- No squared amplitudes are computed.
- No heavy Mathematica/FeynCalc calculation is approved or run.