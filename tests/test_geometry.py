import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import geometry


class TestGeometry(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(geometry.target(0), Fraction(1, 4))
        self.assertEqual(geometry.target(1), Fraction(17, 80))

    def test_type1_obstruction(self):
        t = geometry.type1_obstruction()
        self.assertTrue(t["same_point_law"])
        self.assertTrue(t["same_q1"])
        self.assertTrue(t["same_q2"])
        self.assertEqual(t["q1"], Fraction(17, 80))
        self.assertEqual(t["q2"], Fraction(21, 64))
        self.assertEqual(t["targets"], (Fraction(1, 4), Fraction(17, 80)))
        self.assertEqual(t["target_gap"], Fraction(3, 80))

    def test_type2_obstruction(self):
        t = geometry.type2_obstruction()
        self.assertEqual(t["delta_flat"], Fraction(16, 11))
        self.assertEqual(t["delta_conf"], Fraction(45, 158))
        self.assertTrue(t["q1_equal"])
        self.assertEqual(t["q1"], Fraction(1, 5))
        self.assertTrue(t["point_law_differs"])
        self.assertTrue(t["q2_splits"])
        self.assertEqual(t["q2_gap"], Fraction(5, 7296))

    def test_delta_inverse(self):
        self.assertEqual(geometry.delta_for_q(0, Fraction(1, 5)), Fraction(16, 11))
        self.assertEqual(geometry.delta_for_q(1, Fraction(1, 5)), Fraction(45, 158))


if __name__ == "__main__":
    unittest.main()
