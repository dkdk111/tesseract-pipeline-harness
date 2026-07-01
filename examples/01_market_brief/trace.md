# Trace: competitive market brief

Goal: produce a competitive market brief on the note-taking app space (Notion,
Obsidian, Roam) across pricing, features, positioning, ending with a recommendation.

Box in force: all four axes allowed, max_depth 3, max_breadth 6, max_rounds 3. No
approval-required actions.

## The self-design, node by node

- `root` opened Time. The brief does not close in one pass. It runs draft, review,
  revise, in rounds, until a round stops improving. Reason: one pass is not enough;
  the result of a pass feeds the next. Stopped after round 2 (round 2 improved on
  round 1; a third round would have been a dry round).

- `round-body` opened Order. Inside a round the work has a hard front-to-back
  dependency: collect, then analyze, then write, then review. Each step consumes the
  previous step's output, so they lie on a line.

- `collect` opened Breadth. The three competitors are independent; gathering on one
  does not wait on another, so they fan into three parallel branches.

  - `collect:notion` opened Depth. Notion is too large to summarize flat (product
    lines, pricing tiers, positioning), so this node became a seed and opened its own
    sub-structure: products, pricing, positioning, each a leaf. Depth 1, well under
    max_depth 3.

  - `collect:obsidian` stayed a Leaf. One focused product, small enough for one
    pass. Forcing a depth sweep here would pay nothing, so leaving it a leaf is the
    honest decision.

  - `collect:roam` stayed a Leaf, same reason.

- `analyze` opened Breadth. The three dimensions (pricing, features, positioning)
  are independent lenses over the same collected data, so they fan into three
  parallel branches, each a leaf.

- `write` stayed a Leaf. A single drafting pass over the finished analysis.

- `review` stayed a Leaf. A single adversarial pass over the draft and the
  structure; its finding is what the next time-axis round consumes.

## Verify (before executing leaf work)

- Is the order honest? Yes: analyze genuinely needs collect's output; this is a real
  dependency, not a false one serialized for comfort.
- Is any breadth a false parallel? No: competitors do not depend on each other, and
  the three analysis lenses are independent.
- Is the one depth sweep paid for? Yes: Notion does not fit a flat summary; the two
  leaf competitors were correctly left flat rather than over-split.
- Is anything too large left as a leaf? No: the only oversized node (Notion) was
  opened as a seed.

## Summary

One ordinary task opened all four axes: Time (the revision loop), Order (the
collect-analyze-write-review spine), Breadth (parallel competitors, parallel
lenses), Depth (Notion as a seed). The pipeline was a tesseract, not a line, and the
structure was decided by reading the work, not by a rule baked in advance.
