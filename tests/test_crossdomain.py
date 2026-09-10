import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import crossdomain


class TestCrossDomain(unittest.TestCase):
    def test_causal_observational_equivalence(self):
        w = crossdomain.causal_observational_equivalence()
        self.assertTrue(w["same_observational_law"])
        self.assertEqual(w["chain_P_Z_given_do_X1"], Fraction(1))
        self.assertEqual(w["fork_P_Z_given_do_X1"], Fraction(1, 2))
        self.assertTrue(w["interventions_differ"])

    def test_conformal_marginal_vs_conditional(self):
        w = crossdomain.conformal_marginal_vs_conditional()
        self.assertEqual(w["marginal_coverage"], Fraction(19, 20))
        self.assertTrue(w["marginal_ok"])
        self.assertEqual(w["conditional_coverage_stratum1"], Fraction(0))

    def test_partial_identification(self):
        w = crossdomain.partial_identification()
        self.assertEqual(w["identified_set"], (Fraction(3, 8), Fraction(5, 8)))
        self.assertTrue(w["inside_is_ambiguous"])
        self.assertTrue(w["outside_is_infeasible"])


if __name__ == "__main__":
    unittest.main()
