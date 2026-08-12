# Day-3 Amplitude Backend Audit: B01_ee_to_mumu

- generated_at: `2026-08-12T22:06:31.565733+08:00`
- source_amplitude_ir: `amplitude_ir:b01_ee_to_mumu:generated`
- process_id: `process:b01_ee_to_mumu`
- backend_source: `AmplitudeIR only`
- heavy_calculation_executed: `false`

| amplitude_id | diagram_id | canonical rule IDs | factor IDs | index map |
|---|---|---|---|---|
| `amplitude:b01_ee_to_mumu:amp_s` | `diagram:generated:b01-ee-to-mumu:s:gamma` | `rule:qed_tree_v1:e_e_gamma_vertex`<br>`rule:qed_tree_v1:mu_mu_gamma_vertex`<br>`rule:qed_tree_v1:photon_propagator` | `factor:b01_ee_to_mumu:s:ext:1:u`<br>`factor:b01_ee_to_mumu:s:ext:2:vbar`<br>`factor:b01_ee_to_mumu:s:ext:3:ubar`<br>`factor:b01_ee_to_mumu:s:ext:4:v`<br>`factor:b01_ee_to_mumu:s:vertex:1`<br>`factor:b01_ee_to_mumu:s:vertex:2`<br>`factor:b01_ee_to_mumu:s:prop:1`<br>`factor:b01_ee_to_mumu:s:nonchain:1` | `idx:b01_ee_to_mumu:s:x_1:l_v1_mu` -> `\mu_{1}`<br>`idx:b01_ee_to_mumu:s:x_2:l_v2_mu` -> `\mu_{2}`<br>`idx:b01_ee_to_mumu:s:x_1:l_p1_l` -> `\mu_{3}`<br>`idx:b01_ee_to_mumu:s:x_1:l_p1_r` -> `\mu_{4}`<br>`idx:b01_ee_to_mumu:s:u:d_ext_1` -> `a_{1}`<br>`idx:b01_ee_to_mumu:s:vbar:d_ext_2` -> `a_{2}`<br>`idx:b01_ee_to_mumu:s:ubar:d_ext_3` -> `a_{3}`<br>`idx:b01_ee_to_mumu:s:v:d_ext_4` -> `a_{4}`<br>`idx:b01_ee_to_mumu:s:x_1:d_v1_bar` -> `a_{5}`<br>`idx:b01_ee_to_mumu:s:x_1:d_v1_psi` -> `a_{6}`<br>`idx:b01_ee_to_mumu:s:x_2:d_v2_bar` -> `a_{7}`<br>`idx:b01_ee_to_mumu:s:x_2:d_v2_psi` -> `a_{8}` |

## Backend Constraints

- LaTeX and FeynCalc are rendered from the same AmplitudeIR object.
- Diagram amplitudes are preserved separately and the total amplitude is an ordered symbolic sum.
- Gamma chains are not simplified.
- Squared amplitudes, spin sums, and polarization sums are not performed during generation or smoke tests.
- `compute_m2.wl` is a human-run heavy script and was not executed by generation.
