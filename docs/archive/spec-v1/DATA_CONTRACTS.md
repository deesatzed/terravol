# VOLTERRA — Data contracts and runtime interfaces

Version 1.0 · The JSON schemas in `schemas/` are a minimal machine-readable subset, not the entire application database.

## 1. Identity and storage

Use stable internal IDs, never a ticker alone as a permanent instrument identifier. Instruments carry asset class, exchange, currency, timezone, session calendar and adjustment convention. Futures include root, contract month and actual underlying ID. Options include strike, call/put, expiry, multiplier, exercise and settlement conventions and last-trade time.

SQLite stores transactionally consistent control metadata and audit events. Parquet stores large bars, features and forecast paths. DuckDB reads analytical snapshots. Every referenced artifact is content-hashed. The application has one durable job queue table; retryable jobs have idempotency keys.

Recommended logical tables: `instrument`, `contract_spec`, `evidence_event`, `evidence_revision`, `evidence_dependency`, `feature_snapshot`, `target_definition`, `target_observation`, `model_manifest`, `graph_version`, `forecast`, `forecast_artifact`, `decision`, `budget_reservation`, `outcome_score`, `scenario_branch`, `promotion`, `evaluation_run` and `audit_event`.

Foreign keys and append-only semantics are required. Corrections append superseding records, not in-place changes to what a prior forecast saw. A scored outcome correction must preserve both the original score and the correction history.

## 2. EvidenceEvent

Required fields: `evidence_id`, `instrument_id`, `event_time`, `published_at`, `available_at`, `ingested_at`, `availability_basis`, `source_id`, `source_uri`, `content_sha256`, `revision_id`, `status`, `unit`, `value`, `dependency_group`, `synthetic` and `provenance`.

`event_time` is when the observed phenomenon occurred. `published_at` is when this exact revision was released, where known. `available_at` is the earliest usable time under the declared source/vendor policy. `ingested_at` is when this installation recorded it. All timestamps include offsets and are stored normalized to UTC with original exchange timezone retained at the instrument level.

`availability_basis` is `live_observed`, `certified_archive`, `assumed_archive` or `synthetic_fixture`. In strict live mode, ingestion/receipt must precede use. In certified historical replay, import can occur later, but the verified historical availability must precede origin. Assumed archives are excluded from confirmatory as-of claims unless their uncertainty policy is prespecified.

`status` may be observed, missing, unavailable, stale, contradictory or assumed. Missing and unavailable values are null. Observed zero is a number with an explicit unit. Observation-error metadata can refer to a separate likelihood model; it does not overwrite the raw observation.

News assertions reference a source span, extraction method and dependency cluster. Do not store provider secrets in URIs. A source correction references the superseded revision. A consumer reconstructs the evidence set by revision availability, not the most recent current value.

## 3. FeatureSnapshot

Contains `snapshot_id`, `forecast_origin`, eligible evidence IDs, feature-definition hashes, fitted-transform hashes, availability policy, instrument/calendar metadata and rejected-evidence reasons. Fitted transforms record the maximum available label/input time used during fitting.

A snapshot is sealed before inference and reused by every comparator that is supposed to have identical information. Long-history analogy lookup uses a snapshot-limited view. A synthetic vs real flag propagates through derived features and cannot be cleared by an adapter.

## 4. ForecastDistribution

Contains `forecast_id`, `instrument_id`, `origin`, `issued_at`, `snapshot_id`, `model_manifest_id`, `graph_version`, `calibration_id`, `target_version`, `status`, `synthetic`, `horizon_forecasts`, `joint_path_ref`, `capabilities`, `actual_model_ids`, `failed_model_ids`, `quality_flags` and `revision_parent_id`.

Each horizon forecast includes future target interval, horizon in sessions, annualization convention, variance quantiles, supported mean, annualized-volatility quantiles, representation and missing-capability reasons. Quantile levels must be ordered and unique; values must be monotone. Unsupported means are null with a reason; do not put zero in a field that was not computed.

For joint paths, the manifest includes axes, sampling weights, path count, random seed, dependence-adapter ID, posterior version, support checks and numerical diagnostics. Simulation precision and predictive interval coverage are different fields.

A distribution may be `marginal_only`, `joint_native` or `joint_coupled_validated`. Only the last two permit path-dependent claims. A survival head with independent validation has its own capability flag; it does not silently grant general joint-path capability.

