# Probability and target semantics

This is an implementation guide to [GOAL_UPD.md](../GOAL_UPD.md), not evidence that inference exists.

## Four typed quantities

Event probability describes a frozen event/window. Transmission probability describes a downstream outcome conditional on specified precursor/context. Scenario mass is a normalized law over disjoint joint worlds, including no-event/background mass. Expert weight allocates predictive models. An 85% expert weight is not an 85% event probability, and a token score is neither without a validated target-specific mapping.

## Measurement and maturity

For a supported equity estimator, daily realized variance is overnight squared log return plus squared intraday returns on a frozen grid. Horizon variance sums the following H completed sessions, with annualized volatility `sqrt(A * V / H)`. Store decimal returns and squared decimal units. Daily-close squared-return proxies have a separate target identity. Invalid/nonpositive-price log transforms require a valid alternative task or unsupported state.

Episode thresholds freeze from eligible past data at each origin. Two-session onset/end confirmation, existing episodes and censoring affect maturity. Future calendars can be known; event outcomes, corrected releases and future weather runs cannot enter an earlier snapshot.

## Mixtures and joint paths

```text
Unconditional: F(V | I) = sum_m w_m(I) F_m(V | I)
Conditional worlds: p(V | I) = sum_s q(s | I) sum_m w_m(s,I) p_m(V | s,I)
```

Do not remarginalize an already unconditional expert in each branch. Normalize over exclusive world/model indices, not overlapping concurrent mechanisms. A CDF mixture differs from averaging quantiles, averaging point forecasts or summing random variables. Sparse quantiles require supported scores or an explicit fitted CDF/tail adapter.

For sufficient representations:

```text
CRPS(F_mix,y) = sum_m w_m E|X_m-y|
               - 0.5 sum_m sum_n w_m w_n E|X_m-X'_n|
```

Independent draws define those expectations, including same-model pairs. Minimize the actual mixture objective when that is the stated algorithm; a weighted individual-loss surrogate or loss-to-weight regressor has a different identifier.

Joint outputs use one verified time/instrument/world artifact. Draw shared conditions/parameters coherently, generate variance paths, derive episodes through the target engine and count canonical outcomes once. Preserve branch failures and omitted mass. More simulation reduces Monte Carlo error, not structural uncertainty or the need for independent real events.

## Exact synthetic references

Under the explicitly assumed independent reference cases, three 30% triggers have union 0.657; perfectly shared triggers give 0.30; mutually exclusive triggers give 0.90. With P(B|A)=P(C|A)=0.85, P(A and B)=0.255; conditional independence gives P(A and B and C)=0.21675. Without conditional independence, P(B and C|A) is bounded by [0.70,0.85]. A shared downstream B with zero background risk gives 0.55845 under the stated independent-precursor law; adding P(B|not A)=0.10 to a single-precursor case gives P(B)=0.325. These are required reference calculations, not market estimates.

## Monitoring and credit

Selecting a monitor changes observation/detection coverage, not the event-world probability. Count usable alerts meeting a frozen minimum lead time, with error/outage/latency and cost. Define utility units and conversion coefficients before evaluation. Confirmation updates through an observation model; a predicted precursor remains uncertain.

Learning credit uses matured observations and paired controls. Compare an acquisition against the same reissue time and still-future target; do not credit elapsed time or revealed parts of the outcome. An unrun expert's loss is missing. Assumptions, simulated consensus and scenario outputs never become official realized labels.
