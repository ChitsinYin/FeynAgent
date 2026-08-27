# Day-8 Review Package

Date: 2026-08-27
Repository: ChitsinYin/FeynAgent
Release: v0.1.0
Release commit: 02c9c1c31d56ad816437a21b3f1fa02fa4bfbde3
Release URL: https://github.com/ChitsinYin/FeynAgent/releases/tag/v0.1.0
Review bundle: reports/FeynAgent_Day8_Review_Bundle.zip

## Contents

The review bundle is a self-contained source handoff artifact for Python validation and tests. It excludes `.git`, caches, unrelated old run directories, and large transient Mathematica outputs. It is not a release asset and must not be committed.

The bundle includes the tracked repository source tree plus the Day-8 Markdown closeout reports:

- reports/DAY8_REPORT.md
- reports/DAY8_REVIEW_PACKAGE.md
- reports/DAY8_RELEASE_PUBLICATION.md

## Self-Test Commands

Run from the extracted bundle root. Because the bundle intentionally excludes `.git`, initialize ephemeral Git metadata first if running the full pytest suite:

```powershell
git init
git config user.email review@example.invalid
git config user.name "Review Self-Test"
git add .
git commit -m "review bundle self-test snapshot"
python scripts/validate_examples.py
python -m pytest
```

Self-test result recorded during closeout:

- `python scripts/validate_examples.py`: PASS
- `python -m pytest`: PASS (`125 passed`)

## Release Scope Summary

SUPPORTED:

- Standard QED tree-level 2-to-2 for `e-`, `e+`, `mu-`, `mu+`, and `gamma`.
- Locked B04 `phi phi -> h h` custom route with audited external knowledge.

NOT SUPPORTED:

- Arbitrary gravity.
- Arbitrary BSM.
- Arbitrary SM/QCD.
- Loops.

GENERAL_CUSTOM_GRAVITY_PRODUCTION_READY = NO
PUBLIC_V0_1_READY = YES
GITHUB_V0_1_0_RELEASE = PUBLISHED

No private B04 external knowledge, review ZIP, or B04 M2 rerun output is included.
