# 02. The box: control that expands autonomy

A structure that knows how to grow must also know how to stop. A depth sweep with no
brake digs forever. A breadth sweep with no limit widens until resources burn out.
Control is what draws the box that the dimensions get drawn inside. It does not draw
the dimensions. You draw those. The human draws the box.

The paradox to hold: no control and self-design self-destructs by runaway; too much
control and self-design vanishes into a fixed pipeline. Mature self-design is the
narrow path between. The hand that draws the blueprint is the model's. The hand that
draws the box is the human's.

## The three walls

### Wall 1: Boundary (what may open, and how far)

The boundary sets which axes you may sweep and the ceiling on each: max depth, max
breadth, max rounds, budget. It lets you freely choose which axis to open, while
fencing how far that axis can reach. The live values for this repo are in
`box.config.md`. Read them at the start of every run. If an axis is forbidden there,
you do not open it, even if the work's nature would fit it; you fall back to an
allowed axis or a leaf, and you note the constraint in the trace.

### Wall 2: Stop (when to close)

Every sweep must pair with a stop condition. A sweep with no stop diverges.

- Order stops when the last dependent step completes.
- Breadth stops at max breadth; extra branches are dropped or queued, and the drop
  is noted, never silent.
- Depth stops at max depth or spent budget by forcing the node to become a leaf,
  even if it "wanted" to open further.
- Time stops when max rounds are used, when a round stops improving on the last (a
  dry round), or when the result has converged on the goal.

Stop is the anchor that keeps the generative force of sweep from diverging.

### Wall 3: Verify (what counts as passing)

A structure you propose is a hypothesis, and you can propose a plausible but wrong
one with full confidence. So verification does not stop at checking that output
matches a schema. It re-examines the structure itself, adversarially:

- Is this decomposition honest to the real nature of the work?
- Did I bind a false dependency into an order that should have been breadth?
- Did I over-split into depth that pays nothing?
- Did I leave something too large as a leaf?

This applies the principle "I can be wrong" to the design, not just the result. A
verify gate that passes everything is not a gate. It is a drawing of one. Run it for
real, before you build leaf work on top of the structure.

In engine mode this wall is code: `tesseract_pipeline/verify.py` re-examines the
structure for degenerate and unjustified shapes (a sweep with one branch, a
single-round time loop, a leaf with children, a node with no reason) before execution,
and `--strict` refuses a structure that fails. In agent mode you perform the same
re-examination yourself, in prose, before executing leaf work.

## Above the walls: the approval gate

For any action that is high risk, irreversible, or reaches outside this repository,
you do not self-design and you do not proceed on your own. You stop and request
explicit human approval first. This includes, at minimum:

- Moving money or making purchases.
- Sending messages, emails, or publishing anything externally.
- Deleting or overwriting files outside `.tesseract/`.
- Network calls with side effects.
- Any change that cannot be reversed.

The aim is not full delegation. It is alignment: separating where delegation is safe
from where it is not. Self-design is not the claim that everything goes to the model.
It is the claim that we sort what may be handed over from what may not.

## Why the box enlarges freedom

The clearer the walls (which sweeps are allowed, how far they reach, what passes),
the larger your freedom to open dimensions boldly inside them. When the walls are
sharp, you can propose structure daringly and the system can filter a wrong proposal.
Control is not the opposite of autonomy. It is its precondition.

## How the box fails

- Under-control. Loose walls and self-design runs away: bottomless depth, unbounded
  breadth, unverified structure stacking work on a wrong blueprint.
- Over-control. Walls so tight that nothing is left for you to decide. Every axis
  pre-fixed by the human is no longer self-design, just a fixed pipeline. This
  failure is as common as runaway and quieter: it looks safe, but the concept is
  dead inside it.
- Paper control. Stop conditions and verify gates that exist on paper but never
  actually fire. A wall is a wall only when it really blocks.

## How dimensions collapse (so the walls know what they guard)

Failure is not random. Each axis fails in its own shape, and the three walls each
target one root failure:

- No stop. Depth digs forever, time loops forever. The Stop wall guards this.
- Dishonesty. A false dependency serialized, an over-split that pays nothing, a
  structure that lies about the work. The Verify wall guards this.
- Confident error. A wrong structure proposed without doubt and executed as if true.
  The Verify wall and the approval gate guard this together.

Read collapse backward and it tells you exactly what each wall is for.
