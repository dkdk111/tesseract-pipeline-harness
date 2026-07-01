# Tesseract Pipeline Harness

A runnable starter pack that makes the idea in the book *Tesseract Pipeline*
executable. Point a coding agent (such as Claude Code) at this repository and it
stops running tasks as a line and starts running them as a tesseract: it decides the
structure of a task at runtime, along four orthogonal axes, inside a box you hold,
and leaves a trace that makes the four dimensions visible.

[한국어 README](README.ko.md)

## The idea in one paragraph

What we usually call a pipeline is one-dimensional: a line of steps. Parallelism
opens a second axis and the line becomes a plane. Recursion opens a third and the
plane becomes a solid. An iteration loop opens a fourth, time, and the solid becomes
a tesseract. Every one of these transitions is the same single operation, a sweep:
push a structure along a new orthogonal axis and take the whole trail as the next
structure. The subject that opens these axes is not the human drawing a diagram in
advance. It is the model itself, at runtime, reading the nature of the work, inside
boundaries a human draws. That is self-design, and it is what this harness makes an
executing agent actually do.

## The four axes

| Dim | Axis | Geometry | Mechanism | The decision that opens it |
|-----|------|----------|-----------|----------------------------|
| 1D | Order | line | serial dependency | "this comes after that" |
| 2D | Breadth | plane | parallel independence | "these run at once" |
| 3D | Depth | solid | recursive nesting | "this node opens again inside" |
| 4D | Time | tesseract | iterative self-evolution | "run the whole thing again to grow it" |

All four transitions are the one operation, sweep.

## Try it in 30 seconds, with no model and no keys

A recorded run ships with the repo. Render it:

    python tools/render_tesseract.py examples/01_market_brief/tesseract.json

You will see one ordinary task (a competitive market brief) open all four axes: a
time loop of revision rounds, an order spine of collect-analyze-write-review,
breadth fan-outs of parallel competitors and parallel lenses, and a depth sweep
where one oversized competitor becomes a seed. The renderer is deterministic and
standard-library only. This is the demonstration you can run without attaching
anything.

## Use it with a coding agent

1. Open this repository in your coding agent (Claude Code reads `CLAUDE.md`; other
   agents read `AGENTS.md`; both point to the same operating law).
2. Edit `harness/box.config.md` to set your walls: which axes are allowed, max
   depth, max breadth, max rounds, and which actions require your approval.
3. Give the agent a task (write it into `.tesseract/` using `templates/task.md`, or
   just describe it). The agent will self-design the structure along the four axes,
   stay inside your box, and write a trace under `.tesseract/`.
4. Read the trace, or render its `tesseract.json`, to see the shape it chose and why.

The agent chooses which axes to open by reading the work. You choose the walls. Any
high-risk, irreversible, or outside-the-repo action requires your explicit approval,
never self-design. The clearer your walls, the more freely the agent can design
inside them: the constraint is what expands the autonomy.

## What is in here

    AGENTS.md              The operating law. The agent's brain. Read first.
    CLAUDE.md              Claude Code entry point (points to AGENTS.md).
    harness/
      00_ontology.md       The one operation (sweep) and the four axes.
      01_self_design.md    How the agent decides structure: the four questions.
      02_the_box.md        Control: boundary, stop, verify, and the approval gate.
      03_trace_protocol.md How the agent records the dimensional expansion.
      box.config.md        The live walls for this repo. You edit this.
    examples/
      01_market_brief/     A recorded run that opens all four axes.
    tools/
      render_tesseract.py  Deterministic, keyless trace renderer.
    templates/             Blank task and trace templates.
    .tesseract/            The agent's working area (git-ignored except its README).

## This repo is its own example

The book's law is that a demonstration must be built out of the thing it
demonstrates. So this harness is itself structured along its four axes: the docs sit
in an order of dependency, the four axis definitions were written in parallel, the
box document opens into its three walls by depth, and the whole thing is meant to be
revised in rounds as real runs teach it. The implementation is not a proof bolted
onto the ontology. It is the shadow the ontology casts.

## Companion to the book

This is the companion implementation to *Tesseract Pipeline* (Korean, by DK), a book
that argues an AI execution structure is a tesseract opened along four axes by a
model's self-design. The harness turns that argument into something you can attach to
an agent and watch happen. License: MIT (see `LICENSE`).
