"""A node in a self-designed structure.

Each node records the decision made at one point: which axis it opened (or LEAF),
why (the honest reading of the work's nature), the stop condition that closed it,
and, after execution, the result it produced.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import List, Optional

from .axes import Axis, GEOMETRY


@dataclass
class Node:
    id: str
    goal: str
    axis: Axis = Axis.LEAF
    reason: str = ""
    stop: Optional[str] = None
    rounds: int = 1
    approval_required: bool = False
    children: List["Node"] = field(default_factory=list)
    result: Optional[str] = None

    @property
    def geometry(self) -> str:
        return GEOMETRY[self.axis]

    def clone(self) -> "Node":
        """Deep copy with results cleared, for re-running a subtree in a new round."""
        fresh = copy.deepcopy(self)
        fresh._clear_results()
        return fresh

    def _clear_results(self) -> None:
        self.result = None
        for child in self.children:
            child._clear_results()

    def axes_opened(self) -> set:
        """The set of sweepable axes that appear anywhere in this subtree."""
        found = set()
        if self.axis in (Axis.ORDER, Axis.BREADTH, Axis.DEPTH, Axis.TIME):
            found.add(self.axis)
        for child in self.children:
            found |= child.axes_opened()
        return found

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "axis": self.axis.value,
            "reason": self.reason,
            "geometry": self.geometry,
            "stop": self.stop,
            "rounds": self.rounds,
            "approval_required": self.approval_required,
            "result": self.result,
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        return cls(
            id=data.get("id", "?"),
            goal=data.get("goal", ""),
            axis=Axis(data.get("axis", "leaf")),
            reason=data.get("reason", ""),
            stop=data.get("stop"),
            rounds=int(data.get("rounds", 1)),
            approval_required=bool(data.get("approval_required", False)),
            result=data.get("result"),
            children=[cls.from_dict(c) for c in data.get("children", [])],
        )
