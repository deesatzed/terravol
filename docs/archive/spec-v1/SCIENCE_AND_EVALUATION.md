# VOLTERRA — Scientific and evaluation specification

Version 1.0 · October 17, 2026

**All numerical thresholds below are proposed engineering/research defaults, not observed performance. Freeze them before a confirmatory experiment.** Source keys resolve in `RESEARCH_NOTES.md`.

## 1. Scientific questions

H1: Does an event-conditioned probabilistic ESS improve out-of-sample volatility distributions beyond both a temporal baseline and a nonlinear model supplied with the same evidence?

H2: Does regime-conditioned strategy memory improve on an equal-weight or globally fitted ensemble after accounting for calibration, compute and selection uncertainty?

H3: Does bounded evidence acquisition improve a proper forecast score per unit of cost compared with fixed, random and disagreement-only acquisition policies?

H4: Do forecast-revision contracts identify which new observations genuinely improve the forecast, rather than merely making its explanation more elaborate?

H5, downstream only: Does any forecasting advantage survive the particular options payoff, horizon, quoted prices, fees and execution assumptions?

Hypotheses may fail. Do not redefine success after seeing the test sample. Novelty is an experimentally supported contribution, not the presence of fashionable model families.

## 2. Primary target definitions

For an equity session with reliable intraday prices, define within-session log returns on a frozen sampling grid and a separate previous-close-to-open return:

`R_t = r_overnight,t^2 + sum_j r_t,j^2`.

This is an observed realized-variance estimator, not direct observation of latent integrated variance. Sampling frequency, missing-bar tolerance, market session, price adjustment and microstructure controls are part of `target_version`.

For horizon H trading sessions:

`V_t,H = sum_{j=1..H} R_(t+j)`

`vol_t,H = sqrt(A * V_t,H / H)`

where A is the recorded annualization convention, initially 252 for the equity research profile. Store returns as decimals, variance as squared decimal returns and displayed annualized volatility as a percentage. Squared percent returns cannot be mixed with squared decimal returns.

Primary horizons are 1, 5 and 20 completed trading sessions. Their labels mature after the last required observation and data-quality/revision policy, not merely when a wall-clock timer reaches H days. Preserve overnight and event-window coverage; otherwise the target may omit the risk an option premium includes.

With only daily closes, the sum of squared daily returns is a **daily-return variance proxy**. Name it accordingly and do not silently compare its scores with an intraday-realized-variance benchmark. Insufficient or stale intraday bars are not zero variance.

Log-HAR models log daily variance using short-, medium- and longer-history aggregates. If log predictions are transformed back, use the predictive distribution/appropriate moment adjustment; exponentiating a mean log prediction gives a median under lognormal assumptions, not the variance mean required by some losses.

## 3. Episode onset and duration

A reproducible initial labeling rule:

- At forecast origin t, estimate upper and lower thresholds from the last 252 completed eligible daily variance measurements; proposed percentiles are 80 and 60. Persist those thresholds with the forecast. A separate minimum-history policy determines eligibility.
- A new high-volatility episode starts with the first of two consecutive sessions above the stored upper threshold.
- An episode ends at the first of two consecutive sessions below the stored lower threshold.
- Isolated jumps are scored under a separate single-session exceedance label; do not hide them because they fail the persistence rule.
- If an episode is already active at the origin, report remaining duration/left-censoring rather than pretending a new onset occurs at zero.

The second confirming session is part of label availability. An onset on day H may require observing day H+1. The learner cannot use that label before it matures. Ending an episode can similarly require an extra confirming session.

For a daily hazard conditioned only on information known at the origin:

`h_k = P(T=k | T>=k, I_t)`

`P(T<=H | I_t) = 1 - product_{k=1..H}(1-h_k)`.

If forecasting under specified future evidence, declare that scenario explicitly rather than leaking future observations into `I_t`. A posterior filtered regime uses observations through t; a full-sample smoothed regime does not qualify as a real-time input.

Display the no-event mass. Duration summaries must represent right-censoring; an episode continuing past the simulation horizon is not an episode that ends on the horizon. Observable labels, inferred latent states and hazard-head outputs remain distinct.

## 4. Predictive representation and path validity

Store quantiles and, where available, joint daily-variance paths. The 20-day variance on a path equals the sum of its daily variances. Derive 1/5/20-day summaries from that same representation. Do not independently sample each horizon and then claim coherent durations.

