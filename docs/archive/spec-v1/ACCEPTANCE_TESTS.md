# VOLTERRA — Required application acceptance tests

Version 1.0 · **These are planned application tests, not tests already executed.**
Package-only validation is recorded separately in `PACKAGE_VALIDATION.json`.

## Data and time integrity

| ID | Required behavior |
|---|---|
| D01 | Changing any future target leaves an earlier snapshot and forecast unchanged. |
| D02 | Changing future features, future revisions or future analog outcomes leaves earlier results unchanged. |
| D03 | An exact target value cannot enter a one-step-ahead validation context. |
| D04 | Archive import time is distinct from certified historical availability; mode policy is enforced. |
| D05 | A revised macro value appears only after its revision release becomes available. |
| D06 | A forecast-as-issued weather observation is distinguished from realized/reanalysis weather. |
| D07 | Null/missing/unavailable/stale observations cannot silently become observed zero. |
| D08 | Corporate actions cannot produce artificial volatility through an unadjusted split. |
| D09 | Futures roll adjustment cannot silently create a contract-level return observation. |
| D10 | Nonpositive futures prices are rejected by log-return adapters or routed to an explicitly supported representation. |
| D11 | Exchange sessions, holidays, early closes, offsets and overnight returns are handled by the declared target. |
| D12 | Evidence and job retries are idempotent, with preserved correction lineage. |
| D13 | A label requiring a second confirming session cannot mature on the first session. |
| D14 | Duplicate syndicated stories retain one dependency group rather than independent likelihood multiplication. |

## Predictive distributions and numerical invariants

| ID | Required behavior |
|---|---|
| P01 | Variance samples and allowed quantiles are finite and nonnegative; missing values remain missing. |
| P02 | Quantile levels and values are monotone, uniquely indexed and in declared units. |
| P03 | Percent-return and decimal-return variance conversions agree by known factors. |
| P04 | Cumulative variance equals daily-path sums and never decreases on a path as horizon grows. |
| P05 | Annualized-volatility transforms match the stored convention and need not be monotone with horizon. |
| P06 | Marginal-only experts cannot enable onset, duration or other joint-path outputs. |
| P07 | Identical point predictions do not collapse irreducible predictive uncertainty to zero. |
| P08 | Mixture weights sum to one; mixture sampling semantics differ explicitly from weighted-sum semantics. |
| P09 | Failed experts do not receive credit or identity for a labeled persistence fallback. |
| P10 | Log transforms, moment calculations and heavy-tail parameter domains are validated. |
| P11 | Analytic/reference likelihood and simulation results agree within declared Monte Carlo error on known synthetic models. |
| P12 | Path coupling is assessed for serial dependence and durations, not only marginal interval coverage. |
| P13 | All-zero weights invoke a declared fallback policy rather than hiding an inference error. |
| P14 | Save/reload preserves exact artifacts and forecast equivalence within recorded numerical tolerance. |

## Expert system and scenarios

| ID | Required behavior |
|---|---|
| E01 | Invalid distribution parameters and incompatible supports are rejected with actionable errors. |
| E02 | Median/range inputs with insufficient information require an explicit fitting convention or more parameters. |
| E03 | Instantaneous cycles are rejected; supported positive-lag feedback is explicitly unrolled. |
| E04 | Observation, assumption, parameter, latent state and target node roles remain distinguishable. |
| E05 | Contradictory and correlated evidence is represented without false independence. |
| E06 | Rule priority cannot be overridden by an AI proposal or graph edit. |
| E07 | Extreme but numerically valid forecasts are not automatically rejected for exceeding historical norms. |
| E08 | Scenario edits preserve official evidence, forecast, outcomes and history. |
| E09 | Conditioning and intervention semantics differ; unsupported causal claims are labeled or blocked. |
| E10 | Unsafe executable graph text, commands and unapproved callable functions are rejected. |
| E11 | Low effective sample size or failed convergence triggers degraded/failed inference status, not precise-looking probabilities. |
| E12 | Overlapping mechanisms are not normalized as mutually exclusive hypotheses. |

