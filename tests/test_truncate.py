import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import truncate


class TestTruncate(unittest.TestCase):
    def test_truncation_bounds_denominators(self):
        ws = [Fraction(1, 3), Fraction(2, 7), Fraction(-5, 11)]
        wq = truncate.truncate(ws, 16)
        self.assertTrue(all((w * 16).denominator == 1 for w in wq))
        self.assertLessEqual(truncate.denominator_bits(wq), 16 .bit_length())

    def test_rate_two_bound_and_verdict_survive(self):
        res = truncate.certified_truncation(steps=2)
        # exact weights blow up
        self.assertGreater(res["exact_bits"], 1000)
        kept = [r for r in res["rows"] if not r["degenerate"]]
        self.assertTrue(kept)
        # the rate-two bound holds on every non-degenerate grid
        self.assertTrue(all(r["rate_two_ok"] for r in kept))
        # a coarse grid preserves the verdict at a tiny fraction of the bits
        coarse = res["rows"][0]  # grid 16
        self.assertTrue(coarse["verdict_ok"])
        self.assertLessEqual(coarse["bits"], 6)
        self.assertGreater(res["exact_bits"], 100 * coarse["bits"])


if __name__ == "__main__":
    unittest.main()