A separately trained direct-horizon model is allowed as a comparator. Mark its output `marginal_only` until a dependence model is supplied and validated. When a survival model produces onset probabilities separately from the path model, expose inconsistency instead of quietly substituting one answer.

Distinguish four uncertainty sources: outcome randomness, parameter/model uncertainty, observation uncertainty and numerical approximation error. Between-model spread is a diagnostic for disagreement, not an outcome prediction interval. In particular, identical model predictions can still be very uncertain.

Require finite moments where the consumer needs them. Examples: return Student-t degrees of freedom above two for finite variance; safe finite-moment log-variance families for expected variance; no unexamined exponential transform of an unrestricted Student-t.

For the optional price-path bridge, finite return variance alone is not sufficient. Exponentiating unrestricted Student-t log returns can produce an infinite expected terminal price and straddle payoff. Require a justified finite-exponential-moment return model, an explicitly documented bounded/tempered tail, or another coherent price process with the required payoff moments; numerical Monte Carlo output is not proof those moments exist. Specify the conditional drift or martingale convention and validate displacement distributions separately from variance forecasts.

## 5. Losses and evaluation summaries

### Numerical forecasts

Use CRPS when a sufficiently specified predictive CDF or samples exist, or weighted interval score/quantile loss when only quantiles are available. Do not invent a log-density from nine quantiles. Retain median MAE and variance point-forecast metrics as separate diagnostics.

For positive observed variance v and positive predicted conditional mean f, use the nonnegative QLIKE form:

`QLIKE(v,f) = v/f - log(v/f) - 1`.

Record any measurement floor and sensitivity to it. A missing value cannot become an epsilon-sized variance observation. If a provider legitimately reports zero, use a declared estimator-specific handling policy rather than an undocumented log fix.

### Episodes and tails

Use Brier score and log loss for probability forecasts, time-dependent/integrated Brier scores for survival forecasts with censoring handled explicitly, and proper interval scores for duration distributions where applicable. Report precision-recall, false alerts per observation period, missed episodes, lead time and abstention. Accuracy is not useful alone when expansion events are uncommon.

### Calibration

Report nominal versus observed coverage at multiple levels, interval width, probability reliability, PIT diagnostics when a CDF exists, and conditional results by horizon, asset, evidence quality and market regime. Model intervals are predictions to validate, not guaranteed coverage.

Sequential conformal calibration is a candidate, not magic protection against arbitrary market shifts. State the method's assumptions and whether reported coverage is marginal, long-run, conditional, or simultaneous [R16]. Calibration parameters must be fit using only matured past forecasts. A calibrator cannot simply widen every interval without being penalized by a proper score.

### Aggregation

Report per-instrument loss ratios relative to the same baseline, then aggregate across instruments with a predeclared rule. Include worst-decile, median and tail-period results. Do not let the highest-volatility asset dominate a pooled scale-sensitive metric. Handle near-zero baseline losses explicitly.

## 6. Replay and splitting protocol

Every replay step must reconstruct what was knowable then, create the forecast, seal it, advance time, and only later reveal outcomes. The evaluation engine controls time; models do not query the internet or an unrestricted full-data frame.

Use expanding or rolling-origin outer evaluation with nested, strictly earlier tuning/calibration. Train the mixture on out-of-fold base predictions, not predictions made on their own fitting rows. Purge training labels whose outcome interval overlaps a validation/test boundary, including episode-confirmation lags. Overlapping evaluation outcomes require dependence-aware inference even when there is no training leakage.

Fit scalers, imputers, thresholds, event-feature vocabularies, analog retrieval, residual copulas and Bayesian priors using permissible past data only. No full-sample HMM smoothing. No historical weather realization masquerading as a forecast. No revised macro value backdated to its observation month. No close-of-day feature used to trade on a quote recorded before the close.

A final holdout is consumable: once examined for design decisions, it is not untouched. Record when it was opened, decisions made afterward, and the next forward confirmation window. Repeated promotions cannot reuse the same secret test indefinitely.

### Foundation-model and LLM contamination

A pretrained model may have seen public historical financial data or later event outcomes. Record checkpoint release date, known training cutoff and overlap disclosures. Retrospective results with unknown overlap are exploratory, not leakage-free certification.

LLM event extraction on historical stories may benefit from memorized later outcomes even when retrieval is time-gated. Restrict extraction to cited fields, test entity/date masking and shuffled controls, but do not claim these eliminate contamination. A frozen prospective shadow period is required for the strongest claim about agent-supplied signals.

## 7. Experimental arms

