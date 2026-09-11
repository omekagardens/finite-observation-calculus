import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import transformer


class TestTransformer(unittest.TestCase):
    def test_dual_derivatives(self):
        x = transformer.Dual(Fraction(3), Fraction(1))  # d/dx at x = 3
        self.assertEqual((x * x).d, Fraction(6))        # d(x^2) = 2x
        self.assertEqual((x / x).d, Fraction(0))
        self.assertEqual((transformer.Dual(1) / x).d, -Fraction(1, 9))  # d(1/x) = -1/x^2

    def test_training_is_exact_and_decreases_loss(self):
        history = transformer.train_exact(transformer.TOY_DATA, steps=2)
        losses = [l for _, l in history]
        self.assertTrue(all(isinstance(l, Fraction) for l in losses))
        self.assertTrue(losses[0] > losses[1] > losses[2])
        self.assertTrue(all(isinstance(w, Fraction) for w in history[-1][0]))

    def test_gradient_matches_the_learning_direction(self):
        ws = [Fraction(2 * k + 1, 40) for k in range(22)]
        eta = Fraction(1, 50)
        self.assertLess(transformer.loss(transformer.exact_step(ws, transformer.TOY_DATA, eta),
                                         transformer.TOY_DATA),
                        transformer.loss(ws, transformer.TOY_DATA))


if __name__ == "__main__":
    unittest.main()
