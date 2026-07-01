"""The executor really runs the four axes. These tests pin the execution semantics:
order threads context forward, breadth runs every branch, depth recurses, time runs
rounds."""

import unittest

from tesseract_pipeline import Axis, Executor, Node
from tesseract_pipeline.worker import Worker


class RecordingWorker(Worker):
    """Records the context each leaf saw, and echoes the goal."""

    def __init__(self):
        self.seen = {}

    def run(self, goal, context=""):
        self.seen[goal] = context
        return f"[{goal}]"


class ExecutorTests(unittest.TestCase):
    def test_leaf_calls_worker(self):
        worker = RecordingWorker()
        node = Node(id="n", goal="do it", axis=Axis.LEAF)
        result = Executor(worker).run(node)
        self.assertEqual(result, "[do it]")
        self.assertEqual(node.result, "[do it]")

    def test_order_threads_context_forward(self):
        worker = RecordingWorker()
        node = Node(
            id="seq",
            goal="pipeline",
            axis=Axis.ORDER,
            children=[
                Node(id="a", goal="first", axis=Axis.LEAF),
                Node(id="b", goal="second", axis=Axis.LEAF),
            ],
        )
        Executor(worker).run(node)
        # The second step must have seen the first step's output in its context.
        self.assertEqual(worker.seen["first"], "")
        self.assertIn("[first]", worker.seen["second"])

    def test_breadth_runs_every_branch(self):
        worker = RecordingWorker()
        node = Node(
            id="par",
            goal="fan",
            axis=Axis.BREADTH,
            children=[Node(id=str(i), goal=f"g{i}", axis=Axis.LEAF) for i in range(4)],
        )
        Executor(worker).run(node)
        self.assertEqual(len(worker.seen), 4)

    def test_depth_recurses(self):
        worker = RecordingWorker()
        seed = Node(
            id="seed",
            goal="big",
            axis=Axis.DEPTH,
            children=[Node(id="p", goal="part", axis=Axis.LEAF)],
        )
        result = Executor(worker).run(seed)
        self.assertIn("[part]", result)

    def test_time_runs_to_limit_when_each_round_improves(self):
        # A worker whose output grows with context keeps improving, so the loop runs
        # to the round limit.
        class GrowingWorker(Worker):
            def run(self, goal, context=""):
                return f"[{goal}]" + ("+" * (len(context) + 1))

        body = Node(id="body", goal="draft", axis=Axis.LEAF)
        node = Node(id="loop", goal="iterate", axis=Axis.TIME, rounds=2, children=[body])
        Executor(GrowingWorker()).run(node)
        self.assertEqual(node.rounds, 2)
        self.assertIn("round limit", node.stop)

    def test_time_converges_when_no_improvement(self):
        # A worker whose output does not change across rounds converges immediately.
        worker = RecordingWorker()
        body = Node(id="body", goal="draft", axis=Axis.LEAF)
        node = Node(id="loop", goal="iterate", axis=Axis.TIME, rounds=3, children=[body])
        Executor(worker).run(node)
        self.assertEqual(node.rounds, 1)
        self.assertIn("converged", node.stop)


if __name__ == "__main__":
    unittest.main()
