"""Write the trace: the artifact that makes the four axes visible after a run.

For each run the harness writes, into an output directory:

- ``tesseract.json``  the machine-readable node tree (structure + results).
- ``trace.md``        the human-readable self-design record.
- ``output.md``       the assembled final result.

A run that leaves no trace has reasoned about a tesseract but shown nothing.
"""

from __future__ import annotations

import json
import os
from typing import List

from .axes import Axis, GEOMETRY, MECHANISM
from .box import Box
from .node import Node

_LABEL = {
    Axis.ORDER: "Order",
    Axis.BREADTH: "Breadth",
    Axis.DEPTH: "Depth",
    Axis.TIME: "Time",
    Axis.LEAF: "Leaf",
}


def write_trace(root: Node, goal: str, box: Box, out_dir: str, issues=None) -> dict:
    os.makedirs(out_dir, exist_ok=True)

    tesseract_path = os.path.join(out_dir, "tesseract.json")
    with open(tesseract_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(root.to_dict(), fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    trace_path = os.path.join(out_dir, "trace.md")
    with open(trace_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build_trace_md(root, goal, box, issues))

    output_path = os.path.join(out_dir, "output.md")
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        note = (
            "> Note: the four-axis structure and its execution (ordering, parallelism, "
            "recursion, iteration) are real. The leaf content below is deterministic "
            "placeholder text from the default simulator, not a model's work. Attach a "
            "Worker or LLMWorker for real leaves.\n\n"
        )
        fh.write(note + (root.result or "").strip() + "\n")

    return {
        "tesseract": tesseract_path,
        "trace": trace_path,
        "output": output_path,
        "axes_opened": sorted(a.value for a in root.axes_opened()),
    }


def build_trace_md(root: Node, goal: str, box: Box, issues=None) -> str:
    lines: List[str] = []
    lines.append(f"# Trace: {goal}")
    lines.append("")
    lines.append(f"Goal: {goal}")
    lines.append("")
    lines.append(f"Box in force: {box.summary()}.")
    lines.append("")
    lines.append("## Verify (the structure re-examined before execution)")
    lines.append("")
    if issues:
        lines.append("Issues found:")
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines.append("Passed: no degenerate sweeps, no unjustified nodes, no ambiguous ids.")
    lines.append("")
    lines.append("## The self-design, node by node")
    lines.append("")
    _walk_md(root, 0, lines)
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    opened = sorted((a for a in root.axes_opened()), key=lambda a: list(Axis).index(a))
    names = ", ".join(_LABEL[a] for a in opened) or "none (a single leaf)"
    verdict = _verdict(root.axes_opened())
    lines.append(f"Axes opened: {names}.")
    lines.append("")
    lines.append(verdict)
    lines.append("")
    return "\n".join(lines)


def _walk_md(node: Node, depth: int, lines: List[str]) -> None:
    indent = "  " * depth
    label = _LABEL[node.axis]
    if node.axis == Axis.LEAF and node.approval_required:
        head = f"{indent}- `{node.id}` is a **Leaf held at the approval gate** ({node.geometry})."
    elif node.axis == Axis.LEAF:
        head = f"{indent}- `{node.id}` stayed a **Leaf** ({node.geometry})."
    else:
        rounds = f", {node.rounds} rounds" if node.axis == Axis.TIME else ""
        head = f"{indent}- `{node.id}` opened **{label}** ({node.geometry}{rounds})."
    lines.append(head)
    if node.reason:
        lines.append(f"{indent}  Reason: {node.reason}")
    if node.stop:
        lines.append(f"{indent}  Stop: {node.stop}")
    for child in node.children:
        _walk_md(child, depth + 1, lines)


def _verdict(opened: set) -> str:
    n = len({a for a in opened if a != Axis.LEAF})
    if n == 4:
        return (
            "All four axes opened. This one task is a full tesseract: order, breadth, "
            "depth, and time, decided at runtime by reading the nature of the work, "
            "not by a rule baked in advance. A pipeline is not a line."
        )
    if n == 0:
        return "No axis opened: the task was a single leaf. For a simple goal, one line is the honest structure."
    return (
        "A correct self-design opens exactly the axes the work needs, and no more. "
        "Leaving an axis closed is a decision, not a miss."
    )
