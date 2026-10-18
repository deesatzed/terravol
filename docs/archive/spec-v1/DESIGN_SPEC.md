# VOLTERRA — Revised system design

Version 1.0 · Research checked October 17, 2026

## 1. Design thesis

Build a **volatility observatory with controlled adaptive reasoning**, not a swarm whose consensus is mistaken for probability. The numerical engine predicts distributions. The ESS represents relationships, uncertainty and constraints. Small decision models decide whether additional permitted information is worth acquiring. Learning changes tested numerical parameters and selection policies using realized outcomes.

The differentiation hypothesis is not “AI plus a volatility clock.” ORATS already provides option-implied event-day analytics, and SpotGamma provides a market-structure volatility trigger [R01–R03]. The candidate contribution is **auditable forecasting and forecast revision under imperfect evidence and a fixed compute budget**, with demonstrable incremental value.

## 2. Logical architecture and deployment boundary

```text
Authorized observations / archived evidence / synthetic fixtures
    -> immutable evidence ledger + instrument/calendar registry
    -> as-of query + target/feature builder + data-quality gate
    -> numerical model workers
         classical | foundation | event-conditioned ESS specialist
    -> distribution stacker + calibration + joint-path adapter
    -> forecast object + onset/duration summaries + revision ledger
    -> bounded acquisition router -> permitted evidence retrieval
    -> optional new forecast version, never an overwritten forecast

Matured outcomes -> score ledger -> strategy memory -> challenger lab
    -> versioned promotion gate -> future inference configuration

Scenario branches and options research consume forecasts.
Neither may mutate evidence, outcomes, permission rules or official history.
```

Use a modular monolith first: Python 3.12-compatible core, typed contracts, SQLite control/audit state, Parquet data and path artifacts, DuckDB analytical queries, and isolated worker processes for incompatible ML stacks. Verify the actual dependency intersection and lock it during R0; this package does not pretend to contain a tested dependency lock.

Suggested application interfaces: CLI first; a local API and React/TypeScript graph UI later. Use an ordinary durable job table with idempotent jobs rather than a distributed message bus. An optional cloud LLM call is an adapter, not an architectural requirement. No broker credentials or order routes exist.

The default hardware profile is one Mac M4. CPU operation is the reference; accelerator use is an opt-in capability after numerical parity and memory tests. Load large model workers sequentially by default. A model name, parameter count or provider speed claim is not a measured Mac latency result.

## 3. Four outputs that must remain distinct

### 3.1 Physical volatility forecast

Estimate a distribution over future realized variance and its annualized volatility transform. Name the measurement estimator, session coverage, price-adjustment policy and units. `RV` means variance internally; the UI spells out “realized variance” or “annualized volatility” to avoid a common ambiguity.

### 3.2 Episode forecast

Estimate observable threshold-defined expansion, onset and persistence. A hidden Markov state is a model construct, not ground-truth volatility. Evaluate observable labels and disclose the label rule. Preserve a no-transition probability and right-censored durations.

### 3.3 Market-implied comparison

Represent option-implied quantities under their pricing conventions. An ATM implied-volatility quote is not the whole implied distribution. A physical forecast and an option-implied quantity differ in risk premia, jump treatment, horizon and conventions; do not call every gap a pricing error.

### 3.4 Strategy research

A specific strategy needs its own payoff and exit model. A volatile path can finish at the original strike. The long-straddle expiry payoff depends on terminal displacement, not accumulated path variance [R15]. This consumer may need internal return/terminal-value scenarios without turning the core product into a directional price forecaster.

## 4. Evidence architecture

Each raw observation has an immutable source ID and content hash. Store event time, publication/issue time, vendor first-availability time when known, ingestion time, revision/vintage, evidence availability class, access rights and lineage. Preserve the original observation separately from its parsed interpretation.

Maintain at least these evidence states: observed, missing, unavailable, stale, contradictory, censored, and assumed. Do not impute them all to zero or a neutral probability. A source-reliability parameter is learned from a labeled source history or declared as an expert prior; an LLM's confident prose cannot instantiate a numerical reliability probability.

**Live mode:** use information actually received before inference and log acquisition latency. **Historical replay:** use certified vintage/publication availability plus an explicit latency policy. Do not reject all archived data merely because today's import time is later than the historical origin. Conversely, an archive's observation date does not prove that its revised value was available then. Mark uncertain availability and exclude it from strict claims.

