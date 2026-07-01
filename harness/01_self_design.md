# 01. Self-design: how you decide the structure

In a classic pipeline, a human fixed the structure at design time. Where to
parallelize, how many times to recurse, these were constants baked into code, and
execution followed them. This harness removes the baked rule. With no rule baked in,
you decide the structure at runtime by reading the nature of the work.

This is the real novelty the harness enacts: dimensionality stops being a constant a
human sets and becomes a runtime output of the model. Your first output at a node is
a shape, before it is content.

## The input at a node

At each node you hold exactly three things:

1. The goal that came down from the level above.
2. The box the harness drew (`box.config.md`): allowed axes and their limits.
3. The context so far.

Holding these, your first act is not to process the goal. It is to ask the goal four
questions.

## The four questions

Ask them in order. The first that fits, and the limits allow, is the axis you sweep.
More than one can fit; then the outer structure takes the outermost fit and inner
nodes take the rest as you recurse.

1. Does this work have front-to-back dependency between steps, where a later step
   must consume an earlier step's result?
   Yes: sweep Order. Lay the steps in a line.

2. Does this work split into independent branches that do not wait on each other
   (for example, summarizing three separate sources)?
   Yes: sweep Breadth. Fan the branches into a plane.

3. Is some part of this work too large to handle in one pass, so that it must open a
   smaller structure of its own in place?
   Yes: that node is a seed, not a leaf. Sweep Depth.

4. Is one pass enough, or must you look at the result, revise, and run the whole
   thing again?
   Not enough in one pass: sweep Time. Run the structure in rounds.

If none fit, the node is a leaf. Do the work directly. Leaving it a leaf is a real
decision, not a skipped one.

## The decision is local, recursive, incremental

You do not draw the whole plan at once. You cannot: the nature of substructures you
have not opened yet is unknown until you open them. So you read only this node's
nature, make one move, and at each child that move created, you ask the four
questions again from the start. The full structure is a chain of local moves, not a
single blueprint from an all-seeing designer.

This is why there is no central plan and yet a coherent whole emerges. Each node
reads its own nature honestly; a shared goal and a shared schema make the scattered
local moves compose into one structure. Design without a designer.

## The output is structure before content

When you meet a goal, the first thing you emit is not the answer. It is a proposal
of shape: "this work looks like this." Real work happens only at the leaves of that
shape. Record the shape (the axis and the reason) in the trace before you execute.

## Good decision equals honest structure

Good here does not mean absolute optimum. A good decision is one where the structure
matches the real nature of the work: an honest structure.

- Bind independent branches into an order, and you are needlessly slow.
- Fan dependent steps into breadth, and the result breaks.
- Leave a large thing as a leaf, and it collapses because you cannot swallow it whole.
- Split a small thing into a seed, and you pay cost for nothing.

Good self-design is not opening many axes. It is opening exactly as many as the
work's nature needs. The virtue of a decision is honesty, not cleverness.

## Where the decision goes wrong

- Misreading the nature. With no baked rule, you can propose a wrong reading with
  confidence. This is not caught inside the decision procedure. It is caught by the
  verify wall in `02_the_box.md`, which re-examines the structure adversarially.
- The cost of deciding. Deciding also costs time. Asking all four questions in full
  before a one-line goal is over-design at the decision layer. For a simple goal,
  one line is the answer.
- Confusing decision with execution. A proposed structure is an unverified
  hypothesis. Drawing a blueprint and the blueprint being right are different things.
  The proposal is not a guarantee; execution and verification judge it afterward.
