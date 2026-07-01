# Trace: Ship the v2.1 release

Goal: Ship the v2.1 release

Box in force: allowed axes: order, breadth, depth, time | max_depth 3 | max_breadth 6 | max_rounds 3.

## The self-design, node by node

- `root` opened **Order** (line).
  Reason: Front-to-back dependency: each step consumes the previous step's output. Sweep order and lay the steps on a line.
  Stop: closes when the last dependent step completes
  - `build-the-application` stayed a **Leaf** (point).
    Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
  - `run-the-test-suites` opened **Breadth** (plane).
    Reason: The branches are independent and do not wait on one another. Sweep breadth and fan them out in parallel.
    Stop: 3 branches, under max_breadth 6
    - `run-unit-tests` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `run-integration-tests` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
    - `run-end-to-end-tests` stayed a **Leaf** (point).
      Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
  - `package-the-release-artifacts` stayed a **Leaf** (point).
    Reason: Small enough to handle in one pass; leaving it a leaf is the honest decision.
  - `deploy-v2-1-to-production` is a **Leaf held at the approval gate** (point).
    Reason: A high-risk, irreversible, or outside-the-repo action. It is a leaf, but it is not self-designed or executed autonomously: it waits at the human approval gate above the three walls.
    Stop: held at the human approval gate

## Summary

Axes opened: Order, Breadth.

A correct self-design opens exactly the axes the work needs, and no more. Leaving an axis closed is a decision, not a miss.
