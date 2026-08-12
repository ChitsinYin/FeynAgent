(* Human-run Ward identity check for B02_compton; generated at 2026-08-12T22:06:31.565733+08:00. *)
(* Not executed by default in Day-3 generation. *)
$LoadFeynArts = False;
If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];
Get[FileNameJoin[{DirectoryName[$InputFileName], "amplitudes.wl"}]];
Print["WARD CHECK START: replaces external photon polarization by corresponding momentum."];
wardIncomingRaw = ampTotal /. PolarizationVector[k1, mu_] :> Momentum[k1, mu];
wardOutgoingRaw = ampTotal /. ComplexConjugate[PolarizationVector[k2, mu_]] :> Momentum[k2, mu];
Put[wardIncomingRaw, FileNameJoin[{DirectoryName[$InputFileName], "ward_incoming_raw.m"}]];
Put[wardOutgoingRaw, FileNameJoin[{DirectoryName[$InputFileName], "ward_outgoing_raw.m"}]];
Print["WARD CHECK RAW EXPRESSIONS SAVED; simplify manually if desired."];
Quit[0];
