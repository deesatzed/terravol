# GOAL — VOLTERRA

Version 1.0 · October 17, 2026

## 1. Mission

Build a local-first system that forecasts **future volatility, not directional stock-price targets**, using calibrated time-series models, an editable probabilistic expert system, evidence-aware decision routing, and outcome-grounded adaptive learning. Make every forecast inspectable and replayable. Determine experimentally whether complexity improves on strong simpler baselines.

The optional options module is a downstream research consumer. A volatility forecast is not itself a trade recommendation or proof of a straddle edge.

## 2. Stakeholders and non-negotiable constraints

The primary operator is a technically capable researcher using one Mac M4, with optional bounded external AI calls. Researchers need reproducibility and honest uncertainty; coding agents need unambiguous contracts; future users need clear distinctions between data, assumptions, simulations and validated forecasts.

Use a separate VOLTERRA project. Do not modify the source aXc-ACE repository or import its private datasets, credentials, hospital-specific policies, model weights or performance claims. Extract only reviewed, tested software patterns with license attribution.

Core operation must work without network access on synthetic fixtures. External API spend defaults to zero until explicitly configured. No autonomous brokerage execution, account linking, order placement, short-option selling, or live financial actions belong in scope.

## 3. Product outcomes

For each instrument and origin, return:

1. A predictive distribution of cumulative realized variance and annualized volatility for 1, 5 and 20 trading sessions, with the actual measurement definition and units.
2. Where a validated joint-path model is available, the probability, timing and duration of an explicitly defined high-volatility episode. Include no-event and right-censored outcomes.
3. Evidence provenance, quality, missingness, disagreements and historical calibration records. Uncertainty is not one invented confidence score.
4. A side-by-side scenario branch showing how edited assumptions change the forecast without altering the official record.
5. A forecast revision record that explains changes by new evidence, elapsed time, data revision, calibration change, or model-version change.
6. An optional options-research assessment that can legitimately return `NOT_ASSESSED`, `INSUFFICIENT_DATA`, or `NO_SUPPORTED_EDGE`.

A marginal-quantile model may satisfy outcome 1 while outcome 2 remains unavailable. Never fabricate path-level output merely to complete a dashboard.

## 4. Required capability groups

**G01 — Evidence ledger.** Bitemporal/vintage-aware immutable evidence, instrument identity, exchange calendar, source permissions, availability policy, lineage and contradiction groups.

**G02 — Target engine.** Intraday realized-variance calculation when data permit; explicitly named daily-return proxies otherwise. Correct overnight handling, revisions, splits, futures rolls, nonpositive prices and label maturity.

**G03 — Forecast lab.** Persistence, EWMA, Log-HAR, GJR-GARCH and equal-weight baselines. Replaceable TTM, Chronos-2 and TiRex-2 challengers; other models only after capability/license checks. Forecast distributions and actual fallback identity must survive every adapter.

**G04 — Joint-path engine.** Generative paths or a separately fitted and validated dependence adapter. Duration and onset outputs must derive from coherent paths or a separately validated survival head whose disagreement is disclosed.

**G05 — Expert system.** Typed graph, guarded deterministic rules, conditional probability models, numerical inference, observation-error handling, explainable node updates and a scenario editor. LLMs propose hypotheses; numerical inference computes probabilities.

**G06 — Bounded decision routing.** Fast classification over a compact verified state, including `STOP`, `ABSTAIN`, `RESEARCH_REQUIRED` and permitted acquisition actions. Code handles known facts and permissions. Probabilistic token scores are not automatically calibrated real-world probabilities.

**G07 — Outcome-grounded adaptation.** Immutable prediction/outcome ledger, delayed-feedback scoring, context-conditioned model reliability, controlled challenger promotion and rollback. No learning from a critic's opinion of another critic.

**G08 — Evaluation.** Leakage-resistant replay, proper scoring, predeclared hypotheses, budget-matched ablations, tail tests, selective coverage and an untouched/prospective confirmation stage.

