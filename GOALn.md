# GOAL — Transform VOLTERRA into an Event-Conditioned Volatility and Cascade Intelligence System

**Version:** 2.0  
**Specification date:** October 18, 2026  
**Delivery type:** Implementation contract for Codex or another coding agent  
**Status:** Requirements and research directions, not a claim that the application or experiments have been completed  
**Primary environment:** One Mac M4; local-first, CPU-capable; optional explicitly budgeted external inference  
**Primary scientific objective:** Improve calibrated forecasts of volatility, event propagation, and downstream episode timing—not directional stock-price prediction.

> Build a system that anticipates external developments, estimates how they can propagate into market volatility, identifies genuinely distinct precursor opportunities, and learns which forecasting methods and investigations are useful before, during, and after each cascade. Every published probability must come from a traceable numerical model or an explicitly labeled assumption. Every improvement claim must survive a declared comparison against simpler methods.

---

## 0. Instructions to the implementing agent

This file is the authoritative **transformation contract**, not a request for another conceptual architecture proposal. Implement the missing capabilities in dependency order, test them, and leave a usable application. Do not stop after creating folders, mock screens, a README, or a collection of adapter stubs.

**First inspect the existing VOLTERRA project.** Preserve working implementations, public interfaces, user changes, useful tests, and immutable records. Classify each requirement as `VERIFIED_PRESENT`, `PARTIAL`, `ABSENT`, `BROKEN`, or `BLOCKED`, with file and test evidence. Implement the gaps rather than duplicating completed work. When no application exists, create a clean VOLTERRA project and explicitly record that this is a new implementation.

This version supersedes the earlier GOAL.md and incompatible proposals. It retains compatible scientific safeguards from the v1 design, build plan, science specification, and reuse audit. Do not silently overwrite or erase those documents. Reconcile them into versioned project documentation and record conflicts in an architecture decision record. In particular, the expanded event/cascade workflow and explicit arbitration experiments below replace a generic “add more models” roadmap.

The following distinctions are mandatory:

- A specification requirement is not an implemented feature.
- A successful schema check is not an end-to-end test.
- A synthetic experiment is not financial evidence.
- A numerical forecast is not a trade recommendation.
- A published paper's result is not a reproduced VOLTERRA result.
- A model name is not proof of available weights, local compatibility, licensing, or a supported output capability.

References `[S01]`–`[S27]` in Section 25 document selected research and capability checks. They are implementation starting points, not permission to install every referenced system. Recheck the exact revision and terms before integrating any artifact. No component is mandatory merely because its benchmark rank is high.

### 0.1 First work product and first executable result

Produce `docs/TRANSFORMATION_AUDIT.md`, then a minimal offline vertical slice that:

1. Loads a seeded synthetic market-and-event world.
2. Creates an as-of evidence snapshot.
3. Produces a baseline volatility forecast and an exact small-graph cascade probability.
4. Saves both with explicit synthetic provenance.
5. Advances replay time, reveals outcomes, and records proper scores.
6. Demonstrates that neither future data nor synthetic consensus can update real outcome-based reliability.

Do not require paid data, downloaded model weights, a cloud account, or an LLM to pass this slice. The full transformation continues through the milestones; this slice is not the final application.

---

## 1. Mission, stakeholders, and expected application

### 1.1 Mission

Transform VOLTERRA from a general volatility observatory into an integrated **event forecasting, transmission, cascade, and adaptive arbitration** research application. Forecast distributions over future variability and the timing of episodes. Connect those forecasts to inspectable evidence and conditional mechanisms. Determine whether added complexity is useful rather than presuming it is.

The primary operator is a technically capable researcher. The application must also support reproducible scientific review and clear inspection by a user who is not an expert in probabilistic programming. Coding agents need explicit contracts and acceptance gates. A possible later commercial deployment needs independent model, code, and data entitlements.

### 1.2 Questions the completed application must answer

1. How much volatility is likely over the next 1, 5, and 20 trading sessions?
2. Which external events or information releases could materially change that forecast?
3. What are their occurrence, timing, severity, cancellation, and resolution distributions?
4. Which downstream instruments or volatility episodes could be affected, with what delay?
5. Are several precursor scenarios independent, shared-driver, mutually exclusive, synergistic, or merely duplicate reports?
6. What is the joint probability of at least one qualifying downstream episode, or both specified episodes?
7. Which specialists were run, which received weight, and what past evidence supports their allocation?
8. Which additional observation would most improve the forecast under the current budget?
9. What changed after new evidence arrived, and did that revision improve subsequent scoring?
10. Does an optional, contract-specific options experiment show a supported edge, no edge, or insufficient evidence?

Answers must be computed from stored artifacts or explicitly unavailable. Never populate missing answers with decorative percentages.

### 1.3 Product boundaries

Core scope includes numerical forecasting, typed expert-system reasoning, event/cascade simulation, research monitoring plans, editable scenario branches, learned arbitration, and controlled outcome-grounded adaptation.

The optional economic module is read-only research. Exclude brokerage account linking, broker credentials, orders, autonomous trading, uncovered short options, and portfolio management. An internal return/displacement model for payoff research does not make stock-price targets the product's objective.

Do not build a universal real-time news platform, train a large foundation model from scratch, import an entire large agent framework, or make unrestricted reinforcement learning an MVP dependency.

---

## 2. Migration and reuse strategy

### 2.1 Audit before modification

Inspect repository layout, configuration, dependency files, schemas, persistence, active entry points, test coverage, and current data/model manifests. Record the current commit and dirty state. Run the smallest relevant existing tests before editing. Preserve unrelated work; do not reset or overwrite it.

For each verified implementation, link this contract to its existing module and tests. Mark tests that did not execute as not run. Inspect both a success path and a failure path for a claimed capability. Make state/schema changes through reversible, versioned migrations and backup checkpoints.

### 2.2 aXc-ACE source is a donor, not the application

The previous supplied audit concerns selected paths in `deesatzed/aXc-ace-forecaster` at commit `3bd39789c3811a5b437baf60a65de480aa0486bf`. It records architecture worth reusing and defects requiring replacement. It is not a fresh execution audit or proof that every workflow in that repository behaves identically. See source record `[V1]` in Section 25.

| Donor pattern | Transformation decision |
|---|---|
| Structured model adapters and ensemble records | Reuse the interface idea; preserve distributions and explicit capabilities. |
| SLSQP weight optimization | Retain as an optional optimizer for global/rolling baselines; SLSQP itself does not imply static weights. |
| Outcome feedback and strategy memory | Replace helpful/harmful coalition credit with paired proper-score records and delayed-label accounting. |
| AR(1) regime tags | Retain only as optional numerical features or a comparator, not the definition of a financial regime. |
| Historical Context Engine | Reuse historical analogy and explanation UX with strictly as-of retrieval. Historical percentile is not forecast confidence. |
| Typed prediction safety reports | Preserve the pattern; do not reject a large volatility forecast solely for exceeding recent/historical norms. |
| Chronos T5 point reduction and anonymous persistence fallback | Replace with distribution-preserving adapters and named fallback records. |
| Inspected target-including validation context | Replace with origin/target-indexed rolling replay; add a regression test. |
| Point-prediction spread labeled a 95% interval | Replace with predictive distributions and measured calibration. |
| Independent Beta weight specifications | Do not treat normalized Beta draws as the same marginals; use proper simplex treatment where needed. |

Do not transfer the reported 1.51% hospital-census MAPE, hospital weights, private clinical datasets, environment files, credentials, serialized training artifacts, or clinical plausibility policies. Reproduce any retained numerical claim independently. Preserve license notices for actual substantial code reuse.

### 2.3 Compatibility and historical records

Old forecasts must retain their original versions and interpretation. Do not retroactively replace old predictions with v2 outputs. Legacy intervals that cannot be justified as calibrated predictions must be labeled as such on import, not silently repaired into fictional historical forecasts. Separate code migration from a new scientific evaluation.

---

## 3. Scientific invariants and target definitions

### 3.1 Forecast variability, not a point-price direction

For an equity session with reliable intraday observations, an initial realized-variance estimator is:

```text
R_t = r_overnight,t^2 + sum_j r_intraday,t,j^2
V_t,H = sum_(k=1..H) R_(t+k)
annualized_vol_t,H = sqrt(A * V_t,H / H)
```

Use decimal log returns where valid and record `A`, initially 252 for the declared equity-session profile. Store squared-decimal-return variance internally and percentages only in presentation. A provider's annualized volatility series must be transformed using its documented convention, not guessed.

`R_t` is a measurement estimator, not direct observation of latent integrated variance. Record sampling grid, session boundaries, overnight treatment, corporate-action policy, missing-bar policy, and estimator version. With daily closes alone, label the result `daily_return_variance_proxy`. Do not score it as though it were the same intraday target.

Price gaps at splits or contract rolls are not automatically economic returns. Nonpositive commodity prices are not necessarily corrupt observations; log-return targets are invalid there. Use a declared contract-specific alternative target or mark that task unsupported. Never take absolute prices, silently clip, or discard the episode to obtain a favorable result.

### 3.2 Horizons and label maturity

Primary horizons are 1, 5, and 20 completed trading sessions after the forecast origin. Calendar time, trading time, and information availability are separate. Outcomes become eligible for learning only after their complete target window and declared publication/revision policy have matured.

A paper-replication task may use different horizons or a point-in-time target. Preserve its exact protocol under a separate task ID; do not compare unlike scores or silently change 22 days to 20.

### 3.3 Episode labels

Provide a versioned observable label rule, separate from latent regimes. Proposed initial rule:

- Freeze upper and lower thresholds at each origin using the preceding 252 eligible completed variance measurements, initially the 80th and 60th percentiles.
- Begin an episode at the first of two consecutive sessions above the upper threshold; the second session is required to confirm the label.
- End at the first of two consecutive sessions below the lower threshold, again retaining confirmation delay.
- Score isolated single-session jumps separately.
- Preserve already-active, left-censored, right-censored, and no-event states.

The trailing window and thresholds are research defaults to freeze before evaluation. Do not recompute an origin's threshold from its future outcomes. Do not call a hidden Markov state ground truth.

For onset time `T`, use `h_k = P(T=k | T>=k, I_t)` and `P(T<=H | I_t)=1-product_(k=1..H)(1-h_k)` under the declared discrete-time model. Future evidence is part of a scenario, not observed information at origin t.

### 3.4 Four different probability concepts

Maintain different fields and types for:

- `event_probability`: occurrence of an external or observed market precursor.
- `transmission_probability`: a downstream outcome conditional on specified precursor states and context.
- `scenario_probability`: mass assigned to a coherent joint world or a disjoint scenario partition.
- `expert_weight`: a model's allocation in a predictive mixture.

An 85% expert weight is not an 85% chance of volatility. A classifier token probability is neither one unless separately calibrated for that exact target. An LLM statement is evidence to assess, not a numerical likelihood.

### 3.5 Information integrity

No forecast, feature, scaler, calibration, analogous-event retrieval, event posterior, selector, or arbitrator may use information unavailable under the run's as-of policy. Future-known calendars are permitted; future outcomes are not. No full-sample regime smoothing, historical forecast replaced by later weather realization, revised macro data backdated to the observation month, or evaluated target inside its predictor.

