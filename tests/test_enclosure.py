import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import enclosure as en


class TestBounds(unittest.TestCase):
    def test_masks_select_areas(self):
        areas = [Fraction(1, 12)] * 6
        b = en.bounds(areas, [1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 0])
        self.assertEqual(b["lower"], Fraction(1, 6))
        self.assertEqual(b["upper"], Fraction(1, 2))
        self.assertEqual(b["representative"], Fraction(1, 3))
        self.assertEqual(b["gap"], Fraction(1, 3))

    def test_certificate_and_abs_error(self):
        b = {"lower": Fraction(1, 6), "upper": Fraction(1, 2),
             "representative": Fraction(1, 3), "gap": Fraction(1, 3)}
        checks = en.certify(b, Fraction(8, 25))
        self.assertTrue(all(checks.values()))


class TestErrorDecomposition(unittest.TestCase):
    def test_three_way_identity(self):
        d = en.error_decomposition(Fraction(17, 150), Fraction(1, 3),
                                   Fraction(1, 3), Fraction(8, 25))
        self.assertTrue(d["identity"])
        self.assertEqual(d["sampling"], Fraction(17, 150) - Fraction(1, 3))
        self.assertEqual(d["annotation"], Fraction(0))
        self.assertEqual(d["quadrature"], Fraction(1, 3) - Fraction(8, 25))
        self.assertEqual(d["total"], Fraction(17, 150) - Fraction(8, 25))


class TestRefinement(unittest.TestCase):
    def test_gains_are_nonnegative(self):
        coarse = {"lower": Fraction(1, 6), "upper": Fraction(1, 2), "gap": Fraction(1, 3)}
        fine = {"lower": Fraction(5, 24), "upper": Fraction(1, 2), "gap": Fraction(7, 24)}
        r = en.refine(coarse, fine)
        self.assertEqual(r["lower_gain"], Fraction(1, 24))
        self.assertEqual(r["upper_drop"], Fraction(0))
        self.assertEqual(r["gap_drop"], Fraction(1, 24))
        self.assertTrue(r["lower_gain"] >= 0 and r["upper_drop"] >= 0 and r["gap_drop"] >= 0)


class TestKernelDiscrepancy(unittest.TestCase):
    def test_three_term_identity(self):
        k = en.kernel_discrepancy(Fraction(1, 4), Fraction(1, 5), Fraction(3, 20),
                                  Fraction(1, 10), Fraction(1, 4))
        self.assertTrue(k["identity"])
        self.assertTrue(k["split_ok"])
        self.assertEqual(k["boundary"], Fraction(1, 20))
        self.assertEqual(k["cross_order"], Fraction(1, 20))
        self.assertEqual(k["omission"], Fraction(-1, 10))
        self.assertEqual(k["total"], Fraction(0))


class TestReport(unittest.TestCase):
    def setUp(self):
        self.rep = en.enclosure_report()

    def test_aligned_probe_is_exact(self):
        a = self.rep["aligned"]
        self.assertEqual(a["bounds"], {"lower": Fraction(1, 6), "upper": Fraction(1, 6),
                                       "representative": Fraction(1, 6), "gap": Fraction(0)})
        self.assertEqual(a["volume"], Fraction(1, 6))
        self.assertTrue(all(a["checks"].values()))

    def test_unaligned_bracket(self):
        b = self.rep["unaligned_coarse"]["bounds"]
        self.assertEqual(b, {"lower": Fraction(1, 6), "upper": Fraction(1, 2),
                             "representative": Fraction(1, 3), "gap": Fraction(1, 3)})
        self.assertEqual(self.rep["unaligned_coarse"]["volume"], Fraction(8, 25))
        self.assertTrue(all(self.rep["unaligned_coarse"]["checks"].values()))

    def test_gap_shrinks_but_absolute_error_grows(self):
        r = self.rep["refinement"]
        self.assertTrue(r["gap_drop"] > 0)
        self.assertTrue(self.rep["abs_error_grew"])
        self.assertEqual(self.rep["quadrature_coarse"], Fraction(1, 75))
        self.assertEqual(self.rep["quadrature_fine"], Fraction(-17, 600))

    def test_representative_and_volume_are_not_ordered(self):
        # coarse: G > V ; fine: G < V — the pair is deliberately unordered
        self.assertGreater(self.rep["unaligned_coarse"]["bounds"]["representative"],
                           self.rep["unaligned_coarse"]["volume"])
        self.assertLess(self.rep["unaligned_fine"]["bounds"]["representative"],
                        self.rep["unaligned_fine"]["volume"])

    def test_report_decomposition_and_kernel(self):
        self.assertTrue(self.rep["decomposition"]["identity"])
        self.assertTrue(self.rep["kernel"]["identity"])


if __name__ == "__main__":
    unittest.main()
