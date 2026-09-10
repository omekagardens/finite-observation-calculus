import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import confidence


class TestConfidence(unittest.TestCase):
    def test_marginal_vs_conditional(self):
        m = confidence.marginal_vs_conditional()
        self.assertEqual(m["prob_singleton"], Fraction(3, 64))
        self.assertEqual(m["unconditional_coverage"], Fraction(61, 64))
        self.assertTrue(m["unconditional_coverage_ok"])
        self.assertEqual(m["conditional_error_given_singleton"], Fraction(1))

    def test_distortion_margin(self):
        self.assertEqual(confidence.distortion_margin(Fraction(3, 64), 0),
                         Fraction(3, 64))
        self.assertEqual(confidence.distortion_margin(Fraction(3, 64), Fraction(3, 256)),
                         Fraction(3, 128))
        self.assertEqual(confidence.distortion_margin(Fraction(3, 64), Fraction(3, 128)),
                         Fraction(0))

    def test_bv_table_exact(self):
        rows = {r["name"]: r for r in confidence.bv_table()}

        u0 = rows["uniform/zero"]
        self.assertEqual(u0["D_e"], Fraction(3, 64))
        self.assertEqual(u0["slack"], Fraction(5, 128))
        self.assertEqual(u0["score"], Fraction(100))
        self.assertTrue(u0["sufficient"])

        uq = rows["uniform/quarter"]
        self.assertEqual(uq["D_e"], Fraction(3, 128))
        self.assertEqual(uq["slack"], Fraction(1, 64))
        self.assertEqual(uq["score"], Fraction(16))
        self.assertTrue(uq["sufficient"])

        uc = rows["uniform/contact"]
        self.assertEqual(uc["D_e"], Fraction(0))
        self.assertEqual(uc["slack"], Fraction(-1, 128))
        self.assertEqual(uc["score"], Fraction(4))
        self.assertFalse(uc["sufficient"])

        h0 = rows["half/zero"]
        self.assertEqual(h0["slack"], Fraction(5, 384))
        self.assertEqual(h0["score"], Fraction(100, 9))
        self.assertTrue(h0["sufficient"])

        hq = rows["half/quarter"]
        self.assertEqual(hq["slack"], Fraction(1, 384))
        self.assertEqual(hq["score"], Fraction(4, 9))
        self.assertFalse(hq["sufficient"])

        hc = rows["half/contact"]
        self.assertEqual(hc["D_e"], Fraction(0))
        self.assertFalse(hc["sufficient"])

        one = rows["one/zero"]
        self.assertEqual(one["D_e"], Fraction(0))
        self.assertFalse(one["sufficient"])

        two = rows["two/zero"]
        self.assertEqual(two["D_e"], Fraction(0))
        self.assertFalse(two["sufficient"])

    def test_clopper_pearson_sanity(self):
        low, high = confidence.clopper_pearson(2, 4, Fraction(1, 20))
        self.assertLessEqual(low, Fraction(1, 2))
        self.assertGreaterEqual(high, Fraction(1, 2))

        l0, _ = confidence.clopper_pearson(0, 4, Fraction(1, 20))
        self.assertEqual(l0, Fraction(0))
        _, h4 = confidence.clopper_pearson(4, 4, Fraction(1, 20))
        self.assertEqual(h4, Fraction(1))


if __name__ == "__main__":
    unittest.main()
