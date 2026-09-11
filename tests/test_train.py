import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import train


class TestTrain(unittest.TestCase):
    def test_least_squares_recovers_the_task(self):
        self.assertEqual(train.train_toy("linear")["ls"], (Fraction(1), Fraction(0)))
        self.assertEqual(train.train_toy("quadratic")["ls"], (Fraction(1), Fraction(1)))
        # the data lies on the model's span, so the fit is exact
        self.assertEqual(train.train_toy("quadratic")["loss_ls"], Fraction(0))

    def test_gradient_steps_decrease_loss_exactly(self):
        tr = train.train_toy("quadratic", steps=3, eta=Fraction(1, 20))
        losses = tr["loss_gd"]
        self.assertTrue(all(losses[i] > losses[i + 1] for i in range(len(losses) - 1)))
        self.assertTrue(all(isinstance(v, Fraction) for v in losses))

    def test_trained_audit_quadratic_task(self):
        r = {row["feature"]: row for row in train.trained_audit("quadratic")["rows"]}
        self.assertEqual(r["marginal a"]["verdict"], "separated")
        self.assertEqual(r["correlation c"]["verdict"], "channel-limited")
        self.assertEqual(r["distractor x_3"]["verdict"], "law-surviving")
        self.assertTrue(all(row["correct"] for row in train.trained_audit("quadratic")["rows"]))

    def test_trained_audit_linear_task_correlation_not_learned(self):
        # the linear task needs no product, so training drives c -> 0 and the
        # correlation feature is law-surviving
        r = {row["feature"]: row for row in train.trained_audit("linear")["rows"]}
        self.assertEqual(r["correlation c"]["verdict"], "law-surviving")
        self.assertTrue(all(row["correct"] for row in train.trained_audit("linear")["rows"]))


if __name__ == "__main__":
    unittest.main()