Synthetic, scenario-simulated, assumed, and real observed data must remain distinguishable through all joins. Simulation cannot supply an official realized performance label.

---

## 4. Architecture and module ownership

Use a modular monolith with isolated numerical workers where necessary. Adapt the existing stack when it already satisfies the contract. For a new project, the reference stack is a Python 3.12-compatible core, SQLite control/audit state, Parquet numerical artifacts, DuckDB analytical queries, CLI, and later a local API with an interactive graph interface. Pin a tested dependency intersection; do not claim these dependencies have already been tested together.

```text
Authorized historical/live observations and synthetic fixtures
    -> Evidence ledger + instrument/calendar registry + as-of snapshot
    -> Target/feature builder + cheap state + deterministic eligibility rules
    -> External-event forecast + expectation tracker
    -> Shared-driver event worlds and cascade state
    -> Pre-inference selector + budget reservation
    -> Selected temporal, covariate, and ESS transmission specialists
    -> Event-conditioned numerical arbitrator
    -> Predictive mixture + validated dependence/path model + calibration
    -> Volatility, episode, and joint-cascade forecasts
    -> Scenario Coverage Planner + conditional monitoring plans
    -> Forecast/evidence/scenario/experiment interface

Permitted investigation -> new evidence -> new snapshot and forecast version
Matured observations -> score ledger -> strategy memory -> shadow challengers
    -> reviewed promotion/rollback -> future manifest

Optional options research consumes forecasts and observed quotes.
It cannot modify forecasts, outcomes, permissions, or evaluation definitions.
```

### 4.1 Suggested logical modules

```text
src/volterra/
  contracts/       evidence/        instruments/     targets/
  features/        events/          expectations/    ess/
  cascades/        scenarios/       coverage/        models/
  forecast_store/  arbitration/     selection/       distributions/
  acquisition/     learning/        evaluation/      options/
  storage/         service/
ui/
config/
docs/
tests/{unit,property,integration,replay,adversarial,contracts}/
```

These are ownership boundaries, not permission to create duplicate packages beside working equivalents. Record any mapping to existing modules in the audit.

### 4.2 Single-machine resource contract

CPU is the correctness reference. MPS, MLX, or other acceleration is optional only after capability and numerical-parity tests. Load large workers sequentially by default. Measure available memory, latency, artifact size, and startup cost; do not equate vendor GPU throughput with Mac performance.

Track setup/download costs, model loading, inference, feature computation, event-world simulation, and external acquisition separately. Report cold-cache and warm-cache operation. Use durable idempotent jobs, not an unnecessary distributed message bus.

---

## 5. Data contracts and provenance

Implement typed, versioned application schemas with support/units checks, not a loosely structured JSON bag. Persist immutable snapshots and content-addressed large artifacts. Required fields below are minimum contracts; create complete JSON Schemas and serialization tests during implementation.

| Object | Required identity and content |
|---|---|
| `EvidenceRecord` | ID, source ID, original-content hash/reference, event time, publication time, availability time, received time, vintage/revision, entitlement, observation state, dependency group, source span, supersedes/contradicts links. |
| `AsOfSnapshot` | ID, origin, live/replay policy, eligible evidence IDs and revisions, instrument/calendar versions, state/feature hashes, missingness and availability exclusions. |
| `TargetDefinition` | ID/version, estimator, units, target interval, sampling/session policy, horizon convention, episode rule, maturity/confirmation policy. |
| `EventDefinition` | Stable ID/version, resolvable question, entity/scope, states and thresholds, occurrence window, resolution source, outcome rule, cancellation/resolution rules. |
| `EventBelief` | Definition/version, origin, occurrence and no-event probability, conditional timing/severity/duration distributions, parameter uncertainty, evidence IDs, calibrated status, forecaster version. |
| `ExpectationRecord` | Event/instrument ID, expectation type, value/distribution, timestamp, provenance, survey versus own-model versus proxy label, uncertainty/availability status. |
| `TransmissionEdge` | Parent/child roles, lag/delay, conditional model, baseline hazard, interaction/buffer structure, context, fitted/prior status, uncertainty, training episode count and window, identification status. |
| `ScenarioWorldBatch` | ID, origin, external-event paths, shared latent draws, posterior/model version, weights, seed, scenario identity, residual/dependence version, time grid, convergence diagnostics. |
| `ForecastDistribution` | ID, origin/issued/completed times, snapshot/target IDs, actual model/version, conditionality, scenario ID if applicable, quantiles/CDF/samples capability, moments, units, calibration ID, fallback/failure lineage. |
| `JointPathArtifact` | World/sample IDs, time and instrument axes, daily variance paths, sample weights, dependence model, conditionality, derived episode IDs, numerical diagnostics. |
| `SelectionDecision` | Cheap-state hash, eligible pool, selected pool, excluded reasons, policy version, decision scores, cost estimates, budget reservation, randomized selection probabilities where used. |
| `ArbitrationDecision` | Actual successful forecast IDs, feature snapshot, task/context, combination semantics, expert weights, training cutoff, objective, global/shadow mode and state version. |
| `CoveragePlan` | Query, target definitions, episode deduplication policy, selected monitors, expected marginal coverage/lead-time utility, overlap/shared-driver diagnostics, monitoring costs, sensitivity results. |
| `RevisionContract` | Parent forecast, requested observation/action, possible findings, affected nodes, anticipated numerical revisions, estimated scoring benefit, cost, deadline, comparison/control definition. |
| `OutcomeRecord` | Event/target ID, realized value/state, outcome interval, observation versus first-public-knowledge times, maturity, source/vintage, censoring and correction status. |
| `ScoreRecord` | Forecast and outcome IDs, scoring rule/version, task window, scale normalization, event group, eligibility, cost, paired control, real versus synthetic provenance. |
| `ExperimentManifest` | Universe, origins, snapshots, model/graph/selector/arbitrator/calibrator hashes, splits, target versions, budgets, comparisons, seeds, environment, preregistration and holdout-use log. |
| `PromotionRecord` | Challenger/incumbent versions, fresh evidence window, test/results artifacts, reviewer/approval, scope, effective time, rollback reference and reason. |

Use UTC for storage and explicitly converted exchange/local times for display. An observation's occurrence timestamp does not establish publication or arrival time.

### 5.1 Live versus historical policy

In live mode, an item must actually have arrived before use. In replay, a historical import may be eligible through independently established historical availability plus a recorded latency policy. Today's import timestamp does not invalidate all historical data; an observation date does not certify vintage availability either.

Support `OBSERVED`, `MISSING`, `UNAVAILABLE`, `STALE`, `CONTRADICTORY`, `CENSORED`, and `ASSUMED`. Zero must remain a numerical observation, not a universal missing-value replacement.

Deduplicate upstream events as well as text. Three syndicated reports are not three independent event confirmations. Corrections create new versions and invalidate downstream lineage where applicable without deleting the earlier record.

---

## 6. Model portfolio and research-informed integration

### 6.1 Initial candidates and restrictions

Model adapters are required only for the committed core roster; optional models must not block the offline application. Record `BLOCKED` when a real adapter cannot run; never substitute a fake implementation under its name.

| Group | Candidate | Intended role and constraint |
|---|---|---|
| Mandatory numerical controls | Persistence, EWMA, Log-HAR, GJR-GARCH | Low-cost baseline skill; appropriate distributions or past-fitted residual models. |
| Mandatory simple mixtures | Equal valid-expert mixture; global fitted mixture; rolling fitted mixture | Isolate any benefit from context-aware arbitration. |
| Lightweight nonlinear control | Quantile gradient boosting; XGBoost or a compatible alternative | Same-evidence comparator for ESS and event features. |
| Initial foundation candidate | TTM | Lightweight temporal specialist; pin the exact revision and output representation. |
| First covariate challenger | Chronos-2 | Native past/future-covariate and multivariate support is documented; quantiles do not automatically supply joint paths. [S01] |
| Second covariate challenger | TimesFM 2.5 | XReg covariate pathway; Apache-2.0 weights documented. Do not imply native joint event modeling. [S02] |
| Optional cost control | Chronos-Bolt | Fast univariate-family comparator; native covariate capabilities differ from Chronos-2. [S01] |
| Optional temporal diversity | TiRex/TiRex-2, small Toto 2.0, Granite FlowState/PatchTST-FM | Audit the exact release, public feature support, license, and Mac execution before use. [S08,S10] |
| Restricted research alternatives | Moirai 2.0, downloaded TimesFM 3 weights | Disabled in commercial manifests unless exact terms explicitly permit the intended deployment. Moirai 2.0's paper treats multivariate tasks independently, not cross-variate forecasting. [S02,S09] |
| Later trained specialists | N-HiTS, N-BEATS, TFT, PatchTST, iTransformer, small Chroma-inspired portfolios | Each needs a specific unmet modeling need, a budget, and a simpler matched comparator. [S07] |

Chronos-2 and TimesFM 2.5 are priority additions, not declared winners. A model registry must not force all candidates to run for every instrument or origin. A newer checkpoint is a challenger, never an automatic replacement.

### 6.2 Capability manifest

Each artifact must declare exact model ID/revision/hash, code and weight licenses separately, redistribution/derived-artifact restrictions, library lock, precision/device support, resource profile, minimum history, maximum horizons, covariate semantics, output quantiles/support, multivariate-input capability, native joint-sampling capability, missingness policy, and known pretraining-overlap limitations.

`multivariate_input=true` does not imply `joint_predictive_distribution=true`. Quantiles from 0.1 to 0.9 are not a complete calibrated CDF and do not justify a 95% interval without an explicit, tested extension.

### 6.3 Methods to borrow, modify, and defer

| Research pattern | Required disposition |
|---|---|
| FFORMA | Implement feature-conditioned allocation as a reproducible challenger to equal/global/rolling mixtures. Identify the exact training objective rather than labeling any XGBoost classifier “FFORMA.” [S03] |
| Toto FnF | Borrow lightweight features, expert-conditioned weighting, and frozen reference forecasts. Do not reuse general-benchmark weights or rankings as financial evidence. [S04] |
| CastStar | Borrow cache/manifests and decoupled arbitration. The checked bundle is frozen inference material without its training data/code; implement our own fitting pipeline. [S05] |
| TeeMoE | Borrow separation of numerical aggregation from context processing and cross-fitted upstream forecasts. Add chronological and shared-event constraints. Full large-model refinement is optional. [S06] |
| Synapse | Compare predictive pooling and outcome-driven dynamic weighting. Do not let forward-simulated ensemble medians enter the real score ledger as observed outcomes. [S11] |
| Chroma | Test small specialist portfolios only after enough local training evidence and a compute-matched comparator exist. [S07] |
| Spatial/neighbor ensembles | Use lagged cross-series numerical baselines; do not call correlation a demonstrated cascade. |
| Context is Key | Use as a contextual-reasoning component benchmark, not proof of financial forecasting skill. [S12] |

### 6.4 Adapter protocol

