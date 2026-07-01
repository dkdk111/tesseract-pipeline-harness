"""Render a tesseract.json trace to the terminal.

Deterministic, standard library only, no model and no keys. Shows the sweep
progression, the self-designed tree annotated by axis, an axis tally, and the
verdict. Works on any tesseract.json written by this harness.
"""

from __future__ import annotations

import json
import sys
from typing import Dict, List

FOUR = ["order", "breadth", "depth", "time"]

AXIS_LABEL = {
    "order": "Order   (1D, line)     serial dependency",
    "breadth": "Breadth (2D, plane)    parallel independence",
    "depth": "Depth   (3D, solid)    recursive nesting",
    "time": "Time    (4D, tesseract) iterative self-evolution",
    "leaf": "Leaf    (0D, point)    work done directly",
}

SWEEP = [
    "point",
    "  sweep along Order   ->  line",
    "  sweep along Breadth ->  plane",
    "  sweep along Depth   ->  solid",
    "  sweep along Time    ->  tesseract",
]


def _banner(title: str) -> str:
    bar = "=" * 68
    return f"{bar}\n{title}\n{bar}"


def _walk(node: dict, depth: int, tally: Dict[str, int], lines: List[str]) -> None:
    axis = node.get("axis", "leaf")
    tally[axis] = tally.get(axis, 0) + 1
    indent = "  " * depth
    geo = node.get("geometry", "point")
    rounds = node.get("rounds", 1)
    round_note = f" x{rounds} rounds" if axis == "time" and rounds and rounds > 1 else ""
    gate = "  <APPROVAL GATE>" if node.get("approval_required") else ""
    lines.append(f"{indent}- [{axis}] {node.get('id', '?')}  ({geo}{round_note}){gate}")
    lines.append(f"{indent}    goal:   {node.get('goal', '').strip()}")
    reason = (node.get("reason") or "").strip()
    if reason:
        lines.append(f"{indent}    reason: {reason}")
    stop = node.get("stop")
    if stop:
        lines.append(f"{indent}    stop:   {stop}")
    for child in node.get("children", []) or []:
        _walk(child, depth + 1, tally, lines)


def render_tree(root: dict) -> str:
    out: List[str] = []
    out.append(_banner("TESSERACT PIPELINE  -  trace render"))
    out.append("")
    out.append(f"goal: {root.get('goal', '').strip()}")
    out.append("")
    out.append("The one operation is sweep. Push a structure along a new orthogonal")
    out.append("axis, take the whole trail as the next structure:")
    out.append("")
    out.extend("    " + s for s in SWEEP)
    out.append("")

    out.append(_banner("Self-design tree (axis chosen per node, by reading the work)"))
    out.append("")
    tally: Dict[str, int] = {}
    tree_lines: List[str] = []
    _walk(root, 0, tally, tree_lines)
    out.extend(tree_lines)
    out.append("")

    out.append(_banner("Axes opened"))
    out.append("")
    opened = []
    for axis in FOUR:
        count = tally.get(axis, 0)
        mark = "OPEN " if count > 0 else "  .  "
        out.append(f"  [{mark}] {AXIS_LABEL[axis]}   x{count}")
        if count > 0:
            opened.append(axis)
    out.append(f"          {AXIS_LABEL['leaf']}   x{tally.get('leaf', 0)}")
    out.append("")

    out.append(_banner("Verdict"))
    out.append("")
    if len(opened) == 4:
        out.append("  All four axes opened. This one task is a full tesseract:")
        out.append("  order, breadth, depth, and time, decided at runtime by reading")
        out.append("  the nature of the work, not by a rule baked in advance.")
        out.append("")
        out.append("  A pipeline is not a line.")
    elif opened:
        out.append(f"  Axes opened: {', '.join(opened)}.")
        out.append("  A correct self-design opens exactly the axes the work needs,")
        out.append("  and no more. Leaving an axis closed is a decision, not a miss.")
    else:
        out.append("  No axis opened: the whole task was a single leaf.")
        out.append("  For a simple goal, one line is the honest structure.")
    out.append("")
    out.append("Note: the structure and its execution are real. If a trace was produced by")
    out.append("the default simulator, its leaf content is placeholder text, not a model's")
    out.append("work. Attach a Worker/LLMWorker for real leaves.")
    out.append("")
    return "\n".join(out)


def render_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return render_tree(json.load(fh))


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m tesseract_pipeline.render <tesseract.json>", file=sys.stderr)
        return 2
    try:
        print(render_file(argv[1]))
    except FileNotFoundError:
        print(f"error: file not found: {argv[1]}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {argv[1]}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
