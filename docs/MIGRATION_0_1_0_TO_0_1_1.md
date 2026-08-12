# Migration 0.1.0 To 0.1.1

## Purpose

This migration closes Day 1 semantic gaps before Day 2 feature work. It does not add topology generation, amplitude calculation, loop support, FeynRules integration, phase-space integration, remote execution, or autonomous heavy Mathematica workflows.

## Schema Version Bump

The four canonical contracts now use `schema_version: 0.1.1`.

## PhysicsCard Changes

`approval` is now split into `topology`, `amplitude_generation`, and `heavy_calculation` gates. This prevents topology approval from being silently reused as permission to generate amplitudes or run heavy algebra. B02 is approved only for topology. The approval timestamp was generated from the current local clock during migration.

## ConventionCard Changes

No structural convention fields changed. The schema version was bumped so B02 artifacts consistently declare the same canonical contract version after migration.

## RuleRegistry Changes

`particle_catalog` was added to record particle IDs, antiparticle IDs, self-conjugacy, field roles, and fermion number. Rule `participating_fields` now require `field_id` and `quantum_field_role`; for QED this distinguishes `psi` from `psi_bar`.

The QED rules remain `validated_pending_convention_review`; this migration does not promote them to trusted.

## DiagramIR Changes

`vertex_instances.attached_endpoint_ids` was replaced by `vertex_instances.slot_bindings`.

Each slot binding records `rule_slot`, `endpoint_id`, `endpoint_kind`, `expected_particle_id`, `expected_field_id`, `endpoint_particle_id`, `momentum_label`, `momentum_substitution`, `crossing_treatment`, `convention_conversion`, and `fermion_flow`.

This removes order-based ambiguity and makes all-momenta-incoming vertex conversion explicit while preserving physical external momentum labels.

## Rule Duplication Removal

`benchmarks/B02_compton/rule_manifest.yaml` is no longer a full editable copy of QED rules. It is a lightweight non-canonical selector that references `../../rules/qed/qed_tree_v1.yaml`, records the registry ID, selected rule IDs, and the canonical LF-normalized UTF-8 source SHA-256 hash.

Tests now load the canonical rule registry and verify that the manifest hash matches. A stale benchmark-local copy cannot satisfy the B02 rule-resolution tests.

## Regression Tests Added

B02 tests now check schema validation, rule-slot completeness, rule-slot uniqueness, endpoint existence, particle/field compatibility, explicit crossing conversion, canonical rule-manifest hash matching, and preservation of exactly the s and u channels.

## Compatibility Notes

This is a breaking schema migration for DiagramIR vertex instances and PhysicsCard approval. Existing 0.1.0 examples must be migrated rather than patched locally.
