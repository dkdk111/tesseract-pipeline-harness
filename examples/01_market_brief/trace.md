# Trace: Competitive market brief on note-taking apps

Goal: Competitive market brief on note-taking apps

Box in force: allowed axes: order, breadth, depth, time | max_depth 3 | max_breadth 6 | max_rounds 3.

## The self-design, node by node

- `root` opened **Time** (tesseract, 2 rounds).
  Reason: One pass is not enough: the result of a pass feeds the next. Sweep time and run the whole structure in revision rounds.
  Stop: stopped after 2 rounds (reached max rounds for this run)
  - `root-round` opened **Order** (line).
    Reason: Front-to-back dependency: each step consumes the previous step's output. Sweep order and lay the steps on a line.
    Stop: closes when the last dependent step completes
    - `gather-raw-material-on-each-competitor` opened **Breadth** (plane).
      Reason: The branches are independent and do not wait on one another. Sweep breadth and fan them out in parallel.
      Stop: 3 branches, under max_breadth 6
      - `gather-on-notion` opened **Depth** (solid).
        Reason: This node is too large to handle in one pass, so it is a seed, not a leaf. Sweep depth and open a smaller structure of its own in place.
        Stop: depth 1, under max_depth 3
        - `notion-product-lines` stayed a **Leaf** (point).
          Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
        - `notion-pricing-tiers` stayed a **Leaf** (point).
          Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
        - `notion-positioning` stayed a **Leaf** (point).
          Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `gather-on-obsidian` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `gather-on-roam-research` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `analyze-the-collected-material-across-di` opened **Breadth** (plane).
      Reason: The branches are independent and do not wait on one another. Sweep breadth and fan them out in parallel.
      Stop: 3 branches, under max_breadth 6
      - `compare-pricing-across-competitors` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `compare-features-across-competitors` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `compare-positioning-across-competitors` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `write-the-brief-from-the-analysis` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `review-the-draft-and-verify-the-structur` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.

## Summary

Axes opened: Order, Breadth, Depth, Time.

All four axes opened. This one task is a full tesseract: order, breadth, depth, and time, decided at runtime by reading the nature of the work, not by a rule baked in advance. A pipeline is not a line.
