# Operator Operating Defaults

> Read this after `AGENTS.md` and `harness/box.config.md`, before self-designing.
> This is a **self-design bias, not a wall.** The box (`box.config.md`/`.json`) is
> the human's and **wins on any conflict.** This file only shapes *how* you
> self-design inside the box, so the run reflects the operator's judgment.
>
> Derived from `.tesseract/operator-profile/profile.md` (v0.3). When the profile
> changes, update these defaults to match.

When you take any task in this repo, bias your self-design as follows.

1. **Anti-waste is the objective.** Optimize for *waste avoided*, not *effort
   spent*. The operator's satisfaction tracks motion saved, not hours logged.

2. **Default to iterative refinement, not one-shot perfection.** On non-trivial
   work, open the **Time** axis by default: ship a first pass, then revise. A
   rough-but-revised pass serves the operator better than a perfect one-shot that
   arrives late or never.

3. **Modulate first-pass fidelity by slack** (the operator's perfectionism setpoint
   is a function of slack, not a fixed point):
   - **Time pressure** signaled (deadline, "quick", "just do X", urgency) → take the
     best choice *at this level*, ship fast, queue the refinements.
   - **Slack** signaled (no deadline, "make it great", exploratory) → pursue the
     best; expand depth/breadth further.
   - **Unknown** → assume moderate pressure: one solid pass plus one revision round.

4. **Decompose to find true independence; expert-expand the seeds — but stay in the
   box.** Respect `max_depth`/`max_breadth`, and never open an axis the work does
   not need. A genuinely one-line task stays one line. (Over-decomposition is the
   operator's own flagged failure mode.)

5. **Reify on the 3rd friction, not the 1st.** Do not build a reusable tool on first
   sight — premature abstraction is waste. Abstract when repetition *itself* becomes
   the waste: roughly the 3rd recurrence, or the moment you notice you are
   re-deriving the same thing from scratch.

6. **Every time-stop leaves a revisit hook.** When you ship at "good enough for now,"
   explicitly record *what was deferred* and *the condition to revisit it*. An
   un-revisited deferral is hidden debt — the exact waste the operator hates, only
   invisible. (`box.config` requires every sweep to pair with a stop; this adds that
   the stop must name its follow-up.)

7. **Reject on sight (the operator's "no"):** redundant re-derivation from scratch,
   an obviously suboptimal choice when a better one was cheap, and busywork that
   dodges the real reassembly. Synthesis is where value lives — do not stop after
   the split.

8. **Leave the *why* and the *no* in the trace.** Record not just what you did, but
   why, and what you rejected. That record is how this profile keeps learning the
   operator toward higher fidelity.
