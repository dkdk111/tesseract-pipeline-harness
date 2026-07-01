"""Infer a task's nature from a free-form goal, with no per-axis declaration.

The `planner` turns a declared nature into a four-axis structure. This module adds
the step before it: read a plain-English goal and *infer* that nature, so the human
does not hand-declare sequence/parallel/oversized/iterative. The output is a task
dict that `plan()` consumes.

This is a deterministic heuristic, on purpose. It recognizes a set of common prose
patterns and is intentionally limited; unusual phrasing falls back to fewer axes or
a leaf. Open-domain, robust inference is the job of a model: see `LLMPlanner` below
and `examples/llm_planner_example.py`. The point of this module is that a real code
path exists from raw text to a self-designed structure, honest about its ceiling.

Patterns recognized:

- Iteration -> Time:   "iterate twice", "3 rounds", "refine", "revise", "iteratively"
- Sequence  -> Order:  steps split on "then" and ";"
- List      -> Breadth:"gather X on A, B and C", "compare A, B and C"
- Breakdown -> Depth:  "break X down into A, B and C", "decompose X into ..."
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

_ITER_MARKERS = (
    "iterat",
    "refine",
    "revis",
    "polish",
    "keep improving",
    "loop until",
    "until it converges",
    "in rounds",
)

_LEAD_INS = r"on|for|across|of|over|covering|compare|comparing|among|between|into"


def infer_task(text: str) -> dict:
    """Read a free-form goal and infer a task dict (goal + declared-nature keys)."""
    text = " ".join((text or "").strip().split())
    if not text:
        return {"goal": ""}

    rounds, stripped = _extract_rounds(text)
    iterative = rounds is not None or _has_iter(stripped)
    body_text = _strip_iter_clause(stripped) if iterative else stripped

    steps = _split_steps(body_text)
    if len(steps) >= 2:
        node = {"goal": _label(text), "sequence": [_infer_unit(s) for s in steps]}
    else:
        node = _infer_unit(steps[0] if steps else body_text)
        node["goal"] = _label(text)

    if iterative:
        wrapped = {"goal": node["goal"], "iterative": True, "rounds": rounds or 2}
        for key in ("sequence", "parallel", "oversized", "parts"):
            if key in node:
                wrapped[key] = node[key]
        return wrapped
    return node


def _extract_rounds(text: str) -> Tuple[Optional[int], str]:
    low = text.lower()
    m = re.search(r"(\d+)\s*(?:rounds|times|iterations|x)\b", low)
    if m:
        return int(m.group(1)), re.sub(re.escape(m.group(0)), "", text, flags=re.I)
    for word, n in (("three times", 3), ("thrice", 3), ("twice", 2), ("once", 1)):
        if word in low:
            return n, re.sub(word, "", text, flags=re.I)
    return None, text


def _has_iter(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in _ITER_MARKERS)


def _strip_iter_clause(text: str) -> str:
    # Remove a trailing or embedded iteration clause like ", and iterate twice".
    t = re.sub(r",?\s*(?:and\s+)?(?:iterat\w*|refin\w*|revis\w*|polish\w*)[^,.;]*", "", text, flags=re.I)
    return " ".join(t.split()).strip(" ,.;")


def _split_steps(text: str) -> List[str]:
    parts = re.split(r"\bthen\b|;|\.\s+", text, flags=re.I)
    steps = []
    for part in parts:
        cleaned = _clean_step(part)
        if cleaned:
            steps.append(cleaned)
    return steps


def _clean_step(part: str) -> str:
    part = part.strip()
    part = re.sub(r"^(?:and|first|next|after that|finally|,)\s+", "", part, flags=re.I)
    return part.strip(" ,.;")


def _infer_unit(step: str) -> dict:
    step = step.strip(" ,.;")

    # Depth: "break X down into A, B and C" / "break down X into ..." / "decompose X into ..."
    breakdown = (
        re.search(r"break\s+(?:down\s+)?.+?\s+down\s+into\s+(.+)", step, flags=re.I)
        or re.search(r"break\s+down\s+.+?\s+into\s+(.+)", step, flags=re.I)
        or re.search(r"decompose\s+.+?\s+into\s+(.+)", step, flags=re.I)
    )
    if breakdown:
        parts = _split_list(breakdown.group(1))
        if len(parts) >= 2:
            return {"goal": step, "oversized": True, "parts": [{"goal": _cap(p)} for p in parts]}

    # Breadth: a list of independent branches.
    items = _extract_list(step)
    if len(items) >= 2:
        return {"goal": step, "parallel": [{"goal": _cap(i)} for i in items]}

    return {"goal": _cap(step)}


def _extract_list(step: str) -> List[str]:
    m = re.search(r"\b(?:" + _LEAD_INS + r")\s+(.+)", step, flags=re.I)
    tail = m.group(1) if m else step
    items = [i for i in _split_list(tail) if 0 < len(i.split()) <= 5]
    return items if len(items) >= 2 else []


def _split_list(text: str) -> List[str]:
    raw = re.split(r",|\band\b|&", text, flags=re.I)
    return [r.strip(" ,.;") for r in raw if r.strip(" ,.;")]


def _cap(text: str) -> str:
    text = text.strip()
    return text[:1].upper() + text[1:] if text else text


def _label(text: str) -> str:
    text = text.strip(" ,.;")
    return _cap(text)


class Planner:
    """Interface for turning a free-form goal into a task dict. Override ``infer``."""

    def infer(self, text: str) -> dict:
        raise NotImplementedError


class HeuristicPlanner(Planner):
    """The deterministic, keyless inferer above, wrapped as a Planner."""

    def infer(self, text: str) -> dict:
        return infer_task(text)
