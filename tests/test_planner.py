"""The planner reads declared nature and derives the four-axis structure, enforcing
the box. These tests pin the four questions and the box walls."""

import unittest

from tesseract_pipeline import Axis, Box, plan


class PlannerAxisTests(unittest.TestCase):
    def test_iterative_opens_time(self):
        node = plan({"goal": "g", "iterative": True, "rounds": 2})
        self.assertEqual(node.axis, Axis.TIME)
        self.assertEqual(node.rounds, 2)
        self.assertEqual(len(node.children), 1)

    def test_sequence_opens_order(self):
        node = plan({"goal": "g", "sequence": [{"goal": "a"}, {"goal": "b"}]})
        self.assertEqual(node.axis, Axis.ORDER)
        self.assertEqual([c.axis for c in node.children], [Axis.LEAF, Axis.LEAF])

    def test_parallel_opens_breadth(self):
        node = plan({"goal": "g", "parallel": [{"goal": "a"}, {"goal": "b"}]})
        self.assertEqual(node.axis, Axis.BREADTH)
        self.assertEqual(len(node.children), 2)

    def test_oversized_opens_depth(self):
        node = plan({"goal": "g", "oversized": True, "parts": [{"goal": "a"}, {"goal": "b"}]})
        self.assertEqual(node.axis, Axis.DEPTH)

    def test_plain_goal_is_leaf(self):
        node = plan({"goal": "g"})
        self.assertEqual(node.axis, Axis.LEAF)
        self.assertEqual(node.children, [])

    def test_one_node_opens_one_axis(self):
        # iterative + sequence: time opens here, order opens in the child body.
        node = plan({"goal": "g", "iterative": True, "sequence": [{"goal": "a"}]})
        self.assertEqual(node.axis, Axis.TIME)
        self.assertEqual(node.children[0].axis, Axis.ORDER)


class PlannerBoxTests(unittest.TestCase):
    def test_max_breadth_caps_and_reports(self):
        box = Box(max_breadth=2)
        node = plan({"goal": "g", "parallel": [{"goal": str(i)} for i in range(5)]}, box)
        self.assertEqual(len(node.children), 2)
        self.assertIn("capped", node.stop)

    def test_max_depth_forces_leaf(self):
        box = Box(max_depth=1)
        task = {
            "goal": "g",
            "oversized": True,
            "parts": [
                {"goal": "child", "oversized": True, "parts": [{"goal": "grandchild"}]}
            ],
        }
        root = plan(task, box)
        self.assertEqual(root.axis, Axis.DEPTH)
        forced = root.children[0]
        self.assertEqual(forced.axis, Axis.LEAF)
        self.assertIn("max_depth", forced.stop)

    def test_rounds_capped_by_box(self):
        box = Box(max_rounds=2)
        node = plan({"goal": "g", "iterative": True, "rounds": 9}, box)
        self.assertEqual(node.rounds, 2)

    def test_forbidden_axis_falls_back(self):
        box = Box(allowed_axes=["order", "depth", "time"])  # breadth forbidden
        node = plan({"goal": "g", "parallel": [{"goal": "a"}, {"goal": "b"}]}, box)
        self.assertEqual(node.axis, Axis.LEAF)


if __name__ == "__main__":
    unittest.main()
