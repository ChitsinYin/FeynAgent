# Day-8 Report

Date: 2026-08-27
Repository: ChitsinYin/FeynAgent
Release: v0.1.0
Release URL: https://github.com/ChitsinYin/FeynAgent/releases/tag/v0.1.0
Release commit: 02c9c1c31d56ad816437a21b3f1fa02fa4bfbde3

## Status Vocabulary

- DAY8_RELEASE_HARDENING = PASS
- MAIN_INTEGRATION = PASS
- GITHUB_ZERO_CLONE = PASS
- PUBLIC_QED_V0_1 = PASS
- LOCKED_B04_PUBLIC_ROUTE = PASS
- GENERAL_CUSTOM_GRAVITY_PRODUCTION_READY = NO
- PUBLIC_V0_1_READY = YES
- GITHUB_V0_1_0_RELEASE = PUBLISHED

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

## GitHub Release Verification

- Public tag exists: PASS
- Public release exists: PASS
- Wheel asset exists: PASS
- Source distribution asset exists: PASS
- SHA256SUMS asset exists: PASS
- Release notes accuracy: PASS
- README support matrix accuracy: PASS
- No private gravity knowledge published: PASS

Release assets:

- feynagent-0.1.0-py3-none-any.whl
  - SHA256: 7d811a2162d5615742d86926f4f2bc3f5477bd77832eefd7d4ede4e419671b1f
- feynagent-0.1.0.tar.gz
  - SHA256: 2b495845e66629071841b56c147bac59793befc5e622d1e9db093a7898a2e599
- SHA256SUMS
  - SHA256: 92fbd4b944f6888eb86bd6f219719f513903c79b742776df1e675df48e304eb3

## Fresh Wheel Verification

A fresh temp venv installed the released GitHub wheel asset with `PYTHONPATH` unset.

- `import feynagent`: PASS
- `feynagent.__version__`: 0.1.0
- `importlib.metadata.version("feynagent")`: 0.1.0
- Repository `PYTHONPATH` dependency: NONE (`PYTHONPATH=None`)
- `python -m feynagent init --wolframscript ... --timeout 60`: PASS
- `python -m feynagent doctor --wolframscript ... --timeout 60`: PASS

Note: a fully isolated dependency install attempted first, but live PyPI resolution was blocked by the maintainer machine proxy/SSL path. The final installed-package check used a fresh temp venv with maintainer machine site packages visible, installed the released FeynAgent wheel asset, and did not depend on repository `PYTHONPATH` or editable install.

## Public Scope

Supported in v0.1.0:

- Standard native tree-level QED 2-to-2 workflows for external `e-`, `e+`, `mu-`, `mu+`, and `gamma` states.
- The single locked B04 `phi phi -> h h` custom audited route for `model_id = reheating_scalar_gravity_v1`, requiring separately supplied audited external knowledge.

Not supported in v0.1.0:

- Arbitrary gravity or graviton production beyond locked B04.
- Arbitrary BSM model production workflows.
- Arbitrary Standard Model or QCD production workflows outside the validated standard-QED scope.
- Loops, counterterms, renormalization, or higher-order corrections.
- Ungated production-heavy execution.
- B04 M2 execution without separate explicit authorization.

B04 M2 was not rerun during Day-8 closeout.

## Review Bundle Self-Test

- Extracted `reports/FeynAgent_Day8_Review_Bundle.zip`: PASS
- Initialized ephemeral Git metadata in the extracted copy for the release-invariant test that calls `git ls-files`: PASS
- `python scripts/validate_examples.py`: PASS
- `python -m pytest`: PASS (`125 passed`)
