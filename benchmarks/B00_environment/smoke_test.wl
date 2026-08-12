Print["FEYNAGENT_WOLFRAM_SMOKE_BEGIN"];
Print["WOLFRAM_VERSION=", $Version];
Print["WOLFRAM_VERSION_NUMBER=", ToString[$VersionNumber, InputForm]];

ClearAll[printVersionIfPresent];
printVersionIfPresent[label_String, names_List] := Module[{found = False, value},
  Do[
    If[NameQ[name],
      value = Quiet[Check[ToExpression[name], "unavailable"]];
      Print[label, "_VERSION_SYMBOL=", name];
      Print[label, "_VERSION=", ToString[value, InputForm]];
      found = True;
      Break[];
    ],
    {name, names}
  ];
  If[! found, Print[label, "_VERSION=unknown"]];
];

ClearAll[tryPackage];
tryPackage[label_String, context_String, versionNames_List, smokeExpr_String] := Module[
  {loadOk = False, smokeOk = True, loadResult, smokeResult},
  loadResult = Quiet[Check[Needs[context], $Failed]];
  loadOk = Length[Names[context <> "*"]] > 0;
  If[loadOk,
    Print[label, "_LOAD_STATUS=AVAILABLE"];
    printVersionIfPresent[label, versionNames];
    smokeResult = Quiet[Check[ToExpression[smokeExpr], smokeOk = False; $Failed]];
    If[smokeOk,
      Print[label, "_SMOKE_STATUS=PASS"];
      Print[label, "_SMOKE_RESULT=", ToString[smokeResult, InputForm]],
      Print[label, "_SMOKE_STATUS=FAIL"]
    ],
    Print[label, "_LOAD_STATUS=BLOCKED"];
    Print[label, "_LOAD_RESULT=", ToString[loadResult, InputForm]]
  ];
];

tryPackage[
  "FEYNCALC",
  "FeynCalc`",
  {"FeynCalc`$FeynCalcVersion", "FeynCalc`$FeynCalcStartupMessages"},
  "FCI[SP[p, p]]"
];

tryPackage[
  "FEYNARTS",
  "FeynArts`",
  {"FeynArts`$FeynArtsVersion", "FeynArts`FeynArtsVersion"},
  "Length[Names[\"FeynArts`*\"]]"
];

Print["FEYNAGENT_WOLFRAM_SMOKE_END"];
Quit[0];
