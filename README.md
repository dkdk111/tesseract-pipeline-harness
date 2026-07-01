# Tesseract Pipeline Harness

> A pipeline is not a line. It is a tesseract that a model opens along four
> orthogonal axes, inside a box that a human draws.

[![CI](https://github.com/dkdk111/tesseract-pipeline-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/dkdk111/tesseract-pipeline-harness/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Dependencies: none](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](pyproject.toml)

A runnable harness that turns the idea in the book *Tesseract Pipeline* into working
software. Give it a task, and it decides the task's structure at runtime along four
orthogonal axes (order, breadth, depth, time), executes that structure for real,
stays inside a box you control, and writes a trace that makes the four dimensions
visible. It runs with no model and no API keys out of the box, and it plugs into a
real model or a coding agent when you want one.

---

## The idea in one paragraph

What we usually call a pipeline is one-dimensional: a line of steps. Parallelism
opens a second axis and the line becomes a plane. Recursion opens a third and the
plane becomes a solid. An iteration loop opens a fourth, time, and the solid becomes
a tesseract. Every one of these transitions is the same single operation, a *sweep*:
push a structure along a new orthogonal axis and take the whole trail as the next
structure. The subject that opens these axes is not a human drawing a diagram in
advance; it is the model itself, at runtime, reading the nature of the work, inside
boundaries a human sets. That is *self-design*, and this harness makes it executable.

## The four axes

| Dim | Axis | Geometry | Mechanism | The decision that opens it |
|-----|------|----------|-----------|----------------------------|
| 1D | Order | line | serial dependency | "this comes after that" |
| 2D | Breadth | plane | parallel independence | "these run at once" |
| 3D | Depth | solid | recursive nesting | "this node opens again inside" |
| 4D | Time | tesseract | iterative self-evolution | "run the whole thing again to grow it" |

    point --order--> line --breadth--> plane --depth--> solid --time--> tesseract

All four transitions are the one operation, sweep.

## Quickstart (30 seconds, no model, no keys)

```bash
git clone https://github.com/dkdk111/tesseract-pipeline-harness.git
cd tesseract-pipeline-harness
python -m tesseract_pipeline demo
```

That self-designs and executes one ordinary task (a competitive market brief), opens
all four axes, and prints the trace. No installation, no dependencies, no keys. The
default worker is a deterministic simulator, so the run is fully reproducible; the
four axes, the sweep, and the box are real and really executed, and only the leaf
content is synthetic.

Output ends with:

```
  All four axes opened. This one task is a full tesseract:
  order, breadth, depth, and time, decided at runtime by reading
  the nature of the work, not by a rule baked in advance.

  A pipeline is not a line.
```

## What actually happens on a run

1. Plan (self-design). The planner reads the task's declared nature and asks four
   questions in order: is one pass enough (else Time), is there front-to-back
   dependency (Order), do independent branches split off (Breadth), is a part too big
   to handle flat (Depth). The first that fits, and the box allows, opens. A simple
   task stays a single leaf.
2. Execute. The executor runs the structure for real: Order threads each step's
   output into the next, Breadth runs branches concurrently, Depth recurses, and Time
   re-runs the whole subtree in rounds until it stops.
3. Trace. The harness writes `tesseract.json` (the structure and results), `trace.md`
   (the human-readable self-design record), and `output.md` (the assembled result).
   A run that leaves no trace has demonstrated nothing.

See a full recorded run in [`examples/01_market_brief/`](examples/01_market_brief).

## Demo gallery: many domains, many shapes

The harness is convincing from more than one angle only if it behaves differently on
different work. Six demos, each a different domain and a different structural
signature, ship with the repo. Run them all at once:

    python -m tesseract_pipeline gallery

```
example                domain         O B D T  leaf  perspective
01_market_brief        research       O B D T   10   all four axes open (a full tesseract)
02_software_release    devops         O B . .    6   order + breadth, with a human approval gate on deploy
03_data_pipeline       data / etl     O B D .    8   order, breadth, and depth, with no time axis
04_book_chapter        writing        O B . T    5   time wrapping order and breadth (a revision loop)
05_bulk_translation    localization   . B . .    6   breadth only, and it hits the box's max_breadth wall
06_quick_fix           maintenance    . . . .    1   a single leaf: the harness refuses to invent dimensions
```

(O = order, B = breadth, D = depth, T = time; a dot means the axis was not opened.)

Two of these are the hardest cases to fake, and they work: `02_software_release`
holds its deploy step at a human approval gate instead of executing it, and
`05_bulk_translation` declares more parallel branches than the box allows and hits
the max_breadth wall (the surplus is queued, not dropped silently). And
`06_quick_fix` opens no axis at all, because a one-line job is honestly a line. See
[`examples/README.md`](examples/README.md) for the full tour.

## Use it as a real harness

### Engine mode (Python)

Describe a task's nature in a small JSON file and run it. The task declares
*properties* of the work, not axes; the planner derives the axes.

```bash
python -m tesseract_pipeline new my_task.json     # scaffold a template
python -m tesseract_pipeline run my_task.json      # plan, execute, trace
```

To make the leaves real, swap the default simulator for a model. Only the worker
changes; the planner, the executor, and the box are untouched. See
[`examples/llm_worker_example.py`](examples/llm_worker_example.py).

### Agent mode (Claude Code and other coding agents)

Point a coding agent at this repository. It reads [`CLAUDE.md`](CLAUDE.md) (Claude
Code) or [`AGENTS.md`](AGENTS.md) (generic), which are the operating law: self-design
free-form tasks along the same four axes, obey the same box, and leave a trace under
`.tesseract/`. The agent is the live model; no API code is needed in the repo.

Both modes share one ontology and one box. Engine mode is the reference you can read
and run; agent mode is the harness attached to a live agent.

## The box: control you hold

The model chooses which axes to open. You choose the walls. The canonical,
machine-readable box is [`box.config.json`](box.config.json); its prose
documentation is [`harness/box.config.md`](harness/box.config.md).

```json
{
  "allowed_axes": ["order", "breadth", "depth", "time"],
  "max_depth": 3,
  "max_breadth": 6,
  "max_rounds": 3,
  "approval_required": [
    "moving money, purchases, payments",
    "sending messages, emails, or publishing externally",
    "deleting or overwriting files outside .tesseract/",
    "network calls with side effects",
    "any irreversible change"
  ]
}
```

Three walls plus a gate: Boundary (which axes, how far), Stop (every sweep pairs with
a stop condition), Verify (re-examine the structure adversarially before building on
it), and an Approval gate for high-risk or irreversible actions, which are never
self-designed. The paradox the book insists on holds here: the clearer the walls, the
more freely the model can design inside them. Control is not the opposite of autonomy;
it is its precondition.

## Task schema (declare the nature, not the axes)

```jsonc
{
  "goal": "one line describing the whole job",
  "iterative": true,          // not one-shot -> the planner opens Time
  "rounds": 2,                 // capped by the box's max_rounds
  "sequence": [                // dependency between steps -> Order
    {
      "goal": "a step",
      "parallel": [            // independent branches -> Breadth
        { "goal": "a branch" },
        {
          "goal": "an oversized branch",
          "oversized": true,   // too big to handle flat -> Depth
          "parts": [ { "goal": "a sub-part" } ]
        }
      ]
    },
    { "goal": "a dependent later step" }
  ]
}
```

A unit with none of these properties is a leaf. A unit that declares more than one
opens the outermost axis here and the rest in its child, exactly as the book's local,
recursive, incremental decision requires.

## Repository layout

```
AGENTS.md / CLAUDE.md      Agent-mode operating law (the brain for a coding agent).
box.config.json            The box the engine reads (you edit this).
harness/                   The ontology, shared by both modes.
  00_ontology.md             The sweep and the four axes.
  01_self_design.md          The four-question decision procedure.
  02_the_box.md              Control: boundary, stop, verify, approval gate.
  03_trace_protocol.md       How a run is recorded.
  box.config.md              Prose docs for box.config.json.
tesseract_pipeline/        The engine (standard library only).
  planner.py                 Self-design: nature -> four-axis structure.
  executor.py                Real order, breadth, depth, and time execution.
  worker.py                  Pluggable leaf work; deterministic simulator default.
  box.py, node.py, axes.py   The box, the node tree, the axes.
  trace.py, render.py, cli.py
examples/                  A recorded run and an LLM-worker sketch.
tests/                     Standard-library unittest suite.
tools/render_tesseract.py  Back-compatible renderer shim.
```

## Install (optional)

The harness needs no install to run. To get the `tesseract` console command:

```bash
python -m pip install -e .
tesseract demo
tesseract run examples/01_market_brief/task.json
```

## Tests

Standard library only; no test dependencies.

```bash
python -m unittest discover -s tests -v
```

CI runs the suite and the demo on Python 3.9 through 3.12.

## This repository is its own example

The book's law is that a demonstration must be built out of the thing it
demonstrates. So this harness is structured along its own four axes: the docs lie in
an order of dependency, the axis definitions were written in parallel, the box
document opens into its three walls by depth, and the whole is meant to be revised in
rounds as real runs teach it. The implementation is not a proof bolted onto the
ontology. It is the shadow the ontology casts.

## Companion to the book

This is the companion implementation to *Tesseract Pipeline* by DK, a book that
argues an AI execution structure is a tesseract opened along four axes by a model's
self-design. The harness turns that argument into something you can run, attach to an
agent, and watch happen.

## License

MIT. See [LICENSE](LICENSE).
