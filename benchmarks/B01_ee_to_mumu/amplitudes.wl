(* Day-3 generated amplitudes for B01_ee_to_mumu. *)
(* generated-at: 2026-08-12T22:06:31.565733+08:00 *)
(* source-amplitude-ir: amplitude_ir:b01_ee_to_mumu:generated *)
(* This file is derived from AmplitudeIR only; no amplitude reconstruction is performed here. *)
$LoadFeynArts = False;
If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];
ClearAll[e, epsilon, me, mmu, p1, p2, p3, p4, qS, mu1, mu2, mu3, mu4, ampS, ampTotal];

(* amplitude-id: amplitude:b01_ee_to_mumu:amp_s *)
(* factor-id: factor:b01_ee_to_mumu:s:ext:1:u *)
(* factor-id: factor:b01_ee_to_mumu:s:ext:2:vbar *)
(* factor-id: factor:b01_ee_to_mumu:s:ext:3:ubar *)
(* factor-id: factor:b01_ee_to_mumu:s:ext:4:v *)
(* factor-id: factor:b01_ee_to_mumu:s:vertex:1 *)
(* factor-id: factor:b01_ee_to_mumu:s:vertex:2 *)
(* factor-id: factor:b01_ee_to_mumu:s:prop:1 *)
(* factor-id: factor:b01_ee_to_mumu:s:nonchain:1 *)
(* index-map: idx:b01_ee_to_mumu:s:x_1:l_v1_mu -> mu1 *)
(* index-map: idx:b01_ee_to_mumu:s:x_2:l_v2_mu -> mu2 *)
(* index-map: idx:b01_ee_to_mumu:s:x_1:l_p1_l -> mu3 *)
(* index-map: idx:b01_ee_to_mumu:s:x_1:l_p1_r -> mu4 *)
(* index-map: idx:b01_ee_to_mumu:s:u:d_ext_1 -> a1 *)
(* index-map: idx:b01_ee_to_mumu:s:vbar:d_ext_2 -> a2 *)
(* index-map: idx:b01_ee_to_mumu:s:ubar:d_ext_3 -> a3 *)
(* index-map: idx:b01_ee_to_mumu:s:v:d_ext_4 -> a4 *)
(* index-map: idx:b01_ee_to_mumu:s:x_1:d_v1_bar -> a5 *)
(* index-map: idx:b01_ee_to_mumu:s:x_1:d_v1_psi -> a6 *)
(* index-map: idx:b01_ee_to_mumu:s:x_2:d_v2_bar -> a7 *)
(* index-map: idx:b01_ee_to_mumu:s:x_2:d_v2_psi -> a8 *)

qDefinitions = <|"q_s" -> HoldForm[qS == p1 + p2]|>;
qSubstitutions = {qS -> p1 + p2};
amplitudeFactorIDs = <|"amp_s" -> {"factor:b01_ee_to_mumu:s:ext:1:u", "factor:b01_ee_to_mumu:s:ext:2:vbar", "factor:b01_ee_to_mumu:s:ext:3:ubar", "factor:b01_ee_to_mumu:s:ext:4:v", "factor:b01_ee_to_mumu:s:vertex:1", "factor:b01_ee_to_mumu:s:vertex:2", "factor:b01_ee_to_mumu:s:prop:1", "factor:b01_ee_to_mumu:s:nonchain:1"}|>;
amplitudeIndexMap = <|"idx:b01_ee_to_mumu:s:x_1:l_v1_mu" -> "mu1", "idx:b01_ee_to_mumu:s:x_2:l_v2_mu" -> "mu2", "idx:b01_ee_to_mumu:s:x_1:l_p1_l" -> "mu3", "idx:b01_ee_to_mumu:s:x_1:l_p1_r" -> "mu4", "idx:b01_ee_to_mumu:s:u:d_ext_1" -> "a1", "idx:b01_ee_to_mumu:s:vbar:d_ext_2" -> "a2", "idx:b01_ee_to_mumu:s:ubar:d_ext_3" -> "a3", "idx:b01_ee_to_mumu:s:v:d_ext_4" -> "a4", "idx:b01_ee_to_mumu:s:x_1:d_v1_bar" -> "a5", "idx:b01_ee_to_mumu:s:x_1:d_v1_psi" -> "a6", "idx:b01_ee_to_mumu:s:x_2:d_v2_bar" -> "a7", "idx:b01_ee_to_mumu:s:x_2:d_v2_psi" -> "a8"|>;

ampS = (SpinorVBar[p2, me] . ((-I e) GA[mu1]) . SpinorU[p1, me]) * ((-I MT[mu1, mu2])/(SP[qS, qS] + I epsilon)) * (SpinorUBar[p3, mmu] . ((-I e) GA[mu2]) . SpinorV[p4, mmu]);
diagramAmplitudes = <|"amp_s" -> ampS|>;
ampTotal = ampS;
Print["Loaded generated amplitudes for B01_ee_to_mumu"];
