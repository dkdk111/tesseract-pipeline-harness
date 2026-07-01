# Overview: what this harness means

This document explains what the Tesseract Pipeline Harness is, what it means, and
where its "meta-instructions" live. For hands-on usage, see the [README](../README.md);
for the ontology, see [`harness/`](../harness).

## One sentence

This harness turns the argument of the book *Tesseract Pipeline* from prose into
running software: a pipeline is not a line but a tesseract that a model opens along
four orthogonal axes (order, breadth, depth, time), by reading the nature of the
work, inside a box a human draws. The harness makes that self-expansion executable
and leaves a trace so the four dimensions are visible.

Why it exists: the book's law is that a demonstration must be built out of the thing
it demonstrates. The implementation is not a proof bolted onto the ontology; it is
the shadow the ontology casts.

## The concept, as one operation

```
point --order--> line --breadth--> plane --depth--> solid --time--> tesseract
```

These four transitions are not four techniques. They are a single operation, the
sweep, repeated with a different axis each time: push a structure along a new
orthogonal axis and take the whole trail as the next structure. Because the same
sweep appears at every scale, the structure is fractal and self-similar. See
[`harness/00_ontology.md`](../harness/00_ontology.md).

## Where the meta-instructions live

Yes, the harness contains meta-instructions that drive the pipeline to expand itself
along each dimension. It runs in two modes, and the meta-instructions sit differently
in each.

### Agent mode: the meta-instructions themselves

[`AGENTS.md`](../AGENTS.md) (generic) and [`CLAUDE.md`](../CLAUDE.md) (Claude Code)
are the operating law you attach to a coding agent. They are the meta-instructions
for self-expansion. Their core is a recursive rule:

- One recursive operation: the sweep repeats with the axis swapped; what is swept
  does not matter.
- Local, recursive decision: at every node, decide structure before content; read
  only this node's nature, open one axis, and at each child that move created, ask
  the same four questions again from the start. That recursion ("again from the
  start, at each child") is the engine of meta-level self-expansion.
- Inside the box: the model chooses which axes open; the human holds the walls
  (boundary, stop, verify) and the approval gate.

The canonical meta-instruction set is `AGENTS.md` plus
[`harness/01_self_design.md`](../harness/01_self_design.md) (the four-question
procedure) plus [`harness/00_ontology.md`](../harness/00_ontology.md) (the recursive,
fractal sweep). Attach a live model, and it reads a free-form goal and truly expands
on its own by these instructions.

### Engine mode: a deterministic reference

The Python package `tesseract_pipeline` bakes the same procedure into runnable code:
`planner.py` applies the four questions recursively (self-design), and `executor.py`
executes the four axes for real (order threads context, breadth runs concurrently,
depth recurses, time iterates in rounds). It lets you watch the meta-procedure unfold
with no model and no keys.

### The honest boundary

One thing must be explicit. In engine mode the planner reads the work's nature from a
*declared* form (`task.json`): you declare that the work is iterative, or dependent,
or splits into independent branches, or is too big to handle flat, and the planner
converts that into axes. So you declare the nature, and the engine decides the
structure. This is a faithful, if compact, form of self-design. But inferring the
nature itself from a raw, free-form goal is not something deterministic code does; it
needs a live model. That is exactly agent mode, or the engine with its worker swapped
for a real model (`LLMWorker`).

In short: the meta-instructions for self-expansion are present (`AGENTS.md`,
`harness/`), and the recursive expansion runs as code. The final step, inferring
nature from a raw goal, is completed when a model is attached. Not hiding that seam is
itself faithful to the book (a proposed structure is a hypothesis, not a guarantee).

## File map

```
AGENTS.md / CLAUDE.md   Meta-instructions (operating law). The recursive self-expansion rule.
box.config.json         The box: the walls a human holds.
harness/                The ontology, shared by both modes.
tesseract_pipeline/     The engine (planner, executor, worker, box, node, axes, trace, render, cli).
examples/               Six demos across domains, with generated traces.
```

## How a run flows

1. Plan (self-design): at each node, ask the four questions; open the first fitting,
   allowed axis, else leaf; recurse into each child.
2. Execute: order threads results forward, breadth runs concurrently, depth recurses,
   time iterates in rounds until a stop condition fires.
3. Trace: write `tesseract.json`, `trace.md`, and `output.md`. No trace, no
   demonstration.

## The gallery: many domains, many shapes

| Demo | Domain | Axes | What it shows |
|------|--------|------|---------------|
| 01 market_brief | research | order, breadth, depth, time | one task opens all four (a full tesseract) |
| 02 software_release | devops | order, breadth | deploy is held at the human approval gate |
| 03 data_pipeline | data / etl | order, breadth, depth | depth without time (only the axes needed) |
| 04 book_chapter | writing | order, breadth, time | a revision loop (the book's self-example) |
| 05 bulk_translation | localization | breadth | hits the max_breadth wall (surplus queued) |
| 06 quick_fix | maintenance | none (a leaf) | restraint: a one-line job stays a line |

The spread is the argument: the harness opens exactly the axes the work needs, and no
more. Run `python -m tesseract_pipeline gallery` to see them side by side.

## What it proves, and what it does not

- It proves the concept points at a real structure: the four axes, the sweep, the
  self-design, and the control are how the system actually works, not decoration.
- It does not prove the concept is universally true. As the book itself warns, a case
  is not a proof; a system decomposing cleanly into four axes does not make the
  concept true. This is an example that the concept touches reality, no more.
- "Simulation" means only that the leaf content is synthetic. The structure and the
  execution (ordering, parallelism, recursion, iteration) are real. Swap the worker
  for a model and only the leaves change; the planner, executor, and box are
  untouched.

## See it yourself

```
python -m tesseract_pipeline demo       # one task opens all four axes
python -m tesseract_pipeline gallery     # the six-demo comparison
python -m tesseract_pipeline render examples/02_software_release/tesseract.json  # the approval gate
```

To read the meta-instructions directly: `AGENTS.md` then
`harness/01_self_design.md` then `harness/00_ontology.md`.
