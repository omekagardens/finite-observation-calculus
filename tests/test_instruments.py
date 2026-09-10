import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import instruments as ins
from foc import linalg as la


class TestInstruments(unittest.TestCase):
    def test_states_are_normalized(self):
        for rho in [ins.rho_0(), ins.rho_1(), ins.rho_plus(),
                    ins.rho_minus(), ins.rho_mixed()]:
            self.assertEqual(la.trace(rho), Fraction(1))

    def test_z_probs_from_rho0(self):
        z = ins.z_instrument()
        self.assertEqual(ins.outcome_probability(z, "0", ins.rho_0()), Fraction(1))
        self.assertEqual(ins.outcome_probability(z, "1", ins.rho_0()), Fraction(0))

    def test_x_probs_from_plus(self):
        x = ins.x_instrument()
        self.assertEqual(ins.outcome_probability(x, "+", ins.rho_plus()), Fraction(1))
        self.assertEqual(ins.outcome_probability(x, "-", ins.rho_plus()), Fraction(0))

    def test_channel_is_trace_preserving(self):
        z = ins.z_instrument()
        x = ins.x_instrument()
        for rho in [ins.rho_0(), ins.rho_mixed()]:
            self.assertEqual(la.trace(ins.channel(z, rho)), Fraction(1))
            self.assertEqual(la.trace(ins.channel(x, rho)), Fraction(1))


if __name__ == "__main__":
    unittest.main()