Implement equivalent interfaces for `describe_capabilities`, `fit_or_load`, `forecast`, `save_manifest`, and `reload`. `sample_joint` and `forecast_conditional_worlds` are optional methods whose availability must match the manifest.

Every model must identify its actual fallback. A persistence output produced after a foundation-model failure receives persistence attribution, not the failed model's success credit. Save/reload parity tests must cover fitted parameters, transforms, calibrators, graph state, and model artifacts—not merely configuration dictionaries. An `arch` backend is a candidate for GJR-GARCH [S25]; pin and test its actual interface. SLSQP integration should follow the applicable SciPy contract [S26].

---

## 7. Distribution and joint-path layer

### 7.1 Predictive mixture semantics

The default marginal combination is:

```text
F_mix(y | I_t) = sum_m w_m(I_t) F_m(y | I_t)
w_m >= 0; sum_m w_m = 1
```

A CDF mixture, an average of quantiles, a weighted sum of random variables, and an average of point forecasts are different operations. Name the operation in the contract and score its actual output. Equal quantile weights must not be presented as a recovered continuous tail distribution.

For quantile-only experts, score supported quantiles/intervals or attach a separately fitted, validated monotone CDF-and-tail adapter. Record all extrapolation and support assumptions. Do not default to finite support at the 10th/90th percentiles and pretend tail risk vanished. Do not invent a log-density from sparse quantiles.

### 7.2 Joint distributions are a separate capability

A valid joint-path representation preserves dependence across time, instruments, event worlds, and shared shocks. Use a generative state-space model or an explicitly fitted dependence adapter, such as a residual-block/rank-copula model trained on eligible out-of-fold errors. The adapter itself must be benchmarked.

Select an expert for a whole joint path or use an explicitly fitted switching process. Independently choosing an expert for every instrument and horizon is not sufficient for joint-cascade probabilities. Scenario IDs and shared latent draws must survive aggregation.

Derive cumulative variance from the same nonnegative daily paths. It must be nondecreasing with horizon; annualized volatility need not be. Derive episode labels through the target engine, not a second incompatible threshold calculation.

A marginal-only model can be useful. Until joint support passes its tests, onset/duration and multi-market joint outputs must return `UNSUPPORTED_CAPABILITY`, not invented scenarios.

A return-volatility model such as GARCH does not natively provide the full distribution of an intraday realized-variance estimator. Use an explicitly fitted measurement/link model for that target, or retain a clearly labeled compatible point/mean baseline. Squared simulated daily returns must not silently substitute for a different intraday estimator.

Calibration can also break joint consistency. Calibrate a declared coherent model/path representation and recompute its derived probabilities, or label independently calibrated marginal/episode heads as separate diagnostics. Joint queries use one identified joint artifact, not an arbitrary collection of individually calibrated numbers.

### 7.3 Moments and uncertainty

Separate outcome uncertainty, parameter/model uncertainty, observation uncertainty, and numerical Monte Carlo error. Between-model spread is a disagreement diagnostic, not a prediction interval.

Use finite-moment models where consumers require moments. Exponentiating an unrestricted Student-t log-variance innovation need not yield a finite variance mean. Likewise, a finite-variance Student-t log-return does not guarantee finite expected terminal price after exponentiation. Use justified finite-moment constructions, tempered/bounded families with declared assumptions, or mark the consumer unsupported. Numerical Monte Carlo output is not proof that the population moment exists.

---

## 8. Expert-system responsibilities

### 8.1 Deterministic rules

Implement a small typed rule layer for schema, support, units, availability, contradiction handling, capability eligibility, licensing, budget, and permitted actions. CLIPS/clipspy can be an optional backend; ordinary audited predicates are sufficient initially.

Hard failures include corrupt inputs, invalid probability tables, impossible support, incompatible calendars/targets, failed inference, and unauthorized actions. An unusual forecast or a value beyond historical maxima is a quality/novelty flag, not automatically a hard failure.

Graph and rule editors must not execute arbitrary Python, shell commands, file operations, or network requests. Retrieved material is untrusted data, never instructions to the agent runtime.

### 8.2 Probabilistic graph and inference

Use an inference-library-independent graph representation. Distinguish observations, external events, latent drivers, exposure parameters, deterministic transforms, market-response states, and derived targets. Every edge has type, lag, provenance, uncertainty, and identification status.

Start with an exact finite-state reference graph for known-answer tests, then a small fitted continuous/hybrid specialist using PyMC where appropriate. Use a tested online filter or finite-state forward recursion for sequential updates; do not fit a new MCMC model for every incoming article. pgmpy can provide a discrete reference backend. [S13,S14]

Specify inference eligibility by graph structure. Do not apply NUTS to un-marginalized discrete variables or claim Gibbs supports arbitrary user graphs. Fit/monitor convergence, effective sample size, particle degeneracy, and posterior predictive behavior with declared thresholds.

Support conditional probabilities with multiple parents, shared causes, mutually exclusive branches, conjunctive triggers, buffers, inhibition, and termination. Permit time-lagged feedback through an unrolled temporal graph. Reject unsupported instantaneous cycles.

### 8.3 Scenario editor

Implement `condition_on`, `override_assumption`, `remove_evidence`, and `intervene` as different operations. Interventions require explicit structural/identification assumptions; otherwise provide conditional sensitivity and label it accurately.

Editing a median/range does not uniquely determine every distribution. Require needed parameters or a declared fitting convention with fit diagnostics. Validate support and correlation constraints. Each edit produces a branch with parent, author, reason, changed nodes, and version. Official forecasts and evidence remain unchanged.

---

## 9. External-event forecasting and market transmission

### 9.1 The three clocks

Model and display:

1. **Physical-event time:** when the underlying development occurs.
2. **Information time:** when relevant evidence becomes available to the system under its policy.
3. **Market-response time:** onset, duration, and decay of the modeled volatility response.

An expected physical delay does not prove an exploitable market delay. Prediction, occurrence, confirmation, and resolution are different states. A market may respond before the physical event or before our feed receives it.

### 9.2 Event families and first domain

Provide adapters for scheduled releases, physical developments, operational disruptions, and evolving policy/geopolitical events. Begin with **natural-gas weather and storage scenarios**, after instrument/target integrity is established; broader domains are extension contracts.

Use existing weather ensembles and archived runs rather than asking an LLM to replace physical forecasting. Use regression/nowcasting for scheduled numerical results, survival/state transitions for onset and persistence, and optional temporal point processes for irregular sequences. EasyTPP and chain event graphs are later research candidates, not required infrastructure. [S15,S16]

Every event question needs an observable resolution rule, window, version, and source. Keep no-occurrence, cancellation, and revision mass. Resolve events independently of whether a desired market reaction occurred.

A later LAMP-inspired retrieval challenger may propose candidate antecedents, retrieve supporting/contradicting observations, and score them through a learned event model. This borrows a research workflow, not a claim of market skill or permission for an LLM to invent a likelihood. [S27]

### 9.3 Event states and source uncertainty

Use at least `POSSIBLE`, `DEVELOPING`, `OCCURRED_UNCONFIRMED`, `CONFIRMED`, `PROPAGATING`, `BUFFERED`, `RESOLVED`, `CANCELLED`, and `EXPIRED` where appropriate. These are typed beliefs/observations, not a universal lifecycle that every event must follow.

Treat disputed observations through a measurement/evidence model. Do not force q=1 for a rumor. A confirmed event updates the applicable belief according to the resolution/observation policy. A model predicting an event does not make it observed.

### 9.4 Expectations and surprises

Store our event forecast separately from timestamped consensus, survey dispersion, or explicitly labeled market proxies. A surprise before a release is a distribution over possible deviations from the recorded expectation. After the release, evaluate against its first eligible vintage.

Do not call deviation from our model a “market surprise” without a market-expectation source. Missing consensus means the expectation gap is uncertain, not zero. Physical probabilities and option-implied prices differ in conventions and risk premia; do not translate an IV gap directly into event probability or guaranteed mispricing.

### 9.5 Transmission specialist

Fit how event paths, instrument-specific exposure, and current conditions change the volatility distribution. Candidate mechanism groups are event excitation, liquidity fragility, buffering capacity, and persistence/resolution. These are testable modeling assumptions, not automatically causal facts.

Use an out-of-fold temporal reference forecast as an offset where useful. Fit event corrections and their uncertainty on reference predictions created without their targets. Compare the ESS against an ordinary numerical model with the same evidence.

Unknown future covariates are sampled from event/world distributions and marginalized. Do not insert their point expectation as a known future fact or plug actual future weather/storage values into historical predictions. Calendar-known covariates remain a separate capability.

---

## 10. Dependency-aware Cascade Engine

### 10.1 First-class use case

The operator identifies several modest-probability precursors. Confirmation of one could make downstream volatility much more likely. The system must evaluate both separate opportunity sets and multiple routes into the same downstream outcome, while preserving their dependencies.

Represent shared drivers and shared outcome identities. Different stories about a storm, production outage, and shipping interruption may all be linked. Rewording a scenario or duplicating a feed must not increase the probability estimate.

### 10.2 Required query forms

Support explicit queries for:

- At least one precursor occurring.
- A precursor and a specified downstream episode occurring in the defined order/window.
- Both B and C following A, versus either B or C.
- At least one qualifying cascade among several scenario sets.
- A shared downstream outcome triggered through any of several routes.
- Number of distinct downstream episodes, joint affected instruments, onset delay, and duration.
- Downstream probability when a precursor is absent, confirmed, disputed, delayed, cancelled, or resolved.
- Absence of expected propagation by a given elapsed time.

Every query must name its target events, interval, order constraints, and deduplication rule. “85% chance of increased volatility” without those definitions is not a valid query.

### 10.3 Probability arithmetic acceptance fixtures

Use exactly these **synthetic assumptions**, not market estimates:

```text
For one scenario set:
  P(A)=0.30
  P(B|A)=0.85
  P(C|A)=0.85
For the independent reference case only:
  B and C are conditionally independent given A.
  Three complete scenario sets are independent of each other.
```

Required analytical answers:

```text
P(any A among 3)                     = 1 - 0.70^3
P(A and B)                          = 0.30 * 0.85
P(any A-and-B set among 3)           = 1 - (1 - 0.30*0.85)^3
P(A and B and C)                    = 0.30 * 0.85 * 0.85
P(any complete A-B-C set among 3)    = 1 - (1 - 0.30*0.85*0.85)^3
P(B and C | A), without independence = bounded by [0.70, 0.85]
```

For three perfectly coincident 30% precursors, `P(any A)=0.30`, not 0.657. For three mutually exclusive 30% precursors, `P(any A)=0.90`.

For one **shared** B, independent precursors, `P(B|any A)=0.85`, and `P(B|no A)=0`, require `P(B)=0.85*(1-0.70^3)=0.55845`. Do not use the separate-set formula.

For a single precursor with `P(B|not A)=0.10`, require `P(B)=0.30*0.85+0.70*0.10=0.325`. This is not the 0.255 probability of A and B together.

Unknown dependence must return bounds/sensitivity or an explicitly assumed joint model. Pairwise marginal correlations alone do not generally determine a multi-event joint distribution.

### 10.4 Learn links and their uncertainty

