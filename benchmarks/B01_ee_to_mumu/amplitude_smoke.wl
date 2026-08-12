(* Lightweight smoke test for B01_ee_to_mumu; intentionally no simplification. *)
$LoadFeynArts = False;
status = Check[
  If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];
  Get[FileNameJoin[{DirectoryName[$InputFileName], "amplitudes.wl"}]];
  expectedSymbols = {ampS, ampTotal};
  expectedKeys = {"amp_s"};
  symbolsOK = And @@ (ValueQ /@ expectedSymbols);
  keysOK = Sort[Keys[diagramAmplitudes]] === Sort[expectedKeys];
  Print["SMOKE structural summary: diagrams=", Length[diagramAmplitudes], "; keys=", Keys[diagramAmplitudes], "; q=", Keys[qDefinitions]];
  If[symbolsOK && keysOK, 0, 2],
  Print["SMOKE generation-time exception: ", $MessageList]; 1
];
Quit[status];
