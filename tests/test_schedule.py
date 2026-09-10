import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import instruments as ins
from foc import schedule


class TestSchedule(unittest.TestCase):
    def test_zx_counterexample_from_rho0(self):
        p_zx, p_xz = schedule.zx_counterexample(ins.rho_0())
        self.assertEqual(p_zx[("0", "+")], Fraction(1, 2))
        self.assertEqual(p_zx[("0", "-")], Fraction(1, 2))
        self.assertEqual(p_zx[("1", "+")], Fraction(0))
        self.assertEqual(p_zx[("1", "-")], Fraction(0))
        self.assertEqual(p_xz[("0", "+")], Fraction(1, 4))
        self.assertEqual(p_xz[("0", "-")], Fraction(1, 4))
        self.assertEqual(p_xz[("1", "+")], Fraction(1, 4))
        self.assertEqual(p_xz[("1", "-")], Fraction(1, 4))

    def test_discarded_channels_commute(self):
        z = ins.z_instrument()
        x = ins.x_instrument()
        for rho in [ins.rho_0(), ins.rho_1(), ins.rho_plus(), ins.rho_mixed()]:
            self.assertTrue(schedule.record_discarded_equal(z, x, rho))

    def test_recorded_maps_differ(self):
        z = ins.z_instrument()
        x = ins.x_instrument()
        self.assertFalse(schedule.recorded_equal(z, x, ins.rho_0()))

    def test_joint_probabilities_normalize(self):
        p_zx, _ = schedule.zx_counterexample(ins.rho_mixed())
        self.assertEqual(sum(p_zx.values()), Fraction(1))


if __name__ == "__main__":
    unittest.main()
