import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import itertools
import unittest
from fractions import Fraction

from foc import linalg as la
from foc import ambiguity


def grid(n, vals):
    return [tuple(Fraction(v) for v in t) for t in itertools.product(vals, repeat=n)]


class TestAmbiguity(unittest.TestCase):
    def test_qubit_coherence_classification(self):
        w = ambiguity.qubit_coherence()
        # {Z} leaves the X-coherence invisible (dim 1); {Z, X} removes it
        self.assertEqual(w["dim_accessible"], 1)
        self.assertEqual(w["dim_completed"], 0)
        # channel-limited when X is admissible, law-surviving when it is not
        self.assertEqual(w["class_open"], "channel-limited")
        self.assertEqual(w["class_closed"], "law-surviving")

    def test_two_qubit_locality(self):
        w = ambiguity.two_qubit_locality()
        # one-body access leaves exactly the 9-dim two-body correlation sector
        self.assertEqual(w["dim_local"], 9)
        self.assertEqual(w["dim_joint"], 0)

    def test_classify_separated(self):
        P0 = la.mat([[1, 0], [0, 0]])
        P1 = la.mat([[0, 0], [0, 1]])
        # a diagonal difference IS seen by Z
        self.assertEqual(
            ambiguity.classify(la.mat([[1, 0], [0, -1]]), [P0, P1], [P0, P1]), "separated"
        )

    def test_l_inf_separation(self):
        # binary: matches max(d - 2e, 0) exactly
        P = [Fraction(1, 2), Fraction(1, 2)]
        Q = [Fraction(1, 4), Fraction(3, 4)]
        self.assertEqual(ambiguity.l_inf_separation(P, Q, Fraction(1, 16)), Fraction(1, 8))
        self.assertEqual(ambiguity.l_inf_separation(P, Q, Fraction(1, 8)), Fraction(0))
        self.assertEqual(ambiguity.l_inf_erosion_rate(P, Q), 2)
        # spread: four active components -> e erodes at rate 4, not 2
        P4 = [Fraction(2, 5), Fraction(3, 10), Fraction(1, 5), Fraction(1, 10)]
        Q4 = [Fraction(1, 5), Fraction(1, 5), Fraction(3, 10), Fraction(3, 10)]
        self.assertEqual(ambiguity.l_inf_erosion_rate(P4, Q4), 4)
        self.assertEqual(ambiguity.l_inf_separation(P4, Q4, Fraction(1, 20)), Fraction(1, 10))

    def test_probe_audit(self):
        P0 = la.mat([[1, 0], [0, 0]])
        P1 = la.mat([[0, 0], [0, 1]])
        h = Fraction(1, 2)
        Qp = la.mat([[h, h], [h, h]])
        Qm = la.mat([[h, -h], [-h, h]])
        # the coherence X is separated by the second (finer) family
        self.assertEqual(
            ambiguity.probe_audit(ambiguity.X, [[P0, P1], [P0, P1, Qp, Qm]]), 1
        )
        # ...or never, if only diagonal probes are available -> law-surviving
        self.assertIsNone(ambiguity.probe_audit(ambiguity.X, [[P0, P1]]))

    def test_llm_probe_audit(self):
        rows = {(r["feature"], r["model"]): r["verdict"] for r in ambiguity.llm_probe_audit()}
        # a local feature reads immediately
        self.assertEqual(rows[("site-A logit", "open")], "separated")
        # a cross-site feature needs a joint probe (channel-limited)...
        self.assertEqual(rows[("cross-site correlation", "open")], "channel-limited")
        # ...but if joint probes are inadmissible it is law-surviving
        self.assertEqual(rows[("cross-site correlation", "local-only")], "law-surviving")

    def test_linear_symmetry_algebra(self):
        pts = grid(2, [-2, -1, 1, 2])
        # rotation and scaling are continuous linear symmetries
        self.assertEqual(
            ambiguity.linear_symmetry_dim(lambda t: [[2 * t[0], 2 * t[1]]], pts, 2), 1
        )
        self.assertEqual(
            ambiguity.linear_symmetry_dim(lambda t: [[t[1], t[0]]], pts, 2), 1
        )
        # x^3+y^3 has no continuous linear symmetry (accidental)
        self.assertEqual(
            ambiguity.linear_symmetry_dim(lambda t: [[3 * t[0] ** 2, 3 * t[1] ** 2]], pts, 2), 0
        )
        # (eta+delta, eta*delta) has only a discrete Z/2 symmetry
        pts2 = grid(2, [0, 1, 2, 3])
        self.assertEqual(
            ambiguity.linear_symmetry_dim(
                lambda t: [[Fraction(1), Fraction(1)], [t[1], t[0]]], pts2, 2
            ),
            0,
        )

    def test_symmetry_examples(self):
        rows = {name: (dim, kind) for name, dim, kind in ambiguity.symmetry_examples()}
        self.assertEqual(rows["x^2+y^2"][0], 1)      # continuous
        self.assertEqual(rows["x*y"][0], 1)          # continuous
        self.assertEqual(rows["x^3+y^3"][0], 0)      # accidental
        self.assertEqual(rows["(eta+delta, eta*delta)"][0], 0)  # discrete only

    def test_distortion_collapse(self):
        self.assertEqual(ambiguity.distortion_separation(Fraction(1, 4), Fraction(1, 16)),
                         Fraction(1, 8))
        self.assertEqual(ambiguity.distortion_separation(Fraction(1, 4), Fraction(1, 8)),
                         Fraction(0))
        self.assertFalse(ambiguity.collapses(Fraction(1, 4), Fraction(1, 16)))
        self.assertTrue(ambiguity.collapses(Fraction(1, 4), Fraction(1, 8)))


if __name__ == "__main__":
    unittest.main()
