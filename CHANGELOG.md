# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Demo gallery: six examples across distinct domains and structural signatures
  (research, devops, data/etl, writing, localization, maintenance), each committed
  with its generated trace. New `tesseract gallery` command prints a comparison
  table of which axes each demo opens.
- Human approval gate in the engine: a task unit can declare `"approval": true`, and
  the executor holds that leaf instead of running it, marking it in the trace and
  render. Demonstrated by `02_software_release` (deploy).

### Notes

- `05_bulk_translation` demonstrates the max_breadth wall (surplus branches queued,
  not dropped). `06_quick_fix` demonstrates restraint: no axis opens for a one-line
  job.

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
