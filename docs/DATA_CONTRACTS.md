# Active data-contract implementation map

Authoritative minimum fields and semantics: [GOAL_UPD.md](../GOAL_UPD.md) §§3, 5, 7–15. This document maps them to implementation work. The existing root `schemas/*.json` and `examples/*.json` remain **v1 package fixtures**; they are not complete v2 runtime schemas. Implement typed runtime schemas/migrations at VT01 and persistence/integrity at VT02.

## Storage invariants

- Stable internal instrument/event/target IDs; ticker or scenario title alone is not identity. Preserve exact futures contract, calendar, delivery/settlement, adjustment and nonpositive-price policies.
- Append evidence/score corrections with superseding lineage. Enforce foreign keys and verify actual content-addressed artifacts, not just reference strings.
- Separate physical occurrence, publication/availability, system receipt, model completion and outcome maturity. Live and certified historical replay use different explicit policies.
- Seal origin snapshots before inference. Every learned transform records eligible fitting inputs/labels and their maximum availability/maturity. All comparators sharing information use the same snapshot.
- Derived synthetic/scenario flags are monotone over lineage. Missing, unavailable, stale, contradictory, censored and assumed cannot become observed zero.
- Unknown finite means, unsupported joint output and missing archive/counterfactual results are null/reason states, never invented numbers.

## Object ownership

| Object | Required semantic distinction | First owner |
|---|---|---|
| EvidenceRecord / artifact payload | Exact raw revision, source rights/span/dependency, typed scalar/array/category payload and immutable hash | VT01–VT02 |
| AsOfSnapshot / TargetDefinition | Eligible revisions and fitted transforms versus a versioned future estimator/window/maturity | VT01–VT02 |
| EventDefinition / event instance / EventBelief | Frozen resolvable question versus a particular occurrence and its origin-time forecast | VT03, VT10 |
| ExpectationRecord | Own forecast, market survey and labeled proxy are separate; first release surprise respects recorded expectations | VT10 |
| TransmissionEdge / conditional forecast | Baseline hazard, lag, severity/context, buffer/interactions, fitted support and uncertainty; association versus identified causal effect | VT09–VT12 |
| ScenarioWorldBatch / JointPathArtifact | Shared world IDs, latent/parameter draws, axes, weights, support and finite dependence diagnostics | VT07, VT12 |
| ForecastDistribution / ArbitrationDecision | Actual producers and available CDF/quantile/path capabilities; combination semantics and q-versus-weight identity | VT04–VT07, VT14–VT15 |
| SelectionDecision / budget reservation | Cheap feature lineage, permitted/eligible versus selected pool, worst-case costs and audit propensities | VT02, VT16 |
| OutcomeRecord / ScoreRecord | Resolved/first-public-known/matured/corrected values and real versus synthetic origin; score joins immutable forecast and target | VT02, VT05 |
| RevisionContract / PromotionRecord | Precommitted inquiry and time-matched control versus a later reviewed version/rollback | VT17–VT18 |
| CoveragePlan / ConditionalResearchWatch | Fixed query, canonical outcomes, incremental usable detection coverage and monitor policy; no trades | VT13 |
| ExperimentManifest | Frozen pool, sources, targets, origins, budgets, grouping, attempted configurations and consumed holdouts | VT05 onward |

## Added concrete contracts

`MonitorObservationSpec` references source/purpose permission, upstream dependency group, monitored event/claim, region coverage, cadence, observation/confirmation error model, publication/receipt/processing latency, outage/missingness behavior, deadline and costs. Unknown laws remain explicitly unassessed. Fit or assume these laws with provenance; do not turn missing observations into negative evidence.

`EventState` has independent physical-phase and evidence-status histories. `PropagationState` joins event, instrument, target definition and response window; buffered or resolved in one exposure does not modify another. Store state evidence and transition times with immutable lineage.

`EpisodeIdentityPolicy` freezes query-local target matching/deduplication. `EvaluationClusterPolicy` separately groups overlapping forecasts/shared real episodes for uncertainty estimation. Neither may rewrite an earlier origin's threshold/label or manufacture additional independent episodes.

`SelectiveExpertAudit` records full-pool or randomized execution, actual forecast IDs, selection propensities where supported, cost/latency and eligible outcomes. An unrun model has no observed counterfactual prediction; simulation estimates stay in a separate lane.

`ConditionalBranchFailure` retains affected world mass, actual fallback/remainder identity and diagnostics. A failed rare-risk branch cannot be silently discarded and the surviving mass renormalized into apparent safety.

All rules/function identifiers resolve to a trusted registry owned by code, not a caller-supplied list of executable text. Safe metadata is not an untrusted pickle loader.

## VT01 implemented local primitives

`volterra.contracts` now supplies immutable `EventProbability`, `TransmissionProbability`, `ScenarioProbability`, and `ExpertWeight` types so their numerical values cannot silently stand in for one another. `canonical_json` recursively rejects nonfinite values, including parsed exponent overflow. `QuantileForecast` is explicitly marginal-only: ordered sparse quantiles do not create a CDF tail or joint-path capability. `StudentTSpec` rejects nonpositive degrees of freedom or scale, and a consumer requiring finite variance must call `require_finite_variance`.

`CapabilityManifest` is a static typed claim record only. It does not establish an artifact's availability, license, resource behavior, model output or integration. Those checks remain VT06 work.
