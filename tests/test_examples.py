"""Every shipped example plans and executes, and the special demos (approval gate,
breadth cap, single leaf) behave as advertised."""

import glob
import json
import os
import unittest

from tesseract_pipeline import Axis, Box, Executor, plan
from tesseract_pipeline.cli import main as cli_main

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXAMPLES = sorted(glob.glob(os.path.join(_REPO_ROOT, "examples", "*", "task.json")))


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _run(task):
    box = Box.load(os.path.join(_REPO_ROOT, "box.config.json"))
    root = plan(task, box)
    Executor().run(root)
    return root


def _find(node, predicate):
    if predicate(node):
        return node
    for child in node.children:
        hit = _find(child, predicate)
        if hit is not None:
            return hit
    return None


class ExampleSuiteTests(unittest.TestCase):
    def test_there_are_several_examples(self):
        self.assertGreaterEqual(len(_EXAMPLES), 6, "expected a diverse gallery")

    def test_every_example_runs_and_produces_output(self):
        for path in _EXAMPLES:
            with self.subTest(example=os.path.basename(os.path.dirname(path))):
                root = _run(_load(path))
                self.assertTrue((root.result or "").strip(), "example produced no output")

    def test_gallery_command_runs(self):
        self.assertEqual(cli_main(["gallery"]), 0)


class SpecialCaseTests(unittest.TestCase):
    def _example(self, name):
        return _load(os.path.join(_REPO_ROOT, "examples", name, "task.json"))

    def test_software_release_holds_deploy_at_approval_gate(self):
        root = _run(self._example("02_software_release"))
        deploy = _find(root, lambda n: n.approval_required)
        self.assertIsNotNone(deploy, "deploy should be marked approval-required")
        self.assertEqual(deploy.axis, Axis.LEAF)
        self.assertIn("HELD FOR HUMAN APPROVAL", deploy.result)

    def test_bulk_translation_hits_breadth_wall(self):
        root = _run(self._example("05_bulk_translation"))
        self.assertEqual(root.axis, Axis.BREADTH)
        self.assertEqual(len(root.children), 6)  # capped from 8 by max_breadth
        self.assertIn("capped", root.stop)

    def test_quick_fix_is_a_single_leaf(self):
        root = _run(self._example("06_quick_fix"))
        self.assertEqual(root.axis, Axis.LEAF)
        self.assertEqual(root.children, [])
        self.assertEqual(root.axes_opened(), set())

    def test_data_pipeline_opens_depth_but_not_time(self):
        root = _run(self._example("03_data_pipeline"))
        opened = root.axes_opened()
        self.assertIn(Axis.DEPTH, opened)
        self.assertNotIn(Axis.TIME, opened)


if __name__ == "__main__":
    unittest.main()