| Arm | Components | Isolated question |
|---|---|---|
| A | Persistence, EWMA, Log-HAR, GJR-GARCH and equal-weight baselines | Strength of simpler numerical methods |
| B | A plus selected foundation models, fixed/global mixture | Incremental temporal representation value |
| C | B plus numerical event features in gradient boosting | Value of new evidence without ESS reasoning |
| D | Same information as C, with ESS specialist and controlled stacking | Incremental value of ESS structure |
| E | D plus context-conditioned strategy memory | Value beyond global/equal weights |
| F | E with fixed, random, disagreement and learned acquisition alternatives | Forecast-score improvement per matched budget |
| G | Best frozen forecast arm plus optional economic bridge | Strategy-specific net outcomes |

Run an uncalibrated and past-calibrated variant where necessary to distinguish information from scale correction. Include leave-one-component-out tests; multiple near-identical models do not count as independent architecture evidence. Use the same eligible instruments, origins, evidence and declared budgets for comparisons.

Record all tried configurations and failed runs. Use block or clustered resampling over appropriate time/event units, account for overlapping horizons, and control the prespecified multiple comparisons. Monte Carlo draws do not enlarge the market sample size. Estimate minimum detectable improvements and uncertainty rather than calling a handful of events definitive.

## 8. Proposed promotion contract

A candidate may become the research default only if all engineering invariants pass, licensing/resources are acceptable, calibration is not materially degraded, and a predeclared primary proper-score comparison supports the improvement. Default practical target for planning: at least 3% improvement in the selected cross-asset normalized primary loss, with a dependence-aware confidence interval supporting an improvement on a fresh confirmation set. This is a configurable target, not a performance assertion or a universal statistical threshold.

Also predeclare per-asset/tail loss limits and a calibration noninferiority margin. Choose margins based on use and data before opening outcomes. If the study is underpowered or results are mixed, retain the simpler incumbent and label the candidate exploratory. Passing software tests cannot substitute for this scientific gate.

## 9. Options bridge: three different experiments

### Unhedged expiry straddle

For an ordinary equity option pair with the same strike and expiry, held through a consistently modeled settlement:

`P&L = multiplier * (abs(S_T-K) - entry_call_ask - entry_put_ask) - fees`.

Include financing if material to the declared horizon. This assumes the contractual settlement/delivery consequences are modeled; it is not a universal formula for every cash/physical/futures product. Expected profit needs a terminal-value/displacement distribution, not just expected realized variance. A path that repeatedly moves away from K and returns to K can have high realized variance and a full premium loss [R15].

### Early-exit straddle

Use actual future option bid quotes for realized evaluation. Predictive scenario valuation needs spot/forward state, remaining maturity, implied-volatility surface, rates/dividends and contract conventions. “Exit when IV peaks” is hindsight unless an implementable policy was declared in advance. Do not present model valuations as observed executable prices.

### Delta-hedged volatility position

This is a different strategy. It requires an explicit rehedging rule, hedge prices, financing, transaction costs, jumps, discrete hedging error and capacity assumptions. A comparison of raw realized and implied volatility is not a complete P&L model. Keep this strategy deferred until the simpler bridge is correct.

### Required economic controls

Use real historical quotes with known timing and entitlements, entry at ask/exit at bid as a conservative baseline, sensitivity around feasible fills, fees, position-size limits, overlapping-position capital accounting and drawdown reporting. Midpoints are not guaranteed fills. Missing historical chains produce `NOT_ASSESSED`, not reconstructed evidence of profit.

Contract registry fields include underlying contract identity, multiplier, strike convention, expiration, last-trade date, exercise style, settlement, exchange calendar, tick value and delivery/futures exposure. Trading-day and calendar-time volatility conventions must be reconciled. Core R1 does not need live options data, but bridge feasibility is checked early so data cost is not hidden until the end.

## 10. Required adversarial worlds

Test quiet persistence; abrupt and gradual variance transitions; a one-day jump; a volatile round trip ending at the strike; an event with no market reaction; event postponement; stale quotes; duplicated or contradictory stories; same point forecasts with large irreducible uncertainty; shared model failures; data revision; stock split; futures roll; nonpositive futures price; disappearing model provider; depleted budget; missing weather vintage; future-known calendar but unknown outcome; and apparent improvement created only by target leakage.

Known synthetic generating processes test recovery and correctness. They are not evidence of real-market profitability. Real evaluation and a prospective shadow experiment remain separate gates.
