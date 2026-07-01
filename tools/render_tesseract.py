#!/usr/bin/env python3
"""Render a Tesseract Pipeline trace.

Reads a tesseract.json trace (see harness/03_trace_protocol.md) and prints the
sweep progression, the task tree annotated by axis, an axis tally, and the verdict.

Deterministic, standard library only, no model and no API keys. This is the
"complete simulation" the harness ships: the live model is whatever coding agent
you attach; this renderer shows the four axes from a recorded run alone.

Usage:
    python tools/render_tesseract.py examples/01_market_brief/tesseract.json
"""

import json
import sys

AXES = ["order", "breadth", "depth", "time"]

GEOMETRY_OF_AXIS = {
    "order": "line",
    "breadth": "plane",
    "depth": "solid",
    "time": "tesseract",
    "leaf": "point",
}

AXIS_LABEL = {
    "order": "Order   (1D, line)     serial dependency",
    "breadth": "Breadth (2D, plane)    parallel independence",
    "depth": "Depth   (3D, solid)    recursive nesting",
    "time": "Time    (4D, tesseract) iterative self-evolution",
    "leaf": "Leaf    (0D, point)    work done directly",
}

SWEEP_PROGRESSION = [
    "point",
    "  sweep along Order   ->  line",
    "  sweep along Breadth ->  plane",
    "  sweep along Depth   ->  solid",
    "  sweep along Time    ->  tesseract",
]


def banner(title):
    line = "=" * 68
    return f"{line}\n{title}\n{line}"


def walk(node, depth, tally, lines):
    axis = node.get("axis", "leaf")
    tally[axis] = tally.get(axis, 0) + 1
    indent = "  " * depth
    geo = node.get("geometry", GEOMETRY_OF_AXIS.get(axis, "point"))
    rounds = node.get("rounds", 1)
    round_note = f" x{rounds} rounds" if axis == "time" and rounds and rounds > 1 else ""
    head = f"{indent}- [{axis}] {node.get('id', '?')}  ({geo}{round_note})"
    lines.append(head)
    lines.append(f"{indent}    goal:   {node.get('goal', '').strip()}")
    reason = node.get("reason", "").strip()
    if reason:
        lines.append(f"{indent}    reason: {reason}")
    stop = node.get("stop")
    if stop:
        lines.append(f"{indent}    stop:   {stop}")
    for child in node.get("children", []) or []:
        walk(child, depth + 1, tally, lines)


def render(path):
    with open(path, "r", encoding="utf-8") as fh:
        root = json.load(fh)

    out = []
    out.append(banner("TESSERACT PIPELINE  -  trace render"))
    out.append("")
    out.append(f"file: {path}")
    out.append(f"goal: {root.get('goal', '').strip()}")
    out.append("")

    out.append("The one operation is sweep. Push a structure along a new orthogonal")
    out.append("axis, take the whole trail as the next structure:")
    out.append("")
    for step in SWEEP_PROGRESSION:
        out.append("    " + step)
    out.append("")

    out.append(banner("Self-design tree (axis chosen per node, by reading the work)"))
    out.append("")
    tally = {}
    tree_lines = []
    walk(root, 0, tally, tree_lines)
    out.extend(tree_lines)
    out.append("")

    out.append(banner("Axes opened"))
    out.append("")
    opened = []
    for axis in AXES:
        count = tally.get(axis, 0)
        mark = "OPEN " if count > 0 else "  .  "
        out.append(f"  [{mark}] {AXIS_LABEL[axis]}   x{count}")
        if count > 0:
            opened.append(axis)
    leaf_count = tally.get("leaf", 0)
    out.append(f"          {AXIS_LABEL['leaf']}   x{leaf_count}")
    out.append("")

    out.append(banner("Verdict"))
    out.append("")
    if len(opened) == 4:
        out.append("  All four axes opened. This one task is a full tesseract:")
        out.append("  order, breadth, depth, and time, decided at runtime by reading")
        out.append("  the nature of the work, not by a rule baked in advance.")
        out.append("")
        out.append("  A pipeline is not a line.")
    elif opened:
        names = ", ".join(opened)
        out.append(f"  Axes opened: {names}.")
        out.append("  A correct self-design opens exactly the axes the work needs,")
        out.append("  and no more. Leaving an axis closed is a decision, not a miss.")
    else:
        out.append("  No axis opened: the whole task was a single leaf.")
        out.append("  For a simple goal, one line is the honest structure.")
    out.append("")
    return "\n".join(out)


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        print("error: expected exactly one path to a tesseract.json trace",
              file=sys.stderr)
        return 2
    try:
        print(render(argv[1]))
    except FileNotFoundError:
        print(f"error: file not found: {argv[1]}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {argv[1]}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
