"""The Verify wall catches degenerate and unjustified structures, and passes honest
ones."""

import glob
import json
import os
import unittest

from tesseract_pipeline import Axis, Box, Node, plan, verify_structure

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class VerifyPassTests(unittest.TestCase):
    def test_shipped_examples_pass_verify(self):
        box = Box.load(os.path.join(_REPO_ROOT, "box.config.json"))
        for path in sorted(glob.glob(os.path.join(_REPO_ROOT, "examples", "*", "task.json"))):
            with open(path, "r", encoding="utf-8") as fh:
                task = json.load(fh)
            root = plan(task, box)
            issues = verify_structure(root, box)
            with self.subTest(example=os.path.basename(os.path.dirname(path))):
                self.assertEqual(issues, [], f"unexpected verify issues: {issues}")


class VerifyCatchTests(unittest.TestCase):
    def test_degenerate_order_sweep(self):
        node = Node(
            id="seq", goal="g", axis=Axis.ORDER, reason="r",
            children=[Node(id="only", goal="x", axis=Axis.LEAF, reason="r")],
        )
        issues = verify_structure(node)
        self.assertTrue(any("order sweep has 1 child" in i for i in issues))

    def test_single_round_time(self):
        body = Node(id="b", goal="b", axis=Axis.LEAF, reason="r")
        node = Node(id="t", goal="g", axis=Axis.TIME, reason="r", rounds=1, children=[body])
        issues = verify_structure(node)
        self.assertTrue(any("still photo" in i for i in issues))

    def test_leaf_with_children(self):
        node = Node(
            id="leaf", goal="g", axis=Axis.LEAF, reason="r",
            children=[Node(id="c", goal="c", axis=Axis.LEAF, reason="r")],
        )
        issues = verify_structure(node)
        self.assertTrue(any("leaf has" in i for i in issues))

    def test_missing_reason(self):
        node = Node(id="n", goal="g", axis=Axis.LEAF, reason="")
        issues = verify_structure(node)
        self.assertTrue(any("no reason" in i for i in issues))

    def test_approval_on_non_leaf(self):
        node = Node(
            id="p", goal="g", axis=Axis.BREADTH, reason="r", approval_required=True,
            children=[Node(id="a", goal="a", axis=Axis.LEAF, reason="r"),
                      Node(id="b", goal="b", axis=Axis.LEAF, reason="r")],
        )
        issues = verify_structure(node)
        self.assertTrue(any("approval gate on a non-leaf" in i for i in issues))


if __name__ == "__main__":
    unittest.main()
