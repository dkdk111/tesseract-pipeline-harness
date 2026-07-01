"""The worker: what actually runs at a leaf.

The executor decides the shape (order, breadth, depth, time). The worker does the
work at each leaf. It is deliberately pluggable so the harness can run with no keys
by default and with a real model when you want one.

- ``SimulatedWorker`` (default) produces deterministic, detailed mock content. No
  model, no network, no API keys. This is the "complete simulation" the repo ships:
  the four axes and the sweep are real and really executed; only the leaf content is
  synthetic.
- To make leaf work real, subclass ``Worker`` and call your model in ``run``. See
  ``examples/llm_worker_example.py`` for a sketch (no keys committed).
"""

from __future__ import annotations

import hashlib
import textwrap


class Worker:
    """Interface for leaf work. Override ``run``."""

    def run(self, goal: str, context: str = "") -> str:
        raise NotImplementedError


# Deterministic canned findings, keyed by a keyword in the goal, so the simulated
# brief reads like real material while staying fully reproducible. Dimension
# keywords are listed before competitor names so that "Notion pricing tiers" reads
# as pricing, not as a duplicate of the Notion summary.
_FRAGMENTS = {
    "product": [
        "Product surface spans documents, databases, and collaborative views.",
        "Feature depth is the moat; onboarding cost is the tax.",
    ],
    "pricing": [
        "Free tiers are the funnel; value gates sit at team and sync features.",
        "Per-seat pricing dominates; flat plans read as premium.",
    ],
    "features": [
        "Databases, links, and sync are the axes of differentiation.",
        "Extensibility (plugins, API) separates power tools from simple notes.",
    ],
    "positioning": [
        "The field splits into all-in-one, own-your-data, and networked-thought.",
        "Messaging clarity, not feature count, tends to decide adoption.",
    ],
    "notion": [
        "Positioned as an all-in-one workspace: docs, wikis, projects, and databases.",
        "Pricing spans a free personal tier up to business and enterprise seats.",
        "Breadth is the selling point and the risk: powerful, but a steep first hour.",
    ],
    "obsidian": [
        "Local-first Markdown vault with a strong plugin ecosystem.",
        "Free for personal use; paid sync and publish add-ons.",
        "Owns the power-user, own-your-data niche.",
    ],
    "roam": [
        "Bidirectional links and the daily-notes graph as the core loop.",
        "Premium positioning with a flat subscription.",
        "Defined the networked-thought category, now contested.",
    ],
}

_GENERIC = [
    "Key points gathered and organized for this goal.",
    "Findings are consistent with the brief's scope.",
]


class SimulatedWorker(Worker):
    """Deterministic content generator. Same input, same output, always."""

    def run(self, goal: str, context: str = "") -> str:
        lower = goal.lower()
        bullets = None
        for key, frags in _FRAGMENTS.items():
            if key in lower:
                bullets = frags
                break
        if bullets is None:
            # Stable pseudo-selection from the generic set, keyed by the goal.
            digest = int(hashlib.sha256(goal.encode("utf-8")).hexdigest(), 16)
            count = 2 + (digest % 2)
            bullets = [_GENERIC[i % len(_GENERIC)] for i in range(count)]

        lines = [f"### {goal}"]
        lines.extend(f"- {b}" for b in bullets)
        if context.strip():
            # Later rounds carry a review forward; reflect it so iteration is visible.
            note = _first_line(context)
            if note:
                lines.append(f"- (revised in light of: {note})")
        return "\n".join(lines)


def _first_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return textwrap.shorten(line, width=80, placeholder="...")
    return ""
