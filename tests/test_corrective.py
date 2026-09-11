import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest

from foc import corrective


class TestCorrective(unittest.TestCase):
    def test_localization(self):
        rep = corrective.corrective_report()
        # the annihilator filter blames the node that can see the feature
        self.assertEqual(rep["localize_2body"], ["pairs"])
        self.assertEqual(rep["localize_1body"], ["local"])
        # edge blame follows what the failing downstream reads
        self.assertEqual(rep["blame_Z"], ["overlapping"])
        self.assertEqual(rep["blame_I"], [])

    def test_correction_re_certifies(self):
        c = corrective.corrective_report()["correction"]
        self.assertTrue(c["refinement_safe"])
        self.assertLessEqual(c["annihilator_after"], c["annihilator_before"])
        self.assertEqual(c["annihilator_after"], 8)
        self.assertTrue(c["accepted"])


if __name__ == "__main__":
    unittest.main()
