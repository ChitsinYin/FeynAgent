# Day 4 Native Amplitude Regression

Executive status: **PASS**

Scope: tree-level 2 -> 2 QED using native FeynArts/FeynCalc only. No M2, spin sums, polarization sums, or legacy RuleRegistry amplitude reconstruction were performed.

## Official FeynCalc Examples Located Before Generation

| benchmark | official example | title | FeynCalc version | markdown path/hash | Mathematica path/hash |
|---|---|---|---|---|---|
| B01_ee_to_mumu | `ElAel-MuAmu` | Muon production | `10.1.0` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Markdown\ElAel-MuAmu.md`<br>`9cc3b2a0e5a8dfbeb3f57fafb3ecfe2177c98ea8bdacdd9264f8d7b870e02423` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Mathematica\ElAel-MuAmu.m`<br>`4fd39bd090ced335bff957bb47ae77de78440d2a3ec3cf9f0d3b1350a6c82d86` |
| B02_compton | `ElGa-ElGa` | Compton scattering | `10.1.0` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Markdown\ElGa-ElGa.md`<br>`7bb2b42ccde456340a32fb436016360861779e5a89583beb95c72347d089edc4` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Mathematica\ElGa-ElGa.m`<br>`5dfeb52e426df1d155af336ab775add2b8e94e039f5ed126ced7c689889affc2` |
| B03_emu_to_emu | `ElMu-ElMu` | Electron-muon scattering | `10.1.0` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Markdown\ElMu-ElMu.md`<br>`50176504925c8f12d35f012e2e12f6617e5e47010300b71e0308e9fcbe4acd4c` | `C:\Users\lenovo\AppData\Roaming\Wolfram\Applications\FeynCalc\Examples\QED\Tree\Mathematica\ElMu-ElMu.m`<br>`08b5435b2b80bd349086e241ff2a2d5f1a23edbb20e424e84e1aaacdfe276578` |

The installed examples were read and hashed only; they were not edited.

## Native Generation Summary

| benchmark | FeynArts input fields | process momenta | diagram count | versions | run manifest |
|---|---|---|---:|---|---|
| B01_ee_to_mumu | incoming `['F[2,{1}]', '-F[2,{1}]']` -> outgoing `['F[2,{2}]', '-F[2,{2}]']` | `p1, p2, p3, p4` | 1 | Wolfram `15.0.1 for Microsoft Windows (64-bit) (July 2, 2026)`<br>FeynArts `"FeynArts 3.12 (27 Mar 2025)"`<br>FeynCalc `"10.1.0"` | `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/run_manifest.json` |
| B02_compton | incoming `['F[2,{1}]', 'V[1]']` -> outgoing `['F[2,{1}]', 'V[1]']` | `p1, k1, p2, k2` | 2 | Wolfram `15.0.1 for Microsoft Windows (64-bit) (July 2, 2026)`<br>FeynArts `"FeynArts 3.12 (27 Mar 2025)"`<br>FeynCalc `"10.1.0"` | `runs/day4_native_regression/20260813_105718/B02_compton/run_manifest.json` |
| B03_emu_to_emu | incoming `['F[2,{1}]', 'F[2,{2}]']` -> outgoing `['F[2,{1}]', 'F[2,{2}]']` | `p1, p2, p3, p4` | 1 | Wolfram `15.0.1 for Microsoft Windows (64-bit) (July 2, 2026)`<br>FeynArts `"FeynArts 3.12 (27 Mar 2025)"`<br>FeynCalc `"10.1.0"` | `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/run_manifest.json` |

## Exact Native Calls
### B01_ee_to_mumu
```wolfram
CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]
InsertFields[topologies, {F[2, {1}], -F[2, {1}]} -> {F[2, {2}], -F[2, {2}]}, Model -> "SM", GenericModel -> "Lorentz", Restrictions -> QEDOnly, InsertionLevel -> {Classes}]
```

### B02_compton
```wolfram
CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]
InsertFields[topologies, {F[2, {1}], V[1]} -> {F[2, {1}], V[1]}, Model -> "SM", GenericModel -> "Lorentz", Restrictions -> QEDOnly, InsertionLevel -> {Classes}]
```

### B03_emu_to_emu
```wolfram
CreateTopologies[0, 2 -> 2, ExcludeTopologies -> {Tadpoles, SelfEnergies, WFCorrections}]
InsertFields[topologies, {F[2, {1}], F[2, {2}]} -> {F[2, {1}], F[2, {2}]}, Model -> "SM", GenericModel -> "Lorentz", Restrictions -> QEDOnly, InsertionLevel -> {Classes}]
```

## Output Hashes
### B01_ee_to_mumu

| output | sha256 | bytes |
|---|---|---|
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/feyncalc_amplitude.inputform.txt` | `812a2a0caa2efd2b035b4f414faa1648a680a8f9de4dc205d0b3b16c6e53236a` | 356 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/feyncalc_amplitude.m` | `5838e20ad600d9b38b8df3282a4033be692124fa899edde1c002a24d6dda2daa` | 382 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/native_amplitude.wl` | `de418ba69b87a854040c2ad94bbe5d2cc008e92f1562ffac5bd5b01d2d102061` | 3001 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/native_summary.json` | `49ec722907324b0cb977149d41de7f67a4502d5324d067cfcaac1fb8825d9891` | 702 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/raw_feynarts_amplitude.inputform.txt` | `72d58e6d4ff4f0663f1b40e167ade53ab972c00e1e32383949249160989e284f` | 1656 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/raw_feynarts_amplitude.m` | `cfbbc41dba07448c53b0804de35fdd69d70e5947385d0a3d9d5bd591e0bfbbc7` | 1834 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `runs/day4_native_regression/20260813_105718/B01_ee_to_mumu/stdout.log` | `206311ed5a8831154ce425654ca1093577aadc75fc3f4ced261e69834fefef4c` | 3783 |

### B02_compton

| output | sha256 | bytes |
|---|---|---|
| `runs/day4_native_regression/20260813_105718/B02_compton/feyncalc_amplitude.inputform.txt` | `189b32401efa893ebb1e826e0bec3d760d2a8ddfbc2e83f2795eeb076be6263f` | 902 |
| `runs/day4_native_regression/20260813_105718/B02_compton/feyncalc_amplitude.m` | `9de444ded225d569961cf76a11a603edaaa2baba69ca259faac886571a1addb8` | 981 |
| `runs/day4_native_regression/20260813_105718/B02_compton/native_amplitude.wl` | `f8dbbfd77d85213661bcaf9df2621b0a0a68da6900af57a5fcdcbac13be70ceb` | 3016 |
| `runs/day4_native_regression/20260813_105718/B02_compton/native_summary.json` | `8e76aede25f089fa6286a7bc656a04262c83855492df0bd56e38076f99778202` | 687 |
| `runs/day4_native_regression/20260813_105718/B02_compton/raw_feynarts_amplitude.inputform.txt` | `399cb8bb8d368daad81d57d6205c06d17a8dbf2fd286caa2374366302d07c37a` | 2600 |
| `runs/day4_native_regression/20260813_105718/B02_compton/raw_feynarts_amplitude.m` | `3202dea0aba8174c320071b42727e62299958050aea50bd082b44a54716dfb71` | 2887 |
| `runs/day4_native_regression/20260813_105718/B02_compton/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `runs/day4_native_regression/20260813_105718/B02_compton/stdout.log` | `c2addd52cbf13ca0c305f7b12e08cd181bcfd31914e8753178753e85221a29fe` | 3796 |

