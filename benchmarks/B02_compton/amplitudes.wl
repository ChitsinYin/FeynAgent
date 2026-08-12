(* Day-3 generated amplitudes for B02_compton. *)
(* generated-at: 2026-08-12T22:06:31.565733+08:00 *)
(* source-amplitude-ir: amplitude_ir:b02_compton:generated *)
(* This file is derived from AmplitudeIR only; no amplitude reconstruction is performed here. *)
$LoadFeynArts = False;
If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];
ClearAll[e, epsilon, k1, k2, me, mmu, p1, p2, qS, qU, mu1, mu2, mu3, mu4, ampS, ampU, ampTotal];

(* amplitude-id: amplitude:b02_compton:amp_s *)
(* factor-id: factor:b02_compton:s:ext:1:u *)
(* factor-id: factor:b02_compton:s:ext:3:ubar *)
(* factor-id: factor:b02_compton:s:vertex:1 *)
(* factor-id: factor:b02_compton:s:vertex:2 *)
(* factor-id: factor:b02_compton:s:prop:1 *)
(* factor-id: factor:b02_compton:s:pol:2:eps *)
(* factor-id: factor:b02_compton:s:pol:4:eps_conj *)
(* index-map: idx:b02_compton:s:eps:l_pol_2 -> mu1 *)
(* index-map: idx:b02_compton:s:eps_conj:l_pol_4 -> mu2 *)
(* index-map: idx:b02_compton:s:x_1:l_v1_mu -> mu3 *)
(* index-map: idx:b02_compton:s:x_2:l_v2_mu -> mu4 *)
(* index-map: idx:b02_compton:s:u:d_ext_1 -> a1 *)
(* index-map: idx:b02_compton:s:ubar:d_ext_3 -> a2 *)
(* index-map: idx:b02_compton:s:x_1:d_v1_bar -> a3 *)
(* index-map: idx:b02_compton:s:x_1:d_v1_psi -> a4 *)
(* index-map: idx:b02_compton:s:x_2:d_v2_bar -> a5 *)
(* index-map: idx:b02_compton:s:x_2:d_v2_psi -> a6 *)
(* index-map: idx:b02_compton:s:x_1:d_p1_l -> a7 *)
(* index-map: idx:b02_compton:s:x_1:d_p1_r -> a8 *)
(* amplitude-id: amplitude:b02_compton:amp_u *)
(* factor-id: factor:b02_compton:u:ext:1:u *)
(* factor-id: factor:b02_compton:u:ext:3:ubar *)
(* factor-id: factor:b02_compton:u:vertex:1 *)
(* factor-id: factor:b02_compton:u:vertex:2 *)
(* factor-id: factor:b02_compton:u:prop:1 *)
(* factor-id: factor:b02_compton:u:pol:2:eps *)
(* factor-id: factor:b02_compton:u:pol:4:eps_conj *)
(* index-map: idx:b02_compton:u:eps:l_pol_2 -> mu1 *)
(* index-map: idx:b02_compton:u:eps_conj:l_pol_4 -> mu2 *)
(* index-map: idx:b02_compton:u:x_1:l_v1_mu -> mu3 *)
(* index-map: idx:b02_compton:u:x_2:l_v2_mu -> mu4 *)
(* index-map: idx:b02_compton:u:u:d_ext_1 -> a1 *)
(* index-map: idx:b02_compton:u:ubar:d_ext_3 -> a2 *)
(* index-map: idx:b02_compton:u:x_1:d_v1_bar -> a3 *)
(* index-map: idx:b02_compton:u:x_1:d_v1_psi -> a4 *)
(* index-map: idx:b02_compton:u:x_2:d_v2_bar -> a5 *)
(* index-map: idx:b02_compton:u:x_2:d_v2_psi -> a6 *)
(* index-map: idx:b02_compton:u:x_1:d_p1_l -> a7 *)
(* index-map: idx:b02_compton:u:x_1:d_p1_r -> a8 *)

qDefinitions = <|"q_s" -> HoldForm[qS == p1 + k1], "q_u" -> HoldForm[qU == p1 - k2]|>;
qSubstitutions = {qS -> p1 + k1, qU -> p1 - k2};
amplitudeFactorIDs = <|"amp_s" -> {"factor:b02_compton:s:ext:1:u", "factor:b02_compton:s:ext:3:ubar", "factor:b02_compton:s:vertex:1", "factor:b02_compton:s:vertex:2", "factor:b02_compton:s:prop:1", "factor:b02_compton:s:pol:2:eps", "factor:b02_compton:s:pol:4:eps_conj"}, "amp_u" -> {"factor:b02_compton:u:ext:1:u", "factor:b02_compton:u:ext:3:ubar", "factor:b02_compton:u:vertex:1", "factor:b02_compton:u:vertex:2", "factor:b02_compton:u:prop:1", "factor:b02_compton:u:pol:2:eps", "factor:b02_compton:u:pol:4:eps_conj"}|>;
amplitudeIndexMap = <|"idx:b02_compton:s:eps:l_pol_2" -> "mu1", "idx:b02_compton:s:eps_conj:l_pol_4" -> "mu2", "idx:b02_compton:s:x_1:l_v1_mu" -> "mu3", "idx:b02_compton:s:x_2:l_v2_mu" -> "mu4", "idx:b02_compton:s:u:d_ext_1" -> "a1", "idx:b02_compton:s:ubar:d_ext_3" -> "a2", "idx:b02_compton:s:x_1:d_v1_bar" -> "a3", "idx:b02_compton:s:x_1:d_v1_psi" -> "a4", "idx:b02_compton:s:x_2:d_v2_bar" -> "a5", "idx:b02_compton:s:x_2:d_v2_psi" -> "a6", "idx:b02_compton:s:x_1:d_p1_l" -> "a7", "idx:b02_compton:s:x_1:d_p1_r" -> "a8", "idx:b02_compton:u:eps:l_pol_2" -> "mu1", "idx:b02_compton:u:eps_conj:l_pol_4" -> "mu2", "idx:b02_compton:u:x_1:l_v1_mu" -> "mu3", "idx:b02_compton:u:x_2:l_v2_mu" -> "mu4", "idx:b02_compton:u:u:d_ext_1" -> "a1", "idx:b02_compton:u:ubar:d_ext_3" -> "a2", "idx:b02_compton:u:x_1:d_v1_bar" -> "a3", "idx:b02_compton:u:x_1:d_v1_psi" -> "a4", "idx:b02_compton:u:x_2:d_v2_bar" -> "a5", "idx:b02_compton:u:x_2:d_v2_psi" -> "a6", "idx:b02_compton:u:x_1:d_p1_l" -> "a7", "idx:b02_compton:u:x_1:d_p1_r" -> "a8"|>;

ampS = (SpinorUBar[p2, me] . ((-I e) GA[mu4]) . (I (GS[qS] + me)/(SP[qS, qS] - me^2 + I epsilon)) . ((-I e) GA[mu3]) . SpinorU[p1, me]) * ComplexConjugate[PolarizationVector[k2, mu4]] * PolarizationVector[k1, mu3];
ampU = (SpinorUBar[p2, me] . ((-I e) GA[mu4]) . (I (GS[qU] + me)/(SP[qU, qU] - me^2 + I epsilon)) . ((-I e) GA[mu3]) . SpinorU[p1, me]) * PolarizationVector[k1, mu4] * ComplexConjugate[PolarizationVector[k2, mu3]];
diagramAmplitudes = <|"amp_s" -> ampS, "amp_u" -> ampU|>;
ampTotal = ampS + ampU;
Print["Loaded generated amplitudes for B02_compton"];
