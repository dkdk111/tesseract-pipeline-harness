# .tesseract/ (agent working area)

This is where the attached agent writes its runs. For each task it creates a run
folder, for example `.tesseract/2026-07-01_market-brief/`, and writes `trace.md` and
`tesseract.json` there following `harness/03_trace_protocol.md`, plus any working
outputs for the task.

The agent keeps its work inside this directory unless a task explicitly says
otherwise. Files outside this repository are out of bounds without human approval
(see `harness/box.config.md`).

Run folders are ignored by git (see `.gitignore`); only this README is tracked, so
the working area stays in the repo without committing every run. To keep a run as a
demonstration, move it into `examples/` and commit it there.