### B03_emu_to_emu

| output | sha256 | bytes |
|---|---|---|
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/feyncalc_amplitude.inputform.txt` | `b15f486f3d0334f3adfd7af49886ea590b1024aebbda9b9d904488ae2226a71e` | 355 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/feyncalc_amplitude.m` | `ad6fd6194f722baa5a0aa4b4b2081b041dad95c57c80ab036061ad614a2f2535` | 381 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/native_amplitude.wl` | `b7cfc3816df96f95a85ff5d519a55fa1cdc6cb601aa435c14d193168bc998476` | 2997 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/native_summary.json` | `60d609eae423c23cd9aa0de452ad97d2eb23d849d7228c5af78d532163a2e816` | 700 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/raw_feynarts_amplitude.inputform.txt` | `57632c60da4439625eeb8da6cf2333bdfc98833bf758351f871fd076ae5ce3c1` | 1653 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/raw_feynarts_amplitude.m` | `5c58b20cdbd96fc44d474c9f2042f76923b3b9c5e5e511a4a89d1bdac14df254` | 1831 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `runs/day4_native_regression/20260813_105718/B03_emu_to_emu/stdout.log` | `934fd6bbce37a154d6aa6add069ec4de3068fc368bba15a0109151f9b8c67a51` | 3781 |

## Structural Comparison To Official Examples

### B01_ee_to_mumu vs `ElAel-MuAmu`

- official InsertFields uses {F[2,{1}], -F[2,{1}]} -> {F[2,{2}], -F[2,{2}]} with Restrictions->QEDOnly.
- native InsertFields matches the same electron-positron to muon-antimuon class process.
- native diagram count is 1, matching the official one-diagram s-channel production example.
- native FCFAConvert output contains e/e+ and mu/mu+ external Spinor factors and a massless photon propagator.
- native propagator Momentum[p3+p4] is the s-channel photon under native outgoing momentum labels; official uses outgoing k1,k2.
- single-term sign structure agrees up to dummy-index and global convention differences.

| assertion | status |
|---|---|
| external electron/positron spinors | PASS |
| external muon/antimuon spinors | PASS |
| s-channel photon propagator | PASS |
| no polarization vectors | PASS |
| single diagram term | PASS |

Representative FCFAConvert InputForm:

```text
{I*Spinor[-Momentum[p2], SMP["m_e"], 1] . (I*DiracGamma[LorentzIndex[Lor1]]*SMP["e"]) . Spinor[Momentum[p1], SMP["m_e"], 1]*Spinor[Momentum[p3], SMP["m_mu"], 1] . (I*DiracGamma[LorentzIndex[Lor2]]*SMP["e"]) . Spinor[-Momentum[p4], SMP["m_mu"], 1]*FeynAmpDenominator[PropagatorDenominator[Momentum[p3 + p4], 0]]*Pair[LorentzIndex[Lor1], LorentzIndex[Lor2]]}
```

### B02_compton vs `ElGa-ElGa`

- official InsertFields uses {F[2,{1}], V[1]} -> {F[2,{1}], V[1]} with Restrictions->QEDOnly.
- native InsertFields matches the same Compton class process.
- native diagram count is 2, matching the official s/u electron-exchange example.
- native FCFAConvert output contains one external electron spinor chain per term and two terms.
- native FCFAConvert uses TransversePolarizationVectors -> {k1, k2}, matching the official example pattern.
- native output contains Polarization[k1, I, Transversality -> True] and Polarization[k2, -I, Transversality -> True].
- relative two-diagram structure agrees up to dummy-index, momentum-routing, and global phase conventions.

| assertion | status |
|---|---|
| external electron spinors | PASS |
| two electron propagator channels | PASS |
| incoming/outgoing photon polarization structure | PASS |
| two diagram terms | PASS |

Representative FCFAConvert InputForm:

```text
{I*Spinor[Momentum[p2], SMP["m_e"], 1] . (I*DiracGamma[LorentzIndex[Lor2]]*SMP["e"]) . (DiracGamma[Momentum[k2 + p2]] + SMP["m_e"]) . (I*DiracGamma[LorentzIndex[Lor1]]*SMP["e"]) . Spinor[Momentum[p1], SMP["m_e"], 1]*FeynAmpDenominator[PropagatorDenominator[Momentum[-k2 - p2], SMP["m_e"]]]*Pair[LorentzIndex[Lor1], Momentum[Polarization[k1, I, Transversality -> True]]]*Pair[LorentzIndex[Lor2], Momentum[Polarization[k2, -I, Transversality -> True]]], I*Spinor[Momentum[p2], SMP["m_e"], 1] . (I*DiracGamma[LorentzIndex[Lor1]]*SMP["e"]) . (DiracGamma[Momentum[-k1 + p2]] + SMP["m_e"]) . (I*DiracGamma[LorentzIndex[Lor2]]*SMP["e"]) . Spinor[Momentum[p1], SMP["m_e"], 1]*FeynAmpDenominator[PropagatorDenominator[Momentum[k1 - p2], SMP["m_e"]]]*Pair[LorentzIndex[Lor1], Momentum[Polarization[k1, I, Transversality -> True]]]*Pair[LorentzIndex[Lor2], Momentum[Polarization[k2, -I, Transversality -> True]]]}
```

### B03_emu_to_emu vs `ElMu-ElMu`

- official InsertFields uses {F[2,{1}], F[2,{2}]} -> {F[2,{1}], F[2,{2}]} with Restrictions->QEDOnly.
- native InsertFields matches the same electron-muon scattering class process.
- native diagram count is 1, matching the official one-diagram t-channel scattering example.
- native FCFAConvert output contains electron and muon external Spinor factors and a massless photon propagator.
- native propagator Momentum[-p2+p4] is the t-channel photon under native external labels.
- single-term sign structure agrees up to dummy-index and global convention differences.

| assertion | status |
|---|---|
| external electron spinors | PASS |
| external muon spinors | PASS |
| t-channel photon propagator | PASS |
| no polarization vectors | PASS |
| single diagram term | PASS |

Representative FCFAConvert InputForm:

```text
{I*Spinor[Momentum[p3], SMP["m_e"], 1] . (I*DiracGamma[LorentzIndex[Lor1]]*SMP["e"]) . Spinor[Momentum[p1], SMP["m_e"], 1]*Spinor[Momentum[p4], SMP["m_mu"], 1] . (I*DiracGamma[LorentzIndex[Lor2]]*SMP["e"]) . Spinor[Momentum[p2], SMP["m_mu"], 1]*FeynAmpDenominator[PropagatorDenominator[Momentum[-p2 + p4], 0]]*Pair[LorentzIndex[Lor1], LorentzIndex[Lor2]]}
```

## Assertions

- B01 diagram count = 1: PASS
- B02 diagram count = 2: PASS
- B03 diagram count = 1: PASS
- Old generic `compute_m2.wl` scripts were not run: PASS
- No M2 calculation was performed: PASS

## Known Non-Equality Reasons

Raw text equality is intentionally not required. Dummy Lorentz indices, external momentum labels (`p3/p4` versus official `k1/k2`), momentum routing, and global phase conventions may differ while preserving the same native diagram and amplitude structure.