Macro variables require vintages; ALFRED supports vintage retrieval but is not a guaranteed millisecond publication feed [R13]. Weather-driven experiments need forecasts as issued before the origin, not realized/reanalysis weather presented as future knowledge [R14]. Exact weather-run selection must be verified for the chosen endpoint.

News agents produce schema-bound claims: event type, entity, time window, source, quotation location, asserted fact, uncertainty in extraction, dependency group and novelty relative to existing evidence. They do not output uncalibrated probabilities of future market moves. Related stories are clustered by upstream event/source, not just sentence similarity. A corrected report invalidates derived claims through lineage; it does not erase the prior record.

## 5. Time-series model registry

Every adapter declares exact artifact revision and checksum, package lock, output type, target units, transformations, covariate support, missingness behavior, context limits, resource profile, commercial-use status and known pretraining-contamination limitations.

| Group | Initial candidates | Decision |
|---|---|---|
| Mandatory classical | Persistence, EWMA, Log-HAR, GJR-GARCH with finite-variance returns | Establish credible low-cost floor |
| Mandatory combination | Equal-weight valid-model ensemble; TTM + Log-HAR comparison | Test whether adaptive complexity is needed |
| Lightweight nonlinear | Quantile gradient boosting | Same-evidence comparator for the ESS |
| First foundation challengers | TTM, Chronos-2 | TTM has direct volatility-benchmark relevance; Chronos-2 supports covariates [R04–R06] |
| Recurrent challenger | TiRex-2 | Evaluate CPU/macOS batch forecasting; incremental streaming is not assumed in the public package [R07] |
| Research alternatives | Small Toto 2 variant; TimesFM 2.5 or 3.0 | Pin exact checkpoint and audit code and weights separately [R08–R09] |

TimesFM 3.0's published weights have a noncommercial license [R08]. Do not enable them in a commercial manifest by inheriting the code repository's license. TiRex-2's repository distinguishes public forecasting from Pro incremental streaming [R07]. These are adapter-level constraints, not reasons to make the whole application depend on a commercial upgrade.

Direct financial evidence is more relevant than a general leaderboard. A July 2026 preprint comparing foundation models and econometric forecasts found no broad uniform foundation-model advantage and supported a simple TTM/Log-HAR combination [R04]. That motivates a control, not a promise that the published outcome will reproduce on this dataset.

### Adapter output

Return a `ForecastDistribution` with quantiles, supported finite moments, optional joint samples, calibration ID and capability flags. A point-only predictor gets a separately fitted residual distribution; it is not relabeled probabilistic because a plotting library draws an interval. When a model fails, return a failure record. An orchestrator may call a named fallback and must preserve both identities.

Do not keep just the median of Chronos samples. Do not average model confidence scores. Do not give a failed foundation model credit for the persistence forecast that replaced it.

## 6. Combining models without counterfeit certainty

Default to a predictive mixture:

`p(y | I_t) = sum_m w_m(I_t) p_m(y | I_t)`, with `w_m >= 0` and sum equal to one.

Fit weights from out-of-fold predictive performance. Start with equal weights and a globally regularized stacker; admit context-dependent weights only after enough labeled history and explicit shrinkage toward the simpler estimator. Store model-family and residual-correlation information so ten variants of one model cannot manufacture apparent independent consensus.

For uncertainty over mixture weights, use a proper simplex distribution such as Dirichlet or logistic-normal. Independent Beta draws followed by normalization do not retain the original Beta marginals. Distinguish an optimization warm-start prior from a posterior probability.

Mixture distributions, averages of point estimates, and distributions of weighted sums are different operations. The code must name which it implements. For path mixtures, select a component for a full path, rather than arbitrarily switching experts at every horizon unless a fitted switching process explicitly models that behavior.

### The joint-path requirement

Marginal quantiles at 1, 5 and 20 days do not specify the dependence needed for onset, duration, maximum moves or early-exit payoffs. A foundation model returning nine quantiles at each time step is not automatically a joint simulator.

Use either a generative stochastic model with native joint paths, or an explicitly fitted dependence adapter. An initial challenger can combine marginal predictive distributions with a rank-copula/residual-block model fitted to past out-of-fold errors. Declare the extra assumptions; test episode durations, cross-horizon dependence and path calibration. Until it passes, emit marginal forecasts only.

All aggregation uses the same nonnegative daily-variance paths. Cumulative variance must be nondecreasing in horizon on each path. Its annualized volatility need not be monotone. An interval for a future outcome is a prediction interval; parameter credible intervals and Monte Carlo error bars are separately labeled.

