# Migration: PhysicsCard 0.1.x To 0.2.0

Day 5 repairs the contract boundary between physics intent, backend implementation, and execution authorization.

## PhysicsCard 0.2.0

`PhysicsCard` is now backend-neutral. It records the requested theory intent using structured fields:

- `model_id`
- `sector`

For the current QED benchmarks:

- `model_id: sm_qed`
- `sector: qed`

Backend-specific fields such as direct RuleRegistry or native-registry selection are removed from the canonical PhysicsCard path.

## BackendProfile

Backend implementation is moved into `BackendProfile` objects.

- `profiles/backends/feynarts_sm_qed.yaml` resolves `sm_qed/qed` to FeynArts `SM`, generic model `Lorentz`, `Restrictions -> QEDOnly`, `InsertionLevel -> Classes`, and profile-local particle mappings.
- `profiles/backends/legacy_sm_qed.yaml` resolves `sm_qed/qed` to the legacy audited QED RuleRegistry snapshot `registry:qed_tree_v1` and `ruleset:qed_tree_v1`.

The native particle-to-FeynArts mapping belongs to the native backend profile, not generic particle identity.

## ExecutionRequest

`ExecutionRequest` is runtime authorization, not canonical physics truth. It supports:

- `structural`
- `amplitude_only`
- `benchmark_regression`
- `production_heavy`

It records `backend_profile_id`, `authorized_by`, `authorized_at`, timeout policy, and allowed operations.

## Day-4 Contract Repair

Day-4 bounded M2 regression was explicitly user-authorized as a benchmark regression. Production `heavy_calculation` approval remained not requested. In 0.2.0 this distinction belongs in `ExecutionRequest`: benchmark regression may be authorized without mutating canonical production-heavy approval.

## Benchmark Migration

B01, B02, and B03 now use backend-neutral PhysicsCards with `model_id: sm_qed` and `sector: qed`. Native and legacy execution paths choose implementation via backend profiles.

## Legacy B03 Reclassification

B03 legacy structural generation is no longer blocked by `PhysicsCard` selecting a native-only registry. When generated through `profiles/backends/legacy_sm_qed.yaml`, B03 produces the expected generic t-channel photon exchange. The old Day-4 `LEGACY_LIMITATION` is therefore reclassified as resolved configuration coupling for structural topology generation.
