"""The executor: actually run a self-designed structure.

This is not a description of the four axes. It is their execution:

- Order   runs children sequentially, threading each result into the next.
- Breadth runs children concurrently in a thread pool (real parallelism).
- Depth   recurses into a nested structure and composes the parts.
- Time    re-runs the whole subtree in rounds, feeding each round's review into the
          next, and stops on max_rounds, a dry round, or convergence.

At a leaf, the pluggable worker does the work. The executor writes each node's
produced result back onto the node, so the trace records real output, not a promise.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import List

from .axes import Axis
from .node import Node
from .worker import Worker, SimulatedWorker

_MAX_THREADS = 8


class Executor:
    def __init__(self, worker: Worker = None):
        self.worker = worker or SimulatedWorker()

    def run(self, node: Node, context: str = "") -> str:
        if node.axis == Axis.LEAF:
            if node.approval_required:
                # The approval gate above the three walls: high-risk, irreversible, or
                # outside-the-repo actions are never executed autonomously.
                node.result = (
                    f"[HELD FOR HUMAN APPROVAL] {node.goal}\n"
                    "- Not self-designed or executed by the harness.\n"
                    "- A human must approve this action before it runs."
                )
                return node.result
            node.result = self.worker.run(node.goal, context)
            return node.result
        if node.axis == Axis.ORDER:
            return self._run_order(node, context)
        if node.axis == Axis.BREADTH:
            return self._run_breadth(node, context)
        if node.axis == Axis.DEPTH:
            return self._run_depth(node, context)
        if node.axis == Axis.TIME:
            return self._run_time(node, context)
        raise ValueError(f"unknown axis: {node.axis}")

    # -- Order: serial, dependency-threaded -------------------------------------
    def _run_order(self, node: Node, context: str) -> str:
        ctx = context
        parts: List[str] = []
        for child in node.children:
            result = self.run(child, ctx)
            parts.append(result)
            # Each step's output becomes context for the next: a real dependency.
            ctx = (ctx + "\n\n" + result).strip()
        node.result = _assemble(node.goal, parts)
        return node.result

    # -- Breadth: independent, concurrent ---------------------------------------
    def _run_breadth(self, node: Node, context: str) -> str:
        children = node.children
        if not children:
            node.result = ""
            return node.result
        workers = min(len(children), _MAX_THREADS)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(lambda c: self.run(c, context), children))
        node.result = _assemble(node.goal, results)
        return node.result

    # -- Depth: recursive nesting -----------------------------------------------
    def _run_depth(self, node: Node, context: str) -> str:
        results = [self.run(child, context) for child in node.children]
        node.result = _assemble(node.goal, results)
        return node.result

    # -- Time: iterative rounds -------------------------------------------------
    def _run_time(self, node: Node, context: str) -> str:
        # Two real stop conditions, both reachable: convergence (a round adds no
        # improvement over the last) and the round limit. A round's review is fed
        # forward into the next round's context, so later rounds build on earlier
        # ones until they stop improving.
        body = node.children[0]
        target = max(1, node.rounds)
        prev_result = ""
        prev_score = None
        review = ""
        rounds_run = 0
        final_body = None
        stop = None

        for i in range(1, target + 1):
            fresh = body.clone()
            round_ctx = (context + "\n\n" + review).strip()
            result = self.run(fresh, round_ctx)
            score = _score(result)

            if prev_score is not None and score <= prev_score:
                # This round added nothing over the last: the loop has converged.
                stop = f"converged after round {rounds_run} (round {i} added no improvement)"
                break

            rounds_run = i
            final_body = fresh
            prev_result = result
            prev_score = score
            review = f"a review of round {i} that flags gaps to fill in the next pass"

        if stop is None:
            stop = f"reached the round limit ({target} rounds)"

        node.children = [final_body] if final_body is not None else node.children
        node.rounds = rounds_run
        node.stop = stop
        node.result = prev_result
        return node.result


def _assemble(goal: str, parts: List[str]) -> str:
    body = "\n\n".join(p for p in parts if p and p.strip())
    return f"## {goal}\n\n{body}".strip()


def _score(result: str) -> int:
    """A deterministic proxy for how complete a result is."""
    return len(result)