## 7. The expert system: three explicit responsibilities

### 7.1 Rule layer

Use a small typed predicate system, optionally compiled to CLIPS through clipspy [R10]. Rules check eligibility, units, source freshness, contradictions, inference health, required fields, budget and permissible actions. The most restrictive authorization rule wins. Deterministic conditions belong in code/rules, not in an AI classifier.

Do not reject an extreme forecast solely because it exceeds a historical maximum or three standard deviations. That is a review flag and possibly an out-of-distribution warning, not proof of invalidity. Hard failures include corrupt inputs, impossible support, non-finite values, invalid calendars, missing mandatory contract metadata and failed numerical inference.

Only audited predicates and callable functions are permitted. The graph editor cannot call shell commands, open files, create network clients or execute arbitrary Python.

### 7.2 Probabilistic layer

Use a typed graph intermediate representation independent of any inference library. A node declares its role (observation, latent state, event, parameter, deterministic transform or target), support, unit, family, parameterization, parents with lags, observation model, prior provenance and status.

Use PyMC for offline fitting of continuous/hybrid numerical specialists where appropriate [R11]. The online core uses a tested sequential filter or discrete forward recursion rather than running a new MCMC fit for every observation. pgmpy is an optional discrete-graph reference backend, not a second compulsory numerical authority [R12]. Choose samplers based on model structure: do not automatically apply NUTS to un-marginalized discrete variables or Gibbs to an arbitrary user graph.

A first ESS specialist has three candidate latent mechanisms: **event excitation, liquidity fragility, and volatility persistence**. These are modeling hypotheses, not known causal truths. The filter includes measurement error and unknown evidence. Event timing can be known while event outcome and effect remain uncertain.

For a numerically convenient candidate, model log daily variance with Gaussian innovations or finite Gaussian mixtures and a regime-dependent mean/duration process. Model return innovations with a finite-variance heavy-tailed distribution when returns are needed. Check required moments: exponentiating an unrestricted Student-t log-variance variable does not give a finite expected variance. Do not silently use an undefined mean in QLIKE or strategy valuation.

### 7.3 Scenario and sensitivity layer

Support `condition_on`, `override_assumption`, `remove_evidence` and `intervene` as different operations. Only `intervene` uses causal semantics, and only when the required structural assumptions and identification status are supplied. Otherwise label the result conditional sensitivity, not an identified causal effect.

Every edit creates a branch with parent ID, author, reason, graph version and changed nodes. The official forecast and its original assumptions remain immutable. Invalid distribution parameters, inconsistent bounds, impossible correlations and instantaneous directed cycles are rejected.

Median plus range does not uniquely define every distribution. Ask for the missing required parameters or offer a clearly labeled fitting convention. Fit declared quantiles under support constraints and show goodness of fit. Never silently assign a Gaussian because it is convenient.

## 8. Preventing double-counting in the hybrid

Do not multiply Chronos, HAR and ESS outputs as independent likelihoods when they see the same market history. Do not multiply three syndicated articles as independent evidence of one event. Do not feed a posterior back into the graph as if it were a fresh observation.

Initial implementation: treat the ESS as one event-conditioned probabilistic forecasting specialist in the predictive stack. It can use a temporal reference forecast as an offset, but its event correction and residual distribution must be fitted on genuinely out-of-fold reference predictions. Its full predictive output then competes with a same-information gradient-boosting model and the uncorrected reference.

Later alternatives may fit a unified joint latent-state model. Admit that complexity only through a separate experiment. Graph structure alone does not solve correlation or causal identification.

Alternative explanations are often concurrent: a scheduled announcement and thin liquidity can both be present. Normalize probabilities only over mutually exclusive model indices or partitioned regimes. Display overlapping mechanism probabilities separately.

## 9. Bounded AI decision models

The State Builder emits a compact typed state containing task ID, origin, approved observations, missing fields, data-quality reasons, numeric forecast summaries, disagreement features, expected acquisition costs and explicit allowed actions.

A Jev-style adapter or another small classifier may choose among `PUBLISH_NUMERIC`, `FETCH_APPROVED_EVIDENCE`, `RUN_SPECIALIST`, `CHECK_DATA`, `ABSTAIN` and `STOP`. Its exact action set is supplied by the deterministic rule layer. A classifier cannot add a permission, resolve missing data by imagination, set its own dollar cap or turn a research decision into an order.

