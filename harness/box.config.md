# box.config.md: the walls for this repo

This file documents the box in prose. The canonical, machine-readable box the engine
reads is `box.config.json` at the repository root; the two must agree. The human
edits both; the agent obeys them and never edits them without being asked. This is
the concrete form of "the hand that draws the box." Every run reads the box first.
Change these values to loosen or tighten the box. In agent mode, a coding agent reads
this prose; in engine mode, the Python harness reads `box.config.json`.

## Allowed axes

- order: allowed
- breadth: allowed
- depth: allowed
- time: allowed

An axis set to `forbidden` may not be opened even when the work's nature would fit
it. The agent falls back to an allowed axis or a leaf and notes the constraint.

## Limits

- max_depth: 3        (a depth sweep may nest at most 3 levels; deeper nodes become leaves)
- max_breadth: 6      (a breadth sweep may fan at most 6 branches; extras are queued or dropped, noted)
- max_rounds: 3       (a time sweep may run at most 3 revision rounds)
- budget_notes: keep total work proportionate to the goal; a one-line goal stays one line

## Stop conditions (always on)

- depth stops at max_depth or when the node is small enough to be a leaf
- breadth stops at max_breadth
- time stops at max_rounds, on a dry round (no improvement over the last), or on
  convergence to the goal
- every sweep must pair with a stop condition; a sweep with no stop is forbidden

## Verify (always on)

Before executing leaf work, re-examine the proposed structure adversarially: is it
honest to the work, is any dependency false, is any split unpaid, is anything too
large left as a leaf.

## Approval-required actions (never self-designed)

The agent must stop and get explicit human approval before any of these:

- moving money, purchases, payments
- sending messages, emails, or publishing externally
- deleting or overwriting files outside `.tesseract/`
- network calls with side effects
- any irreversible change

## Working area

- The agent writes runs and outputs under `.tesseract/` unless a task says otherwise.
- Files outside this repository are out of bounds without approval.