Estimate background hazard, conditional response, severity/context effects, delay, and resolution—not just a fixed arrow percentage. Include events with no response, negative evidence, and never-activated forecasts. Group repeated predictions from one event episode appropriately.

Use hierarchical shrinkage or another justified regularization toward baseline behavior for sparse event families. Record posterior/parameter uncertainty and sample support. A few observed successes cannot create certainty. Do not equate Granger-predictive structure with demonstrated intervention causality.

### 10.5 Coherent world simulation

For each world:

1. Draw parameter uncertainty and shared latent conditions under the fitted model.
2. Sample external event occurrence, severity, timing, and future information, preserving dependencies.
3. Generate instrument-specific volatility paths through the conditional response model.
4. Derive market-volatility episodes from those paths using the frozen target definition.
5. Evaluate the requested logical conditions and count each distinct outcome once.

Do not independently sample a future “B volatility episode” and a contradictory variance path. A finite-state episode-only reference is allowed as a separate capability; it must not claim continuous-path support. Future market-state feedback must use a consistent time-lagged generative model.

An expert forecast is not another independent evidence source. Do not feed the posterior back into the graph as a new observation.

### 10.6 Rare paths and numerical safeguards

Keep no-event and unmodeled/background risk. Pruning must preserve omitted probability mass in a documented remainder rather than renormalizing risk away. Importance or stratified sampling requires correct world weights, diagnostics, and effective sample-size reporting. More Monte Carlo draws reduce numerical error, not structural uncertainty or the need for real observations.

If a delay model is used, update the posterior when a downstream response fails to appear. Account for reporting delays and censoring; “not observed” is not necessarily “did not occur.”

---

## 11. Scenario Coverage Planner

### 11.1 Objective

Select a bounded set of **monitoring and research actions**, not trades. Optimize incremental coverage of distinct, relevant downstream episodes with useful lead time and acceptable evidence quality, net of monitoring cost.

For a set of monitors S, a reference objective is:

```text
U(S) = E_world[utility of distinct qualifying episodes detected through S]
       - monetary_cost(S) - latency_cost(S)
```

The event worlds are unchanged by choosing which ones to monitor. Selection changes our observation policy and coverage, not the world's event probabilities.

Store the utility definition, horizon, minimum useful lead time, episode identity rule, budget, and graph version. Do not optimize “something volatile somewhere” without relevance, calibration, and lead-time constraints.

### 11.2 Required comparisons and outputs

Provide forward search from a precursor and reverse search from a target instrument. Return marginal additional coverage, overlap/common-driver explanations, shared-outcome deduplication, no-cascade probability, and sensitivity to uncertain links.

Compare top individual probability, random eligible selection, cheapest-first, and dependency-aware greedy selection. Use exact enumeration for small candidate sets as a correctness comparator. Greedy selection is a heuristic when interactions break its required mathematical conditions; do not claim an approximation guarantee without verifying those conditions.

Avoid zero-cost duplicate scenarios, unlimited scenario expansion, and post hoc narrowing to a successful story. Log the original candidate universe, rejected candidates, selection version, and all monitored outcomes.

A displayed coverage probability is conditional on the model and query. It is not the probability of making money.

---

## 12. Event-Conditioned Forecast Arbitration

### 12.1 Separate selection from weighting

**Pre-inference selection** chooses which eligible specialists to run using cheap information already available. **Post-inference arbitration** combines outputs from the specialists that actually ran.

A selector using every expensive model's fresh prediction has not saved that inference cost. Maintain different feature contracts and cost accounting for the two stages. Features include their computation lineage and as-of availability.

### 12.2 Required arbitration controls

Implement and compare on the same frozen expert pool:

1. Equal-weight predictive mixture.
2. Globally fitted regularized mixture.
3. Rolling mixture fitted only to matured past outcomes.
4. FFORMA-inspired feature-conditioned allocation.
5. Event/cascade-conditioned allocation with shrinkage toward the simpler model.

SLSQP is an optimizer that may be used for appropriate global/rolling objectives. The experiment compares allocation policies, not an optimizer's age.

### 12.3 Features

Start with a compact, justified set: target/horizon, recent log-variance levels, volatility persistence, lagged jumps, known calendar distance, history length, data quality, past model scores, event probability and uncertainty, event stage, elapsed time since confirmation, predicted propagation delay, missing evidence, and shared-driver state.

Post-inference features may additionally include actual forecast spread and residual-family diversity. Disagreement is not a calibrated failure probability without validation. Do not put the realized future event label or target into a gating feature.

Apply identical past-only fitting rules to feature extraction, categorical encodings, learned embeddings, event forecasters, and arbitrator outputs. Multiseries cross-fitting alone is insufficient; enforce chronology and shared-event grouping throughout the stack.

### 12.4 Trainable objective and naming

A simple first challenger predicts per-expert out-of-fold proper losses with a regularized regressor and converts predicted losses to weights with a validation-selected temperature. Name this `loss_to_weight`, not an exact FFORMA reproduction.

A feature-softmax gate trained against a declared weighted-expert-loss surrogate can be labeled `fforma_inspired`; document that minimizing average individual expert losses is not necessarily the same as minimizing the proper score of the final mixture. A paper-exact reproduction requires its own implementation and protocol.

Add a low-capacity gate that directly minimizes the actual predictive mixture's proper score. For experts with sufficiently specified samples/CDFs, CRPS admits:

```text
CRPS(F_mix,y) = sum_m w_m A_m(y) - 0.5 * sum_m sum_n w_m*w_n B_mn
A_m(y) = E|X_m-y|
B_mn  = E|X_m-X'_n|
```

Here draws are independent for the expectation, including m=n. Use a documented numerical estimator, bounded memory, and derivative/known-answer checks. This is a proposed implementation choice, not a claim that the cited ensemble packages optimize this objective.

When only quantiles are supplied, use the supported score or explicitly fitted CDF adapter. A mixture's quantiles must come from the mixture, not be presumed equal to weighted component quantiles. Log score requires a validated density; do not fabricate it.

Fit temperature, regularization, feature selection, weight-change constraints, and calibration on strictly earlier validation data. Use uncertainty and shrinkage for rare stages. There is no hard-coded rule that an event must always increase ESS weight.

### 12.5 Scenario-aware fusion without double-counting

Support two explicitly different modes:

**Mode A — Unconditional predictive stacking (required first).** Each expert supplies `p_m(V|I_t)`, including any internal event marginalization. Combine once. Event probabilities may be gating features, but do not multiply the result by those probabilities again.

**Mode B — Conditional-world arbitration (required for the advanced cascade path).** Use a coherent external-world distribution and conditional-capable experts:

```text
p(V|I_t) = sum_s q_t(s) [sum_m w_m(s,I_t) p_m(V|s,I_t)]
```

The outer q is event/world mass; inner w is model allocation. Register disjoint scenarios or use weighted joint-world samples. Preserve no-event mass. Do not mix an already marginalized expert into each conditional branch as though it were a conditional model. A scenario-neutral baseline is allowed only with its invariance assumption declared and tested.

Training on completed historical outcomes is allowed under ordinary chronological training. A gate fitted using hindsight branch labels but presented with uncertain forecast branches at inference is a different model; prevent this train/inference mismatch through cross-fitted event beliefs and scenario integration. Oracle realized-branch experiments are diagnostic only.

Joint-path arbitration must keep shared world identity and dependence. Horizon-specific marginal gates remain marginal-only unless a compatible joint construction is supplied and verified.

### 12.6 No self-confirming learning

Never update real expert reliability using the ensemble median, another expert's forecast, an LLM critic's opinion, or a hypothetical branch as ground truth. Synapse-style simulated forward adaptation may exist only as a separately labeled research comparator that cannot mutate the official outcome ledger. [S11]

Consensus can be wrong. A minority event specialist must not be penalized merely for disagreeing before the observation matures.

---

## 13. Forecast store and outcome-grounded strategy memory

Store every requested origin, including failures and abstentions. Base forecasts are immutable and reusable for multiple gate experiments. Index at least by instrument, origin, target/version, scenario/conditionality, model revision, feature snapshot, and calibration version.

Cache keys must include all semantically relevant context, graph, scenario, covariance/dependence, and artifact revisions. Do not return an old conditional forecast for a changed branch because the numerical price history is unchanged. Record computation time separately from the simulated forecast origin.

Learning records must distinguish a model's standalone error, a coalition's score, marginal contribution under a paired comparison, and acquisition benefit. Do not give every member identical causal credit for one successful ensemble.

Model failures are excluded according to a declared fallback policy, with actual fallback forecasts scored separately. Losing models and negative findings remain in records. Score corrections create new versions; replay learning from the corrected evidence window rather than silently editing previously deployed states.

Automatic online parameter/weight updates may occur only under an approved fixed algorithm and schedule, with all input label IDs and state versions logged. Structural changes and new algorithms require shadow evaluation and promotion.

---

## 14. Bounded decisions, investigation, and revision contracts

### 14.1 Decision-model role

A Jev-style decision adapter or another compact classifier chooses only among permitted action IDs supplied by deterministic rules:

```text
PUBLISH_NUMERIC
FETCH_APPROVED_EVIDENCE
RUN_SPECIALIST
CHECK_DATA
ABSTAIN
STOP
```

No permission, external spending cap, graph authority, or trade capability may originate from the classifier. Record its model/version, prompt/schema, option IDs/order, raw scores, calibration status, and actual action. Test paraphrase, irrelevant-field, option-order, timeout, and invalid-output sensitivity.

LLMs can propose a resolvable event question, structured claims, candidate antecedents, or an approved source request. They do not directly write event probabilities or likelihood ratios without an explicit validated numerical conversion model.

### 14.2 Budget enforcement

Reserve external-call budgets transactionally before dispatch. Include in-flight reservations, retries, failures, and cancellation. Reconcile actual cost. At a zero-dollar external budget, no paid call occurs. Default network access is disabled in the offline profile; downloads and subscriptions need explicit authorization independent of per-inference budgets.

Stop at the configured action/deadline limit. An unavailable source produces an unavailable record, not an imagined answer or automatic substitution with a weaker historical source.

### 14.3 Revision contract and meaningful reward

Before acquisition, record the question, modeled possible findings, affected event/edge/forecast components, estimated proper-score benefit, cost, deadline, and a planned comparison. Afterward, store evidence and create a new forecast version.

For scientific attribution, compare against a time-matched no-extra-acquisition control at the same reissue time, with the same routine information and still-future target window. Do not credit ordinary elapsed time, revealed parts of the target, or a shorter horizon as acquisition skill. Preserve the earlier official forecast as well, but distinguish its operational comparison from the controlled acquisition experiment.

A proposed acquisition objective is expected reduction in a proper forecast loss minus monetary and latency costs. Reducing entropy alone is insufficient; useful evidence can legitimately widen a distribution.

Start with fixed rules. Then compare random, disagreement-driven, and contextual-bandit acquisition under matched budgets. Log behavior-policy propensities and coverage of candidate actions when using off-policy estimators; unobserved counterfactual results are not free labels. Use full-information shadow runs only when paid for and recorded as extra evaluation cost.

### 14.4 Information versus financial lead time

