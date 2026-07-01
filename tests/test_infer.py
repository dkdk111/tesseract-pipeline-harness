"""Free-form inference: a plain-English goal, with no axis declared, becomes a
four-axis structure. This is the real self-design path (heuristic, keyless)."""

import unittest

from tesseract_pipeline import Axis, Executor, infer_task, plan


def _axes(text):
    root = plan(infer_task(text))
    Executor().run(root)
    return root.axes_opened()


class InferTests(unittest.TestCase):
    def test_full_sentence_opens_all_four_axes(self):
        text = (
            "Research the space, then gather notes on Notion, Obsidian and Roam, then "
            "break the market down into pricing, features and positioning, then write "
            "the brief, and iterate twice."
        )
        self.assertEqual(
            _axes(text),
            {Axis.ORDER, Axis.BREADTH, Axis.DEPTH, Axis.TIME},
            "a single declared-nothing sentence should self-design a full tesseract",
        )

    def test_iteration_detected(self):
        self.assertTrue(infer_task("polish the essay, iterate twice").get("iterative"))
        self.assertEqual(infer_task("draft it in 3 rounds").get("rounds"), 3)
        self.assertTrue(infer_task("refine the plan").get("iterative"))

    def test_then_makes_a_sequence(self):
        task = infer_task("collect data then analyze it then report")
        self.assertIn("sequence", task)
        self.assertGreaterEqual(len(task["sequence"]), 3)

    def test_list_makes_breadth(self):
        task = infer_task("summarize sources on alpha, beta and gamma")
        self.assertIn("parallel", task)
        self.assertEqual(len(task["parallel"]), 3)

    def test_breakdown_makes_depth(self):
        task = infer_task("break the system down into frontend, backend and data")
        self.assertTrue(task.get("oversized"))
        self.assertEqual(len(task["parts"]), 3)

    def test_plain_goal_is_a_leaf(self):
        task = infer_task("fix the header alignment")
        for key in ("sequence", "parallel", "oversized", "iterative"):
            self.assertNotIn(key, task)


if __name__ == "__main__":
    unittest.main()
