# Active VOLTERRA architecture

Canonical contract: [GOAL_UPD.md](../GOAL_UPD.md). Current application status: **NOT_IMPLEMENTED**. The package currently implements scaffold/control inspection only.

## Flow and ownership

```text
authorized archive / live receipt / explicit synthetic world
 -> evidence + instrument registry + as-of snapshot + target/maturity engine
 -> event beliefs + expectations + physical/evidence/propagation state
 -> cheap eligibility/policy/budget guard -> selected numerical specialists
 -> actual forecast store -> post-inference arbitration
 -> distributions + verified time/instrument/world dependence + calibration
 -> sealed forecasts + episode/cascade queries + conditional research watches
 -> observation-aware coverage and permitted monitoring/acquisition
 -> new evidence / new snapshot / new forecast version

matured outcomes -> proper scores -> versioned approved state / shadow challengers
 -> reviewed promotion and reversible future manifests
```

| Future owner under `src/volterra/` | Responsibility | First tickets |
|---|---|---|
| `contracts`, `instruments`, `targets` | Safe typed identities, units, calendars, estimator, labels/maturity and capabilities | VT01–VT02 |
| `storage`, `evidence`, `policy` | SQLite control/audit/jobs/budgets, revisions, as-of snapshots, permissions and dispatch guard | VT02 |
| `fixtures`, `cascades` | Seeded known worlds and exact reference; later fitted shared-driver/outcome queries | VT03, VT12 |
| `models`, `distributions` | Classical/checkpoint/ESS forecasts, measurement links, mixtures, calibration and paths | VT04, VT06–VT07, VT11 |
| `forecast_store`, `evaluation` | Sealed base outputs, scores, replay, ablations, grouping, confirmation and receipts | VT05, VT08, VT20–VT21 |
| `ess`, `scenarios` | Safe graph compiler/filter, conditional/intervention semantics and immutable branches | VT09 |
| `events`, `expectations` | Resolvable definitions, clocks/vintages, event forecasts and monitor observation laws | VT10 |
| `coverage` | Fixed-query incremental useful coverage, monitor budgets and watch plans | VT13 |
| `arbitration`, `selection` | Actual-output pooling versus cheap pre-inference execution policy | VT14–VT16 |
| `acquisition`, `learning` | Bounded investigations, time-matched revisions, outcome memory and promotion | VT17–VT18 |
| `service`, `ui` | CLI/durable local jobs and computed workbench | VT08, VT19 |
| `options` | Optional read-only economic experiment with exact quotes/contracts | VT22 |

These are planned ownership boundaries. The scaffold deliberately does not ship empty forecast adapters or create a fake implemented package for each name.

## Boundaries

Use a modular monolith, Python 3.12 CPU reference, transactional SQLite metadata, content-hashed Parquet arrays and DuckDB analytical reads when their dependencies are tested. Isolate incompatible numerical workers; load large models sequentially initially. Keep source/data/model entitlements independent.

The deterministic call guard exists before any provider path. The learned selector only chooses among already permitted specialists/actions. Cached output identity includes target, origin, scenario/conditionality, graph, transforms, calibrator, dependence and model artifact revisions. New evidence or a manual assumption creates a new version, never an overwritten official forecast.

An unconditional expert is stacked once. Conditional-world fusion uses a coherent outer world mass and inner expert weights; a marginalized expert cannot pretend to be conditional. Joint paths preserve shared worlds and model identity. Independently calibrated marginals do not imply a joint distribution.

A research watch references event beliefs, exposure/response forecasts, monitor observations, expiry/non-propagation rules and later score records. It is a joined workflow, not an independent source of probability or permission. Preparing a watch does not enable an external recurring job.