Record precursor occurrence, public availability, system receipt, inference completion, forecast issuance, and first eligible downstream decision time. No historical options fill can precede forecast completion. The monitoring planner may find predictive utility without a financially exploitable interval; report the difference.

---

## 15. Controlled learning, recursive evaluation, and specialist discovery

Maintain three lanes:

- **Frozen inference:** approved algorithms, artifacts, and versioned online state produce official forecasts.
- **Shadow adaptation:** candidate weights, graphs, prompts, specialists, and acquisition policies are tested without changing official behavior.
- **Promotion:** fresh evidence and declared gates permit a reversible new configuration.

Learn numerical parameters, calibrated event probabilities, transmission/delay relationships, context-conditioned expert allocation, and evidence-acquisition policies from matured outcomes. This must be observable as versioned parameter/policy changes, not simply a new prompt saying “learn from mistakes.”

Use proper-score residuals to investigate failure categories: event probability error, timing error, transmission error, dependence error, covariate error, calibration error, or data failure. Assign credit through paired controls or designed ablations, not an LLM narrative.

Optional research lanes include Chroma-style specialist portfolios, Hopfield-style episode retrieval, Hebbian updates, and stigmergic evidence memory. Compare each with ordinary nearest-neighbor retrieval, regularized statistical memory, or a contextual bandit. Biological terminology does not substitute for an algorithm, ablation, and measurable outcome.

Full reinforcement learning requires a separate approved experiment showing that sequential actions and delayed rewards need it. Do not optimize sparse simulated trading P&L before forecast and execution validity. Learners cannot redefine labels, deadlines, benchmark splits, source rights, or safety gates to improve their score.

A model-catalog check may register a new candidate with capabilities, license, cost, and tests. It cannot automatically download, enable, or promote it. Old manifests must remain reproducible after catalog updates.

---

## 16. Required user workflows

### Workflow W01 — Initial forecast

Choose an instrument, task, horizon, and as-of time. Validate data and permissions, freeze a snapshot, compute cheap state, select specialists, run them, combine distributions, validate/calibrate the supported representation, and seal a forecast. Show evidence, unavailable fields, actual model IDs, weights, and benchmark context.

### Workflow W02 — External-event forecast

Choose a versioned event definition. Reconstruct available evidence and expectations, forecast occurrence/timing/severity/no-event, create world scenarios, and generate a volatility distribution through the transmission specialist. Compare with the temporal-only and same-evidence numerical controls.

### Workflow W03 — Linked-event query

Specify A, B, C, time windows, ordering, and whether the request concerns both outcomes, either outcome, or at least one scenario set. Inspect shared drivers/outcomes, compute through the joint model, display assumed versus learned links and uncertainty, and save the exact query and result.

### Workflow W04 — Precursor monitoring plan

Select a target instrument or precursor universe and a budget. Run forward/reverse scenario search, rank incremental distinct-episode coverage, and create a conditional monitoring plan. A plan schedules no external monitoring until the application operator explicitly enables its job/cadence and budget. It places no trades.

### Workflow W05 — New confirmation, contradiction, or non-propagation

Ingest the new evidence as a new record; distinguish predicted, disputed, and observed states. Update only eligible beliefs, rerun affected worlds and forecasts, expire invalidated branches, and preserve the parent forecast. Absence updates use censoring-aware delay models. Do not overwrite forecast history.

### Workflow W06 — Manual ESS scenario

Edit a valid parameter, observation assumption, delay, or dependency. Create an immutable branch. Recompute all affected conditional probabilities, paths, and coverage queries. Display which changes came from the user's assumption rather than new data. Invalid edits produce specific diagnostics.

### Workflow W07 — Compare arbitrators

Freeze one expert pool and eligible forecast store. Fit equal/global/rolling/feature/event-cascade gates with strictly earlier data. Evaluate identical origins and budgets; report losses, calibration, tails, joint outcomes, and costs. Do not confound a new gate with a simultaneously expanded model pool.

### Workflow W08 — Investigate a missing fact

Generate a revision contract, reserve cost, retrieve permitted evidence, build a new snapshot, issue a new forecast, and later score its time-matched improvement. Stop when no useful action remains or the budget/deadline is reached.

### Workflow W09 — Learn and propose promotion

Reveal only matured outcomes, score all eligible forecasts, update approved online state, and train shadow challengers. Produce a promotion report with negative findings, fresh confirmation, scope, and rollback. Without sufficient evidence, retain the incumbent and label the result inconclusive.

### Workflow W10 — Optional options research

Consume a frozen forecast, authorized quote history, and actual contract metadata. Apply a predeclared strategy/exit policy with feasible quote timing and costs. Report `NOT_ASSESSED`, `INSUFFICIENT_DATA`, `NO_SUPPORTED_EDGE`, or a qualified research result. Never infer profitability from a volatility probability alone.

---

## 17. Workbench and presentation requirements

Deliver a usable local interface after the CLI slice. Reuse existing UI where possible. Required views are:

| View | Required behavior |
|---|---|
| Forecast | Actual target, horizon, distribution, origin, data/model version, calibration evidence, baseline comparison, failure/abstention status. |
| Event and three clocks | Event definition, occurrence versus belief, information arrival, response delay, expectations, no-event/cancellation mass, provenance. |
| Cascade graph | Distinct node/edge roles, shared drivers, shared outcomes, AND/OR/exclusive logic, parameter uncertainty, delayed propagation and resolution. |
| Coverage planner | Incremental coverage, redundant paths, no-cascade probability, monitoring budget, useful lead time, query definition and sensitivity. |
| Arbitration | Which specialists were eligible/run/failed, why selected, actual allocations, past supporting scores, stage/context, cost. Weights are not event probabilities. |
| Scenario comparison | Immutable branches, changed assumptions, recomputed output, conditional versus intervention label, source drill-down. |
| Experiments and learning | Paired controls, per-asset/horizon/event results, calibration/tails/joint scores, failures, costs, promotion history and rollback. |
| Options research | Separate payoff/quote assumptions and no-edge status; no buy/sell button. |

Graph editing must modify the real numerical model through validated contracts, not only its drawing. Probability displays need a denominator/event definition, conditioning, time window, and synthetic/research/live label. No animated confidence score or invented demo values outside the clearly marked synthetic mode.

Provide accessible labels, useful empty/error states, and export of a bounded reproducibility manifest plus permitted results. Do not export licensed raw data through a convenience download.

---

## 18. Data and benchmark tracks

An external dataset is a candidate until its exact access, version, fields, coverage, timestamps, and rights are verified. Do not purchase data or assume institutional entitlements. Keep tiny permitted fixtures and acquisition scripts separate from restricted raw archives.

| Track | Candidate sources | Purpose and restrictions |
|---|---|---|
| `VT-SYNTH` | Seeded known-generating-process market/event worlds | Mandatory offline correctness, probability arithmetic, dependence and failure tests. Not evidence of financial profitability. |
| `VT-CORE` | VOLARE; `tsfm-rv` paper/code | Reproduce relevant volatility baselines, then run our separately named cumulative-variance tasks. Dataset and replication-code rights differ. [S17,S18] |
| `VT-EVENT-GAS` | Contract-specific gas data, archived weather runs, EIA releases, CFTC vintages | Test external event forecasts, transmission, cascades, and acquisition with point-in-time evidence. [S20–S23] |
| `VT-MACRO` | ALFRED/FRED vintages and timestamped release calendars | Validate revision-aware macro-event features; vintage dates alone may not prove exact intraday availability. [S19] |
| `VT-CONTEXT` | Context is Key plus our postponed/cancelled/contradictory-event fixtures | Component-level context sensitivity, not market profitability. [S12] |
| `VT-ROBUSTNESS` | Separately authorized alternative variance estimators/data | Determine whether apparent skill depends on one measurement method; reconcile units/sessions. |
| `VT-MICRO` | Optiver competition data, when authorized | Optional short-horizon order-book specialist; anonymized/shuffled identifiers cannot be assumed chronological. Verify host terms and task. |
| `VT-OPTIONS` | Authorized historical equity/ETF options or contract-specific futures options | Separate financial-research gate; exact quote times, bids/asks, underlying, settlement, and entitlements required. |
| `VT-FORWARD` | Frozen newly arriving observations | Prospective confirmation after model/policy selection; no retrospective claims of having already run it. |

The financial benchmark paper reports no universal foundation-model advantage and motivates a TTM/Log-HAR control, not a promised winner. [S18]

Use operational weather forecasts as issued, not reanalysis/actual weather or a later reforecast product masquerading as an earlier forecast. CFTC reporting reference dates and publication dates differ. Preserve first release and later revisions for economic/energy series. [S19–S23]

If strict historical availability is unknown, label that experiment exploratory. Do not fabricate past publication timestamps or call present-day web retrieval a historical information feed.

---

## 19. Evaluation protocol and scientific promotion

### 19.1 Required experimental comparisons

| Arm | Components or comparison | Isolated question |
|---|---|---|
| A0 | Classical numerical controls and simple mixtures | Credible baseline. |
| A1 | A0 plus individual foundation challengers, fixed combination | Incremental model diversity. |
| A2 | Same pool: equal/global/rolling/feature-conditioned gates | Value of learned arbitration independent of new models. |
| A3 | Same numerical information plus known event calendars | Value of scheduled information timing. |
| A4 | Predicted external-event features in ordinary boosting | Value of new evidence without ESS structure. |
| A5 | ESS transmission with the same event forecasts/evidence | Incremental structured reasoning. |
| A6 | Dependency-aware cascades versus direct/cross-market and independent-event controls | Value of conditional propagation and correct joint probability. |
| A7 | Event/cascade-conditioned arbitration on the same pool | Value of allocating expertise by event stage. |
| A8 | Fixed/full-pool versus cost-aware selection | Quality–cost tradeoff with complete accounting. |
| A9 | Fixed/random/disagreement/bandit acquisition with matched budget | Value of selective investigation. |
| A10 | Frozen versus approved adaptive state | Genuine prospective learning benefit and stability. |
| A11 | Optional fixed options strategy consuming selected forecasts | Whether forecasting skill survives the specific payoff and costs. |

Run uncalibrated and past-calibrated variants where needed to separate new information from scale correction. Include event-mask, irrelevant-context, shuffled-context, duplicate-source, and leave-one-component-out controls. Hindsight event-oracle experiments may diagnose error sources but cannot compete as deployable policies.

### 19.2 Proper scoring and joint outcomes

Use CRPS for sufficient CDF/sample representations; otherwise supported quantile or weighted interval scores. For positive observed variance v and forecast conditional mean f, use `QLIKE(v,f)=v/f-log(v/f)-1`, recording any estimator-specific zero/floor policy. Do not use a predictive median as a mean by accident.

Use Brier/log loss for event and downstream probabilities, censoring-aware survival scoring for timing/duration, and explicit joint-event Brier scores. For vector/path distributions, add normalized energy/variogram or another justified multivariate score plus targeted joint-tail and episode diagnostics; one marginal score cannot certify dependence.

Report interval coverage and width, reliability, false alerts, missed episodes, useful lead time, no-event calibration, abstention/selective coverage, tail losses, compute, latency, and acquisition cost. Increased scenario coverage alone is not evidence of a useful or profitable system.

