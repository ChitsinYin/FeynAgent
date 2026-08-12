# Day-3 Amplitude Backend Audit: B02_compton

- generated_at: `2026-08-12T22:06:31.565733+08:00`
- source_amplitude_ir: `amplitude_ir:b02_compton:generated`
- process_id: `process:b02_compton`
- backend_source: `AmplitudeIR only`
- heavy_calculation_executed: `false`

| amplitude_id | diagram_id | canonical rule IDs | factor IDs | index map |
|---|---|---|---|---|
| `amplitude:b02_compton:amp_s` | `diagram:generated:b02-compton:s:e-` | `rule:qed_tree_v1:e_e_gamma_vertex`<br>`rule:qed_tree_v1:electron_propagator` | `factor:b02_compton:s:ext:1:u`<br>`factor:b02_compton:s:ext:3:ubar`<br>`factor:b02_compton:s:vertex:1`<br>`factor:b02_compton:s:vertex:2`<br>`factor:b02_compton:s:prop:1`<br>`factor:b02_compton:s:pol:2:eps`<br>`factor:b02_compton:s:pol:4:eps_conj` | `idx:b02_compton:s:eps:l_pol_2` -> `\mu_{1}`<br>`idx:b02_compton:s:eps_conj:l_pol_4` -> `\mu_{2}`<br>`idx:b02_compton:s:x_1:l_v1_mu` -> `\mu_{3}`<br>`idx:b02_compton:s:x_2:l_v2_mu` -> `\mu_{4}`<br>`idx:b02_compton:s:u:d_ext_1` -> `a_{1}`<br>`idx:b02_compton:s:ubar:d_ext_3` -> `a_{2}`<br>`idx:b02_compton:s:x_1:d_v1_bar` -> `a_{3}`<br>`idx:b02_compton:s:x_1:d_v1_psi` -> `a_{4}`<br>`idx:b02_compton:s:x_2:d_v2_bar` -> `a_{5}`<br>`idx:b02_compton:s:x_2:d_v2_psi` -> `a_{6}`<br>`idx:b02_compton:s:x_1:d_p1_l` -> `a_{7}`<br>`idx:b02_compton:s:x_1:d_p1_r` -> `a_{8}` |
| `amplitude:b02_compton:amp_u` | `diagram:generated:b02-compton:u:e-` | `rule:qed_tree_v1:e_e_gamma_vertex`<br>`rule:qed_tree_v1:electron_propagator` | `factor:b02_compton:u:ext:1:u`<br>`factor:b02_compton:u:ext:3:ubar`<br>`factor:b02_compton:u:vertex:1`<br>`factor:b02_compton:u:vertex:2`<br>`factor:b02_compton:u:prop:1`<br>`factor:b02_compton:u:pol:2:eps`<br>`factor:b02_compton:u:pol:4:eps_conj` | `idx:b02_compton:u:eps:l_pol_2` -> `\mu_{1}`<br>`idx:b02_compton:u:eps_conj:l_pol_4` -> `\mu_{2}`<br>`idx:b02_compton:u:x_1:l_v1_mu` -> `\mu_{3}`<br>`idx:b02_compton:u:x_2:l_v2_mu` -> `\mu_{4}`<br>`idx:b02_compton:u:u:d_ext_1` -> `a_{1}`<br>`idx:b02_compton:u:ubar:d_ext_3` -> `a_{2}`<br>`idx:b02_compton:u:x_1:d_v1_bar` -> `a_{3}`<br>`idx:b02_compton:u:x_1:d_v1_psi` -> `a_{4}`<br>`idx:b02_compton:u:x_2:d_v2_bar` -> `a_{5}`<br>`idx:b02_compton:u:x_2:d_v2_psi` -> `a_{6}`<br>`idx:b02_compton:u:x_1:d_p1_l` -> `a_{7}`<br>`idx:b02_compton:u:x_1:d_p1_r` -> `a_{8}` |

## Backend Constraints

- LaTeX and FeynCalc are rendered from the same AmplitudeIR object.
- Diagram amplitudes are preserved separately and the total amplitude is an ordered symbolic sum.
- Gamma chains are not simplified.
- Squared amplitudes, spin sums, and polarization sums are not performed during generation or smoke tests.
- `compute_m2.wl` is a human-run heavy script and was not executed by generation.