## Decision models, budgets and learning

| ID | Required behavior |
|---|---|
| A01 | Classifier actions must belong to the deterministic allowed-action set. |
| A02 | Known arithmetic and permission decisions use code rather than uncertain token predictions. |
| A03 | Option permutation/paraphrase instability is measured and can cause abstention. |
| A04 | Zero paid-call budget prevents all paid dispatch, including retries and hidden tool calls. |
| A05 | Parallel requests reserve spend transactionally; interruption cannot duplicate charges or exceed the cap. |
| A06 | Acquisition completion time is recorded; evidence cannot support an earlier fictitious decision or trade. |
| A07 | Only matured outcomes update weights, retrieval, calibration and acquisition policy. |
| A08 | Coalition credit is not awarded identically to every active component without a paired attribution design. |
| A09 | Shadow learners cannot modify benchmarks, permissions, audit requirements or official models. |
| A10 | Promotion and rollback preserve old manifests, failed candidates and fresh confirmation requirements. |
| A11 | Raw option-token probabilities remain distinct from calibrated market-event probabilities. |
| A12 | Revision contracts and subsequent realized forecast-score changes are recorded even when the investigation was unhelpful. |

## Scientific evaluation

| ID | Required behavior |
|---|---|
| S01 | All transforms, calibration, analogs and stacking use strictly eligible earlier data. |
| S02 | Label-overlap purging includes episode confirmation and outcome availability, not just nominal horizon. |
| S03 | Full-sample smoothed regimes cannot serve as historical real-time input. |
| S04 | Every added intelligence component has a same-information, declared-budget simpler control. |
| S05 | Failed and abstained origins remain in coverage, error and resource reports. |
| S06 | Per-asset, tail and regime results are reported in addition to aggregate metrics. |
| S07 | All tested configurations and opened holdouts are tracked to expose repeated-selection bias. |
| S08 | Intervals and tests account for dependence/overlapping outcomes; simulation draws do not inflate sample size. |
| S09 | Unknown pretraining overlap and retrospective LLM outcome knowledge are disclosed; prospective confirmation is separate. |
| S10 | A negative result or underpowered result retains the simpler incumbent rather than triggering post-hoc goal changes. |

## Options-research bridge

| ID | Required behavior |
|---|---|
| O01 | A high-variance path ending at the strike can lose the entire premium in an unhedged expiry-straddle test. |
| O02 | A correct large-move prediction can still lose under an expensive entry premium/IV-crush scenario. |
| O03 | Ask entry, bid exit, commissions and other declared costs are included and midpoint sensitivity is labeled. |
| O04 | A pre-close quote cannot be used as an executable entry for a post-close forecast. |
| O05 | Multipliers, contract identity, exercise, expiry and settlement are required and tested by instrument. |
| O06 | Missing historical option quotes yield NOT_ASSESSED/INSUFFICIENT_DATA, not synthetic profitability. |
| O07 | Early-exit policies are defined before outcomes and cannot use the future IV peak. |
| O08 | No API or worker can place orders or mutate brokerage accounts. |
| O09 | Physical versus implied volatility differences are not automatically labeled mispricing or profitable edge. |
| O10 | Overlapping positions, capital allocation, financing and drawdowns use a declared accounting policy. |

## Operations and interface

| ID | Required behavior |
|---|---|
| U01 | Core fixtures, schemas and numeric smoke tests run without network access. |
| U02 | Credentials/private source datasets do not enter logs, example files, exports or model prompts. |
| U03 | Untrusted pickle or arbitrary serialized code is not loaded. |
| U04 | UI capabilities and numbers reflect actual computed fields; unavailable outputs are clearly unavailable. |
| U05 | Every displayed forecast links to immutable evidence, model, calibration and target versions. |
| U06 | Process failure, cancellation and restart preserve budget/accounting and do not create duplicate forecasts. |

## Completion semantics

Passing engineering tests does not establish superior forecasting or profitable trading. Scientific promotion follows the preregistered comparison protocol. Synthetic recovery tests and real-market validation must be reported separately.
