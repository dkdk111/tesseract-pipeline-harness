"""Sketch: make leaf work real by plugging a model into the harness.

The harness executes the four axes (order, breadth, depth, time) for real. Only the
leaf content is simulated by default. To make the leaves real, subclass Worker and
call your model. Nothing here commits keys; the model call is left as a stub so the
file is safe to read and copy.

Run shape (after you fill in a real client):

    from tesseract_pipeline import Box, Executor, plan
    from tesseract_pipeline.trace import write_trace

    task = {...}                      # your task's declared nature
    box = Box.load("box.config.json")
    root = plan(task, box)            # self-design (unchanged)
    Executor(LLMWorker()).run(root)   # execution with real leaves
    write_trace(root, task["goal"], box, ".tesseract/my-run")

Because the worker is the only thing that changes, the four axes, the sweep, and the
box stay exactly as they are in the keyless demo. That is the point of the seam.
"""

from __future__ import annotations

import os

from tesseract_pipeline.worker import Worker


class LLMWorker(Worker):
    """Example worker that would call a model at each leaf.

    Reads the API key from the environment; never hard-code or commit a key. If no
    key is set, it raises, so a misconfigured run fails loudly instead of silently
    falling back.
    """

    def __init__(self, model: str = "your-model-id"):
        self.model = model
        self.api_key = os.environ.get("YOUR_PROVIDER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Set YOUR_PROVIDER_API_KEY in the environment to use LLMWorker, "
                "or use the default SimulatedWorker for a keyless run."
            )

    def run(self, goal: str, context: str = "") -> str:
        prompt = _leaf_prompt(goal, context)
        # Replace the next line with a real client call, for example an Anthropic or
        # OpenAI SDK request that returns the model's text.
        raise NotImplementedError(
            "Wire a real model client here. Prompt was:\n\n" + prompt
        )


def _leaf_prompt(goal: str, context: str) -> str:
    parts = [f"Do this leaf task and return only its result.\n\nGoal: {goal}"]
    if context.strip():
        parts.append("\nContext from earlier steps:\n" + context.strip())
    return "\n".join(parts)
