# Day-8 Public Release Publication

Release: FeynAgent v0.1.0
Release date: 2026-08-27
Release tag: v0.1.0
Release commit: 02c9c1c31d56ad816437a21b3f1fa02fa4bfbde3
GitHub Release URL: https://github.com/ChitsinYin/FeynAgent/releases/tag/v0.1.0

## Approval

APPROVE_PUBLIC_V0_1_0_RELEASE was explicitly approved by the human release gate.

## Human Gate Evidence

- CI = PASS
- PREMERGE_RC = PASS
- MAIN_MERGE = PASS
- GITHUB_ZERO_CLONE = PASS
- QED_PUBLIC_E2E = PASS
- B04_MISSING_KNOWLEDGE_GUARD = PASS
- B04_MAINTAINER_SMOKE = PASS
- PRIVATE_KNOWLEDGE_AUDIT = PASS
- VERSION_METADATA = READY

## Local Verification

- Canonical branch: main
- Local main SHA: 02c9c1c31d56ad816437a21b3f1fa02fa4bfbde3
- Origin main SHA: 02c9c1c31d56ad816437a21b3f1fa02fa4bfbde3
- pyproject version: 0.1.0
- CHANGELOG release date: 2026-08-27
- CITATION.cff date-released: 2026-08-27

## Final QA

- python scripts/validate_examples.py: PASS
- python -m pytest: 125 passed
- python -m build: PASS
- git diff --check: PASS

B04 M2 was not rerun.

## Release Assets

- feynagent-0.1.0-py3-none-any.whl
  - SHA256: 7d811a2162d5615742d86926f4f2bc3f5477bd77832eefd7d4ede4e419671b1f
- feynagent-0.1.0.tar.gz
  - SHA256: 2b495845e66629071841b56c147bac59793befc5e622d1e9db093a7898a2e599
- SHA256SUMS
  - SHA256: 92fbd4b944f6888eb86bd6f219719f513903c79b742776df1e675df48e304eb3

No private B04 external knowledge or review ZIP was attached.

## Publication Result

PUBLICATION_PASS