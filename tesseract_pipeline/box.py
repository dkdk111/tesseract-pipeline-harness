"""The box: the walls a human draws around the model's self-design.

The agent chooses which axes to open. The human chooses how far each may go and
which actions require approval. Control is not the opposite of autonomy; it is its
precondition. The clearer the walls, the more freely the agent can design inside
them.

The canonical, machine-readable box is ``box.config.json`` at the repository root.
``harness/box.config.md`` is the prose that documents it.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List

from .axes import Axis, FOUR_AXES

DEFAULTS = {
    "allowed_axes": ["order", "breadth", "depth", "time"],
    "max_depth": 3,
    "max_breadth": 6,
    "max_rounds": 3,
    "approval_required": [
        "moving money, purchases, payments",
        "sending messages, emails, or publishing externally",
        "deleting or overwriting files outside .tesseract/",
        "network calls with side effects",
        "any irreversible change",
    ],
}


@dataclass
class Box:
    allowed_axes: List[str] = field(default_factory=lambda: list(DEFAULTS["allowed_axes"]))
    max_depth: int = DEFAULTS["max_depth"]
    max_breadth: int = DEFAULTS["max_breadth"]
    max_rounds: int = DEFAULTS["max_rounds"]
    approval_required: List[str] = field(default_factory=lambda: list(DEFAULTS["approval_required"]))

    @classmethod
    def load(cls, path: str = "box.config.json") -> "Box":
        """Load the box from JSON, falling back to defaults for any missing field."""
        data = dict(DEFAULTS)
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                data.update(json.load(fh))
        return cls(
            allowed_axes=list(data["allowed_axes"]),
            max_depth=int(data["max_depth"]),
            max_breadth=int(data["max_breadth"]),
            max_rounds=int(data["max_rounds"]),
            approval_required=list(data["approval_required"]),
        )

    def allows(self, axis: Axis) -> bool:
        return axis.value in self.allowed_axes

    def summary(self) -> str:
        allowed = ", ".join(a for a in ("order", "breadth", "depth", "time") if a in self.allowed_axes)
        return (
            f"allowed axes: {allowed} | "
            f"max_depth {self.max_depth} | max_breadth {self.max_breadth} | "
            f"max_rounds {self.max_rounds}"
        )
