(* Human-run heavy M2 script for B01_ee_to_mumu; generated at 2026-08-12T22:06:31.565733+08:00. *)
(* DO NOT run from the live agent loop. This script performs spin/polarization sums and simplification. *)
$LoadFeynArts = False;
outputDir = FileNameJoin[{DirectoryName[$InputFileName], "m2_outputs"}];
doneSentinel = FileNameJoin[{outputDir, "DONE"}];
force = TrueQ[$ForceM2];
If[FileExistsQ[doneSentinel] && !force, Print["Existing successful M2 detected; set $ForceM2=True to overwrite."]; Quit[2]];
If[!DirectoryQ[outputDir], CreateDirectory[outputDir]];
stdoutPath = FileNameJoin[{outputDir, "compute_m2.stdout.log"}];
stderrPath = FileNameJoin[{outputDir, "compute_m2.stderr.log"}];
stdout = OpenWrite[stdoutPath];
stderr = OpenWrite[stderrPath];
log[msg_] := (Print[msg]; WriteString[stdout, ToString[msg] <> "\n"]);
fail[msg_] := (WriteString[stderr, ToString[msg] <> "\n"]; Close /@ {stdout, stderr}; Quit[1]);
log["HEAVY COMPUTATION START: spin sums, polarization sums, averaging, and simplification."];
status = Check[
  If[!MemberQ[$Packages, "FeynCalc`"], Quiet[Get["FeynCalc`"], FrontEndObject::notavail]];
  Get[FileNameJoin[{DirectoryName[$InputFileName], "amplitudes.wl"}]];
  initialAverage = 1/4;
  rawInterference = ampTotal ComplexConjugate[ampTotal];
  spinSummed = FermionSpinSum[rawInterference];
  polSummed = spinSummed;
  Do[polSummed = DoPolarizationSums[polSummed, mom], {mom, {p1, p2, p3, p4, k1, k2}}];
  m2Raw = initialAverage polSummed;
  Put[m2Raw, FileNameJoin[{outputDir, "m2_raw.m"}]];
  m2Simplified = FullSimplify[Contract[m2Raw /. qSubstitutions]];
  Put[m2Simplified, FileNameJoin[{outputDir, "m2_simplified.m"}]];
  Put[<|"benchmark" -> "B01_ee_to_mumu", "process" -> "b01_ee_to_mumu", "status" -> "DONE"|>, FileNameJoin[{outputDir, "compute_m2_report.m"}]];
  Put[DateString[], doneSentinel];
  log["DONE: raw and simplified M2 saved."]; 0,
  fail["Heavy computation failed; DONE sentinel was not written."]
];
Close /@ {stdout, stderr};
Quit[status];
