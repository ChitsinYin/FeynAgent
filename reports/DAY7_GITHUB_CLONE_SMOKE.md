# Day 7 GitHub Clone Smoke: QED Compton

## Summary

- Status: PASS
- Process: `e- gamma -> e- gamma`
- Git commit: `3ef996a3dfc1a5481357b2d3c452f1708f9034ab`
- Installed FeynAgent version: `0.1.0`
- FeynAgent skill discovered: PASS
- FeynAgent workflow used: PASS; used installed `feynagent` skill instructions plus repository-local `skills/feynagent/scripts/ensure_initialized.py`, `skills/feynagent/scripts/run_feynagent.py`, and `python -m feynagent run`
- Constraint note: work was performed only in this current smoke clone; no other local FeynAgent checkout was inspected or used.

## Backend And Environment

- Request classification: `standard_native`
- Backend classification: `feynarts_feyncalc_native`
- Backend profile: `profiles/backends/feynarts_sm_qed.yaml`
- FeynAgent doctor: PASS
- Wolfram version: `15.0.1 for Microsoft Windows (64-bit) (July 2, 2026)`
- FeynCalc version: `10.1.0`
- FeynArts version: `FeynArts 3.12 (27 Mar 2025)`
- LaTeX: PASS, `lualatex`

## Official Reference

- Official example id: `ElGa-ElGa`
- Official example path: `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Mathematica\ElGa-ElGa.m`
- Official example SHA256: `5dfeb52e426df1d155af336ab775add2b8e94e039f5ed126ced7c689889affc2`
- Official Markdown path: `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Markdown\ElGa-ElGa.md`
- Official Markdown SHA256: `7bb2b42ccde456340a32fb436016360861779e5a89583beb95c72347d089edc4`
- Official comparison artifact: `runs/20260818_081454_b02_compton_38a609ae/official_reference_comparison.json`
- Official comparison result: PASS; `FCCompareResults=True`, `FullSimplify equivalence=True`

## Run Artifacts

- Run id: `20260818_081454_b02_compton_38a609ae`
- Run directory: `runs/20260818_081454_b02_compton_38a609ae`
- Run manifest: `runs/20260818_081454_b02_compton_38a609ae/run_manifest.json`
- Validation report: `runs/20260818_081454_b02_compton_38a609ae/validation_report.json`
- Native summary: `runs/20260818_081454_b02_compton_38a609ae/native_summary.json`
- Execution request: `runs/day7_github_clone_smoke_inputs/execution_request.yaml`

## Diagrams

- Diagram count: 2
- Channels: `s`, `u`
- Complete tree diagram source: `runs/20260818_081454_b02_compton_38a609ae/diagram_source.m`
- Diagram PDF: `runs/20260818_081454_b02_compton_38a609ae/diagrams.pdf`
- Diagram PDF SHA256: `e61844252e2be27b23c3e48d0c6fc2ab683f21dd299ed2c7b0939b073a02a322`
- CreateTopologies: `CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]`
- InsertFields: `InsertFields[topologies, {F[2, {1}], V[1]} -> {F[2, {1}], V[1]}, Model -> "SM", GenericModel -> "Lorentz", Restrictions -> QEDOnly, InsertionLevel -> {Classes}]`

## Amplitudes

- FeynCalc amplitude artifact: `runs/20260818_081454_b02_compton_38a609ae/feyncalc_amplitudes.m`
- Raw FeynArts amplitude artifact: `runs/20260818_081454_b02_compton_38a609ae/raw_feynarts_amplitude.m`
- Human-readable LaTeX: `runs/20260818_081454_b02_compton_38a609ae/amplitudes.tex`
- Amplitudes PDF: `runs/20260818_081454_b02_compton_38a609ae/amplitudes.pdf`
- Amplitudes PDF SHA256: `7f053807de37305bcc6a843228cd9839746b29889c5c78a5c3f3be431ba66e7d`
- M_s FeynCalc artifact: `runs/20260818_081454_b02_compton_38a609ae/M_s.m`
- M_s SHA256: `a91664d13e155443342989efd6d62ce83318fba006f550fd205f32a994f11f0b`
- M_u FeynCalc artifact: `runs/20260818_081454_b02_compton_38a609ae/M_u.m`
- M_u SHA256: `e961269205a1e09e53b64123fa8c7a7e9123648b4c1cbef1cd80e239aa34e984`
- Total amplitude artifact: `runs/20260818_081454_b02_compton_38a609ae/M_total.m`
- Total amplitude SHA256: `6a4cf4d5f6b83aaa62d8a14e8349e6905274f65be85298995dcada4e01fde24a`
- Channel split manifest: `runs/20260818_081454_b02_compton_38a609ae/channel_amplitudes.json`

## M2 Regression

- Execution-policy status: PASS; approved `benchmark_regression`, fixed timeout `180` seconds, required operations authorized.
- M2 executed: true
- M2 manifest: `runs/20260818_081454_b02_compton_38a609ae/m2_manifest.json`
- M2 result file: `runs/20260818_081454_b02_compton_38a609ae/m2_simplified.m`
- M2 result: `(-2*(s^2 + u^2)*SMP["e"]^4)/(s*u)`
- M2 comparison result: PASS
- Initial spin average factor: `1/4`
- External photon polarization sums: `{k1, k2}`
- Massless replacement: `{SMP["m_e"] -> 0}`

## Verification

- `skills/feynagent/scripts/ensure_initialized.py --root .`: PASS
- `python -m feynagent doctor`: PASS
- `python -m feynagent run ...`: PASS
- `pytest tests/test_b02_compton.py tests/test_feynarts_feyncalc_backend.py`: PASS, 29 passed
- `scripts/validate_examples.py`: PASS
- Diagram count check: PASS
- Channel amplitude check: PASS
- LaTeX/PDF check: PASS
- FeynCalc artifact check: PASS
- M2 regression check: PASS
- Official reference comparison check: PASS

## Warnings

- The benchmark-regression M2 path was explicitly authorized by the execution request and completed quickly; no unrelated heavy calculation was performed.
- The existing repository had an unrelated untracked `DAY7_GITHUB_CLONE_INSTALL_RETRY.md` before this report was created.
