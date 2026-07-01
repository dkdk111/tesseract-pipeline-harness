# 08_llm_freeform: a live-model run (captured)

This is the one example produced by a real model, end to end, from a free-form goal
with nothing declared. It closes the loop the other demos leave open: both the
structure inference and the leaf work are done by a live model, not the heuristic and
the simulator.

- `prompt.txt`: the plain-English goal handed to the harness (no axes declared).
- `tesseract.json`, `trace.md`, `output.md`: the captured result.

What the model did here:

1. Read the prose and inferred the work's nature (the `LLMPlanner` seam).
2. The engine's `plan()` turned that nature into a structure. The model opened
   order, breadth, and time, and correctly did NOT open depth, because it judged
   nothing oversized. That restraint is the point: genuine self-design opens exactly
   the axes the work needs.
3. The engine executed the four axes for real and the model did each leaf's work (the
   `LLMWorker` seam). `output.md` is the actual launch-plan draft it produced.

## How to run one live

    export TESSERACT_LLM_PROVIDER=anthropic   # or gemini, openai
    export ANTHROPIC_API_KEY=...               # the matching provider key; never committed
    python -m tesseract_pipeline think --llm --file examples/08_llm_freeform/prompt.txt \
        --out examples/08_llm_freeform

The provider is selectable; the default is Anthropic (`claude-opus-4-8`). See
`tesseract_pipeline/llm.py`. Because a live model is non-deterministic, a re-run will
produce different (equally valid) output than the capture committed here.

## Why it is separate from the gallery

The gallery (`python -m tesseract_pipeline gallery`) is deterministic and keyless, so
it only includes the reproducible demos. This example is a live-model capture: it is
non-deterministic and needs a key, so it is committed as a reference and is not
re-run in CI or the gallery. Re-running it will produce different (equally valid)
output.
