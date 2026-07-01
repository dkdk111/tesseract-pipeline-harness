# Trace: <task name>

Goal: <restate the goal>

Box in force: <axes allowed, max_depth, max_breadth, max_rounds, any approval gates>

## The self-design, node by node

- `root` opened <axis>. <Reason: the honest reading of the work that chose it.>
  <Stop condition if one fired.>
- `<node-id>` opened <axis>. <Reason.>
  - `<child-id>` opened <axis> / stayed a Leaf. <Reason.>
- ...

## Verify (before executing leaf work)

- Is the order honest (no false dependency serialized)? <yes/no, why>
- Is any breadth a false parallel? <yes/no, why>
- Is every depth sweep paid for? <yes/no, why>
- Is anything too large left as a leaf? <yes/no, why>

## Summary

<Which axes the task actually opened, and the one-line verdict: was it a line, a
plane, a solid, or a tesseract, and was the structure honest to the work.>
