# Day 8 Security and Publication Audit

Status: PASS_NO_PRIVATE_EXTERNAL_KNOWLEDGE_TRACKED

Branch: `release/v0.1.0`
Audit date: 2026-08-26

## Scope

This audit covered tracked repository content only, using `git ls-files` and `git grep`. Untracked local scratch files and Git author metadata were intentionally excluded from privacy and publication findings.

No Git history was rewritten. No physics code was changed. No B04 M2 calculation was rerun. No release tag or GitHub release was created.

## Trust documentation updates

Created or updated:

- `SECURITY.md`
- `docs/CUSTOM_KNOWLEDGE_TRUST.md`
- `README.md`
- `docs/QUICKSTART.md`

Documented public trust boundaries:

- custom Wolfram `.wl`, `.m`, and `.nb` files are executable code and require user trust before execution;
- FeynAgent does not automatically trust arbitrary Wolfram scripts, notebooks, helper package output, or pasted expressions;
- locked custom routes require convention, rule, and hash validation;
- FeynGrav and package-helper output may be evidence but is not automatically physics authority;
- production-heavy execution requires explicit authorization;
- private/source external knowledge is not bundled in the repository;
- Apache-2.0 applies only to FeynAgent-owned content and does not vendor, sublicense, or relicense FeynCalc, FeynArts, Mathematica/Wolfram, FeynGrav, or private external knowledge packages.

The active public install docs were also sanitized to replace a development-machine-specific skill validator path with a placeholder path.

## Tracked repository scan

Commands used:

```bash
git ls-files
git grep -n -I -E "absolute local path patterns"
git grep -n -I -E "credential and token-like patterns"
git ls-files | Select-String "archive, run, .feynagent, notebook, pdf, external knowledge patterns"
git grep -l -I -i -E "B04 and locked custom route patterns"
```

Findings:

| Category | Result | Notes |
| --- | --- | --- |
| Private external knowledge tracked | PASS | No tracked private external knowledge package root, raw package directory, or private payload was found. The B04 committed manifest is hash-only metadata. |
| Accidental `.feynagent/` state | PASS | No tracked `.feynagent/` files. |
| Generated `runs/` outputs | PASS | Tracked `runs/` content is limited to `runs/.gitkeep`. |
| Raw private notebooks | PASS | No tracked `.nb` files. |
| Raw private PDFs | PASS | No tracked private/source PDF payloads. The only tracked PDFs are curated public gallery artifacts. |
| Stale review ZIP/archive binaries | PASS | No tracked `.zip`, `.7z`, `.rar`, `.tar`, `.tgz`, or `.tar.gz` files. |
| Credential/token/password-like material | PASS_WITH_FALSE_POSITIVES | Matches were prose about GitHub authentication failure or code/test variable names such as `token`; no actual secret material was found. |
| Absolute Windows/local paths | SANITIZE_RECOMMENDED | Active README/Quickstart user docs were sanitized. Historical reports and tests still contain local path evidence or mocked local paths; these are not private external knowledge, but should be sanitized or excluded from a polished release artifact if desired. |

Tracked files still containing absolute local path evidence after active-doc sanitization:

- `reports/DAY2_FEYNARTS_CROSSCHECK.md`
- `reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md`
- `reports/DAY4_PRECLEAN_MANIFEST.md`
- `reports/DAY4_REPOSITORY_CLEANUP.md`
- `reports/DAY4_ZIP_SELFTEST.md`
- `reports/DAY5_SKILL_E2E.md`
- `reports/DAY5_ZIP_SELFTEST.md`
- `reports/DAY6_CODEX_SKILL_INSTALL.md`
- `reports/DAY6_RELEASE_METADATA_AUDIT.md`
- `reports/DAY6_RELEASE_RC_REPORT.md`
- `reports/DAY6_WHEEL_INSTALL_E2E.md`
- `reports/DAY7_B04_AMPLITUDE_CLOSURE.md`
- `reports/DAY7_B04_TOPOLOGY.md`
- `reports/DAY7_GITHUB_CLONE_SMOKE.md`
- `reports/DAY7_PHASE1B_SKILL_METADATA_REPAIR.md`
- `reports/DAY7_REPORT.md`
- `reports/DAY8_PHASE0_RELEASE_BASELINE.md`
- `tests/test_initialization.py`

These are historical audit/test evidence, not tracked private external knowledge. They are publication hygiene items, not stop-condition findings.

## Public B04 file classification

