"""The worker: what actually runs at a leaf.

The executor decides the shape (order, breadth, depth, time). The worker does the
work at each leaf. It is deliberately pluggable so the harness can run with no keys
by default and with a real model when you want one.

- ``SimulatedWorker`` (default) produces deterministic, detailed mock content. No
  model, no network, no API keys. This is the "complete simulation" the repo ships:
  the four axes and the sweep are real and really executed; only the leaf content is
  synthetic.
- To make leaf work real, use ``LLMWorker`` from ``tesseract_pipeline.llm`` (a live
  model, provider-selectable), or subclass ``Worker`` and call your own model in
  ``run``.
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
    # Software / DevOps
    "build": [
        "Compiled and bundled from a clean checkout; artifact hash recorded.",
        "Build is green and reproducible.",
    ],
    "unit test": [
        "Unit suite passed; fast feedback on core logic.",
        "Coverage held above the agreed threshold.",
    ],
    "integration test": [
        "Integration suite passed against staging dependencies.",
        "Contract boundaries verified.",
    ],
    "end-to-end": [
        "End-to-end journeys passed on a production-like environment.",
        "No regressions in the critical user paths.",
    ],
    "package": [
        "Release artifacts packaged and signed.",
        "Version, changelog, and checksums attached.",
    ],
    # Data / ETL
    "validate": [
        "Nulls, duplicates, and out-of-range values flagged and quarantined.",
        "Row counts reconciled against the source.",
    ],
    "ingest": [
        "Source pulled incrementally since the last watermark.",
        "Schema and volume checks passed at the boundary.",
    ],
    "sessioni": [
        "Events grouped into sessions by inactivity gap.",
        "Session boundaries stable across reruns.",
    ],
    "dimension": [
        "User dimensions derived with slowly-changing history kept.",
        "Keys conform to the warehouse model.",
    ],
    "revenue": [
        "Revenue facts computed and reconciled to billing.",
        "Currency and refunds handled explicitly.",
    ],
    "load": [
        "Loaded idempotently; partitions swapped atomically.",
        "A downstream freshness signal was emitted.",
    ],
    # Writing
    "outline": [
        "A spine set from macro to micro before any prose.",
        "Each section earns its place against the chapter's claim.",
    ],
    "opening": [
        "Opens on the live question, not a definition.",
        "Earns attention before it asks for it.",
    ],
    "argument": [
        "The core claim stated, then pressured, then held.",
        "Objections invited rather than hidden.",
    ],
    "closing": [
        "Closes by handing the reader the next question.",
        "Recovers the chapter's spine in one line.",
    ],
    "draft": [
        "Drafted for thought, not decoration; one idea per paragraph.",
        "Voice kept plain and load-bearing.",
    ],
    "edit": [
        "Tightened for rhythm; even cadence broken on purpose.",
        "Cut what the argument did not need.",
    ],
    # Localization
    "translate": [
        "Rendered for meaning and register, not word for word.",
        "Idioms localized; terminology kept consistent.",
    ],
    # Small fixes
    "typo": [
        "The incorrect token located and corrected in place.",
        "No surrounding text touched.",
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
