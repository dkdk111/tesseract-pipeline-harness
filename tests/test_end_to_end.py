"""End to end: the bundled example task opens all four axes and produces a trace and
an output, with no keys."""

import json
import os
import tempfile
import unittest

from tesseract_pipeline import Axis, Box, Executor, plan
from tesseract_pipeline.trace import write_trace

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TASK = os.path.join(_REPO_ROOT, "examples", "01_market_brief", "task.json")


class EndToEndTests(unittest.TestCase):
    def setUp(self):
        with open(_TASK, "r", encoding="utf-8") as fh:
            self.task = json.load(fh)
        self.box = Box.load(os.path.join(_REPO_ROOT, "box.config.json"))

    def test_example_opens_all_four_axes(self):
        root = plan(self.task, self.box)
        Executor().run(root)
        opened = root.axes_opened()
        self.assertEqual(
            opened,
            {Axis.ORDER, Axis.BREADTH, Axis.DEPTH, Axis.TIME},
            "the example task should open every axis",
        )

    def test_run_is_deterministic(self):
        root_a = plan(self.task, self.box)
        Executor().run(root_a)
        root_b = plan(self.task, self.box)
        Executor().run(root_b)
        self.assertEqual(root_a.to_dict(), root_b.to_dict())

    def test_trace_files_written_and_output_nonempty(self):
        root = plan(self.task, self.box)
        Executor().run(root)
        with tempfile.TemporaryDirectory() as tmp:
            info = write_trace(root, self.task["goal"], self.box, tmp)
            for key in ("tesseract", "trace", "output"):
                self.assertTrue(os.path.exists(info[key]), f"{key} not written")
            with open(info["output"], "r", encoding="utf-8") as fh:
                self.assertGreater(len(fh.read().strip()), 0)
            self.assertEqual(info["axes_opened"], ["breadth", "depth", "order", "time"])


if __name__ == "__main__":
    unittest.main()
