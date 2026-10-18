# Research notes and source register

**Checked October 17, 2026.** This register supports technology selection and corrections to earlier conceptual designs. Vendor claims are attributed; no competitor product or forecasting benchmark was independently run. Live upstream pages can change: pin exact revisions and licenses when implementing.

## Competition: define a narrower contribution

**R01 — ORATS Data API.** The provider documents historical option data, proprietary IV/slope forecasts, and WHAM event-day analytics. Its near-EOD quote snapshots are recorded before the close, which matters when aligning a forecast origin. It also notes that its underlying reference values are derived from option prices; obtain actual price bars separately for target construction.

Source: https://orats.com/data-api

**R02 — ORATS WHAM.** Public documentation describes decomposing which days the options market prices for larger moves. Therefore merely identifying a “volatility clock” or displaying market-implied event timing is not sufficient differentiation. VOLTERRA should compare independent physical forecasts and evidence-sensitive revisions against such implied measures.

Source: https://orats.com/wham

**R03 — SpotGamma Volatility Trigger.** Described as a proprietary level associated with a change in anticipated feedback/volatility behavior. This is evidence of overlapping functionality, not proof that its indicator outperforms or matches the proposed system.

Source: https://support.spotgamma.com/hc/en-us/articles/15297954935699-Volatility-Trigger

## Time-series methods

**R04 — Direct volatility study.** Alessio Brini, *Forecasting Realized Volatility with Time Series Foundation Models: A Comparison with Econometric Benchmarks*, July 6, 2026, preprint. The study reports heterogeneous results, a narrow TTM advantage under its per-asset comparisons, and competitive TTM/Log-HAR averaging. It motivates mandatory classical and simple-ensemble controls, not transferred performance claims.

Source: https://arxiv.org/abs/2607.05291

**R05 — Chronos-2 model card.** Official Amazon card describes a 120M-parameter model supporting univariate, multivariate and covariate-informed quantile forecasts. Its quantile outputs must not be assumed to supply a joint path law.

Source: https://huggingface.co/amazon/chronos-2

Code/docs: https://github.com/amazon-science/chronos-forecasting

**R06 — IBM Granite time-series repository.** Includes TTM examples, benchmarking utilities and model references. Treat the actual selected checkpoint and adapter as an explicit dependency; do not infer forecast-distribution capability from the repository name.

Source: https://github.com/ibm-granite/granite-tsfm

**R07 — TiRex-2 repository and official model card.** Support multivariate/covariate forecasts and CPU examples. Importantly, public docs list incremental streaming updates among Pro extensions. Do not infer free incremental stateful-inference availability solely from the research architecture. The official model card labels the checkpoint Apache-2.0; preserve exact revision/license checks.

Sources: https://github.com/NX-AI/tirex-2 and https://huggingface.co/NX-AI/TiRex-2

Paper: https://arxiv.org/abs/2607.01204

**R08 — TimesFM 3.0 official weights.** The official card explicitly lists the TimesFM Non-Commercial License v1.0. The source-code repository's license does not automatically authorize commercial use of those weights. Research testing and commercial deployment are separate registry statuses.

Source: https://huggingface.co/google/timesfm-3.0-pytorch

Release explanation: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/

**R09 — Toto 2.0.** Datadog's official release describes a range of model sizes and multivariate forecasting. It is an optional diversity/cost challenger. Actual checkpoint license, output semantics, contamination disclosures and hardware compatibility still require the adapter acceptance process.

Sources: https://www.datadoghq.com/blog/ai/toto-2/ and https://github.com/datadog/toto

## Expert-system and inference tools

**R10 — clipspy.** Official Python bindings for CLIPS. Suitable as a rule-engine backend for audited predicates, not as the numerical distribution inference layer.

Source: https://clipspy.readthedocs.io/en/latest/

**R11 — PyMC distributions documentation.** Documents continuous, discrete and mixture distributions. Use for explicit offline probabilistic models; inference strategy and diagnostics remain model-specific engineering work.

Source: https://www.pymc.io/projects/docs/en/stable/api/distributions.html

**R12 — pgmpy documentation.** Describes probabilistic/causal graphical-model workflows. A graph visualization or learned directed graph does not alone establish an identified causal effect. Use as an optional reference backend for a supported subset, not a universal automatic continuous-time ESS compiler.

Source: https://pgmpy.org/index.html

## Data and financial interpretation

**R13 — ALFRED help.** Describes vintage economic data and source release dates; additions commonly follow release rather than guaranteeing exact intraday receipt. Supports the need for publication/vintage-aware replay.

Source: https://alfred.stlouisfed.org/help

**R14 — Open-Meteo historical forecasts.** Documents historical weather forecast access. The adapter must verify exact forecast issue/run and lead-time semantics. A convenient stitched series is not automatically the exact forecast known at an arbitrary historical origin.

Source: https://open-meteo.com/en/docs/historical-forecast-api

**R15 — Options Industry Council, Long Straddle.** Explains the strategy and its premium, expiration, volatility and time-decay considerations. Supports keeping strategy payoff distinct from realized-volatility prediction.

Source: https://www.optionseducation.org/strategies/all-strategies/long-straddle

**R16 — Chen Xu and Yao Xie, Sequential Predictive Conformal Inference for Time Series, ICML 2023.** Provides a time-series conformal method. Do not extrapolate a particular method's assumptions into unconditional crisis-proof interval guarantees.

Source: https://proceedings.mlr.press/v202/xu23r.html

**R17 — arch forecasting documentation.** Documents analytical, simulation and bootstrap forecasting approaches for volatility models. Supports a strong classical/reference implementation before foundation-model complexity.

Source: https://arch.readthedocs.io/en/latest/univariate/forecasting.html

## Private source audit

See `REUSE_AUDIT.md` for pinned source paths, inspected ranges, code-level findings and license. Source code was inspected; its full runtime and numerical claims were not independently validated.

## Remaining uncertainties to resolve in T00

Exact data-provider costs/entitlements for the desired instruments; usable as-issued weather and consensus archives; actual Mac memory/latency; dependency compatibility; checkpoint training overlap; public streaming interfaces; stable probability extraction from a selected decision model; sample size needed for each scientific comparison. None is resolved by labeling a module “SOTA.”
