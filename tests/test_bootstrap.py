import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import bootstrap


class TestBootstrap(unittest.TestCase):
    def test_parse_json_tolerates_prose(self):
        text = 'Sure:\n```json\n{"regimes": [{"name": "a"}]}\n```\ndone'
        self.assertEqual(bootstrap.parse_json(text), {"regimes": [{"name": "a"}]})

    def test_train_node_is_exact(self):
        ex = [{"x": [1, 1], "y": 1}, {"x": [2, 1], "y": 2},
              {"x": [1, 2], "y": 2}, {"x": [2, 2], "y": 4}]
        node = bootstrap.train_node(ex)  # y = x1 * x2 exactly
        self.assertEqual(node["coefficients"], (Fraction(0), Fraction(0), Fraction(1)))
        self.assertEqual(node["loss"], Fraction(0))

    def test_mock_bootstrap_recovers_regimes(self):
        rep = bootstrap.bootstrap("toy", bootstrap.MockLLM())
        self.assertEqual(rep["regimes"], ["linear", "interaction"])
        self.assertEqual(rep["nodes"][0]["coefficients"],
                         (Fraction(1), Fraction(0), Fraction(0)))
        self.assertEqual(rep["nodes"][1]["coefficients"],
                         (Fraction(0), Fraction(0), Fraction(1)))
        self.assertTrue(rep["nodes"][1]["uses_product"])


if __name__ == "__main__":
    unittest.main()
