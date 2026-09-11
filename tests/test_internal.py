import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest

from foc import internal


class TestInternal(unittest.TestCase):
    def test_self_consistency(self):
        rep = internal.internal_report()
        self.assertTrue(rep["stable"])     # fixed point: self-reinforcement stable
        self.assertFalse(rep["unstable"])  # not a fixed point
        self.assertTrue(rep["witness"]["no_replacement"])  # local instability certificate

    def test_composition_is_monotone(self):
        rep = internal.internal_report()
        self.assertEqual(rep["annihilator_local_node"], 9)
        self.assertEqual(rep["annihilator_pairs_node"], 6)
        self.assertEqual(rep["annihilator_composed"], 0)
        # adding nodes can only shrink the invisible sector
        self.assertLessEqual(
            rep["annihilator_composed"],
            min(rep["annihilator_local_node"], rep["annihilator_pairs_node"]),
        )


if __name__ == "__main__":
    unittest.main()
