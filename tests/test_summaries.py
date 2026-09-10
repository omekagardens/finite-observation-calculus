import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import instruments as ins
from foc import summaries


class TestSummaries(unittest.TestCase):
    def test_two_classes_for_mixed_state(self):
        classes = summaries.zthenx_classes(ins.rho_mixed())
        self.assertEqual(len(classes), 2)
        hists_by_state = {tuple(sorted(h)) for _st, h in classes}
        self.assertIn((("0", "+"), ("1", "+")), hists_by_state)
        self.assertIn((("0", "-"), ("1", "-")), hists_by_state)

    def test_summary_loses_weights(self):
        w0p, w1p = summaries.summary_loses_weights()
        self.assertEqual(w0p, Fraction(3, 8))
        self.assertEqual(w1p, Fraction(1, 8))
        self.assertNotEqual(w0p, w1p)


if __name__ == "__main__":
    unittest.main()
