# Examples

A recorded run you can inspect and render with no model and no API keys. It shows
one ordinary task opening all four axes of the Tesseract Pipeline.

## 01_market_brief

Goal: produce a competitive market brief on the note-taking app space.

- `task.md`: the goal and input handed to the harness.
- `trace.md`: the self-design trace, node by node, with the axis and reason at each.
- `tesseract.json`: the same tree, machine-readable, tagged by axis.

This one task naturally opened every axis:

- Time (outermost): the brief runs in draft-review-revise rounds, not one pass.
- Order: inside a round, collect, then analyze, then write, then review, a
  dependency chain.
- Breadth: inside collect, the competitors are gathered in parallel; inside analyze,
  the dimensions (pricing, features, positioning) run in parallel.
- Depth: one competitor is too large to summarize flat, so it becomes a seed and
  opens its own sub-structure.

## Render it

    python tools/render_tesseract.py examples/01_market_brief/tesseract.json

The renderer is deterministic and uses only the Python standard library. It prints
the sweep progression (point to line to plane to solid to tesseract), walks the
task tree with each node's axis and reason, tallies which axes were opened, and
confirms the verdict: this pipeline is a tesseract, not a line.

This is the "complete simulation" the harness ships: the live model is whatever
coding agent you attach, but this recorded run demonstrates the four axes with
nothing running but a tree walk.
