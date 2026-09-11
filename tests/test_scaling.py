import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import unittest

from foc import mathbench, hierarchical, distributed


class TestRicherLifts(unittest.TestCase):
    def test_min_lift_matches_ground_truth(self):
        rows = {r["task"]: r for r in mathbench.benchmark_tasks()}
        self.assertEqual(rows["add"]["min_lift"], "linear")
        self.assertEqual(rows["cube"]["min_lift"], "cubic")
        self.assertEqual(rows["quart"]["min_lift"], "quartic")
        self.assertEqual(rows["div"]["min_lift"], "rational")
        self.assertEqual(rows["modp"]["min_lift"], "none")
        self.assertTrue(all(r["min_lift"] == r["expected_lift"] for r in mathbench.benchmark_tasks()))


class TestHierarchical(unittest.TestCase):
    def test_nesting_adds_and_routes(self):
        rep = hierarchical.benchmark_hierarchy()
        self.assertTrue(rep["nesting_costs_more"])
        self.assertGreaterEqual(rep["nested_router_bits"], rep["flat_router_bits"])
        tree = hierarchical.build_tree(rep["positions"])
        for pos in rep["positions"]:  # each position routes to its own leaf
            self.assertEqual(hierarchical.route(tree, pos), pos)


class TestDistributed(unittest.TestCase):
    def test_serial_certificates_are_json(self):
        certs = distributed.run_serial(["add", "mul"])
        self.assertEqual(certs[0]["min_lift"], "linear")
        self.assertEqual(certs[1]["min_lift"], "quadratic")
        json.dumps(certs)  # certificates must be transportable


if __name__ == "__main__":
    unittest.main()
