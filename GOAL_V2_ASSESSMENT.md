# Assessment of the v2 goal and earlier VOLTERRA analysis

**Date:** October 18, 2026. **Task:** assess the four named files and continue brainstorming. This is a document assessment and proposed direction, not adoption of a new governing goal or authorization to implement the full transformation.

## 1. What was assessed previously, and now

| File | Previous-turn coverage | Assessment in this turn |
|---|---|---|
| `VOLTERRA GOAL v2.txt` | Not assessed | Read in full. It is a handoff summary referring to a generated goal, not the detailed implementation contract itself. Its old sandbox download link does not establish which local goal is active. |
| `GOALn.md` | Not assessed | Read all 1,235 lines. This is the substantive v2 transformation proposal, including event/cascade forecasting and a considerably more explicit adaptive-ensemble research program. |
| `PROGRESS.md` | Created as the prior audit log | Re-read and compared with the current files. It accurately records that earlier audit's actions, but its next-ticket recommendation belongs to the v1 scope used then. |
| `VOLTUPD_GAP_ANALYSIS.md` | Created and verified in the previous turn | Re-read in full against v2. Most foundational/event/cascade findings remain applicable; the arbitration, selection and milestone mapping need a v2 supplement. Its inventory is historical. |

`GOAL.md` and `AGENTS.md` still contain the v1 scope and T00–T03 first assignment. `GOALn.md:20` declares that it supersedes the older goal. These files need explicit reconciliation before implementation; a request to assess and brainstorm does not itself rename or activate a document.

## 2. Verdict

**GOALn.md is the fuller candidate specification for the intended product.** It incorporates the event/cascade safeguards and adds a substantial, testable question: does event-aware selection and allocation of forecasting expertise improve calibrated outcomes or resource use?

Keep three independently measurable contributions:

1. **Information:** do archived event forecasts improve downstream volatility predictions?
2. **Structure:** do transmission/cascade representations improve on an ordinary numerical model with the same information?
3. **Allocation:** do selection and arbitration improve on the same expert pool under the declared budget?

Success on one does not prove success on the others. All three can share evidence, snapshots, forecast storage and evaluation infrastructure.

## 3. Material changes relative to the earlier gap analysis

| Addition or refinement | Location in `GOALn.md` | Assessment |
|---|---|---|
| Separate cheap pre-inference selection from post-inference weighting | 530–556 | Essential distinction. Running every model to decide which ones to run cannot demonstrate inference savings. The earlier report did not assess this requirement in comparable depth. |
| Equal/global/rolling/feature/event-stage allocation on the same pool | 538–548 | A useful controlled experiment. Freeze the pool so an allocation gain cannot be explained by adding a better model. |
| Distinct loss-to-weight, FFORMA-inspired and direct-mixture objectives | 558–576 | Stronger than a generic “learn weights” requirement. Individual-expert loss and final-mixture loss are different objectives. |
| Unconditional stacking versus conditional-world fusion | 578–594 | Resolves a major double-counting risk. World mass and expert allocation must remain separate, including in training and cache identity. |
| Explicit prohibition on consensus-as-outcome learning | 596–614 | Retain. Hypothetical ensemble outcomes can support a labeled simulation experiment, not official reliability updates. |
| Time-matched acquisition control | 643–655 | Improves the older paired-revision recommendation: compare at the same reissue time, using the same still-future target window and routine information. |
| GARCH target/measurement link and joint calibration safeguards | 323–341 | Valuable precision: return variance is not automatically a full distribution of an intraday variance estimator; separately calibrated heads do not automatically form a coherent joint forecast. |
| TimesFM 2.5 gains priority; TiRex becomes optional | 260–279, 849 | A roster change relative to v1, to record explicitly when adopting v2. Preserve the proposed TTM/Chronos-2/TimesFM 2.5 roster rather than silently substituting models. Local compatibility remains untested. |
| Plans schedule no external monitoring until enabled by the operator | 693–695 | Separates preparing a research plan from starting a recurring external job. |
| Complete workflows, generated artifacts and new acceptance identifiers | §§16, 21–24 | More actionable than the narrative update, but still requirements. Counted 24 tickets, 10 workflows and 100 unique acceptance IDs; none is an executed application test. |

The original 24 capability gaps should be mapped into VT00–VT23 rather than maintained as a competing implementation roadmap alongside T/VU/NG tickets.

## 4. Remaining issues to resolve in the design discussion

### A01 — One canonical goal and milestone boundary

The new first result in lines 35–42 includes a baseline forecast, an exact cascade query and proper scores. The ticket table places the exact graph in VT03, classical forecasts in VT04, and scoring/forecast storage in VT05, while M0 is VT00–VT03. The dependency graph is acyclic, but the description of the first completed slice and the milestone labels are inconsistent.

**Proposed resolution:** retain an integrity foundation gate, then identify VT04–VT05 as the first complete scored offline demonstration. Alternatively, split out a minimal baseline and score path explicitly. Do not label schema/ledger/graph completion as the complete scored application slice.

