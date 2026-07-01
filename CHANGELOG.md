# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-01

### Added

- Live-model path: `tesseract_pipeline/llm.py` provides `LLMPlanner` (infer a
  structure from a raw goal) and `LLMWorker` (do real leaf work), selectable across
  providers (anthropic, gemini, openai) over the standard library only, no SDK. A
  `--llm` flag on `think` and `run` uses it; the provider is chosen with
  `TESSERACT_LLM_PROVIDER` and each provider reads its own key from the environment.
- `examples/08_llm_freeform/`: a captured live-model run that infers structure from
  prose and does real leaf work end to end. Kept out of the
  deterministic gallery and CI because it is non-deterministic and needs a key.

### Changed

- Output/trace note now distinguishes a live-model run from a simulated one.
- Removed the two placeholder LLM sketches under `examples/`, superseded by the real
  `llm.py` implementation.

## [0.2.0] - 2026-07-01

### Added

- Free-form self-design: `tesseract_pipeline/infer.py` reads a plain-English goal and
  infers its nature (no axis declared), with a new `tesseract think "<goal>"` command
  and a `07_freeform_inference` demo that opens all four axes from one sentence. A
  deterministic heuristic with an explicit `LLMPlanner` seam for open-domain goals.
- The Verify wall in code: `tesseract_pipeline/verify.py` re-examines a structure for
  degenerate or unjustified shapes before execution, surfaced in the run output and
  the trace, with a `--strict` flag to refuse a failing structure.

### Changed

- Time axis now has two real, reachable stop conditions: convergence (a round adds no
  improvement over the last) and the round limit. Removed the previously unreachable
  string-matched convergence branch (dead code).
- Output and render now state plainly that the structure and its execution are real
  while, under the default simulator, the leaf content is placeholder text.
- `docs/OVERVIEW.md`: a conceptual guide to what the harness means, where the
  meta-instructions live, and how agent mode and engine mode differ.
- Demo gallery: examples across distinct domains and structural signatures
  (research, devops, data/etl, writing, localization, maintenance, free-form), each
  committed with its generated trace. New `tesseract gallery` command prints a
  comparison table of which axes each demo opens.
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