Aggregate per-instrument normalized losses using a frozen rule and handle near-zero denominators. Include event-family, horizon, stage, source quality, and worst-performing strata. Keep failed and abstained origins visible; common-case-only model comparisons and full-operational comparisons answer different questions.

### 19.3 Leakage and statistical uncertainty

Use rolling/expanding-origin outer evaluation with strictly earlier nested tuning/calibration. Purge training labels whose outcome/confirmation windows cross boundaries. Cross-fit **every learned stage**: event forecasts, expectation proxies, ESS corrections, base forecasts, arbitrators, and calibrators.

Group shared event episodes and use block/clustered resampling appropriate to overlapping horizons and cross-market dependence. A thousand predictions during one disruption are not a thousand independent disruptions. Record all attempted configurations and predeclare primary comparisons/multiplicity handling.

A consumed holdout is no longer untouched. Track when it was opened and subsequent design changes. Modern pretrained models may have seen historical series or event outcomes; checkpoint cutoffs, training-overlap disclosures, masked controls, and prospective confirmation are required qualifications. Time-gated retrieval alone does not remove memorization risk.

### 19.4 Promotion gates

A candidate may become the default only when engineering invariants pass, resource/license constraints are met, and the preregistered comparison supports useful improvement without unacceptable calibration or tail degradation.

The v1 planning target of 3% normalized primary-loss improvement may remain a configurable proposal, not a promised gain or universal threshold. Before confirmation, freeze the practical improvement margin, calibration noninferiority margin, per-stratum guardrails, uncertainty method, and minimum evidence requirement. Underpowered or mixed results retain the simpler incumbent.

Engineering completion is possible with a negative research result. Scientific superiority and economic viability remain separate statuses. Never tune until a desired headline appears and call that confirmation.

---

## 20. Optional options bridge

Retain the bridge as a downstream experiment. Long-straddle mechanics depend on terminal displacement, premiums, time, and contract terms, not merely realized variance. [S24]

For an ordinary same-strike equity pair held to consistently modeled expiry/settlement, a reference calculation is:

```text
P&L = multiplier * (abs(S_T-K) - entry_call_ask - entry_put_ask) - fees
```

Include material financing and actual delivery/exercise conventions. This is not a universal commodity/futures-option formula. For an early exit, score against eligible observed bid quotes under a declared implementable exit policy; do not select the best future IV peak. A delta-hedged experiment requires its own rehedging, financing, liquidity, and jump-risk specification and remains deferred.

Forecast completion must precede any proposed entry quote. Use a genuine underlying-price source appropriate to the contract; do not substitute an option-implied reference for realized stock returns. Model-generated option values are scenarios, not observed fills.

For linked-event opportunities, evaluate the entire declared research policy, including non-activations, delayed confirmations, false triggers, overlapping exposure, spread costs, and capital usage. A high probability that one of three cascades occurs does not imply positive expected P&L from buying three straddles.

No quotes or required contract fields means `NOT_ASSESSED`. No supported edge is an acceptable outcome.

---

## 21. Dependency-ordered implementation milestones

The IDs below describe transformation deliverables, not work automatically assumed absent. Satisfy an item with audited existing code when appropriate. Map each acceptance requirement in Section 22 to tests and the earliest responsible ticket.

| Ticket | Dependencies | Deliverable and exit evidence |
|---|---|---|
| VT00 | None | Transformation audit, current-state capture, gap matrix, scope/source/rights decisions, baseline test output. |
| VT01 | VT00 | Versioned contracts, target definitions, capability manifests, safe serialization, schema migrations. |
| VT02 | VT01 | Evidence ledger, as-of queries, source/revision reconstruction, target engine, label maturity. |
| VT03 | VT01,VT02 | Seeded synthetic worlds and exact finite-state cascade reference with known-answer tests. |
| VT04 | VT02,VT03 | Classical forecasting controls and distribution/residual treatment with valid moments. |
| VT05 | VT04 | Immutable forecast store, proper scores, past-only calibration, paired outcome ledger. |
| VT06 | VT05 | TTM, Chronos-2, TimesFM 2.5 adapters; actual capability/license/resource and reload tests. |
| VT07 | VT05 | Joint time/instrument paths, horizon coherence, episode derivation, dependence diagnostics. |
| VT08 | VT05,VT06,VT07 | CLI numerical vertical slice and reproducible chronological benchmark; explicit blocked adapters where applicable. |
| VT09 | VT01,VT03,VT05 | Typed ESS graph, safe rules, inference validation, offline fit/online filtering, scenario branches. |
| VT10 | VT02,VT09 | Resolvable external events, archived forecast adapters, expectation tracker, three clocks and event scoring. |
| VT11 | VT07,VT09,VT10 | Event-conditioned transmission specialist and same-evidence numerical comparator. |
| VT12 | VT03,VT07,VT11 | Shared-driver/shared-outcome cascades, joint-world queries, absence/cancellation/delay updates. |
| VT13 | VT12 | Scenario Coverage Planner, forward/reverse queries, duplicate/overlap controls and monitoring plans. |
| VT14 | VT05,VT06,VT08 | Global/rolling/feature-conditioned arbitration on the same cached pool; objective-specific tests. |
| VT15 | VT10,VT11,VT12,VT14 | Event/cascade-stage gating, conditional-world fusion, probability/weight separation and OOF integration. |
| VT16 | VT14,VT15 | Cheap pre-selector, capability gating, resource and transactional budget controls, cold/warm cost accounting. |
| VT17 | VT10,VT13,VT16 | Bounded decision adapter, approved retrieval, revision contracts, time-matched acquisition controls. |
| VT18 | VT05,VT15,VT17 | Outcome-grounded memory, delayed-feedback policy, shadow/promotion/rollback and optional bandit challenger. |
| VT19 | VT08,VT09,VT12,VT13,VT15,VT18 | Interactive workbench covering W01–W09 with real computations and explicit unavailable states. |
| VT20 | VT11,VT12,VT15,VT18 | Reproducible complete ablation suite, event-group uncertainty, contamination and negative-result reporting. |
| VT21 | VT20 | Frozen prospective collection protocol and job implementation; results remain pending until actual labels mature. |
| VT22 | VT07,VT08,VT12,VT20 | Optional authorized options bridge/W10 with actual quotes and contract/latency accounting. |
| VT23 | VT19,VT20,VT21 | End-to-end acceptance, resource/security/license audit, documentation reconciliation and evidence-backed release report. |

**Milestone grouping:** M0=VT00–VT03; M1=VT04–VT08; M2=VT09–VT11; M3=VT12–VT13; M4=VT14–VT16; M5=VT17–VT18; M6=VT19–VT20; M7=VT21/optional VT22; M8=VT23.

A missing optional data entitlement or model does not stop unrelated implementation. Record the blocked capability, complete its failure behavior and interfaces, and proceed on permitted numerical/synthetic tracks. Do not mark a real-model or real-data acceptance test passed using a mock.

VT23 engineering release may record prospective confirmation as pending. It cannot claim research superiority or economic readiness until their separate gates actually pass. Optional trained specialist families and research-only models are later tickets with their own hypothesis and budget, not hidden blockers.

---

## 22. Acceptance suite and adversarial cases

Create executable tests for every applicable requirement below. Exact arithmetic tests use analytical reference values; stochastic tests use a declared seed, tolerance, and Monte Carlo uncertainty to avoid flaky pass/fail behavior. A passed test proves only the condition it actually checks.

### 22.1 TIME requirements

| ID | Required acceptance condition |
|---|---|
| AC-TIME-01 | Changing data published after the origin leaves the earlier frozen forecast unchanged. |
| AC-TIME-02 | The scored target cannot appear inside a model context, scaler fit, gate feature, or analog retrieval. |
| AC-TIME-03 | Historical availability and live receipt policies are tested separately; imported archives are not rejected merely for being imported today. |
| AC-TIME-04 | First releases and revisions reconstruct different eligible snapshots at the appropriate times. |
| AC-TIME-05 | One-, five-, and twenty-session labels mature only after their complete intervals and publication rules. |
| AC-TIME-06 | Episode confirmation lags, existing episodes, and right censoring are represented correctly. |
| AC-TIME-07 | Cross-fitted event forecasts and upstream ensembles respect chronology and shared-event groups. |
| AC-TIME-08 | Forecast completion and source arrival times prevent fictitious earlier entries or earlier knowledge. |
| AC-TIME-09 | Reusing an examined holdout for a fresh confirmation claim is rejected by the experiment manifest. |

### 22.2 PROB requirements

| ID | Required acceptance condition |
|---|---|
| AC-PROB-01 | Event probability, transmission probability, scenario mass, and expert weight have distinct typed fields. |
| AC-PROB-02 | Invalid conditional tables, non-normalized exclusive branches, and probabilities outside [0,1] fail validation. |
| AC-PROB-03 | Concurrent mechanisms are not normalized as though they were mutually exclusive outcomes. |
| AC-PROB-04 | Background B risk when A is absent is included in total probability calculations. |
| AC-PROB-05 | Predicted A cannot trigger the same update as independently observed/confirmed A. |
| AC-PROB-06 | Conflicting or unreliable observations do not silently create certainty. |
| AC-PROB-07 | Unknown dependence yields declared assumptions, bounds, or an unsupported result—not silent independence. |
| AC-PROB-08 | User assumptions and interventions remain separate from observations and conditional sensitivities. |
| AC-PROB-09 | Intervals over parameters and Monte Carlo error are not mislabeled as predictive outcome intervals. |

### 22.3 CASC requirements

| ID | Required acceptance condition |
|---|---|
| AC-CASC-01 | Three independent 30% precursors produce P(any A)=0.657 in the reference graph. |
| AC-CASC-02 | The independent complete-set and A-and-B arithmetic in Section 10.3 matches exact enumeration. |
| AC-CASC-03 | Three perfectly coincident 30% triggers produce 0.30, not 0.657. |
| AC-CASC-04 | Three mutually exclusive 30% triggers produce 0.90. |
| AC-CASC-05 | A shared downstream B under the specified assumptions produces 0.55845 and is counted once. |
| AC-CASC-06 | Two conditional 85% marginals preserve joint bounds [0.70,0.85] without an independence assumption. |
| AC-CASC-07 | Both B-and-C and either B-or-C queries are distinct and independently tested. |
| AC-CASC-08 | Duplicating or renaming a source/scenario does not increase world probability or coverage. |
| AC-CASC-09 | AND interactions, inhibitory/buffering paths, mutually exclusive branches, and lagged feedback behave as declared. |
| AC-CASC-10 | Cancelled, postponed, expired, and non-propagating precursors update the correct future windows. |
| AC-CASC-11 | Sampled market episodes and derived variance paths cannot contradict each other in a joint-capable artifact. |
| AC-CASC-12 | Pruning/importance sampling preserves no-event and remainder mass with correct weights and uncertainty. |

### 22.4 DIST requirements

