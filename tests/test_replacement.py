import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import replacement as rp


class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.problem = rp._demo_problem()

    def test_affine_excess(self):
        self.assertTrue(rp.affine_in_t(self.problem))

    def test_values_are_nondecreasing_and_nonpositive(self):
        values = rp.minimax_values(self.problem)
        for row in values:
            self.assertTrue(all(v <= 0 for v in row))
            self.assertTrue(all(row[i] <= row[i + 1] for i in range(len(row) - 1)))

    def test_sharp_case_minimizer(self):
        certs = {(c["assumed"], c["bound"]): c for c in rp.minimax_certificate(self.problem)}
        self.assertEqual(certs[(0, 0)]["minimax"], Fraction(-1, 4))
        self.assertEqual(certs[(0, 0)]["minimizer_weights"], [Fraction(1)])
        self.assertEqual(certs[(1, 0)]["minimax"], Fraction(-1, 4))

    def test_all_ties_retained(self):
        certs = {(c["assumed"], c["bound"]): c for c in rp.minimax_certificate(self.problem)}
        # at bound 1/2 the three rules all tie at zero
        self.assertEqual(certs[(0, 1)]["minimax"], Fraction(0))
        self.assertEqual(certs[(0, 1)]["minimizer_indices"], [0, 1, 2])

    def test_coarse_always_available(self):
        self.assertTrue(all(c["coarse_available"] for c in rp.minimax_certificate(self.problem)))

    def test_subtract_before_max(self):
        # the worst case of the excess is not the excess of the worst risks
        g = self.problem["worlds"][2]["coarse"]
        we = rp.worst_excess(self.problem, 0, 2, 1)
        self.assertEqual(we, max(r - g for r in
                                 [self.problem["worlds"][t]["risks"][0][1] for t in range(3)]))


class TestEnvelope(unittest.TestCase):
    def test_full_replacement_max_and_flatness(self):
        sharp = [[Fraction(1, 2), Fraction(1, 2), Fraction(0)], [Fraction(1, 4), Fraction(3, 4)]]
        self.assertEqual(rp.full_replacement_max(sharp), Fraction(5, 4))
        self.assertFalse(rp.all_fibers_flat(sharp))
        flat = [[Fraction(1, 3), Fraction(1, 3)]]
        self.assertTrue(rp.all_fibers_flat(flat))

    def test_envelope_attained_when_fibers_flat(self):
        p = rp.envelope_profile(Fraction(1, 10), [[Fraction(1, 3), Fraction(1, 3)]],
                                [Fraction(0), Fraction(1, 2), Fraction(1)])
        self.assertEqual(p["maximum"], Fraction(1, 3))
        self.assertTrue(p["full_support_maximum_attained"])

    def test_envelope_not_attained_when_sharp_and_shifted(self):
        p = rp.envelope_profile(Fraction(1, 10),
                                [[Fraction(1, 2), Fraction(1, 2), Fraction(0)],
                                 [Fraction(1, 4), Fraction(3, 4)]],
                                [Fraction(0), Fraction(1, 2), Fraction(1)])
        self.assertFalse(p["zero_is_worst"])
        self.assertFalse(p["full_support_maximum_attained"])

    def test_envelope_attained_when_clean_is_worst(self):
        p = rp.envelope_profile(Fraction(2), [[Fraction(1), Fraction(1, 2), Fraction(0)]],
                                [Fraction(0), Fraction(1, 2), Fraction(1)])
        self.assertTrue(p["zero_is_worst"])
        self.assertTrue(p["full_support_maximum_attained"])
        self.assertEqual(p["maximum"], Fraction(2))

    def test_envelope_is_affine_in_t(self):
        self.assertEqual(rp.envelope(Fraction(1, 10), Fraction(5, 4), Fraction(1, 2)),
                         Fraction(27, 40))


class TestContinuousRetention(unittest.TestCase):
    def test_optimizer_and_minimum(self):
        A, B = Fraction(1, 2), Fraction(3, 10)
        self.assertEqual(rp.retention_optimizer(A, B)["weight"], Fraction(3, 5))
        self.assertEqual(rp.retention_minimum(A, B), Fraction(-9, 50))

    def test_flat_interval_and_endpoints(self):
        self.assertEqual(rp.retention_optimizer(Fraction(0), Fraction(0))["kind"], "interval")
        self.assertEqual(rp.retention_optimizer(Fraction(0), Fraction(1))["weight"], Fraction(1))
        self.assertEqual(rp.retention_optimizer(Fraction(0), Fraction(-1))["weight"], Fraction(0))

    def test_kkt_identity(self):
        A, B = Fraction(1, 2), Fraction(3, 10)
        astar = rp.retention_optimizer(A, B)["weight"]
        for a in (Fraction(0), Fraction(1, 2), Fraction(1)):
            self.assertTrue(rp.retention_kkt(A, B, a, astar))

    def test_menu_gap_and_sharp_bound(self):
        A, B, menu = Fraction(1, 2), Fraction(3, 10), [Fraction(0), Fraction(1, 2), Fraction(1)]
        self.assertEqual(rp.menu_gap(A, B, menu), Fraction(1, 200))
        self.assertTrue(rp.menu_gap_sharp(A, B, menu))


class TestAggregateIsNotPerInstance(unittest.TestCase):
    def setUp(self):
        self.histories = [(Fraction(1, 2), Fraction(1), Fraction(1, 2)),
                          (Fraction(1, 2), Fraction(1), Fraction(0))]

    def test_aggregate_zero_hides_risk(self):
        res = rp.aggregate_zero_hides_risk(self.histories, Fraction(1, 2))
        self.assertTrue(res["is_zero"])
        self.assertTrue(res["hides"])
        self.assertEqual(res["positive"], Fraction(1, 8))
        self.assertEqual(res["negative"], Fraction(-1, 8))

    def test_group_polynomials_sum_to_aggregate(self):
        groups = rp.group_polynomials(self.histories, Fraction(3, 4))
        total = rp.history_excess(Fraction(1), Fraction(1, 2), Fraction(3, 4)) / 2 \
            + rp.history_excess(Fraction(1), Fraction(0), Fraction(3, 4)) / 2
        self.assertEqual(groups["aggregate"], total)

    def test_aggregate_coefficients(self):
        self.assertEqual(rp.aggregate_coefficients(self.histories),
                         (Fraction(1), Fraction(1, 4)))


class TestStressTilts(unittest.TestCase):
    def test_tilts_opposite_and_uniform_mean(self):
        self.assertTrue(rp.tilts_are_opposite(4))
        self.assertEqual(rp.forward_tilt(4),
                         [Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5)])
        self.assertEqual(rp.reverse_tilt(4),
                         [Fraction(2, 5), Fraction(3, 10), Fraction(1, 5), Fraction(1, 10)])
        self.assertEqual(rp.tilt_mean(4), [Fraction(1, 4)] * 4)

    def test_tilt_cancellation(self):
        self.assertTrue(rp.tilt_cancellation(Fraction(3, 20), Fraction(-3, 20), Fraction(0)))
        self.assertFalse(rp.tilt_cancellation(Fraction(3, 20), Fraction(-1, 20), Fraction(0)))


class TestReport(unittest.TestCase):
    def test_report_assembles(self):
        rep = rp.replacement_report()
        self.assertTrue(rep["affine"])
        self.assertEqual(rep["retention"]["optimizer"], Fraction(3, 5))
        self.assertTrue(rep["aggregate_zero"]["hides"])
        self.assertTrue(rep["tilts"]["opposite"])
        self.assertTrue(rep["tilts"]["cancellation"])


if __name__ == "__main__":
    unittest.main()
