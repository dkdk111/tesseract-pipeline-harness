"""Live-model planner and worker, standard library only, provider-selectable.

The engine ships keyless: the default `HeuristicPlanner` infers structure from a
free-form goal by rule, and the default `SimulatedWorker` fills leaves with
deterministic placeholder text. This module is the real-model seam:

- `LLMPlanner` asks a model to read a raw goal and return the work's nature, which
  the engine's `plan()` then turns into a four-axis structure. This is genuine
  open-domain self-design, the step the heuristic cannot do.
- `LLMWorker` calls a model to do each leaf's actual work.

Only these two seams change; the planner's four questions, the executor's four-axis
execution, and the box are identical to the keyless path.

No SDK dependency: this calls each provider's HTTP API directly over urllib, so the
package stays dependency-free. Pick a provider with the `TESSERACT_LLM_PROVIDER`
environment variable (default `anthropic`); each reads its own key from the
environment and it is never stored, logged, or committed.

    provider   key env var                    default model
    anthropic  ANTHROPIC_API_KEY              claude-opus-4-8
    gemini     GEMINI_API_KEY / GOOGLE_API_KEY  gemini-2.5-flash
    openai     OPENAI_API_KEY                gpt-4o-mini

Override the model with `TESSERACT_LLM_MODEL`.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .infer import Planner
from .worker import Worker

_API_VERSION = "2023-06-01"

_DEFAULT_MODELS = {
    "anthropic": "claude-opus-4-8",
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4o-mini",
}


def _provider() -> str:
    return os.environ.get("TESSERACT_LLM_PROVIDER", "anthropic").lower()


def _model() -> str:
    return os.environ.get("TESSERACT_LLM_MODEL") or _DEFAULT_MODELS.get(_provider(), "")


def _require(env_names) -> str:
    for name in env_names:
        value = os.environ.get(name)
        if value:
            return value
    raise RuntimeError(
        f"Set {' or '.join(env_names)} to use the live-model path. The default "
        "HeuristicPlanner and SimulatedWorker need no key."
    )


def _post(url: str, body: dict, headers: dict) -> dict:
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST")
    for key, value in headers.items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:  # pragma: no cover - network path
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"{_provider()} API error {exc.code}: {detail}")


def call_model(system: str, user: str, max_tokens: int = 1024, json_mode: bool = False) -> str:
    """One request to the selected provider. Returns the model's text.

    json_mode asks the provider to guarantee a valid JSON object where supported
    (Gemini, OpenAI); on Anthropic the prompt does the constraining.
    """
    provider = _provider()
    if provider == "anthropic":
        return _call_anthropic(system, user, max_tokens)
    if provider == "gemini":
        return _call_gemini(system, user, max_tokens, json_mode)
    if provider == "openai":
        return _call_openai(system, user, max_tokens, json_mode)
    raise RuntimeError(f"unknown TESSERACT_LLM_PROVIDER: {provider!r} (use anthropic, gemini, or openai)")


def _call_anthropic(system: str, user: str, max_tokens: int) -> str:
    payload = _post(
        "https://api.anthropic.com/v1/messages",
        {
            "model": _model(),
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
        {
            "content-type": "application/json",
            "x-api-key": _require(["ANTHROPIC_API_KEY"]),
            "anthropic-version": _API_VERSION,
        },
    )
    parts = [b.get("text", "") for b in payload.get("content", []) if b.get("type") == "text"]
    return "".join(parts).strip()


def _call_gemini(system: str, user: str, max_tokens: int, json_mode: bool = False) -> str:
    key = _require(["GEMINI_API_KEY", "GOOGLE_API_KEY"])
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{_model()}:generateContent?key={key}"
    generation_config = {"maxOutputTokens": max_tokens}
    if json_mode:
        generation_config["responseMimeType"] = "application/json"
    payload = _post(
        url,
        {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": generation_config,
        },
        {"content-type": "application/json"},
    )
    candidates = payload.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts).strip()


def _call_openai(system: str, user: str, max_tokens: int, json_mode: bool = False) -> str:
    body = {
        "model": _model(),
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    payload = _post(
        "https://api.openai.com/v1/chat/completions",
        body,
        {
            "content-type": "application/json",
            "authorization": "Bearer " + _require(["OPENAI_API_KEY"]),
        },
    )
    choices = payload.get("choices", [])
    if not choices:
        return ""
    return (choices[0].get("message", {}).get("content") or "").strip()


_PLANNER_SYSTEM = """You read a goal and describe the NATURE of the work as JSON, so a
separate engine can decide how to structure it. Do NOT name axes or mention order,
breadth, depth, or time. Use only these keys:

- goal (string, required)
- iterative (bool) + rounds (int): when the work needs revision passes
- sequence (list of units): when steps depend on each other, kept in order
- parallel (list of units): when branches are independent and could run at once
- oversized (bool) + parts (list of units): when a piece is too big to handle in one
  pass and must open its own smaller structure
- approval (bool): when a leaf action is high-risk, irreversible, or reaches outside
  the working repository (deploying, sending, paying, deleting)

A unit has the same shape recursively: a goal, optionally with the keys above. A
simple task is just {"goal": "..."}. Open only what the work genuinely needs; do not
over-decompose. Return ONLY the JSON object: no prose, no explanation, no code fence."""


def _parse_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return json.loads(text)


class LLMPlanner(Planner):
    """Infer a task's nature from a free-form goal, using a live model."""

    def infer(self, text: str) -> dict:
        return _parse_json(call_model(_PLANNER_SYSTEM, f"Goal: {text}", max_tokens=1500, json_mode=True))


_WORKER_SYSTEM = (
    "You perform one small leaf task and return only its result. Be concise and "
    "concrete. No preamble, no restating the task, no meta-commentary."
)


class LLMWorker(Worker):
    """Do a leaf's real work with a live model."""

    def run(self, goal: str, context: str = "") -> str:
        user = f"Task: {goal}"
        if context.strip():
            user += "\n\nContext from earlier steps:\n" + context.strip()[:4000]
        return call_model(_WORKER_SYSTEM, user, max_tokens=700)
