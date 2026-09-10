import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import unittest
from fractions import Fraction

from foc import linalg as la
from foc import ambiguity
from foc import certificate


def _qubit():
    P0 = la.mat([[1, 0], [0, 0]])
    P1 = la.mat([[0, 0], [0, 1]])
    h = Fraction(1, 2)
    Qp = la.mat([[h, h], [h, h]])
    Qm = la.mat([[h, -h], [-h, h]])
    return [P0, P1], [P0, P1, Qp, Qm]


class TestCertificate(unittest.TestCase):
    def test_build_and_verify_three_labels(self):
        A, C = _qubit()
        Z = la.mat([[1, 0], [0, -1]])
        separated = certificate.build_certificate(Z, A, C)
        self.assertEqual(separated["label"], "separated")
        self.assertTrue(certificate.verify_certificate(separated))

        channel = certificate.build_certificate(ambiguity.X, A, C)
        self.assertEqual(channel["label"], "channel-limited")
        self.assertTrue(certificate.verify_certificate(channel))

        surviving = certificate.build_certificate(ambiguity.X, A, A)
        self.assertEqual(surviving["label"], "law-surviving")
        self.assertTrue(certificate.verify_certificate(surviving))

    def test_tampering_rejected(self):
        A, C = _qubit()
        good = certificate.build_certificate(ambiguity.X, A, C)
        relabeled = dict(good)
        relabeled["label"] = "separated"
        self.assertFalse(certificate.verify_certificate(relabeled))
        bad_witness = dict(good)
        bad_witness["witness"] = A[0]  # in the family but Tr(X P0) = 0
        self.assertFalse(certificate.verify_certificate(bad_witness))

    def test_wire_roundtrip(self):
        A, C = _qubit()
        cert = certificate.build_certificate(ambiguity.X, A, C)
        wire = certificate.to_wire(cert)
        json.dumps(wire)  # must be JSON-serializable
        self.assertTrue(certificate.verify_wire(wire))
        self.assertEqual(certificate.from_wire(wire)["label"], "channel-limited")


if __name__ == "__main__":
    unittest.main()