For an LLM decision implementation, record model/version, option IDs, raw scores, prompt/schema version and any calibration mapping. Test sensitivity to option ordering, paraphrase and irrelevant fields. A softmax over option tokens is a model score, not a market-event probability.

Preserve critical numbers, units, provenance, unknown states and contradictions losslessly in the State Builder. Optional context compression is tested against an uncompressed control. A high compression ratio is not a quality criterion. Content hashing and embedding similarity serve different purposes.

## 10. Active investigation and falsifiable forecast revisions

Investigations should target facts likely to improve the forecast, not merely produce a persuasive explanation. Examples: resolve whether an announcement was postponed; verify a liquidity-feed anomaly; obtain an archived weather ensemble; establish whether several stories share a single source.

Choose actions by estimated reduction in a proper prediction loss minus monetary, latency and acquisition costs. Entropy reduction alone is insufficient: discovering a real hazard can legitimately widen the forecast. The first policy is deterministic; a contextual bandit is a challenger after a labeled acquisition history exists.

Before a material acquisition, record a **revision contract**: which observations are being sought, the modeled range of their possible values, which forecast components they could alter, and the estimated value of obtaining them. After the observation, record the numerical revision and later score whether that revision improved the forecast. This tests the reasoning mechanism, not just its narrative.

An investigation must stop at its budget or iteration limit. Future release outcomes unavailable at the origin are not retrievable evidence in a replay. A live response that arrives after the decision timestamp cannot support a fictitious earlier options fill.

## 11. Real learning and controlled recursion

Learn four things from matured outcomes: model parameters, context-dependent mixture weights, calibration maps, and acquisition policies. Every change has an originating evidence window and a version. Retain failed and abstained forecasts in evaluation.

Strategy memory stores typed performance episodes with forecast ID, model family, context, horizon, score, reference score, cost, availability and outcome-maturity timestamp. Attribute credit from paired comparisons or designed ablations. Do not give every component in a successful coalition identical causal credit.

Preserve the useful idea of stigmergic shared memory as an evidence ledger. Optional Hopfield-style associative retrieval, Hebbian updates or sparse learned controllers are research challengers against ordinary nearest-neighbor retrieval, regularized regressions and contextual bandits. They are not mandatory components or sources of unearned scientific novelty.

Separate three lanes: **frozen inference**, **shadow adaptation**, and **promotion**. Agents may propose graph/model changes only in the shadow lane. Promotion requires declared comparisons, calibration checks, resource/license gates and a reversible version change. Evaluation definitions, permissions, budget caps and audit logging remain outside the learner's authority.

Full RL is deferred until sequential decisions and delayed rewards demonstrably justify it. Do not optimize a sparse simulated trading return before the underlying probabilistic forecasts and execution model are trustworthy.

## 12. UX requirements

The first useful screen answers: what outcome, over which horizon, under which data and model version, and with what demonstrated calibration? It includes an evidence drill-down, missingness warnings and baseline comparison.

The graph view distinguishes facts, parameters, latent states and proposed causal links. Each node shows distribution family, support, source, inferred vs manually specified status and update history. Side-by-side branches expose which assumption changed and how much the numerical output moved.

The experiment view shows performance by asset, horizon, event family, regime and cost; a global average cannot hide failures in a few assets. Use uncertainty bars for evaluation estimates. Show `NOT_IMPLEMENTED` or `INSUFFICIENT_EVIDENCE`, not invented values.

The options view is visibly separate: a strong volatility warning may coexist with `NO_SUPPORTED_EDGE`. No “buy now” control exists.

## 13. Operational guarantees to implement

Reserve external-call budgets transactionally before dispatch, reconcile actual spend, bound retries and parallelism, and persist failed attempts. Default API cap is zero. Data subscription fees are tracked separately from per-call AI cost.

Run inference with a frozen manifest, random seeds, input hashes, library versions and precision settings. Promise exact reproducibility only where supported; otherwise specify numerical tolerance. Recover from process interruption without duplicate evidence, forecasts, outcomes or budget charges.

Use safe serialization for metadata and trusted signed/hashed model artifacts. Do not load untrusted pickle files. Redact credentials, exclude private source-repository datasets from the new project, and enforce licensed-data export policies.

Monitor forecast skill, calibration, selective coverage, input quality, drift, resource use and provider/model availability separately. A model outage leads to a labeled degraded result or abstention, not silent synthetic data.
