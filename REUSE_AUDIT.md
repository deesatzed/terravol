# aXc-ACE reuse audit

**Inspected:** October 17, 2026

**Repository:** `deesatzed/aXc-ace-forecaster`

**Pinned commit:** `3bd39789c3811a5b437baf60a65de480aa0486bf` (main, commit date August 28, 2026).

**Scope:** Selected source methods and the license were read. No full-clone execution, external-service test, complete test-suite run or numerical-performance reproduction occurred. Conclusions below apply to the inspected paths. Another workflow in the repository may differ.

## Reuse matrix

| Source | Verified observation | VOLTERRA disposition |
|---|---|---|
| `ace_hospital/core/ace_ensemble_unified.py` | Structured ensemble records, model adapters, weight optimization and outcome feedback exist | Extract interfaces and workflow ideas; replace distribution, validation and learning details |
| Same: `ChronosSingleton.predict` | T5 Chronos samples are reduced to one median; failures return the last observation | Rewrite adapter to retain distributions and identify actual fallbacks |
| Same: `_generate_validation_predictions` | Chronos context includes `full_context[:i+1]` while outputs are aligned against `val_data[i]` | Replace with origin/target-indexed prequential validation |
| Same: validation persistence/fallback paths | `val_data[0]` or first validation value seeds several fallback predictions | Do not copy; prior training history or explicitly named rolling baseline must supply context |
| Same: `predict` | `lower_95` and `upper_95` equal point ensemble plus/minus 1.96 times standard deviation across model point predictions | Replace with calibrated predictive distributions; retain disagreement only as a feature |
| Same: `save`/`load` excerpt | The inspected method serializes configuration/weights/deltas; it does not itself serialize all fitted base models | Require complete artifact manifests and save/reload forecast-parity tests; inspect any separate model-saving workflow before reuse |
| Same: weight-prior helpers | ACE/stigmergic performance is converted into per-model Beta specifications | Reuse prior-generation interface only; use proper simplex priors and distinguish warm starts from Bayesian posteriors |
| `ace_hospital/core/strategy_memory.py` | Helpful/harmful counts, shared coalition credit, mutation suggestions and JSON persistence exist | Reuse versioned memory concept; replace credit assignment and scores with paired proper-score evidence |
| Same: `get_codon_confidence` | Confidence is `min(total/20,1)` | Do not represent as calibrated probability or certainty |
| `ace_hospital/core/historical_context_engine.py` | Whole supplied history is summarized for anomaly, percentile and seasonal context | Retain analogy UX; enforce origin-specific history views and replace percentile-based “confidence” with actual calibration |
| `ace_hospital/monitoring/prediction_validator.py` | Historical-range and >3-sigma deviations can be errors; large daily change can fail validation | Retain typed gate/report pattern only. Exceptional volatility must not automatically fail the forecast |
| `LICENSE` | MIT license, copyright 2025 deesatzed | Preserve notices for copied substantial code; audit dependencies and data rights separately |

## The validation defect, precisely

The inspected Chronos validation loop creates context from the validation series through index i and asks for a one-step-ahead forecast, but assigns that result to validation target i. This is both a target-availability and alignment problem: the value being scored is already in the input. When Chronos falls back to persistence, that last input value can equal the target exactly.

This does not prove every reported repository result used this path. It does establish that this path is unsuitable as evidence for VOLTERRA forecasting performance. Reproduce any desired old result using an independently correct origin/target harness before transferring claims.

## Why the interval and gate changes matter

Across-model standard deviation measures disagreement, not all predictive uncertainty. Identical forecasts can produce a zero-width displayed interval despite large future uncertainty. Conversely, a failed model can inflate disagreement without adding legitimate probability mass.

The existing conservative clinical gate is aimed at a different operational problem. A volatility-warning system is explicitly supposed to anticipate unusual values; rejecting them solely for being unusual would suppress the signal it is built to find. Keep schema, unit and inference-health gates, while routing statistical extremes to risk/quality flags.

## Extraction process

Create a clean new package. Copy no private clinical data, credentials, .env files, persisted pickles or pretrained hospital artifacts. Preserve source commit/file attribution for code actually extracted. Add adapter contracts and origin-invariance tests before moving a helper.

Do not import the entire old project to save a few helper functions. Most value is in architectural patterns: modular experts, outcome memory, explanatory context and typed validation. Forecasting weights, claims of compression, reported accuracy and production badges are not transferable assets.

## Pinned source references

- [Unified ensemble](https://github.com/deesatzed/aXc-ace-forecaster/blob/3bd39789c3811a5b437baf60a65de480aa0486bf/ace_hospital/core/ace_ensemble_unified.py). Inspected lines 1–250, 750–1040 and 1080–1330.
- [Strategy memory](https://github.com/deesatzed/aXc-ace-forecaster/blob/3bd39789c3811a5b437baf60a65de480aa0486bf/ace_hospital/core/strategy_memory.py). Inspected lines 1–285.
- [Historical context engine](https://github.com/deesatzed/aXc-ace-forecaster/blob/3bd39789c3811a5b437baf60a65de480aa0486bf/ace_hospital/core/historical_context_engine.py). Inspected lines 1–250.
- [Prediction validator](https://github.com/deesatzed/aXc-ace-forecaster/blob/3bd39789c3811a5b437baf60a65de480aa0486bf/ace_hospital/monitoring/prediction_validator.py). Inspected lines 1–220.
- [MIT license](https://github.com/deesatzed/aXc-ace-forecaster/blob/3bd39789c3811a5b437baf60a65de480aa0486bf/LICENSE).
