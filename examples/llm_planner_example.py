"""Sketch: infer structure from a raw goal with a model instead of the heuristic.

`tesseract_pipeline.infer` ships a deterministic, keyless inferer that recognizes a
handful of prose patterns. That is real (raw text in, four-axis structure out) but
intentionally limited. For open-domain goals, a model should read the goal and
propose the structure. That is what this file sketches. No keys are committed; the
model call is a stub.

The seam is small: a planner turns text into a task dict, and the rest of the
harness (`plan`, `Executor`, the box, the trace) is unchanged. Compare with
`llm_worker_example.py`, which makes the *leaves* real; this makes the *self-design*
real. Together they close the loop: a model reads a raw goal, proposes the four-axis
structure, and does the leaf work, all inside the human's box.

    from tesseract_pipeline import Box, Executor, plan
    from tesseract_pipeline.trace import write_trace

    box = Box.load("box.config.json")
    task = LLMPlanner().infer("Ship a competitive brief and keep refining it.")
    root = plan(task, box)          # the box still constrains the model's proposal
    Executor().run(root)
    write_trace(root, task["goal"], box, ".tesseract/llm-run")
"""

from __future__ import annotations

import json
import os

from tesseract_pipeline.infer import Planner

_SCHEMA_HINT = """
Return ONLY JSON describing the work's nature, using these keys:
  goal (str), and optionally:
  iterative (bool) + rounds (int)   when the work needs revision passes,
  sequence [units]                  when steps depend on each other,
  parallel [units]                  when branches are independent,
  oversized (bool) + parts [units]  when a piece is too big to handle flat,
  approval (bool)                   when a leaf is high-risk or irreversible.
A unit is the same shape recursively. Do not name axes; declare the nature.
"""


class LLMPlanner(Planner):
    """Example planner that would ask a model to infer the structure of a goal."""

    def __init__(self, model: str = "your-model-id"):
        self.model = model
        self.api_key = os.environ.get("YOUR_PROVIDER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Set YOUR_PROVIDER_API_KEY to use LLMPlanner, or use the keyless "
                "HeuristicPlanner / infer_task for deterministic inference."
            )

    def infer(self, text: str) -> dict:
        prompt = f"Read this goal and return its nature as JSON.\n\nGoal: {text}\n{_SCHEMA_HINT}"
        # Replace with a real client call that returns the model's JSON text.
        raise NotImplementedError("Wire a model client here. Prompt was:\n\n" + prompt)

    @staticmethod
    def _parse(model_json_text: str) -> dict:
        return json.loads(model_json_text)
