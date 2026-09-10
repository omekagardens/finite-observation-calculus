import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import linalg as la
from foc import forgetting
from foc import instruments as ins


class TestForgetting(unittest.TestCase):
    def test_kraus_instrument_is_valid_and_nonprojective(self):
        self.assertTrue(forgetting.is_instrument([forgetting.D0, forgetting.D1], 2))
        e0 = la.mat_mul(la.transpose(forgetting.D0), forgetting.D0)
        # a projector satisfies E^2 = E; these do not, so the instrument is
        # genuinely non-projective (the source of the obstruction).
        self.assertNotEqual(e0, la.mat_mul(e0, e0))
        self.assertEqual(
            e0,
            la.mat([[Fraction(16, 25), 0], [0, Fraction(9, 25)]]),
        )

    def test_z_example(self):
        z = forgetting.z_example()
        mixed = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]]
        self.assertEqual(z["forgotten"], mixed)
        self.assertEqual(z["recombined"], ins.rho_plus())
        self.assertTrue(z["forgotten_is_dephased"])
        self.assertTrue(z["recombined_is_identity"])
        self.assertTrue(z["differ"])

    def test_coherent_and_incoherent_differ_on_coherence(self):
        rho = la.mat([[Fraction(2, 5), Fraction(1, 5)], [Fraction(1, 5), Fraction(3, 5)]])
        self.assertNotEqual(
            forgetting.coherent_recombination([forgetting.D0, forgetting.D1], rho),
            forgetting.incoherent_sum([forgetting.D0, forgetting.D1], rho),
        )

    def test_impossibility_witness(self):
        w = forgetting.impossibility_witness()
        mixed = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]]

        # the coarse channel merges the two inputs
        self.assertEqual(w["coarse_state"], mixed)
        self.assertEqual(w["coarse_plus"], mixed)
        self.assertEqual(w["coarse_minus"], mixed)
        self.assertTrue(w["coarse_merges"])

        # the fine feedback separates them
        self.assertEqual(
            w["fine_plus"],
            [[Fraction(1, 2), Fraction(12, 25)], [Fraction(12, 25), Fraction(1, 2)]],
        )
        self.assertEqual(
            w["fine_minus"],
            [[Fraction(1, 2), Fraction(-12, 25)], [Fraction(-12, 25), Fraction(1, 2)]],
        )
        self.assertTrue(w["fine_separates"])

        # ...so no coarse-only replacement exists
        self.assertTrue(w["no_replacement"])

    def test_feedback_is_trace_preserving(self):
        # the witness feedback must itself be a physical instrument
        w = forgetting.impossibility_witness()
        self.assertEqual(la.trace(w["fine_plus"]), Fraction(1))
        self.assertEqual(la.trace(w["fine_minus"]), Fraction(1))


if __name__ == "__main__":
    unittest.main()