**G09 — User interface.** Forecast, evidence, ESS graph, scenario comparison, model health and experiment views. Show real data or explicitly synthetic fixtures; never animated confidence theater.

**G10 — Optional economic bridge.** Contract-aware, timestamp-consistent, cost-aware straddle research. Separate unhedged expiry, early exit and delta-hedged strategies. No execution adapters.

## 5. Immutable design rules

- Inputs to a forecast must have been available under its declared historical or live availability policy. A date alone is not sufficient intraday evidence.
- Every transform, calibration fit, model selection, analogy retrieval and learning update must obey the same cutoff.
- Future-known calendar events are allowed. Their future outcomes are not.
- A forecast issued at origin t predicts outcomes after t. Never feed the scored target into its predictor.
- Correlated reports and experts are not independent confirmations. Preserve source/dependency groups.
- Predictive uncertainty must include outcome variability, not just disagreement of point forecasts.
- A forecast outside historical norms is not automatically invalid. Invalid units, corrupt data, impossible support and failed inference are separate from exceptional risk.
- A fallback must identify the actual fallback model. It cannot retain the failed model's identity or receive its learning credit.
- Missing, unavailable, withheld, stale and zero are different states.
- A user's manual edit is an assumption or intervention proposal, never a newly observed fact.
- No arbitrary executable code may be entered through a graph, news item, rule editor, model output or serialized object.
- No production model, prompt, graph structure, benchmark, license policy or authorization rule may change without a versioned promotion decision.
- Monte Carlo samples are computational draws, not additional independent market observations.
- Research-only or unresolved-license weights cannot enter a commercial deployment manifest.
- Data-provider entitlements and model licenses are independent of source-code licenses.
- The statistical forecasting product remains useful when the economic bridge cannot find an edge.

## 6. Scope boundaries

Initial numeric engineering universe: a small frozen list of broad-market equity ETFs, such as SPY, QQQ and IWM, subject to available authorized data. These are test instruments, not recommendations. Start with session-close research, not high-frequency execution. Price bars remain inputs needed to measure volatility.

Add a **contract-specific natural-gas adapter** after the equity integrity tests pass. Do not silently substitute an energy ETF or a back-adjusted continuous futures series for a deliverable futures contract. Commodity options require additional settlement and expiry metadata.

Defer a universal multi-asset platform, training a foundation model from scratch, every-news-source ingestion, autonomous graph mutation, unconstrained RL, automated trading and claims of proven causality. Preserve extension contracts for these research directions without making them MVP dependencies.

## 7. Completion gates

**Engineering-complete R1:** Offline slice, real contracts, correct targets, distribution-preserving adapters, immutable replay, baseline evaluation, tested failure behavior and reproducible setup. This gate does not mean profitable or scientifically superior.

**Research-supported R2/R3:** Predeclared experiments demonstrate incremental calibrated forecasting value, or explicitly reject the added mechanism. Failed experiments are valid outputs. No unconditional promise of a particular accuracy improvement.

**Economic-research-ready R4:** Authorized historical quotes, actual contract specifications, trade-time availability, conservative fill assumptions and all bridge invariants verified. Forecast accuracy and economic performance reported separately.

**Deployment-ready:** All applicable tests pass; operational failure modes are documented; model/data licenses resolved; budget and resource limits enforced; no hidden credential, paid-data or cloud dependency; forecast history auditable. Performance must be demonstrated on a prospective or genuinely untouched sample before marketing superiority.

## 8. Anti-drift expectations

At completion, the operator can ask: “What is likely to happen to volatility, when, why, what would change the forecast, and how well has this worked before?” The system answers using recorded numerical outputs and evidence, or states exactly why an answer is not supported.

It must not become a stock picker, a collection of agents debating unsupported percentages, a dashboard whose intervals reflect only model disagreement, or a backtest optimized until it looks impressive.

Implement tickets in `BUILD_PLAN.md` in dependency order. Report completed tests, failed tests, unimplemented capabilities and the next ticket without inventing progress.