| File | Classification | Rationale |
| --- | --- | --- |
| `benchmarks/B04_phi_phi_to_hh/convention_reference.yaml` | PUBLIC_SAFE | Sanitized convention metadata; no private payload. |
| `benchmarks/B04_phi_phi_to_hh/expected_topology.yaml` | PUBLIC_SAFE | Expected topology metadata only. |
| `benchmarks/B04_phi_phi_to_hh/knowledge_manifest.yaml` | PUBLIC_SAFE | Hash-only external knowledge manifest; no raw source package, no local root value. |
| `benchmarks/B04_phi_phi_to_hh/physics_card.yaml` | PUBLIC_SAFE | Locked process card with external knowledge referenced only through logical lock policy. |
| `benchmarks/B04_phi_phi_to_hh/process_description.yaml` | PUBLIC_SAFE | Sanitized process description and gate status. |
| `benchmarks/B04_phi_phi_to_hh/README.md` | PUBLIC_SAFE | Explicitly says private/source material and local roots must not be committed. |
| `benchmarks/B04_phi_phi_to_hh/rule_manifest.yaml` | PUBLIC_SAFE | Logical rule IDs and trust status only; no raw formulas from private package. |
| `profiles/backends/b04_custom_gravity_audited.yaml` | PUBLIC_SAFE | Locked backend routing metadata only. |
| `examples/B04_locked_scalar_gravity/manifest.yaml` | PUBLIC_SAFE | Documentation manifest; states external knowledge is separate and unbundled. |
| `examples/B04_locked_scalar_gravity/README.md` | PUBLIC_SAFE | Public-safe example text; explicitly excludes private PDFs, notebooks, and local paths. |
| `examples/gallery/B04_locked_scalar_gravity_topology.pdf` | PUBLIC_SAFE | Curated generated topology artifact with provenance and SHA256 recorded; not raw private source material. |
| `examples/gallery/README.md` | PUBLIC_SAFE | Curated artifact provenance and hashes only. |
| `README.md` | PUBLIC_SAFE | Public scope and trust boundary wording; active local path example sanitized. |
| `CHANGELOG.md` | PUBLIC_SAFE | Release notes with locked B04 scope; no private payload. |
| `CITATION.cff` | PUBLIC_SAFE | Citation metadata and external-package reminders; no release date claim or private payload. |
| `CONTRIBUTING.md` | PUBLIC_SAFE | Contribution trust and licensing boundaries. |
| `pyproject.toml` | PUBLIC_SAFE | Package metadata only. |
| `docs/ARCHITECTURE.md` | PUBLIC_SAFE | Architecture and B04 route description without private payload. |
| `docs/BACKEND_STRATEGY.md` | PUBLIC_SAFE | Backend trust boundaries and unsupported scope. |
| `docs/CI_AND_RELEASE_GATES.md` | PUBLIC_SAFE | CI/release gate policy; no private payload. |
| `docs/CUSTOM_KNOWLEDGE_TRUST.md` | PUBLIC_SAFE | New custom knowledge trust policy. |
| `docs/MIGRATION_DAY7_B04_CUSTOM_IDS.md` | PUBLIC_SAFE | Schema ID migration note; no private payload. |
| `docs/QUICKSTART.md` | PUBLIC_SAFE | Public setup/use instructions; active local path example sanitized. |
| `docs/READINESS_LEVELS.md` | PUBLIC_SAFE | Readiness scope and locked B04 caveats. |
| `docs/RELEASE_SCOPE_V0_1.md` | PUBLIC_SAFE | Validated public release scope. |
| `docs/SCOPE_V0_1.md` | PUBLIC_SAFE | Public v0.1 scope statement. |
| `docs/SKILL_USAGE.md` | PUBLIC_SAFE | Skill routing and execution-gate policy. |
| `schemas/backend_profile.schema.json` | PUBLIC_SAFE | Schema only. |
| `src/feynagent/schemas/backend_profile.schema.json` | PUBLIC_SAFE | Packaged schema copy only. |
| `scripts/check_release_invariants.py` | PUBLIC_SAFE | Release hygiene script; includes deny-patterns, not secrets. |
| `scripts/day7_b04_amplitudes.py` | PUBLIC_SAFE | Helper script; no private payload. |
| `scripts/day7_b04_phase7_closure.py` | PUBLIC_SAFE | Helper script; no private payload. |
| `scripts/day7_b04_topology.py` | PUBLIC_SAFE | Helper script; no private payload. |
| `scripts/validate_examples.py` | PUBLIC_SAFE | Example validation script; no private payload. |
| `scripts/verify_knowledge_lock.py` | PUBLIC_SAFE | Hash/lock verification helper; no private payload. |
| `skills/feynagent/SKILL.md` | PUBLIC_SAFE | Public skill policy with locked route and unsupported scope. |
| `skills/feynagent/evals/smoke_cases.json` | PUBLIC_SAFE | Skill eval cases only. |
| `skills/feynagent/references/BACKEND_POLICY.md` | PUBLIC_SAFE | Backend routing/trust policy. |
| `skills/feynagent/scripts/ensure_initialized.py` | PUBLIC_SAFE | Skill initialization helper. |
| `skills/feynagent/scripts/run_feynagent.py` | PUBLIC_SAFE | Skill route helper. |
| `src/feynagent/b04_amplitudes.py` | PUBLIC_SAFE | Source contains private-path guardrails and hash verification references; no private payload. |
| `src/feynagent/b04_phase7_closure.py` | PUBLIC_SAFE | Deterministic closure/audit code; no private payload. |
| `src/feynagent/b04_topology.py` | PUBLIC_SAFE | Topology code with private-path guardrails; no private payload. |
| `src/feynagent/backends/b04_custom.py` | PUBLIC_SAFE | Locked backend adapter; no private payload. |
| `src/feynagent/custom_knowledge.py` | PUBLIC_SAFE | Local mapping resolver; does not commit local mapping contents. |
| `src/feynagent/dispatch.py` | PUBLIC_SAFE | Route classification code. |
| `src/feynagent/init.py` | PUBLIC_SAFE | Environment probing code; no private payload. |
| `src/feynagent/runner.py` | PUBLIC_SAFE | Runner/gate code. |
| `tests/test_b04_amplitude_closure.py` | PUBLIC_SAFE | Regression tests; no private payload. |
| `tests/test_b04_custom_gravity.py` | PUBLIC_SAFE | Regression tests and private-path guard assertions. |
| `tests/test_b04_phase7_closure.py` | PUBLIC_SAFE | Regression tests; no private payload. |
| `tests/test_b04_skill_dispatch.py` | PUBLIC_SAFE | Skill dispatch tests; no private payload. |
| `tests/test_b04_topology_phase5.py` | PUBLIC_SAFE | Topology tests and private-path guard assertions. |
| `reports/DAY4_NATIVE_AMPLITUDE_REGRESSION.md` | SANITIZE | Historical report includes machine-local FeynCalc example paths; not B04-private content. |
| `reports/DAY5_REPORT.md` | PUBLIC_SAFE | Historical release report; no private B04 payload identified. |
| `reports/DAY5_REVIEW_PACKAGE.md` | PUBLIC_SAFE | Historical review report; no private B04 payload identified. |
| `reports/DAY6_RELEASE_RC_REPORT.md` | SANITIZE | Historical report includes machine-local run paths; no private B04 payload. |
| `reports/DAY7_B04_AMPLITUDE_CLOSURE.md` | SANITIZE | Historical B04 evidence includes machine-local worktree/run paths; no private knowledge payload. |
| `reports/DAY7_B04_BACKEND_FEASIBILITY.md` | PUBLIC_SAFE | B04 feasibility report; no private payload identified. |
| `reports/DAY7_B04_PHASE7_CLOSURE.md` | PUBLIC_SAFE | B04 closure report; no private payload identified. |
| `reports/DAY7_B04_SKILL_E2E.md` | PUBLIC_SAFE | B04 skill E2E report; records no external private absolute paths. |
| `reports/DAY7_B04_TOPOLOGY.md` | SANITIZE | Historical B04 topology report includes a machine-local generated PDF path; no private knowledge payload. |
| `reports/DAY7_PHASE0_DAY6_CLOSURE.md` | PUBLIC_SAFE | Historical bridge report; no private B04 payload identified. |
| `reports/DAY7_REPORT.md` | SANITIZE | Historical closeout includes canonical/worktree local paths; no private knowledge payload. |
| `reports/DAY7_REVIEW_PACKAGE.md` | PUBLIC_SAFE | Explicitly excludes private external gravity source material and B04 M2 rerun artifacts. |
| `reports/DAY8_CI_SETUP.md` | PUBLIC_SAFE | CI report and Actions URL only. |
| `reports/DAY8_PHASE0_RELEASE_BASELINE.md` | SANITIZE | Baseline report includes canonical local repository path; no private knowledge payload. |
| `reports/DAY8_PUBLIC_EXAMPLES_AUDIT.md` | PUBLIC_SAFE | Example/gallery provenance and hashes; no private payload. |
| `reports/DAY8_PUBLIC_SCOPE_AUDIT.md` | PUBLIC_SAFE | Public scope audit; no private payload. |

No B04-related file is classified `REMOVE_FROM_RELEASE` in this audit. The `SANITIZE` items are historical report hygiene items caused by local path evidence, not private external knowledge tracking.

## License and vendoring audit

Confirmed:

- `LICENSE`, `README.md`, `CONTRIBUTING.md`, `CITATION.cff`, `SECURITY.md`, and `docs/CUSTOM_KNOWLEDGE_TRUST.md` state or preserve the boundary that Apache-2.0 applies only to FeynAgent-owned code/documentation.
- The repository does not vendor FeynCalc, FeynArts, Mathematica/Wolfram, or FeynGrav source material.
- The repository does not relicense external physics packages, their examples, their documentation, or private/source external knowledge packages.
- B04 external knowledge is represented by sanitized cards and a hash-only manifest; the private/source package is not bundled.

## Stop-condition check

Private external knowledge tracked: NO.

Because no private external knowledge payload or private external knowledge root is tracked, the stop condition did not trigger.
## Local validation

PASS:

- `python scripts/check_release_invariants.py`
- `python scripts/validate_examples.py`
- `python -m pytest` (`123 passed`)
- `git diff --check` (exit 0; CRLF normalization warnings only)
