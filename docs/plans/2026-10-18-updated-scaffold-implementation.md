# Updated VOLTERRA Scaffold Implementation Plan

> **For Codex:** Use the installed `executing-plans` skill when executing a later application plan task by task. This scaffold increment is executed in the current authorized workspace.

**Goal:** Deliver a consistent, inspectable project scaffold and a complete canonical `GOAL_UPD.md` without misrepresenting unimplemented application behavior.

**Architecture:** A Python 3.12 modular monolith will own the application; this increment supplies only project-control validation and a doctor entry point. JSON controls drive ticket/acceptance traceability; archived v1 documents preserve the original package.

**Tech Stack:** Python 3.12 standard library for scaffold commands/tests; pinned build tooling and jsonschema only for packaging and legacy contract validation. Statistical and ML dependencies are deferred until tested in their responsible tickets.

## Task 1 — Preserve inputs and establish authority

Create `docs/archive/spec-v1/` with every original manifest entry and verify its hash. Preserve `GOALn.md`, `voltupd.md`, `aXcupd.md` and the v2 summary. Create the active control files and canonical goal; make `GOAL.md` a pointer. Record authority, milestone, monitoring and roster decisions in `DECISIONS.md`.

## Task 2 — Build traceable controls

Create `config/implementation_queue.json`, `config/acceptance_matrix.json`, `config/offline.json`, `config/model_registry.json` and `config/project.json`. Retain all 100 v2 acceptance IDs and add explicit controls for the assessed gaps. Map each acceptance to its earliest ticket and intended test path; all application results start as not implemented.

## Task 3 — Test scaffold failure behavior before implementation

Create `tests/scaffold/test_cli.py`, covering controls through the public command boundary. Run with `PYTHONPATH=src python3.12 -B -m unittest discover -s tests/scaffold -v` and retain the expected missing-module failure before adding scaffold code. Then implement only `src/volterra/scaffold.py`, `__main__.py`, package metadata and entry-point configuration. Verify cycle/missing-reference rejection, safe defaults, no fabricated completion, doctor status, and nonzero failure exits.

## Task 4 — Document the complete application path

Create `docs/ARCHITECTURE.md`, `docs/DATA_CONTRACTS.md`, `docs/PROBABILITY_SEMANTICS.md`, `docs/WORKFLOWS.md`, `docs/BENCHMARK_PROTOCOL.md`, `docs/TRANSFORMATION_AUDIT.md`, `docs/STATUS.md`, `docs/ACCEPTANCE_MATRIX.md` and ownership notes in `src/volterra/README.md`, `tests/README.md` and `ui/README.md`. Update older root entry points to reference active documentation and archived v1 semantics.

## Task 5 — Verify and report

Run scaffold tests and both supplied commands, validate every local link and acceptance/ticket reference, verify archived v1 hashes, and reproduce the archived package-only validator without overwriting the old receipt. Record environment, results and remaining VT00 work in `PROGRESS.md` and `reports/scaffold/verification.json`. Initialize isolated VOLTERRA version control with donor/private/runtime exclusions if absent; never stage the donor subtree or secrets. Do not claim application readiness from scaffold checks.

## First application plan after the scaffold

VT01 closes finite-number and Student-t validation defects with failing regressions, then typed manifests/serialization. VT02 adds durable evidence/as-of/target/policy stores. VT03 supplies seeded worlds and exact enumerated cascade inference. VT04 adds genuine statistical forecasts and measurement-compatible residual distributions. VT05 seals forecasts, matures outcomes, scores them and replays the complete offline demonstration. Each task must have its contract, failure case, executed tests and result artifacts before completion.