| ID | Required acceptance condition |
|---|---|
| AC-DIST-01 | Identical point experts can retain nonzero predictive uncertainty through their outcome distributions. |
| AC-DIST-02 | Quantiles are ordered with valid support; sparse quantiles cannot silently imply full tails or joint paths. |
| AC-DIST-03 | A CDF mixture and a weighted-quantile average are distinguished on a known counterexample. |
| AC-DIST-04 | The empirical/analytic mixture CRPS identity matches a direct reference calculation. |
| AC-DIST-05 | Variance is nonnegative; cumulative variance equals path sums; annualized volatility is not forced monotone. |
| AC-DIST-06 | Marginal-only adapters cannot serve duration, joint-tail, or simultaneous multi-market queries. |
| AC-DIST-07 | A joint mixture preserves world/expert identity and shared dependence across its full path. |
| AC-DIST-08 | Unsupported/infinite required moments block the relevant score or payoff consumer with a specific reason. |
| AC-DIST-09 | Point/mean return-variance baselines do not silently masquerade as full intraday realized-variance distributions. |
| AC-DIST-10 | Independent calibration heads cannot be combined into an unverified coherent joint probability. |

### 22.5 ARB requirements

| ID | Required acceptance condition |
|---|---|
| AC-ARB-01 | Equal/global/rolling/feature/event-stage policies can be evaluated on the identical forecast pool. |
| AC-ARB-02 | Post-inference features cannot be used to claim pre-inference cost savings. |
| AC-ARB-03 | Feature and gate parameters are fitted only on eligible earlier observations and out-of-fold forecasts. |
| AC-ARB-04 | Loss-to-weight, FFORMA-inspired surrogate, and direct-mixture objectives have explicit distinct identifiers. |
| AC-ARB-05 | An unconditional expert is not multiplied by scenario probabilities twice. |
| AC-ARB-06 | An unsupported expert cannot be represented as a conditional-world forecaster. |
| AC-ARB-07 | An expert failure is credited to its named fallback, not the failed model. |
| AC-ARB-08 | A scenario change invalidates affected cache entries even when price history is unchanged. |
| AC-ARB-09 | Consensus or simulated ensemble medians cannot enter real performance updates. |
| AC-ARB-10 | Rare-context shrinkage and bounded weight updates are verified against their declared policy. |

### 22.6 EVT requirements

| ID | Required acceptance condition |
|---|---|
| AC-EVT-01 | Event outcome rules are frozen independently of the observed market response. |
| AC-EVT-02 | Storage/macro first-release timing, original weather runs, and publication-lagged data obey their vintages. |
| AC-EVT-03 | A forecast future covariate is marginalized through scenarios rather than treated as a certain observation. |
| AC-EVT-04 | Own-model error is not relabeled market surprise without an eligible expectation source. |
| AC-EVT-05 | Event occurrence, information receipt, and market response can have different clocks. |
| AC-EVT-06 | Non-occurrence, cancellation, and uncertainty resolution remain possible outcomes. |
| AC-EVT-07 | An ESS graph and a plain numerical comparator receive matched eligible evidence. |
| AC-EVT-08 | Unobserved downstream response is distinguished from delayed or missing reporting. |

### 22.7 SEL requirements

| ID | Required acceptance condition |
|---|---|
| AC-SEL-01 | A zero external-call budget produces no paid API call or implicit paid fallback. |
| AC-SEL-02 | Concurrent reservations, retries, cancellation, and failures cannot exceed the configured budget. |
| AC-SEL-03 | Capability and license ineligibility removes an expert before dispatch. |
| AC-SEL-04 | Selecting more monitors changes coverage, not the underlying event probabilities. |
| AC-SEL-05 | The coverage planner handles shared outcomes/common drivers and is compared with exact small-set enumeration. |
| AC-SEL-06 | Disabled networking, expired deadlines, and action limits produce explicit stop states. |
| AC-SEL-07 | Acquisition scoring uses a same-time, same-future-target control rather than crediting elapsed time. |
| AC-SEL-08 | Off-policy learning records supported action propensities and does not invent unobserved counterfactual rewards. |

### 22.8 LEARN requirements

| ID | Required acceptance condition |
|---|---|
| AC-LEARN-01 | Actual matured observations, simulated outcomes, critic scores, and assumptions are isolated in storage. |
| AC-LEARN-02 | Every approved online update records its algorithm, training label IDs, and resulting state version. |
| AC-LEARN-03 | Graph/model/prompt structural changes run in shadow until promotion approval. |
| AC-LEARN-04 | A learner cannot change evaluation targets, splits, budgets, permissions, or entitlements. |
| AC-LEARN-05 | Paired contribution credit is distinct from coalition success and model standalone accuracy. |
| AC-LEARN-06 | Corrected outcomes produce a versioned correction/replay rather than silent history changes. |
| AC-LEARN-07 | Rollback restores the declared model, gate, calibrator, graph, and online state. |
| AC-LEARN-08 | An inconclusive or negative benchmark preserves the incumbent and cannot become a superiority badge. |

### 22.9 DATA requirements

| ID | Required acceptance condition |
|---|---|
| AC-DATA-01 | Variance units, annualization, session coverage, estimator identity, and proxy labels remain consistent. |
| AC-DATA-02 | Missing intraday bars and stale observations are not interpreted as zero variance. |
| AC-DATA-03 | Splits and futures rolls do not create unmarked economic jumps. |
| AC-DATA-04 | Nonpositive commodity prices use an explicit valid target or unsupported status, not silent log clipping. |
| AC-DATA-05 | Paper replication and application-specific targets/horizons have separate task IDs. |
| AC-DATA-06 | Raw restricted datasets and model artifacts cannot be exported under the code license alone. |
| AC-DATA-07 | Pretraining overlap/unknown-cutoff limitations are retained in research reports and prospective gates. |

### 22.10 UI requirements

| ID | Required acceptance condition |
|---|---|
| AC-UI-01 | Every numerical card exposes its target, conditioning, horizon, version, and synthetic/research/live status. |
| AC-UI-02 | The graph editor changes validated numerical assumptions and creates a new branch, not merely a visual edge. |
| AC-UI-03 | Empty, failed, unavailable, and unsupported states are visible without invented probabilities. |
| AC-UI-04 | Coverage is labeled as research/monitoring coverage rather than profit probability. |
| AC-UI-05 | Arbitration displays show actual run/failure/weight/cost lineage, not arbitrary model confidence. |
| AC-UI-06 | All mandatory workflows can be reproduced through the CLI and inspected in the workbench. |

### 22.11 OPS requirements

| ID | Required acceptance condition |
|---|---|
| AC-OPS-01 | Clean offline setup and a full synthetic vertical slice run without model downloads or external accounts. |
| AC-OPS-02 | Save/reload parity includes all fitted numerical and state artifacts, not configuration alone. |
| AC-OPS-03 | Idempotent replay/job recovery creates no duplicate evidence, forecasts, charges, or outcomes. |
| AC-OPS-04 | Graph text, retrieved documents, and serialized data cannot execute arbitrary code. |
| AC-OPS-05 | Credentials and private donor data are excluded from logs, artifacts, and the new repository. |
| AC-OPS-06 | Model/data licenses and capabilities are pinned and enforced independently. |
| AC-OPS-07 | CPU/reference and any accelerator paths have measured parity/resource tests with honest unsupported states. |
| AC-OPS-08 | Release reports distinguish tests run, failed, blocked, synthetic-only, and not implemented. |

### 22.12 ECO requirements

| ID | Required acceptance condition |
|---|---|
| AC-ECO-01 | A high-variance path ending at the strike can lose the entire unhedged straddle premium. |
| AC-ECO-02 | Payoff calculations use contract-specific multiplier, expiry, exercise/settlement, and eligible underlying prices. |
| AC-ECO-03 | Entry/exit timing, bid/ask costs, financing where material, overlapping capital, and non-activations are retained. |
| AC-ECO-04 | Missing quotes return NOT_ASSESSED; model valuations are never relabeled observed historical fills. |
| AC-ECO-05 | No brokerage credentials, execution endpoint, or autonomous trade action exists. |

---

## 23. Proposed command-line and configuration contracts

These commands are **interfaces to implement or map to existing equivalents**. This Markdown file does not ship an executable CLI. During implementation, every documented command must be backed by code, help text, exit-code behavior, and tests; otherwise label it unavailable.

```bash
volterra doctor --profile offline
volterra audit --goal GOAL.md
volterra fixtures generate --scenario linked-events --seed 17
volterra replay run --config config/offline.yaml
volterra forecast inspect <forecast_id>
volterra events forecast --definition <event_definition_id> --snapshot <snapshot_id>
volterra cascades query --spec <query.json> --snapshot <snapshot_id>
volterra coverage plan --spec <coverage_query.json> --budget <budget_id>
volterra arbitration compare --manifest <experiment_manifest.json>
volterra scenario branch --parent <forecast_id> --edit <validated_edit.json>
volterra acquisition evaluate --contract <revision_contract_id>
volterra learning update --through <eligible_maturity_timestamp>
volterra promotion propose --challenger <manifest_id> --report <report_id>
volterra promotion apply --proposal <proposal_id> --approval <approval_id>
volterra evaluation report --run <run_id>
```

The command names must not grant authority. `promotion apply` still verifies an appropriate approval. A natural-language request inside retrieved content cannot act as approval. Commands must be idempotent or explicitly identify their mutation and version.

### 23.1 Reference offline profile

This is a proposed schema-validating configuration surface, not a tested runtime configuration. Evolve field names through a migration if the existing application has equivalents.

```yaml
schema_version: 2
profile: offline
execution:
  device: cpu
  max_parallel_model_workers: 1
  allow_network: false
  allow_model_downloads: false
  max_external_usd: 0.0
  max_acquisition_steps_per_forecast: 3
  seed: 17
forecast:
  horizons_sessions: [1, 5, 20]
  target_family: cumulative_realized_variance
  fusion_mode: unconditional_stack
  require_joint_for_cascade_queries: true
  allow_silent_fallback: false
models:
  enabled: [persistence, ewma, log_har, gjr_garch]
  external_checkpoints_enabled: false
arbitration:
  incumbent: equal_mixture
  challengers: [global_mixture, rolling_mixture, loss_to_weight,
                fforma_inspired, direct_mixture_gate, event_conditioned_gate]
  allow_consensus_as_outcome: false
cascade:
  unknown_dependence_policy: bounds_or_explicit_assumption
  retain_no_event_mass: true
  deduplicate_shared_outcomes: true
learning:
  label_source: matured_observations
  structural_changes: shadow_only
  require_approval_for_promotion: true
options:
  enabled: false
  execution_enabled: false
```

Only eligible numerical challengers run before their input capabilities and training history exist. This profile must not make every listed challenger a startup dependency. A second explicit local-research profile can enable locally installed licensed checkpoints; a separate authorized profile can permit specific archived/live source adapters within budget.

### 23.2 Required generated project artifacts

The implementation must maintain or create equivalents of:

