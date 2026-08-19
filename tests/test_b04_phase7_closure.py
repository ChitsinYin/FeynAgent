import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feynagent.b04_phase7_closure import (
    audit_m2_script,
    compare_m2_to_gold,
    parse_assignments,
    parse_monomial,
)


class B04Phase7ClosureTests(unittest.TestCase):
    def test_restricted_parser_matches_wolfram_parenthesization_and_implicit_products(self):
        self.assertEqual(parse_monomial("(18*M^4)/MP^4"), parse_monomial("18 M^4/MP^4"))
        self.assertEqual(parse_monomial("(-48*M^4)/MP^4"), parse_monomial("-48 M^4/MP^4"))
        self.assertEqual(parse_monomial("M^4/(2*MP^4)"), parse_monomial("M^4/(2 MP^4)"))

    def test_assignment_parser_handles_multiple_gold_assignments_per_line(self):
        assignments = parse_assignments("MaGold=0; MbGold=0;\nMc2Gold=18 M^4/MP^4;\n")
        self.assertEqual(assignments["MaGold"], "0")
        self.assertEqual(assignments["MbGold"], "0")
        self.assertEqual(assignments["Mc2Gold"], "18 M^4/MP^4")

    def test_exact_m2_gold_comparison_passes_all_five_quantities(self):
        generated = """
Mc2Generated = (18*M^4)/MP^4;
Md2Generated = (32*M^4)/MP^4;
McMdInterferenceGenerated = (-48*M^4)/MP^4;
M2PolarizationSummedRawGenerated = (2*M^4)/MP^4;
M2PublishedRateConventionGenerated = M^4/(2*MP^4);
"""
        gold = """
Mc2Gold=18 M^4/MP^4;
Md2Gold=32 M^4/MP^4;
McMdInterferenceGold=-48 M^4/MP^4;
M2PolarizationSummedRawGold=2 M^4/MP^4;
M2PublishedRateConventionGold=M^4/(2 MP^4);
"""
        comparisons = compare_m2_to_gold(generated, gold)
        self.assertEqual(set(comparisons), {"Mc2", "Md2", "interference", "raw_total", "rate_convention"})
        self.assertTrue(all(item["status"] == "PASS" for item in comparisons.values()))

    def test_mismatch_is_a_conflict_and_is_not_averaged(self):
        generated = "Mc2Generated = 17*M^4/MP^4;"
        gold = "Mc2Gold = 18*M^4/MP^4;"
        comparisons = compare_m2_to_gold(generated, gold)
        self.assertEqual(comparisons["Mc2"]["status"], "CONFLICT_REQUIRES_REVIEW")

    def test_script_audit_rejects_utf8_bom(self):
        result = audit_m2_script(b"\xef\xbb\xbfrepo = \"x\";")
        self.assertEqual(result["status"], "CONFLICT_REQUIRES_REVIEW")
        self.assertTrue(result["utf8_bom"])


if __name__ == "__main__":
    unittest.main()
