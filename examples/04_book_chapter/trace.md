# Trace: Write the chapter 'What a Question Is'

Goal: Write the chapter 'What a Question Is'

Box in force: allowed axes: order, breadth, depth, time | max_depth 3 | max_breadth 6 | max_rounds 3.

## The self-design, node by node

- `root` opened **Time** (tesseract, 2 rounds).
  Reason: One pass is not enough: the result of a pass feeds the next. Sweep time and run the whole structure in revision rounds.
  Stop: stopped after 2 rounds (reached max rounds for this run)
  - `root-round` opened **Order** (line).
    Reason: Front-to-back dependency: each step consumes the previous step's output. Sweep order and lay the steps on a line.
    Stop: closes when the last dependent step completes
    - `outline-the-chapter-from-macro-to-micro` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `draft-the-sections` opened **Breadth** (plane).
      Reason: The branches are independent and do not wait on one another. Sweep breadth and fan them out in parallel.
      Stop: 3 branches, under max_breadth 6
      - `draft-the-opening` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `draft-the-argument` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
      - `draft-the-closing` stayed a **Leaf** (point).
        Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `edit-for-voice-and-rhythm` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.

## Summary

Axes opened: Order, Breadth, Time.

A correct self-design opens exactly the axes the work needs, and no more. Leaving an axis closed is a decision, not a miss.