### A02 — Deterministic call controls must precede external adapters

VT06 introduces checkpoint adapters and VT10 source adapters; VT16 contains transactional budget/resource controls. Section 14 already requires enforcement before calls, but the ticket order does not assign the early minimal enforcement implementation.

**Proposed resolution:** split VT16 into an early deterministic policy/reservation/timeout/completion service and a later learned selector. Local authorized archive-file imports can remain offline. Preserve zero paid-call defaults and explicit download/source permissions.

### A03 — Make offline readiness independent of checkpoint availability

VT08 lists VT06 as a dependency even though the initial offline demonstration needs no downloaded models and v2 permits blocked adapters. Clarify the actual gate: a reproducible classical/offline path can work while a particular checkpoint integration is blocked, but that does not make the checkpoint integration verified.

**Proposed resolution:** publish capability-specific readiness and an explicit offline release profile. Keep the planned model roster and the full integration obligations visible. Do not confuse an optional/blocked-model exception with complete verification of all mandatory integrations.

### A04 — Monitoring needs an observation model

The planner's utility in lines 505–516 includes detection, lead time and costs. It still needs a concrete contract for **what a monitoring action lets us observe, with what delay, coverage, error and failure probability**.

A cascade can be likely while its earliest reliable confirmation arrives after the market response. Selecting that monitor cannot provide the same utility as observing an early, reliable signal. Two feeds of the same upstream event may add resilience without adding independent event probability.

**Proposed resolution:** define each monitor's observation/receipt process, false/missed-confirmation behavior, cadence, deadline and cost. Evaluate whether its usable alert precedes the qualifying episode by the required lead time. Selecting monitors changes this observation process, not the modeled occurrence probability of the external event.

The utility also needs comparable units or explicit tradeoff coefficients before subtracting monetary and latency costs. Freeze them before policy evaluation.

### A05 — Event state is multidimensional

The state list at lines 395–399 mixes physical phase, knowledge/confirmation and downstream response. The text correctly says it is not one universal lifecycle, but an executable schema must express the separation.

**Proposed resolution:** keep physical state, evidence/confirmation state, and instrument-specific propagation state separately. One event may be confirmed while its impact is buffered for one contract and active for another. `BUFFERED` should not erase the fact that the precursor occurred or apply to every exposed instrument.

### A06 — A selective expert policy needs reliability audit data

Once a cheap selector stops running some models, their forecasts for those origins do not exist. A matured target alone does not reveal what an unrun expert would have predicted. Gate training on cached full-pool predictions and operational savings are therefore different accounting stages.

**Proposed resolution:** train initial selectors from a frozen, chronologically generated full-pool forecast store. Charge that computation. For later adaptation, use bounded full-pool audit runs or supported randomized selection where justified; preserve missing counterfactual forecasts as missing. Extend the acquisition propensity/counterfactual safeguards to expert selection.

### A07 — Episode identity and fitting support need an explicit convention

Origin-frozen thresholds are appropriate forecast targets, but different origins may label overlapping pieces of the same physical market episode. Distinct-world counting, cross-origin evaluation grouping and learned delay estimates cannot rely on scenario names alone.

**Proposed resolution:** define query-local episode matching/deduplication and a separate evaluation clustering rule. Preserve each origin's frozen target rather than retrospectively changing its threshold to create one convenient episode. Begin with one fixed instrument/target window before expanding cross-market matching.

Also freeze the initial trainable relationship set and regularization. Sparse event histories will not support an unconstrained graph, a rich event-stage gate and a learned monitoring policy simultaneously merely because the contracts permit them.

### A08 — Data feasibility still determines the first real experiment

No document establishes that the same authorized historical period contains usable exact gas contracts, the chosen variance estimator, as-issued weather ensembles, release vintages and timely observation metadata. Benchmark task replication and cumulative-variance application tasks must remain separate, as v2 already requires.

**Proposed resolution:** run a small feasibility intersection audit before promising a real gas/weather study. Keep missing consensus explicitly unknown. Use synthetic worlds for engineering, and prospective collection where historical availability cannot be established; neither supplies retrospective financial validation.

## 5. Current-state qualification

A read-only metadata check now finds `aXc-ace-forecaster/` at commit `3bd39789c3811a5b437baf60a65de480aa0486bf`, matching the prior donor audit's pin. Its working tree contains tracked deletions. No changes were restored, and no donor scripts, data files, environment contents or serialized models were opened or executed for this assessment.

Excluding that donor subtree, the Python-file inventory still finds only `tools/validate_specs.py`. The earlier statement about one implementation file therefore describes the VOLTERRA package at the earlier audit, not the newly present donor tree. A matching donor commit does not verify the working tree or make it a VOLTERRA implementation.

The old package-test receipt remains historical evidence of 28 package checks, not 100 v2 acceptance tests. No application or model benchmark was rerun in this document assessment. The earlier validator defects remain unresolved; v2 prose has not fixed their code.

