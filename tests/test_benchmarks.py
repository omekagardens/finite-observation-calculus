import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fractions import Fraction

from foc import mathbench, nested, longsession


class TestMathBench(unittest.TestCase):
    def test_ladder_matches_the_dichotomy(self):
        rows = {r["task"]: r for r in mathbench.benchmark_tasks()}
        self.assertEqual(rows["add"]["verdict"], "separated")
        self.assertEqual(rows["mul"]["verdict"], "channel-limited")
        self.assertEqual(rows["square"]["verdict"], "channel-limited")
        self.assertEqual(rows["modp"]["verdict"], "law-surviving")
        self.assertTrue(all(r["verdict"] == r["expected"] for r in mathbench.benchmark_tasks()))

    def test_exact_fits(self):
        self.assertEqual(mathbench.fit("mul", "quadratic")["loss"], Fraction(0))
        self.assertNotEqual(mathbench.fit("modp", "quadratic")["loss"], Fraction(0))


class TestNested(unittest.TestCase):
    def test_ceil_log2(self):
        self.assertEqual(nested.ceil_log2(Fraction(1, 2)), 0)   # 2^0 = 1 >= 1/2
        self.assertEqual(nested.ceil_log2(Fraction(20)), 5)     # 2^4=16 < 20 <= 32
        self.assertEqual(nested.ceil_log2(Fraction(1)), 0)

    def test_nesting_adds_and_modularity_saves(self):
        rep = nested.benchmark_regimes()
        self.assertGreaterEqual(rep["nested_router_bits"], rep["flat_router_bits"])
        self.assertLess(rep["modular_bits"], rep["monolithic_bits"])
        self.assertEqual(rep["parallel_speedup"], 4)

    def test_bits_vs_steps_is_logarithmic(self):
        self.assertEqual(nested.bits_vs_steps(1), 1)
        self.assertEqual(nested.bits_vs_steps(1024), 11)   # 1 + 10
        self.assertLess(nested.bits_vs_steps(4096) - nested.bits_vs_steps(1024), 3)


class TestLongSession(unittest.TestCase):
    def test_bits_bounded_and_loss_falls(self):
        rep = longsession.benchmark_long_session(steps=6, grid=64)
        self.assertLessEqual(rep["max_bits"], 8)                    # bounded, not growing
        self.assertLess(rep["loss_last"], rep["loss_first"])        # training works
        self.assertEqual(rep["projected_bits"], nested.bits_vs_steps(6))


if __name__ == "__main__":
    unittest.main()
