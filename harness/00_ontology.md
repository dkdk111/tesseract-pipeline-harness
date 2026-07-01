# 00. Ontology: the sweep and the four axes

This file is the ground. It defines the one operation and the four axes that the
rest of the harness runs on. It is condensed from the book *Tesseract Pipeline*.

## The one operation: sweep

Geometry builds a tesseract by repeating a single motion. Take a point and push it
one direction: its trail is a line. Push that line along a direction at a right
angle to it: the trail is a plane. Push the plane at a right angle: a solid. Push
the solid at a right angle: a tesseract. Every step is the same motion. Take a
shape, push it along a new right-angle direction it does not yet have, and take the
whole trail as the new shape.

Definition. A sweep moves an N-dimensional structure along a new axis orthogonal to
its existing axes, and takes the entire trail of that motion as an (N+1)-dimensional
structure. Three requirements:

- New axis. Pushing along an axis you already have only lengthens the shape. No new
  dimension appears.
- Orthogonal. The new axis must carry an independence the existing axes cannot be
  reduced to. It is a genuinely new degree of freedom.
- Take the trail. The new structure is not the endpoint of the motion. It is the
  whole trajectory the motion left behind.

Execution structures obey the same operation. What is swept only grows in size; the
motion is invariant. Because the same sweep appears at every scale, the structure is
fractal and self-similar. Self-similarity is not a mystical property here. It is the
plain consequence of repeating one operation.

## The four sweeps

### Sweep a point along Order, and you get a line

One act (one model call, one task) pushed along order: "this act, then another,
then another." The trail along the order axis is the chain of steps, the line we
used to call a pipeline. A point became a line.

### Sweep a line along Breadth, and you get a plane

Take that whole line and push it along a new axis orthogonal to order: "alongside
this flow, another flow that does not wait on it." The trail is a plane of parallel
flows. Note that what is swept is now a line, not a point. Sweep does not care what
it moves. A line became a plane.

### Sweep a plane along Depth, and you get a solid

Take one cell of the plane. If it is too large to handle in one pass and must open
its own structure in place, push it along depth: "inside this cell, another
structure of the same kind." The trail is a structure seated inside the cell. That
cell was a seed, not a leaf. A plane became a solid.

### Sweep a solid along Time, and you get a tesseract

Take the whole solid and push it along time, the axis orthogonal to all three
before it: "this whole structure again, next round, revised by what the result
showed." The trail across rounds is the tesseract. A solid became a tesseract.

## The axis table

| Dim | Axis | Geometry | Mechanism | The decision that opens it |
|-----|------|----------|-----------|----------------------------|
| 1D | Order | line | serial dependency | "this comes after that" |
| 2D | Breadth | plane | parallel independence | "these run at once" |
| 3D | Depth | solid | recursive nesting | "this node opens again inside" |
| 4D | Time | tesseract | iterative self-evolution | "run the whole thing again to grow it" |

## What makes a new axis new

A sweep is real only when the push direction is genuinely a new axis. The judge is
orthogonality: a repetition is a sweep to a new axis when, and only when, it
introduces an independence the existing axes cannot express.

- Order cannot express simultaneity. Placing independent flows side by side is a
  sweep to breadth, not more order.
- Breadth cannot express nesting. Seating a structure inside one cell is a sweep to
  depth.
- Depth cannot express change across time. Running the whole structure again is a
  sweep to time.

## Honest boundaries: not every repetition is a sweep

- A repetition that adds no new orthogonal axis is not a sweep. Doing the same task
  three times in a row is a longer line, not a plane. The test is always
  orthogonality: did a new independence appear.
- A sweep of length zero raises no dimension. A parallel with one branch is a line,
  not a plane. A recursion that never nests is a leaf, not a solid. A loop that runs
  once is a still photo of a solid, not a tesseract. A dimension is an axis you can
  sweep, not a cell you must always fill. This is an honest boundary, not a flaw.
- Sweep is a metaphor of generation, not of physical sliding. The rigor is in "new
  orthogonal degree of freedom plus self-similar trail," not in anything literally
  sliding.