## 6. Three approaches for the next brainstorm

All approaches share the integrity foundation and the exact synthetic reference. They differ in the first research proof, not the eventual scope.

| Approach | First useful result | Tradeoff |
|---|---|---|
| **One event, complete forecasting chain — recommended starting assumption** | After instrument integrity, one defined gas/weather event, one exact contract, an ordinary variance reference, an event-feature comparator, a small transmission model, and an inspectable conditional research plan | Directly tests the product's distinctive purpose. Historical data intersection and useful lead time must first be feasible. |
| **Arbitration laboratory first** | On a frozen authorized volatility task and expert pool, compare equal/global/rolling/feature gates, then resource-aware execution | Isolates the newly emphasized ensemble contribution. It can succeed without proving event transmission or monitoring usefulness. |
| **Cascade workbench first** | Exact finite-state queries, shared causes/outcomes, branch updates and bounded monitor selection on synthetic or explicitly assumed models | Gives a concrete interactive reasoning tool early. Correct assumed-probability arithmetic does not establish learned market relationships. |

The preference question was presented separately. No answer is inferred from elapsed time; the first row is a recommendation for discussion, not approved scope.

### Proposed organizing object: a conditional research watch

Instead of making the first useful product a large model catalog, organize one user-visible result around a defined question:

> Which precursor could change this contract's volatility forecast, what evidence could confirm or weaken it, when would that evidence arrive, and would the downstream prediction window still be open?

A proposed watch joins existing v2 concepts rather than creating a second authority:

- The event definition, current belief, its uncertainty and supporting evidence.
- The instrument-specific conditional response and the ordinary baseline.
- The observations that could change the forecast, with receipt/processing latency and monitoring cost.
- The conditional plan's activation, expiry, contradiction and non-propagation conditions.
- The models actually run, their weights and evidence of past usefulness.
- The later event, volatility and revision scores, including false warnings and no response.

This gives arbitration a specific role: learn whether model allocation should change as an event develops, is confirmed, fails to propagate or resolves. Start with a small fixed pool and shrink toward a simple mixture. The event probability does not mechanically become the event specialist's weight. Then test whether explicit cascade structure and selective monitoring add further value.

This is a brainstorm proposal, not an approved design or an implemented workflow.

## 7. Focused research and mathematical checks

Primary documentation was checked for consequential new claims, without installing the models or reproducing their benchmarks:

- [Chronos-2's official card](https://huggingface.co/amazon/chronos-2) documents quantile outputs and native past/future covariates and multivariate inputs. This supports its proposed adapter role, not joint-path or VOLTERRA skill claims.
- [TimesFM's official repository](https://github.com/google-research/timesfm) documents TimesFM 2.5 XReg support and distinguishes its Apache-2.0 weights from downloaded TimesFM 3 restrictions. These source statements do not establish a tested Mac deployment or grant data rights.
- The [FFORMA author page](https://robjhyndman.com/publications/fforma/) supports feature-conditioned combination as an established method. The [Toto 2.0 report, §5.3](https://arxiv.org/html/2605.20119v1) describes its FFORMA/XGBoost weighting approach. These motivate controls; their fitted allocations are not transferable market evidence.
- [CastStar's artifact card](https://huggingface.co/USTC-AGI/CastStar) explicitly says its frozen bundle contains no training data or training code. It is not a ready-made VOLTERRA fitting pipeline.
- [TeeMoE's appendix A.5](https://arxiv.org/html/2609.40265v1) describes source-series cross-fitting of numerical reference forecasts. It also constructs bounded empirical distributions from supplied quantiles. V2 appropriately adds chronological/shared-event constraints and avoids treating sparse quantiles as complete financial tails.
- The [Synapse paper's forward-simulation section](https://arxiv.org/html/2511.05460v1) uses an ensemble median as a simulated observation. V2's separation of that experiment from official outcome learning is justified.

The CRPS mixture identity in lines 564–572 was checked on a finite-distribution reference calculation: the direct mixture score was approximately 0.54 and the component/cross-distance identity was 0.54. Two point experts at 0 and 1 with equal weights and outcome 0 give mixture CRPS 0.25, while average individual CRPS is 0.50. This confirms why the proposed training objectives should have distinct names. It is not a trained gate or application acceptance result.

Programmatic document checks found **100 distinct AC IDs, 24 tickets, 10 workflows, no undefined listed VT dependency, and no cycle in those dependencies**. These are structural results only. The full set of 27 research references was not independently replicated, and no forecasting superiority, resource performance or economic result was measured.

## 8. Handoff status

Assessment completed; the priority preference remains open for the continuing brainstorm. Keep `GOALn.md` as the candidate full v2 target, reconcile the issues above into the design, and then deliberately activate one canonical goal when that design is accepted. The existing goal files were not replaced. No application code was changed, no implementation ticket was completed, and no donor work was modified.
