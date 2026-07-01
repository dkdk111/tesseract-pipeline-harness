"""Tesseract Pipeline: a working harness that self-designs a task along four
orthogonal axes (order, breadth, depth, time), unified by the single sweep
operation, inside a human-held box, and records a trace that makes the four
dimensions visible.

Companion implementation to the book *Tesseract Pipeline* by DK.

Two ways to run it:

- Engine mode (this package): describe a task's nature, and the planner derives
  the four-axis structure and the executor actually runs it (real parallelism,
  recursion, and iteration rounds) with a pluggable worker. The default worker is
  a deterministic simulator, so it runs with no model and no API keys.
- Agent mode (AGENTS.md / CLAUDE.md): point a coding agent at the repository and it
  self-designs and executes free-form tasks against the same ontology and box.
"""

from .axes import Axis, GEOMETRY, FOUR_AXES
from .box import Box
from .node import Node
from .planner import plan
from .executor import Executor
from .worker import Worker, SimulatedWorker
from .infer import infer_task, HeuristicPlanner
from .verify import verify_structure

__version__ = "0.2.0"

__all__ = [
    "Axis",
    "GEOMETRY",
    "FOUR_AXES",
    "Box",
    "Node",
    "plan",
    "Executor",
    "Worker",
    "SimulatedWorker",
    "infer_task",
    "HeuristicPlanner",
    "verify_structure",
    "__version__",
]
