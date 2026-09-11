import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import composition as cp


class TestIntegrals(unittest.TestCase):
    def test_one_dimensional_reference_values(self):
        self.assertEqual(cp.pair_int_1d(0, 1, 0, 1), Fraction(1, 2))
        self.assertEqual(cp.triple_int_1d(0, 1, 0, 1, 0, 1), Fraction(1, 6))

    def test_empty_intervals_vanish(self):
        self.assertEqual(cp.pair_int_1d(1, 1, 0, 1), Fraction(0))
        self.assertEqual(cp.triple_int_1d(0, 1, 0, 1, 0, 0), Fraction(0))

    def test_two_dimensional_factorization(self):
        clip = (Fraction(0), Fraction(1), Fraction(0), Fraction(1))
        self.assertEqual(cp.clip_volume(*clip), Fraction(1, 2))
        self.assertEqual(cp.pair_measure(clip, clip), Fraction(1, 16))
        self.assertEqual(cp.triple_measure(clip, clip, clip), Fraction(1, 288))


class TestUnitRectangle(unittest.TestCase):
    def setUp(self):
        self.u = cp.unit_rectangle_report()

    def test_pair_vs_triple_numbers(self):
        self.assertEqual(self.u["pair_fraction"], Fraction(1, 4))
        self.assertEqual(self.u["triple_fraction"], Fraction(1, 36))
        self.assertEqual(self.u["pair_product"], Fraction(1, 128))
        self.assertEqual(self.u["triple"], Fraction(1, 288))

    def test_pair_additivity_does_not_close(self):
        self.assertTrue(self.u["noncompositional"])
        self.assertEqual(self.u["product_error"], Fraction(1, 128) - Fraction(1, 288))

    def test_conditionals_are_not_transitions(self):
        self.assertFalse(self.u["row_sum_is_one"])
        self.assertEqual(self.u["squared_pair_fraction"], Fraction(1, 16))
        self.assertTrue(self.u["squaring_mismatch"])

    def test_middle_covariance(self):
        self.assertEqual(self.u["middle_covariance"], Fraction(-5, 576))


class TestCovarianceIdentity(unittest.TestCase):
    def test_identity_holds_on_case(self):
        res = cp.covariance_identity_1d(0, 1, Fraction(1, 4), Fraction(3, 4), 0, 1)
        self.assertTrue(res["identity"])
        self.assertEqual(res["T"], Fraction(11, 96))
        self.assertEqual(res["P"], Fraction(1, 8))
        self.assertEqual(res["covariance"], Fraction(-1, 48))

    def test_identity_holds_on_several_clips(self):
        cases = [
            (0, 1, Fraction(1, 4), Fraction(3, 4), 0, 1),
            (Fraction(1, 5), Fraction(4, 5), 0, 1, Fraction(1, 2), Fraction(3, 2)),
            (0, 2, Fraction(1, 3), Fraction(4, 3), Fraction(1, 2), 2),
        ]
        for case in cases:
            self.assertTrue(cp.covariance_identity_1d(*case)["identity"])


class TestCoarsening(unittest.TestCase):
    def test_geometric_weights_sum_to_one(self):
        w = cp.coarsening_weights([Fraction(1, 4), Fraction(1, 4)],
                                  [Fraction(1, 4), Fraction(1, 2)],
                                  Fraction(1, 2), Fraction(3, 4))
        self.assertEqual(sum(sum(row) for row in w), Fraction(1))
        self.assertEqual(w, [[Fraction(1, 6), Fraction(1, 3)], [Fraction(1, 6), Fraction(1, 3)]])

    def test_aggregation_matches_report(self):
        agg = cp.composition_report()["aggregation"]
        self.assertTrue(agg["geometric_ok"])
        self.assertTrue(agg["differ"])
        self.assertEqual(agg["weighted"], Fraction(11, 24))
        self.assertEqual(agg["unweighted"], Fraction(7, 16))

    def test_undefined_conventions(self):
        self.assertIsNone(cp.pair_product(Fraction(1, 4), Fraction(1, 4), Fraction(0)))
        self.assertIsNone(cp.conditional(Fraction(1, 4), Fraction(0), Fraction(1)))
        self.assertIsNone(cp.coarsening_weights([Fraction(1)], [Fraction(1)],
                                                Fraction(0), Fraction(1)))


if __name__ == "__main__":
    unittest.main()
