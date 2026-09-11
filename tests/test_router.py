import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import router


class TestRouter(unittest.TestCase):
    def test_certified_routing(self):
        w = [Fraction(3, 5), Fraction(-4, 5)]
        self.assertEqual(router.route(w, (Fraction(3), Fraction(1))), "A")
        self.assertEqual(router.route(w, (Fraction(1), Fraction(3))), "B")
        # the boundary input is ambiguous, the well-separated ones are certified
        self.assertIsNone(router.certified_route(w, (Fraction(1, 2), Fraction(1, 2)), Fraction(1, 2)))
        self.assertEqual(router.certified_route(w, (Fraction(3), Fraction(1)), Fraction(1, 2)), "A")

    def test_router_precision(self):
        rep = router.router_report()
        self.assertEqual(rep["router_precision"]["grid"], 4)
        self.assertEqual(rep["router_precision"]["bits"], 3)

    def test_routing_type_criterion(self):
        rep = router.router_report()
        self.assertFalse(rep["type_orthogonal_classical"])   # type immaterial
        self.assertTrue(rep["type_orthogonal_coherent"])     # coherence -> material
        self.assertTrue(rep["type_overlapping_classical"])   # overlap -> material

    def test_replacement_criterion(self):
        rep = router.replacement_report()
        self.assertTrue(rep["counts_valid"])       # blind downstream: replacement valid
        self.assertFalse(rep["reads_Z_valid"])     # Z-reading downstream: not valid
        self.assertTrue(rep["witness"]["no_replacement"])


if __name__ == "__main__":
    unittest.main()
