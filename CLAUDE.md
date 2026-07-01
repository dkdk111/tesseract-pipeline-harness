# CLAUDE.md

This repository is a harness. When you (a coding agent such as Claude Code) are
pointed at it, you run tasks as a Tesseract Pipeline: you self-design the structure
of a task along four orthogonal axes (order, breadth, depth, time), stay inside a
box the human holds, and leave a trace that makes the dimensions visible.

Your operating law is `AGENTS.md`. Read it in full first. It is the single source
of truth for how you behave here; this file only adds the entry sequence.

## Start here, every task

1. Read `AGENTS.md` (the operating law).
2. Read `harness/box.config.md` (the live walls for this repo: which axes are
   allowed, max depth, max breadth, max rounds, budget, approval-required actions).
   These bind the current run.
3. Run the task using the four-question self-design procedure in
   `harness/01_self_design.md`, obeying the box in `harness/02_the_box.md`.
4. Record the run as a trace under `.tesseract/`, following
   `harness/03_trace_protocol.md`.

## The harness in one screen

- One operation: `sweep`. Push a structure along a new orthogonal axis, take the
  whole trail as the next structure. See `harness/00_ontology.md`.
- Four axes: order (dependency, line), breadth (independence, plane), depth
  (nesting, solid), time (revision loop, tesseract).
- You choose which axes open, by reading the work's nature. The human chooses the
  walls. High-risk or outside-the-repo actions require human approval, never
  self-design.
- The trace is the proof. No trace, no demonstration.

## Ground rules for this repo

- Do your working and outputs under `.tesseract/` unless the task says otherwise.
- Do not touch files outside this repository, send anything to a network with side
  effects, or perform irreversible actions without explicit human approval.
- If a task is genuinely one line, leave it as one line. Opening axes the work does
  not need is a self-design failure, not thoroughness.

## Try it without an agent

A recorded example runs with no model and no keys:

    python tools/render_tesseract.py examples/01_market_brief/tesseract.json

It prints how one task opened all four axes. See `examples/README.md`.
