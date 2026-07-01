# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-01

### Added

- Working engine that self-designs a task along four orthogonal axes and executes
  it: `planner` (the four-question self-design), `executor` (real order, breadth,
  depth, and time execution), pluggable `worker` (deterministic simulator by
  default, no keys), `box` (boundary, stop, verify, approval gate), and `trace`.
- Command line interface: `tesseract demo`, `tesseract run`, `tesseract render`,
  `tesseract new`. Also runnable as `python -m tesseract_pipeline`.
- Deterministic, keyless demonstration: a bundled market-brief example that opens
  all four axes, with committed trace artifacts and a terminal renderer.
- Agent-mode operating law (`AGENTS.md`, `CLAUDE.md`) and the harness reference
  (`harness/`) so a coding agent can self-design free-form tasks against the same
  ontology and box.
- Test suite (standard library `unittest`) and CI across Python 3.9 to 3.12.