- `docs/TRANSFORMATION_AUDIT.md` — present/partial/absent/broken/blocked mapping and source attribution.
- `docs/ARCHITECTURE.md` and `docs/DECISIONS.md` — actual ownership, fusion semantics, migrations, and rejected alternatives.
- `docs/DATA_CONTRACTS.md`, versioned schemas, and `docs/PROBABILITY_SEMANTICS.md` — model-ready definitions and invariants.
- `docs/MODEL_REGISTRY.md` and machine-readable model/data manifests — exact revisions, capabilities, terms, costs, and limitations.
- `docs/WORKFLOWS.md` and CLI help — all runnable workflows with clear permissions and failure states.
- `docs/BENCHMARK_PROTOCOL.md`, immutable run manifests, and paired result artifacts — no handwritten “passing” claims.
- `docs/ACCEPTANCE_MATRIX.md` — each AC identifier linked to real tests and the latest executed result.
- `docs/STATUS.md` and `docs/RELEASE_REPORT.md` — engineering, scientific, prospective, and economic states separately.
- Source-attributed synthetic generators and permitted tiny fixtures; restricted raw data remains outside source control.

These artifacts are deliverables for the implementing agent. They are not claimed to be included with this GOAL.md.

---

## 24. Definition of done and anti-drift contract

### 24.1 Engineering completion

All mandatory workflows and contracts operate end-to-end with explicit failure behavior. Core tests execute offline. At least one real, authorized numerical benchmark runs when the required dataset is accessible; absence is reported as blocked rather than faked. Installed foundation adapters are smoke-tested and evaluated as actual models. The interactive graph controls the numerical system. Budgets, lineage, versions, migrations, and rollback work.

Where a required checkpoint or dataset is unavailable, its adapter and failure contract may be implemented while its integration test remains blocked. Do not describe the entire transformation as fully verified when mandatory integrations remain untested. Report an honest engineering status by capability and evidence.

### 24.2 Scientific completion

A preregistered comparison supports or rejects the hypothesis for each added mechanism. Event, transmission, dependence, arbitration, acquisition, and cost effects are separated. Negative or inconclusive findings are preserved. No accuracy improvement is promised. Prospective results exist only after genuinely new outcomes mature.

### 24.3 Optional economic readiness

The financial bridge has real authorized quotes, correct contract logic, temporal alignment, implementable exits, and full declared costs. Predictive skill and economic performance remain separate. A no-edge result is acceptable. No trading execution is added.

### 24.4 Final acceptance demonstration

Demonstrate the following on explicit synthetic fixtures, then on eligible real data where supported:

1. A quiet-market volatility forecast with its baseline comparison.
2. Three 30% independent precursors and their correct joint coverage.
3. The same-looking scenario list with a shared driver, showing reduced or otherwise correctly changed coverage.
4. Several routes into one downstream episode, counted once.
5. Confirmation of A changing B/C forecasts without confusing a model prediction with observation.
6. A delayed/cancelled/non-propagating event revising its timing and uncertainty.
7. Different arbitration methods on the same forecast store, with outcome-based—not consensus-based—learning.
8. A manual graph branch changing the actual computed distribution while preserving the official forecast.
9. An acquisition whose benefit is measured against the correct time-matched control.
10. A strong volatility forecast that nevertheless yields no supported options edge or no economic assessment.

### 24.5 Coding-agent work reports

At each milestone report actual files changed, tests executed and their results, unimplemented/blocked capabilities, resource costs, deviations from this contract, and the next unmet dependency. Do not claim a source audit, statistical experiment, license check, or external connector test occurred unless it actually did.

Do not turn the project into a stock picker, a numerical-consensus reward loop, a probability calculator that assumes all scenarios are independent, a graph-only dashboard, or an ensemble enlarged until its backtest looks impressive.

**The final application should make its reasoning testable through forecast revisions and realized outcomes. It must remain useful when a simpler model wins, an event never occurs, a cascade is buffered, or the options market already prices the risk.**

---

## 25. Research and source register

Selected primary references below were checked while preparing this document on **October 18, 2026**. A live documentation page is not a pinned deployment artifact. The implementing agent must record the exact package/checkpoint/data revision and applicable terms at integration time. No cited benchmark result is represented as a VOLTERRA reproduction. Research methods below motivate experiments; the detailed engineering choices in this document are proposed requirements.

**[V1] Earlier supplied project documents.** `GOAL.md`, `DESIGN_SPEC.md`, `BUILD_PLAN.md`, `SCIENCE_AND_EVALUATION.md`, and `REUSE_AUDIT.md` in the VOLTERRA v1 handoff, dated October 17, 2026. They were read as design/audit sources, not as proof of current application state. The donor audit pins `deesatzed/aXc-ace-forecaster` at `3bd39789c3811a5b437baf60a65de480aa0486bf`; it describes selected inspected methods and explicitly excludes a full execution audit. Preserve this scope. This v2 GOAL is self-contained when those documents are not mounted.

**[S01] Amazon Chronos-2 official model card.** Native covariate and multivariate capabilities, quantile outputs, Apache-2.0 label, and the distinction from Chronos-Bolt's external-covariate workaround. Source: `https://huggingface.co/amazon/chronos-2`

**[S02] Google TimesFM official repository.** TimesFM 2.5 XReg support and Apache-2.0 weights; downloaded TimesFM 3 weight restrictions are separate from the source-code license. Review an authorized cloud service under its own terms rather than generalizing self-hosted restrictions. Source: `https://github.com/google-research/timesfm`

**[S03] Montero-Manso et al., FFORMA (2020).** Feature-based meta-learning of forecast-combination weights. It is an established method, not a new 2026 invention. Source: `https://robjhyndman.com/publications/fforma/`

**[S04] Toto 2.0 technical report, FnF section.** Documents an FFORMA-style feature-based XGBoost ensemble. Borrow the pattern, not its reported allocations or financial conclusions. Source: `https://arxiv.org/html/2605.20119v1`

**[S05] CastStar official artifact card.** The checked artifact contains frozen inference/reproduction files and explicitly not training data or code. Source: `https://huggingface.co/USTC-AGI/CastStar`

**[S06] OpenTSLM TeeMoE paper and implementation.** Modular numerical/contextual workflows and cross-fitted reference forecasts. Our chronological financial adaptation adds constraints rather than claiming an exact reproduction. Sources: `https://arxiv.org/html/2609.40265v1` and `https://github.com/OpenTSLM/OpenTSLM-TeeMoE`

**[S07] Test-Time Efficient Pretrained Model Portfolios for Time Series Forecasting (Chroma).** Research motivation for smaller specialist portfolios. Source: `https://arxiv.org/abs/2510.06419`

**[S08] Datadog Toto official repository.** The checked Toto 2.0 release distinguishes its multivariate/quantile support from exogenous-variable and fine-tuning features not yet included in that release. Source: `https://github.com/DataDog/toto`

**[S09] Moirai 2.0 paper and named model card.** The paper explicitly treats multiple variates as independent univariate tasks; the named checkpoint carries a noncommercial license label. Sources: `https://arxiv.org/html/2511.11698v1` and `https://huggingface.co/Salesforce/moirai-2.0-R-small`

**[S10] Optional local-model artifacts.** IBM Granite FlowState/PatchTST-FM/TTM cards and TiRex-2's official repository are discovery points. TiRex-2 distinguishes public forecasting from additional Pro capabilities; audit the actual artifact rather than importing the whole feature list. Sources: `https://huggingface.co/ibm-granite/granite-timeseries-flowstate-r1`, `https://huggingface.co/ibm-granite/granite-timeseries-patchtst-fm-r1`, `https://huggingface.co/ibm-granite/granite-timeseries-ttm-r2`, and `https://github.com/NX-AI/tirex-2`

**[S11] Synapse paper, forward-simulation section.** Documents using the ensemble's forecast median as a simulated observation for within-horizon adaptation. Our official learning path deliberately excludes that as realized evidence. Source: `https://arxiv.org/html/2511.05460v1`

**[S12] Context is Key official benchmark repository.** Contextual forecasting component tests, not a financial-volatility certification. Source: `https://github.com/ServiceNow/context-is-key-forecasting`

**[S13] PyMC official overview.** Probabilistic modeling/inference reference; backend selection and diagnostics still depend on the actual graph. Source: `https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html`

**[S14] pgmpy official repository.** Probabilistic graphical-model inference and simulation reference backend. Source: `https://github.com/pgmpy/pgmpy`

**[S15] EasyTPP official repository.** Optional temporal point-process benchmarking and event-sequence models. Source: `https://github.com/ant-research/EasyTemporalPointProcess`

**[S16] cegpy: Modelling with Chain Event Graphs in Python.** Optional representation for history-dependent branching event processes. Source: `https://arxiv.org/abs/2211.11366`

**[S17] VOLARE data paper.** Realized-volatility measurement archive; actual data exports and rights require separate verification. Source: `https://arxiv.org/abs/2602.19732`

**[S18] Financial-volatility foundation-model comparison and replication repository.** Direct financial benchmark context and exact-task replication candidate. Reported heterogeneous model results motivate classical/simple-ensemble controls. Sources: `https://arxiv.org/abs/2607.05291` and `https://github.com/Alessiobrini/tsfm-rv`

**[S19] FRED/ALFRED real-time periods.** Vintage-aware economic data retrieval. Source: `https://fred.stlouisfed.org/docs/api/fred/realtime_period.html`

**[S20] NOAA GEFS archive documentation.** Operational weather ensemble/archive discovery; confirm the required issue times and historical availability. Source: `https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast`

**[S21] Open-Meteo Single Runs API.** Individually issued historical forecast runs; do not substitute a stitched or realized historical weather series. Source: `https://open-meteo.com/en/docs/single-runs-api`

**[S22] EIA Open Data.** Source discovery for energy observations; release/vintage metadata and market expectations are separate acquisition requirements. Source: `https://www.eia.gov/opendata/`

**[S23] CFTC Commitments of Traders.** Position reference dates and publication timing must be kept separate. Source: `https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm`

**[S24] Options Industry Council, Long Straddle.** Payoff and risk mechanics; not a universal futures-options settlement specification. Source: `https://www.optionseducation.org/strategies/all-strategies/long-straddle`

**[S25] arch official volatility-model documentation.** Candidate implementation for GARCH-family controls. Source: `https://arch.readthedocs.io/en/latest/univariate/univariate_volatility_modeling.html`

**[S26] SciPy SLSQP documentation.** Optimizer API, not a restriction to static forecasting policies. Source: `https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html`

**[S27] LAMP: Language Models Can Improve Event Prediction by Few-Shot Abductive Reasoning.** Research precedent for candidate antecedents, retrieval, and learned event scoring; not established market performance. Source: `https://proceedings.neurips.cc/paper_files/paper/2023/hash/5e5fd18f863cbe6d8ae392a93fd271c9-Abstract-Conference.html`

---

## 26. Implementation kickoff

Read this file, inspect the repository, record the actual gap matrix, and execute the first unmet dependency. Preserve verified existing work. Establish the offline known-answer vertical slice before adding large models or external retrieval. Continue through the required event, cascade, arbitration, investigation, and evaluation workflows. Report actual evidence at each gate. Do not ask the user to restate the approved architecture or replace implementation with another roadmap.

**Success means an auditable system that forecasts volatility under uncertain external events, represents linked opportunities without false diversification, and learns from the world—not from its own agreement.**
