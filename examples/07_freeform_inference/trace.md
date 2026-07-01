# Trace: Research the space, then gather notes on Notion, Obsidian and Roam, then break the market down into pricing, features and positioning, then write the brief, and iterate twice

Goal: Research the space, then gather notes on Notion, Obsidian and Roam, then break the market down into pricing, features and positioning, then write the brief, and iterate twice

Box in force: allowed axes: order, breadth, depth, time | max_depth 3 | max_breadth 6 | max_rounds 3.

## Verify (the structure re-examined before execution)

Passed: no degenerate sweeps, no unjustified nodes, no ambiguous ids.

## The self-design, node by node

- `root` opened **Time** (tesseract, 2 rounds).
  Reason: One pass is not enough: the result of a pass feeds the next. Sweep time and run the whole structure in revision rounds.
  Stop: reached the round limit (2 rounds)
  - `root-round` opened **Order** (line).
    Reason: Front-to-back dependency: each step consumes the previous step's output. Sweep order and lay the steps on a line.
    Stop: closes when the last dependent step completes
    - `research-the-space` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `gather-notes-on-notion-obsidian-and-roam` opened **Breadth** (plane).
      Reason: The branches are independent and do not wait on one another. Sweep breadth and fan them out in parallel.
      Stop: 3 branches, under max_breadth 6
      - `notion` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `obsidian` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `roam` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `break-the-market-down-into-pricing-featu` opened **Depth** (solid).
      Reason: This node is too large to handle in one pass, so it is a seed, not a leaf. Sweep depth and open a smaller structure of its own in place.
      Stop: depth 1, under max_depth 3
      - `pricing` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `features` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `positioning` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `write-the-brief` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.

## Summary

Axes opened: Order, Breadth, Depth, Time.

All four axes opened. This one task is a full tesseract: order, breadth, depth, and time, decided at runtime by reading the nature of the work, not by a rule baked in advance. A pipeline is not a line.
