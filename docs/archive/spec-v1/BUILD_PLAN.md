# VOLTERRA — Dependency-ordered implementation plan

Version 1.0 · No elapsed-time estimates are implied. A release advances when its gates pass, not when its dashboard looks complete.

## Proposed source layout

```text
src/volterra/
  contracts/       # schemas, types, units, invariant checks
  evidence/        # bitemporal ledger, revisions, deduplication, permissions
  instruments/     # identities, sessions, corporate actions, futures/options
  targets/         # variance estimators, horizon and episode labels
  features/        # cutoff-safe transforms and state construction
  models/          # classical, foundation and ESS specialist adapters
  distributions/  # predictive mixture, calibration, joint paths
  ess/             # graph IR, safe rules, offline fit, online filtering
  decisions/       # bounded classifier and acquisition policies
  learning/        # outcome scores, memory, challengers and promotions
  scenarios/       # immutable scenario branches
  options/         # research-only quote/contract/payoff adapters
  evaluation/      # replay, baselines, ablations and statistical reports
  storage/         # SQLite repositories and Parquet artifact registry
  service/         # CLI, durable jobs and optional local API
ui/                # added after the CLI vertical slice
config/
tests/{unit,property,integration,adversarial,replay}/
```

Each model implements `describe_capabilities`, `fit_or_load`, and `forecast`. `sample_joint` is optional and must agree with the capability manifest. Engine-facing contracts are independent of model-provider libraries.

## R0 — Trustworthy foundations

| Ticket | Dependencies | Deliverable | Acceptance |
|---|---|---|---|
| T00 | None | Freeze scope, source audit, target definitions, data feasibility, licenses and CPU dependency matrix | Record actual tested package versions; no unsupported “all models work” claim; identify options-data gap without buying anything |
| T01 | T00 | Typed contracts, schemas, versioned manifests, safe serialization and fixture validator | Reject invalid distributions, timestamps and missing identity; package-only checks distinguished from model tests |
| T02 | T01 | Evidence ledger, revision reconstruction, as-of access, immutable snapshots and idempotent jobs | Future-mutation invariance and revision/availability tests pass |
| T03 | T01–T02 | Seeded synthetic worlds and known-answer tests | Reproduce expected variance/episode/payoff arithmetic without a network or ML model |

Do not clone the old source repository wholesale. Extract only a helper with a clear owner, purpose and test. Source repository remains unchanged.

## R1 — Useful numerical volatility lab

| Ticket | Dependencies | Deliverable | Acceptance |
|---|---|---|---|
| T04 | T02–T03 | Target engine, instrument/session rules, variance/proxy separation and outcome maturity | Splits, missing bars, overnight gaps, roll events and label-confirmation lag handled |
| T05 | T04 | Persistence, EWMA, Log-HAR, GJR-GARCH, equal-weight controls | Correct origin/target alignment; analytic/simulated baselines; finite supported moments |
| T06 | T05 | Predictive distributions, proper scores, out-of-fold residual fitting and past-only calibration | Identical point experts retain nonzero outcome uncertainty; scores match known examples |
| T07 | T01,T06 | TTM and Chronos-2 adapters, then TiRex-2 challenger | Real capability/license manifests, failure identity, model artifact hashes, CPU smoke tests; no silent sample collapse |
| T08 | T06 | Native or fitted joint-path layer; coherent horizon aggregation and episode outputs | No independent marginal sampling masquerading as paths; right/left censoring supported |
| T09 | T04–T08 | Walk-forward replay, nested calibration/tuning, baseline/ablation report | All origins including failures accounted for; transforms and weights obey cutoff; no impressive-result gate required |
| T10 | T09 | CLI vertical slice and minimal inspection report | Operator can reproduce forecast, evidence, matured score and baseline comparison from a manifest |

Required workflow, to be implemented:

```text
volterra fixtures generate --scenario switching-variance --seed 17
volterra replay run --config config/research.yaml
volterra forecast inspect <forecast_id>
volterra evaluation report <run_id>
```

These are proposed interfaces, not commands supplied by this specification package. R1 can pass engineering acceptance even when a simple benchmark wins.

## R2 — ESS and evidence-conditioned scenarios

| Ticket | Dependencies | Deliverable | Acceptance |
|---|---|---|---|
| T11 | T01,T06 | Graph IR, per-family validators, safe function registry and deterministic gate engine | Reject inconsistent support, cycles and executable payloads; extreme forecasts do not automatically fail |
| T12 | T08,T11 | Small fitted ESS specialist, online filter and optional discrete reference backend | Known-answer inference tests, posterior/MC diagnostics, explicit unsupported graph errors |
| T13 | T02,T11 | Structured event evidence and minimal archived-source adapters | Timestamped claims, source spans, contradiction and duplicate-source tests; no guessed numerical confidence |
| T14 | T09,T12–T13 | ESS vs same-information numerical comparator; immutable scenario branching and initial graph UI | Full ablation report; edits never mutate official forecasts or targets; conditions and interventions distinguished |

Start with numeric event/calendar fixtures before introducing free-text retrieval. The ESS may be informative for scenarios yet fail to improve forecasting; show that result rather than hiding it.

## R3 — Bounded adaptive intelligence

| Ticket | Dependencies | Deliverable | Acceptance |
|---|---|---|---|
| T15 | T13–T14 | Bounded State Builder and decision-model adapters | Known facts stay in rules; option order, invalid action and missingness tests pass |
| T16 | T02,T15 | Budget ledger, permitted acquisition dispatcher and revision contracts | Pre-dispatch reservation, bounded retries, stop behavior, time-of-arrival and no-paid-call-at-zero-budget tests |
| T17 | T09,T16 | Context-conditioned performance memory and acquisition-bandit challenger | Matured labels only; paired contribution scores; exploration and selection probabilities logged where needed |
| T18 | T17 | Frozen/shadow/promotion lanes, rollback and model-catalog candidate workflow | Learner cannot edit authorization/benchmarks; fresh confirmation gate; old manifests replay unchanged |

Promotion order: fixed rules, then regularized supervised routing, then a contextual bandit. Full RL and biological-memory analogues require a separate written experimental hypothesis and matched simpler control.

## R4 — Optional options research bridge

| Ticket | Dependencies | Deliverable | Acceptance |
|---|---|---|---|
| T19 | T00,T04,T09 | Authorized quote adapter and complete contract registry | Exact source timestamps, historical quote coverage, expiry/settlement/multiplier and entitlement checks |
| T20 | T08,T19 | Unhedged expiry-straddle evaluation with fixed policy | High-variance round-trip counterexample, conservative fill costs, no synthetic quotes mixed with real evaluation |
| T21 | T20 | Optional early-exit scenario model and bid-quote realized evaluation | No hindsight exits; availability and model-price vs actual-price distinction enforced |
| T22 | T18,T20 | Frozen prospective shadow protocol and final paired research report | Forecast skill and economic returns separated; failures and no-edge decisions retained |

A contract-specific natural-gas extension requires its own T04/T19 acceptance and a nonpositive-price policy. Do not assume the equity adapter covers it. Delta-hedged experiments follow a separate specification after R4; automated execution remains excluded.

## Definition of a completed ticket

Code exists, its contract is documented, relevant tests actually run, artifacts/results are attached, limitations are recorded, and no earlier gate regressed. A screenshot, README claim, mocked connector response or successful import is not proof that the ticket is complete.

Every coding-agent work report states: files changed, tests run, exact results, unresolved risks, implementation-vs-simulation status, and the next dependency-eligible ticket.
