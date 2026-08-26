# Day 8 Release PR Audit

Status: PR_BODY_READY_MANUAL_CREATION_REQUIRED

Audit date: 2026-08-26
Repository: `ChitsinYin/FeynAgent`
Source branch: `release/v0.1.0`
Target branch: `main`

## Branch Verification

- `git fetch origin`: PASS
- Active branch: `release/v0.1.0`
- Day-7 closeout commit: `02cf9c0ea9689d89f4287bb1e3278a04f61c0928`
- Day-7 closeout contained in release branch: PASS
- `main`: `3ef996a3dfc1a5481357b2d3c452f1708f9034ab`
- `origin/main`: `3ef996a3dfc1a5481357b2d3c452f1708f9034ab`
- Main remote divergence: NONE OBSERVED
- Release content audit SHA before this PR audit report: `1f6db2560759113fd18f9ac49738bed1a7e19026`
- `origin/release/v0.1.0` before final PR-report push: `591e61b6b1fb55cf384e3051cbd54f651388a287`

The tracked release worktree was clean after committing the Day 8 security and premerge QA audit files. Local untracked scratch files were left unstaged and are not part of the release branch or PR.

## Diff Review

Reviewed the full `origin/main...release/v0.1.0` diff.

High-level contents:

- public release documentation and metadata updates;
- locked B04 benchmark cards, manifests, backend profile, dispatcher, tests, and reports;
- public examples and curated gallery artifacts;
- GitHub CI workflow and release invariant checks;
- security/trust documentation;
- Day 8 audit reports.

Commit divergence after the Day 8 security/premerge audit commit:

- commits unique to `origin/main`: 0
- commits unique to `release/v0.1.0`: 6

## Forbidden Content Audit

Explicitly checked the PR diff for forbidden generated, private, and binary content.

| Category | Result | Notes |
| --- | --- | --- |
| `.feynagent/` tracked state | PASS | No `.feynagent/` paths in the PR diff. |
| `runs/` generated outputs | PASS | No tracked `runs/` outputs in the PR diff. Generated-run references are documentation/provenance text only. |
| Private external knowledge | PASS | No private/source external knowledge package, private root mapping, raw package payload, or absolute private knowledge root is included. |
| Raw notebooks | PASS | No `.nb` files in the PR diff. |
| Raw/private PDFs | PASS | No raw private PDFs. The only PDFs are curated public gallery artifacts with recorded provenance and SHA256. |
| Build/dist outputs | PASS | No `build/` or `dist/` paths in the PR diff. |
| Secrets | PASS_WITH_FALSE_POSITIVES | Text scan found policy prose, variable names such as `token`, and a historical GitHub auth-failure message; no credentials, tokens, passwords, or key material were found. |
| Review ZIP binaries | PASS | No `.zip`, `.7z`, `.rar`, `.tar`, `.tgz`, or `.tar.gz` review/archive binaries in the PR diff. |

Curated public PDFs in the PR diff:

- `examples/gallery/B02_compton_diagrams.pdf`
- `examples/gallery/B02_compton_amplitudes.pdf`
- `examples/gallery/B04_locked_scalar_gravity_topology.pdf`

These were previously recorded in `reports/DAY8_PUBLIC_EXAMPLES_AUDIT.md` with publication provenance and SHA256.

## Validation Summary

- GitHub Actions CI PASS observed for `release/v0.1.0` at commit `591e61b6b1fb55cf384e3051cbd54f651388a287`: https://github.com/ChitsinYin/FeynAgent/actions/runs/32952672750
- Local release invariant checks PASS after staging the Day 8 security/premerge audit files.
- `python scripts/validate_examples.py` PASS after staging the Day 8 security/premerge audit files.
- `git diff --check --cached` PASS after staging the Day 8 security/premerge audit files.
- Full local premerge RC QA: `PREMERGE_RC_PASS`, recorded in `reports/DAY8_PREMERGE_RC_QA.md`.

## PR Body

The prepared PR body is recorded in `reports/DAY8_PR_BODY.md`.

## Merge Gate

Do not merge until all of the following are true:

- GitHub CI passes on the final PR head;
- local `PREMERGE_RC_PASS` is accepted;
- human diff review is approved.

## PR Creation Attempt

Automatic PR creation was attempted after pushing `release/v0.1.0`.

- `gh --version`: unavailable; GitHub CLI is not installed in this environment.
- GitHub connector read check for existing open PRs: PASS; no existing open PR from `release/v0.1.0` to `main` was found.
- GitHub connector PR creation: FAIL; GitHub API returned `403 Resource not accessible by integration`.

Because no authenticated PR-creation CLI/API is available in this environment, the PR was not created automatically. The prepared PR body remains recorded in `reports/DAY8_PR_BODY.md`.

Manual GitHub UI steps:

1. Open `https://github.com/ChitsinYin/FeynAgent/compare/main...release/v0.1.0`.
2. Confirm base branch is `main` and compare branch is `release/v0.1.0`.
3. Set the PR title to `release: FeynAgent v0.1.0`.
4. Paste the body from `reports/DAY8_PR_BODY.md`.
5. Create the PR without merging it.
6. Wait for GitHub CI to pass on the final PR head.
7. Merge only after GitHub CI PASS, local `PREMERGE_RC_PASS`, and human diff review approval.

No merge, release tag, GitHub release, B04 M2 rerun, or history rewrite was performed during this PR audit.
