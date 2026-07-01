"""Command line interface for the Tesseract Pipeline harness.

    tesseract demo                 Run the bundled example end to end (no keys).
    tesseract run <task.json>      Plan, execute, and trace a task.
    tesseract render <file.json>   Pretty-print a tesseract.json trace.
    tesseract new <path>           Scaffold a task.json template.

Also runnable without installing, from the repo root:

    python -m tesseract_pipeline demo
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import List, Optional

from . import __version__
from .axes import Axis
from .box import Box
from .executor import Executor
from .node import Node
from .planner import plan
from .render import render_tree
from .trace import write_trace
from .worker import SimulatedWorker

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)
_DEMO_TASK = os.path.join(_REPO_ROOT, "examples", "01_market_brief", "task.json")

_TASK_TEMPLATE = {
    "goal": "Describe the whole job in one line",
    "iterative": True,
    "rounds": 2,
    "sequence": [
        {
            "goal": "First step (later steps depend on this)",
            "parallel": [
                {"goal": "An independent branch"},
                {
                    "goal": "A branch too big to handle flat",
                    "oversized": True,
                    "parts": [
                        {"goal": "A sub-part"},
                        {"goal": "Another sub-part"},
                    ],
                },
            ],
        },
        {"goal": "A dependent later step"},
    ],
}


def _load_task(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _run_task(task: dict, box: Box, out_dir: str, quiet: bool = False) -> dict:
    root = plan(task, box)
    Executor(SimulatedWorker()).run(root)
    info = write_trace(root, task.get("goal", ""), box, out_dir)
    if not quiet:
        print(render_tree(root.to_dict()))
        print(f"trace written to: {out_dir}")
        print(f"  structure: {os.path.relpath(info['tesseract'])}")
        print(f"  narrative: {os.path.relpath(info['trace'])}")
        print(f"  output:    {os.path.relpath(info['output'])}")
    return info


def _cmd_demo(args: argparse.Namespace) -> int:
    task = _load_task(_DEMO_TASK)
    box = Box.load(_box_path(args.box))
    out_dir = args.out or os.path.join(_REPO_ROOT, ".tesseract", "demo")
    _run_task(task, box, out_dir)
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    task = _load_task(args.task)
    box = Box.load(_box_path(args.box))
    default_out = os.path.join(_REPO_ROOT, ".tesseract", _slug(task.get("goal", "run")))
    out_dir = args.out or default_out
    _run_task(task, box, out_dir)
    return 0


def _count(node: Node, predicate) -> int:
    total = 1 if predicate(node) else 0
    for child in node.children:
        total += _count(child, predicate)
    return total


def _axes_marks(opened: set) -> str:
    order = [Axis.ORDER, Axis.BREADTH, Axis.DEPTH, Axis.TIME]
    return " ".join(a.value[0].upper() if a in opened else "." for a in order)


def _cmd_gallery(args: argparse.Namespace) -> int:
    box = Box.load(_box_path(args.box))
    paths = sorted(glob.glob(os.path.join(_REPO_ROOT, "examples", "*", "task.json")))
    if not paths:
        print("no examples found under examples/*/task.json", file=sys.stderr)
        return 1

    rows = []
    for path in paths:
        task = _load_task(path)
        root = plan(task, box)
        Executor(SimulatedWorker()).run(root)
        opened = root.axes_opened()
        leaves = _count(root, lambda n: n.axis == Axis.LEAF)
        gates = _count(root, lambda n: n.approval_required)
        rounds = root.rounds if root.axis == Axis.TIME else 1
        name = os.path.basename(os.path.dirname(path))
        rows.append(
            {
                "name": name,
                "domain": task.get("domain", "-"),
                "axes": _axes_marks(opened),
                "leaves": leaves,
                "rounds": rounds,
                "gates": gates,
                "perspective": task.get("perspective", ""),
            }
        )

    bar = "=" * 96
    print(bar)
    print("TESSERACT PIPELINE  -  gallery  (O=order  B=breadth  D=depth  T=time; a dot means not opened)")
    print(bar)
    header = f"{'example':22} {'domain':16} {'O B D T':9} {'leaf':>4} {'rnd':>3} {'gate':>4}  perspective"
    print(header)
    print("-" * 96)
    for r in rows:
        print(
            f"{r['name']:22} {r['domain']:16} {r['axes']:9} {r['leaves']:>4} "
            f"{r['rounds']:>3} {r['gates']:>4}  {r['perspective']}"
        )
    print(bar)
    print(f"{len(rows)} demos. Each opens exactly the axes its work needs, and no more.")
    print("Render any one in full with: python -m tesseract_pipeline render examples/<name>/tesseract.json")
    return 0


def _cmd_render(args: argparse.Namespace) -> int:
    with open(args.file, "r", encoding="utf-8") as fh:
        print(render_tree(json.load(fh)))
    return 0


def _cmd_new(args: argparse.Namespace) -> int:
    if os.path.exists(args.path) and not args.force:
        print(f"error: {args.path} exists (use --force to overwrite)", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(args.path)), exist_ok=True)
    with open(args.path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(_TASK_TEMPLATE, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"wrote task template to {args.path}")
    return 0


def _box_path(explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    return os.path.join(_REPO_ROOT, "box.config.json")


def _slug(text: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "run"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tesseract",
        description="Self-design a task along four axes (order, breadth, depth, time), "
        "run it, and trace it.",
    )
    parser.add_argument("--version", action="version", version=f"tesseract-pipeline {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_demo = sub.add_parser("demo", help="run the bundled example end to end")
    p_demo.add_argument("--out", help="output directory for the trace")
    p_demo.add_argument("--box", help="path to box.config.json")
    p_demo.set_defaults(func=_cmd_demo)

    p_run = sub.add_parser("run", help="plan, execute, and trace a task.json")
    p_run.add_argument("task", help="path to a task.json")
    p_run.add_argument("--out", help="output directory for the trace")
    p_run.add_argument("--box", help="path to box.config.json")
    p_run.set_defaults(func=_cmd_run)

    p_gallery = sub.add_parser("gallery", help="run every example and print a comparison table")
    p_gallery.add_argument("--box", help="path to box.config.json")
    p_gallery.set_defaults(func=_cmd_gallery)

    p_render = sub.add_parser("render", help="pretty-print a tesseract.json trace")
    p_render.add_argument("file", help="path to a tesseract.json")
    p_render.set_defaults(func=_cmd_render)

    p_new = sub.add_parser("new", help="scaffold a task.json template")
    p_new.add_argument("path", help="path to write the template to")
    p_new.add_argument("--force", action="store_true", help="overwrite if it exists")
    p_new.set_defaults(func=_cmd_new)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
