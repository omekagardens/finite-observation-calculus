import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import modelrun


class TestModelRun(unittest.TestCase):
    def test_verdicts_match_ground_truth(self):
        rows = {r["feature"]: r for r in modelrun.model_run()}
        self.assertEqual(rows["marginal a"]["verdict"], "separated")
        self.assertEqual(rows["correlation c"]["verdict"], "channel-limited")
        self.assertEqual(rows["null b"]["verdict"], "law-surviving")
        self.assertTrue(all(r["correct"] for r in modelrun.model_run()))

    def test_separations(self):
        rows = {r["feature"]: r for r in modelrun.model_run()}
        self.assertEqual(rows["marginal a"]["sep_local"], Fraction(1))
        self.assertEqual(rows["correlation c"]["sep_local"], Fraction(0))
        self.assertEqual(rows["correlation c"]["sep_joint"], Fraction(1))
        self.assertEqual(rows["null b"]["sep_joint"], Fraction(0))

    def test_margin_effect(self):
        coarse = modelrun.model_run(margin=Fraction(2))  # above every separation (<= 1)
        self.assertTrue(all(r["verdict"] == "law-surviving" for r in coarse))
        fine = modelrun.model_run(margin=Fraction(1, 2))
        self.assertEqual([r["verdict"] for r in fine],
                         ["separated", "channel-limited", "law-surviving"])


if __name__ == "__main__":
    unittest.main()
