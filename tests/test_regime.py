import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import regime


class TestRegime(unittest.TestCase):
    def test_routing_is_a_record(self):
        # hard routing (sum of maps) differs from soft routing (recombination)
        r = regime.routing_laws()
        self.assertTrue(r["differ"])

    def test_per_regime_precision_refines_bits(self):
        res = regime.regime_precision([Fraction(1, 4), Fraction(12, 25)])
        bits = [row["bits"] for row in res["per_regime"]]
        self.assertLess(bits[0], bits[1])  # the coarse regime needs fewer bits
        self.assertLess(res["modular_bits"], res["monolithic_bits"])  # modular saves


if __name__ == "__main__":
    unittest.main()
