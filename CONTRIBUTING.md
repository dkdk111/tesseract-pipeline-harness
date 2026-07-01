# Contributing

Thanks for your interest in the Tesseract Pipeline harness. This project is small,
dependency-free, and meant to stay legible. Contributions that keep it that way are
very welcome.

## Ground rules

- The library uses the Python standard library only. Please do not add runtime
  dependencies without opening an issue first.
- Tests run on `python -m unittest` (also standard library only). Every change to
  the engine should come with a test.
- Keep the ontology faithful. The four axes (order, breadth, depth, time), the
  single sweep operation, and the box (boundary, stop, verify, approval gate) are
  the spine of both the book and this code. Changes to their meaning need a strong
  reason in the pull request.

## Development

    git clone https://github.com/dkdk111/tesseract-pipeline-harness.git
    cd tesseract-pipeline-harness

    # run everything, no install and no keys needed
    python -m unittest discover -s tests -v
    python -m tesseract_pipeline demo

    # optional: install the console script
    python -m pip install -e .
    tesseract demo

## What is easy to contribute

- New example tasks under `examples/` that exercise the axes in a different shape.
- A new provider for the live-model path (`tesseract_pipeline/llm.py`), or a real
  `Worker`/`Planner` subclass for one.
- Docs and clarity fixes.

## Pull requests

- Keep the diff focused. One idea per pull request.
- Run the tests and the demo before opening the request.
- Describe which axis or wall your change touches, and why.

## Reporting issues

Use the issue templates. A minimal `task.json` that reproduces the behavior is worth
more than a long description.
