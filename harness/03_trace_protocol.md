# 03. Trace protocol: making the four axes visible

The demonstration is the trace. As you self-design a task, record which axis each
node opened and why. A run that leaves no trace has reasoned about a tesseract but
shown nothing. This protocol defines the artifact you leave behind.

For each task, write files under `.tesseract/<run-id>/`:

- `trace.md`: the human-readable record (what follows).
- `tesseract.json`: the machine-readable node tree (schema below), which
  `python -m tesseract_pipeline render <file>` can render.
- `output.md`: the assembled result of the run.

Use a short run id, for example `.tesseract/2026-07-01_market-brief/`. In engine
mode the harness writes all three files for you (see `tesseract_pipeline/trace.py`);
in agent mode you write them by hand to the same shape.

## trace.md

Start with the goal, the box values in force, then walk the tree node by node. For
each node record: its id, the axis it opened (or `leaf`), the reason (the honest
reading of the work's nature that chose the axis), and any stop condition that fired.
End with a one-line summary of which axes the task actually opened.

Template is in `templates/trace.md`.

## tesseract.json

A tree of nodes. Each node:

```json
{
  "id": "root",
  "goal": "one line describing this node's goal",
  "axis": "order | breadth | depth | time | leaf",
  "reason": "the honest reading of the work's nature that chose this axis",
  "geometry": "point | line | plane | solid | tesseract",
  "stop": "the stop condition that closed this node, or null",
  "rounds": 1,
  "children": []
}
```

Field notes:

- `axis` is how this node sweeps its children. `leaf` means no sweep; do the work
  directly. A leaf has no children.
- `geometry` is the local shape this node's sweep produces, using the axis-to-shape
  map: order is a line, breadth is a plane, depth is a solid, time is a tesseract, a
  leaf is a point.
- `rounds` matters only for a `time` node: how many revision rounds ran. Use 1
  elsewhere.
- `stop` records which wall closed the node (max depth reached, dry round, budget
  spent, goal converged), or null if it closed naturally.

## The rule that keeps the trace honest

Write the node's axis and reason before you execute its leaf work, not after. The
trace is the blueprint you commit to, then verify, then build on. Written after the
fact, it is decoration; written before, it is the self-design record the concept
requires. If verification changes the structure, update the node and note why. The
trace should read as a decision made, tested, and sometimes corrected, which is what
an honest self-design run looks like.
