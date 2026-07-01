"""Self-design: derive a four-axis structure by reading the nature of the work.

You describe a task's nature; the planner asks the four questions and derives the
structure, enforcing the box. The task does not name an axis. It declares
properties of the work (dependency, independence, oversized parts, iteration), and
the planner decides the axis. That decision, computed rather than hand-drawn, is
the self-design step the book describes.

The four questions, in order (the first that fits, and the box allows, wins):

    1. iterative        -> Time     (one pass is not enough; run in rounds)
    2. sequence[]       -> Order    (each step consumes the previous step's output)
    3. parallel[]       -> Breadth  (independent branches, run at once)
    4. oversized+parts  -> Depth    (too big to swallow whole; a seed, not a leaf)
    else                -> Leaf     (small enough for one pass)

A single node opens at most one axis (one sweep, one local move). When a unit
declares more than one property, the outermost axis opens here and the rest open in
the child, exactly as the book's local, recursive, incremental decision requires.
"""

from __future__ import annotations

import re
from typing import Optional

from .axes import Axis
from .box import Box
from .node import Node


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "node"


def _unit_id(unit: dict, fallback: str) -> str:
    return unit.get("id") or slugify(unit.get("goal", fallback))


def plan(task: dict, box: Optional[Box] = None, depth: int = 0, node_id: str = "root") -> Node:
    """Read the task's declared nature and return the self-designed Node tree."""
    box = box or Box()
    goal = task.get("goal", "")

    # Question 1: is one pass enough? If not, sweep Time.
    if task.get("iterative") and box.allows(Axis.TIME):
        rounds = min(int(task.get("rounds", box.max_rounds)), box.max_rounds)
        body = {k: v for k, v in task.items() if k not in ("iterative", "rounds", "id")}
        child = plan(body, box, depth, f"{node_id}-round")
        return Node(
            id=node_id,
            goal=goal,
            axis=Axis.TIME,
            rounds=rounds,
            reason=(
                "One pass is not enough: the result of a pass feeds the next. "
                "Sweep time and run the whole structure in revision rounds."
            ),
            stop=f"stops at {rounds} rounds, on a dry round, or on convergence",
            children=[child],
        )

    # Question 2: is there front-to-back dependency? If so, sweep Order.
    if task.get("sequence") and box.allows(Axis.ORDER):
        steps = task["sequence"]
        children = [
            plan(u, box, depth, _unit_id(u, f"{node_id}-{i}"))
            for i, u in enumerate(steps)
        ]
        return Node(
            id=node_id,
            goal=goal,
            axis=Axis.ORDER,
            reason=(
                "Front-to-back dependency: each step consumes the previous step's "
                "output. Sweep order and lay the steps on a line."
            ),
            stop="closes when the last dependent step completes",
            children=children,
        )

    # Question 3: do independent branches split off? If so, sweep Breadth.
    if task.get("parallel") and box.allows(Axis.BREADTH):
        units = list(task["parallel"])
        dropped = 0
        if len(units) > box.max_breadth:
            dropped = len(units) - box.max_breadth
            units = units[: box.max_breadth]
        children = [plan(u, box, depth, _unit_id(u, f"{node_id}-b{i}")) for i, u in enumerate(units)]
        if dropped:
            stop = f"capped at max_breadth {box.max_breadth}; {dropped} branch(es) queued, not dropped silently"
        else:
            stop = f"{len(children)} branches, under max_breadth {box.max_breadth}"
        return Node(
            id=node_id,
            goal=goal,
            axis=Axis.BREADTH,
            reason=(
                "The branches are independent and do not wait on one another. "
                "Sweep breadth and fan them out in parallel."
            ),
            stop=stop,
            children=children,
        )

    # Question 4: is this too big to handle in one pass? If so, sweep Depth.
    if task.get("oversized") and task.get("parts"):
        if depth >= box.max_depth or not box.allows(Axis.DEPTH):
            return Node(
                id=node_id,
                goal=goal,
                axis=Axis.LEAF,
                reason=(
                    "The work would open depth, but the box's max_depth is reached. "
                    "Forced to a leaf: the Stop wall closes the sweep."
                ),
                stop=f"max_depth {box.max_depth} reached",
            )
        parts = task["parts"]
        children = [plan(u, box, depth + 1, _unit_id(u, f"{node_id}-p{i}")) for i, u in enumerate(parts)]
        return Node(
            id=node_id,
            goal=goal,
            axis=Axis.DEPTH,
            reason=(
                "This node is too large to handle in one pass, so it is a seed, not "
                "a leaf. Sweep depth and open a smaller structure of its own in place."
            ),
            stop=f"depth {depth + 1}, under max_depth {box.max_depth}",
            children=children,
        )

    # None of the four fit: it is a leaf. Leaving it a leaf is a real decision.
    return Node(
        id=node_id,
        goal=goal,
        axis=Axis.LEAF,
        reason="Small enough to handle in one pass; leaving it a leaf is the honest decision.",
    )
