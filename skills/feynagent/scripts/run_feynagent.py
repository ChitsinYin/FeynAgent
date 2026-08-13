"""Deterministic helpers for the FeynAgent Codex skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

STANDARD_TERMS = {
    "compton": "ElGa-ElGa",
    "e- gamma": "ElGa-ElGa",
    "electron photon": "ElGa-ElGa",
    "e- e+": "ElAel-MuAmu",
    "annihilation": "ElAel-MuAmu",
    "muon pair": "ElAel-MuAmu",
    "mu- mu+": "ElAel-MuAmu",
    "e- mu-": "ElMu-ElMu",
    "electron muon": "ElMu-ElMu",
}
CUSTOM_TERMS = ["custom", "yukawa", "new interaction", "nonstandard", "user supplied", "lagrangian"]
AMBIGUOUS_TERMS = ["whatever", "something", "unknown", "unspecified", "invent", "guess"]


def classify_request(text: str, *, initialized: bool = True) -> dict[str, Any]:
    lowered = text.lower()
    if not initialized:
        return {
            "classification": "unsupported_requires_review",
            "reason": "missing initialization",
            "action": "check .feynagent/environment.yaml or run python -m feynagent init",
        }
    if any(term in lowered for term in AMBIGUOUS_TERMS):
        return {
            "classification": "unsupported_requires_review",
            "reason": "ambiguous or unsupported custom physics request",
            "requires_review": ["custom rules", "conventions", "provenance"],
        }
    if any(term in lowered for term in CUSTOM_TERMS):
        if _has_rule_like_detail(lowered):
            return {
                "classification": "custom_audited",
                "reason": "custom interaction with rule-like details present",
                "backend_preference": "custom FeynArts-compatible model/adapter; legacy fallback/reference only",
            }
        return {
            "classification": "unsupported_requires_review",
            "reason": "custom request lacks explicit rule/convention/provenance",
            "requires_review": ["explicit custom rule", "conventions", "provenance"],
        }
    for term, example_id in STANDARD_TERMS.items():
        if term in lowered:
            return {
                "classification": "standard_native",
                "reason": f"matched standard-sector cue: {term}",
                "example_hint": example_id,
                "backend": "feynarts_feyncalc_native",
            }
    return {
        "classification": "unsupported_requires_review",
        "reason": "no supported standard process or audited custom rule detected",
    }


def _has_rule_like_detail(text: str) -> bool:
    return bool(re.search(r"\b(l\s*=|lagrangian|y\s*\bar|phi|rule|vertex|provenance|metric)\b", text))


def search_reference_index(root: Path, query: str) -> list[dict[str, Any]]:
    path = root / ".feynagent" / "reference_index.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    terms = [term for term in re.split(r"[^A-Za-z0-9]+", query.lower()) if term]
    hits = []
    for entry in data.get("entries", []):
        haystack = " ".join(str(entry.get(key, "")) for key in ("relative_path", "title", "path")).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            item = dict(entry)
            item["score"] = score
            hits.append(item)
    return sorted(hits, key=lambda item: (-item["score"], item.get("relative_path", "")))[:10]


def run_eval(path: Path) -> dict[str, Any]:
    cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    results = []
    for case in cases:
        result = classify_request(case["request"], initialized=case.get("initialized", True))
        passed = result["classification"] == case["expected_classification"]
        if case.get("expected_action_contains"):
            passed = passed and case["expected_action_contains"] in json.dumps(result)
        results.append({"id": case["id"], "passed": passed, "expected": case["expected_classification"], "actual": result})
    return {"passed": all(item["passed"] for item in results), "count": len(results), "results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    classify = sub.add_parser("classify")
    classify.add_argument("request")
    classify.add_argument("--not-initialized", action="store_true")
    search = sub.add_parser("search-examples")
    search.add_argument("query")
    search.add_argument("--root", type=Path, default=Path.cwd())
    eval_parser = sub.add_parser("eval")
    eval_parser.add_argument("--cases", type=Path, default=Path(__file__).resolve().parents[1] / "evals" / "smoke_cases.json")
    args = parser.parse_args(argv)
    if args.command == "classify":
        print(json.dumps(classify_request(args.request, initialized=not args.not_initialized), indent=2, sort_keys=True))
        return 0
    if args.command == "search-examples":
        print(json.dumps(search_reference_index(args.root.resolve(), args.query), indent=2, sort_keys=True))
        return 0
    if args.command == "eval":
        result = run_eval(args.cases)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["passed"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
