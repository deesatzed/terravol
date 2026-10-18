# VOLTERRA engineering standards

Scope and completion contract: [GOAL_UPD.md](GOAL_UPD.md). Decisions: [DECISIONS.md](DECISIONS.md). These rules govern application implementation; the current scaffold does not yet implement that application.

## Repository and ownership

- Preserve unrelated work. Use the VOLTERRA root as the application workspace; `aXc-ace-forecaster/` is a read-only donor and excluded from source control/build inputs. Never restore its dirty files or import private datasets, environment files or serialized models.
- Keep one canonical goal and one machine ticket/acceptance source. Preserve old documents in the verified v1 archive. Record real contradictions and scope changes in the decision log.
- Keep module ownership in `docs/ARCHITECTURE.md`. Implement the next dependency-eligible increment; do not create duplicate systems beside verified working equivalents.

## Correctness, privacy and permissions

- Use finite, typed, unit-aware records and safe serialization. Reject exponent overflow, invalid distribution parameters, untrusted pickle and executable graph/document content.
- Append revisions and seal origin snapshots before inference. Enforce referential/artifact integrity and propagate synthetic/scenario lineage through every join/export.
- Implement target/calendar/measurement contracts before adapters. Missing, censored, stale, zero, unavailable and unsupported are distinct.
- Permissions, allowlists, budgets and maturity are deterministic controls. Build the dispatcher guard at VT02 before runtime external calls; paid allowance and offline networking default to zero/disabled. Development package installation is not permission for application data/model retrieval.
- Keep raw restricted data outside the repository. Code, weights and data rights are independently enforced. Never add brokerage credentials, execution endpoints or automated financial actions.

## Forecasting and learning

- Preserve output support, distributions, actual producer/fallback identity, parameter uncertainty and joint capabilities. Marginal outputs cannot answer path queries.
- Separate event probability, conditional transmission probability, world mass and expert weight. Never count duplicate reports as independent events or shared outcomes twice.
- Store physical, evidence and per-instrument propagation state separately. Monitoring value requires an observation/receipt model and useful lead time.
- Score matured observed outcomes only. Unrun experts have missing counterfactual forecasts. Charge full-pool audits and preserve supported propensities.
- Fit every learned stage chronologically on eligible earlier data; use same-information/same-budget controls. Negative and inconclusive results retain the simpler incumbent.

## Tests and evidence

- Write a meaningful failing regression before fixing a defect or introducing numerical behavior. Preserve leakage, maturity, restart, permission and arithmetic tests.
- Run the smallest relevant tests first, then required integration/replay checks. Do not write tests merely to mirror trivial edits or inflate counts.
- Keep scaffold tests, package validation, synthetic application tests, real integration tests and scientific experiments separate. A planned test path is not a test; a skipped test is not a pass.
- Every completed ticket links changed interfaces, assumptions, executed commands/results, retained artifacts, failures and remaining capability limits. Never mark a ticket complete because documentation exists.

## Resources and UX

- Python 3.12/CPU is the reference. Pin actually tested dependencies and artifacts. Benchmark cold/warm loading, peak memory, latency and total setup/inference/acquisition costs; enable acceleration only after parity checks.
- CLI first, computed local workbench later. Graph edits must alter a validated numerical branch. Show conditioning, target, horizon, data mode, versions and unsupported states. Do not invent probabilities for empty views.
- Human approval is required for structural production promotion and enabling external monitoring jobs/cadence/budget, as specified by the goal. Routine reversible implementation within the authorized scope continues without repeated permission questions.

## Definition of done

The relevant code exists, success/failure behavior is exercised, required receipts are retained, ownership/contracts/docs match implementation, and earlier invariants remain intact. Report engineering, scientific, prospective and optional economic status independently.