`status`: `OK`, `DEGRADED`, `ABSTAINED`, `INSUFFICIENT_DATA` or `FAILED`. Successful fallback returns `DEGRADED` unless the frozen policy explicitly accepts that reduced ensemble as a named model. Every failed model and its failure reason remain visible.

## 5. GraphSpec and NodeSpec

Graph-level fields: immutable graph ID/version, prior version, domain adapter, node list, edge list with time lag, rule-set version, inference backend, approved function registry and causal-status declaration.

Node-level fields: ID, role, unit, support, distribution family, parameters or parameter references, prior provenance, origin of numerical values, observation status, effect-lag scope and whether the node is editable. Directed within-time cycles are invalid; positive-lag feedback is unrolled explicitly. Every distribution family has its own parameter/support validator.

Possible families include Gaussian for unconstrained/log states; lognormal/gamma for positive states; beta for uncertain Bernoulli probabilities; categorical for regimes; Dirichlet/logistic-normal for a probability simplex; and finite-variance Student-t for return innovations. There is no universal “range and median” constructor.

A deterministic node names an audited function; it never contains executable source code. The backend adapter rejects unsupported graph structures instead of guessing a sampler. Mixed discrete/continuous inference requires explicit marginalization/filtering/sampling design.

## 6. DecisionState / DecisionResult

A State Builder output declares its criterion, permitted action IDs, evidence and forecast references, unknowns, data-quality issues, bounded context and cost envelope. The result identifies the selected allowed action, reason codes, model version, calibration status, estimated cost, and policy approval.

A decision score is separate from the probability that a market event occurs. Optional token scores are raw model diagnostics until a validated mapping exists. Return `ABSTAIN` when option-order instability, missing required evidence or unsupported questions prevent a trustworthy selection.

Permissions are external to the model. The dispatcher verifies them again after the model responds. The budget service reserves a worst-case upper cost bound before dispatch and reconciles after completion; unknown pricing is ineligible when it prevents enforcing the cap.

## 7. OutcomeScore and strategy memory

An outcome joins exactly one original forecast ID and target version. It records label ID, maturity time, scored time, metric version, reference-model ID, score, uncertainty where estimated, and correction lineage. Unmatured labels cannot influence weights, retrieval or calibration.

Learning episodes carry asset/horizon/context and sample support. Acquisitions include selection probabilities when used for bandit/off-policy evaluation. Record failed attempts and the realized cost. An unqueried expensive expert has no measured counterfactual performance unless a separate audit run actually computed it.

## 8. ScenarioBranch

Required: branch ID, official parent forecast, graph version, changed nodes, operation type, author, reason, timestamp, inference manifest and branch result. Operation types are `condition_on`, `override_assumption`, `remove_evidence` and `intervene`.

A hypothetical branch is marked `scenario`, even when it begins from real evidence. Do not use branch outputs as observed training labels. An intervention requires an explicit structural model and causal-status notice. User edits cannot change historical prices, the official outcome, permissions or the test split.

## 9. OptionsResearchResult

Contains forecast reference, snapshot timing, strategy policy ID, contract IDs, quote IDs, entry/exit rules, pricing model assumptions, fee/funding schedule, payoff scenarios, realized evaluation if available and exclusion reasons.

Statuses: `NOT_ASSESSED`, `INSUFFICIENT_DATA`, `NO_SUPPORTED_EDGE`, `RESEARCH_CANDIDATE`. Avoid turning a candidate into an order or personalized recommendation. The core API has no execution endpoint.

## 10. Proposed API surface

These endpoints are design contracts, not implemented services:

- `POST /v1/forecasts`: immutable forecast job from an instrument, origin and manifest.
- `GET /v1/forecasts/{id}`: retrieve forecast, status, lineage and capabilities.
- `GET /v1/evidence/{id}`: evidence and source/revision history subject to entitlements.
- `POST /v1/scenarios`: validated branch operation.
- `GET /v1/scenarios/{id}`: branch/official comparison.
- `POST /v1/replays`: frozen, declared evaluation run.
- `GET /v1/replays/{id}`: all run artifacts and failed/abstained origins.
- `GET /v1/models`: versioned capability/license registry.
- `POST /v1/promotions/proposals`: shadow candidate proposal, not automatic approval.
- `GET /v1/health`: component availability, data freshness and resource health.

All writes accept idempotency keys. Async jobs are durable status records with logs and cancellation, not promises by an agent. Local operation is default; authentication and source entitlement checks are required before any remote exposure.
