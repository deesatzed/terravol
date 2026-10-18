# VOLTERRA

Local-first research into external events, market-volatility transmission, dependent cascades and outcome-grounded allocation of forecasting expertise.

**Current delivery: project scaffold and canonical build contract. The forecasting application is not implemented.** The only supplied commands inspect/validate the scaffold; they do not produce forecasts or start monitoring.

## Start here

Read [GOAL_UPD.md](GOAL_UPD.md), then [STANDARDS.md](STANDARDS.md), [IMPLEMENT.md](IMPLEMENT.md), [DECISIONS.md](DECISIONS.md), [PROGRESS.md](PROGRESS.md) and [TASK_QUEUE.md](TASK_QUEUE.md). The goal preserves the full event/cascade/arbitration/monitoring program and resolves the prior authority and dependency conflicts.

## Run the scaffold without installing dependencies

Python 3.12 is the reference:

```bash
PYTHONPATH=src python3.12 -B -m volterra doctor --profile offline
PYTHONPATH=src python3.12 -B -m volterra scaffold validate
PYTHONPATH=src python3.12 -B -m unittest discover -s tests/scaffold -v
```

These commands require only Python's standard library and make no network calls. `--root PATH` selects another control workspace. A zero exit means scaffold validity, not application readiness. Invalid controls exit 2; application commands are explicitly unavailable.

For the locked development/package environment:

```bash
uv sync --locked --python 3.12
uv run --locked volterra doctor --profile offline
uv run --locked volterra scaffold validate
```

Initial environment installation may download permitted development packages. It does not enable application network access, source retrieval, model downloads or spending.

## Implementation gates

Integrity foundations: VT00–VT03. First genuine scored offline slice: VT04–VT05. Numerical/path replay and external-checkpoint integrations have separate gates. Then build one contract-specific gas/weather/transmission experiment, dependency-aware cascades and watches, same-pool arbitration/selection, bounded investigation/learning and a computed workbench. Scientific and prospective results have their own evidence requirements. Options research is optional and contains no trading execution.

The [application acceptance matrix](docs/ACCEPTANCE_MATRIX.md) contains 120 planned requirements with first-owner tickets and future test paths. Scaffold tests and legacy package checks never count as executed application acceptance.

## Preserved sources

The exact original v1 package and manifest are in [docs/archive/spec-v1](docs/archive/spec-v1/GOAL.md). `GOALn.md`, `voltupd.md`, `aXcupd.md`, the v2 summary and assessments remain provenance. The nested `aXc-ace-forecaster/` is a read-only donor, excluded from the new package/repository. No donor datasets, credentials, serialized models or old performance claims are application assets.

Current source ownership: [architecture](docs/ARCHITECTURE.md). Runtime/data contracts: [contracts](docs/DATA_CONTRACTS.md). Actual workflow availability: [workflows](docs/WORKFLOWS.md). Evidence: [status](docs/STATUS.md) and [scaffold verification](reports/scaffold/verification.json).
