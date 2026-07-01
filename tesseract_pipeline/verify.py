"""The Verify wall: re-examine a proposed structure before executing it.

A structure the planner proposes is a hypothesis, not a fact. The book's third
control wall is verification: re-examine the structure itself, adversarially, before
building leaf work on top of it. This module implements that wall as a set of
structural-honesty checks. It does not judge the content (that needs a model); it
catches degenerate and dishonest shapes that the ontology forbids.

Checks:

- A node with no reason (structure proposed without justification).
- A degenerate sweep: order, breadth, or depth with fewer than two children. A sweep
  shorter than two raises no real dimension (a plane with one branch is a line).
- A degenerate time sweep: fewer than two rounds (a single round is a still photo,
  not a tesseract), or not wrapping exactly one body.
- A leaf with children (a leaf does no sweeping).
- An approval gate on a non-leaf (approval applies to atomic actions).
- Duplicate sibling ids (an ambiguous trace).

`verify_structure` returns a list of human-readable issues. An empty list means the
structure passed. Callers may warn and proceed, or refuse in strict mode.
"""

from __future__ import annotations

from typing import List, Optional

from .axes import Axis
from .box import Box
from .node import Node


def verify_structure(root: Node, box: Optional[Box] = None) -> List[str]:
    issues: List[str] = []
    _walk(root, issues)
    return issues


def _walk(node: Node, issues: List[str]) -> None:
    axis = node.axis
    n = len(node.children)

    if not (node.reason or "").strip():
        issues.append(f"{node.id}: node has no reason (a structure proposed without justification)")

    if axis in (Axis.ORDER, Axis.BREADTH, Axis.DEPTH) and n < 2:
        issues.append(
            f"{node.id}: {axis.value} sweep has {n} child; a sweep shorter than two "
            "raises no real dimension, so this should collapse to a leaf"
        )

    if axis == Axis.TIME:
        if node.rounds < 2:
            issues.append(
                f"{node.id}: time sweep runs {node.rounds} round; a single round is a "
                "still photo, not a tesseract"
            )
        if n != 1:
            issues.append(f"{node.id}: a time node should wrap exactly one body, but has {n}")

    if axis == Axis.LEAF and n > 0:
        issues.append(f"{node.id}: leaf has {n} child(ren); a leaf does no sweeping")

    if node.approval_required and axis != Axis.LEAF:
        issues.append(
            f"{node.id}: approval gate on a non-leaf; approval applies to atomic actions, not sweeps"
        )

    child_ids = [c.id for c in node.children]
    for dup in sorted({i for i in child_ids if child_ids.count(i) > 1}):
        issues.append(f"{node.id}: duplicate child id '{dup}' (an ambiguous trace)")

    for child in node.children:
        _walk(child, issues)
