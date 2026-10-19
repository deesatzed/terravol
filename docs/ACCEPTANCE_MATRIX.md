# VOLTERRA application acceptance matrix

Canonical requirements: [GOAL_UPD.md](../GOAL_UPD.md). Machine source: [acceptance_matrix.json](../config/acceptance_matrix.json).

**120 application requirements; 96 executed.** Scaffold tests and v1 package checks are separate. AC-ECO-01 through AC-ECO-04 are the optional VT22 research lane; AC-ECO-05 (no brokerage/execution) is mandatory VT02 work. Each passed row has an application-test receipt; every remaining test path is planned. Preserve all original 100 v2 IDs; the additional 20 requirements close consolidation gaps.

## Execution receipt contract

`PASSED` and `FAILED` records require existing application test references, a `last_run` object with `run_id`, timezone-aware `executed_at`, `command` and integer `exit_code`, plus a JSON receipt under `reports/`. Its scope is `application_acceptance`, status matches the record, `requirement_ids` includes the exact ID, `test_refs` includes the referenced tests, `tests_run` is positive, and run identity/time/command/exit match. Unexecuted states carry no last run. A ticket completion uses `ticket_verification` receipts identifying that ticket, and all dependencies must already be complete.

The scaffold validates receipt consistency, not the scientific correctness of a test or authenticity of a manually authored receipt. Actual runner outputs and code review remain required. Metadata fixtures inside scaffold tests do not execute or satisfy application requirements.

| ID | First ticket | Status | Requirement | Planned test |
|---|---|---|---|---|
| AC-TIME-01 | VT02 | PASSED | Changing data published after the origin leaves the earlier frozen forecast unchanged. | `tests/application/test_time.py::test_ac_time_01` |
| AC-TIME-02 | VT04 | PASSED | The scored target cannot appear inside a model context, scaler fit, gate feature, or analog retrieval. | `tests/application/test_time.py::test_ac_time_02` |
| AC-TIME-03 | VT02 | PASSED | Historical availability and live receipt policies are tested separately; imported archives are not rejected merely for being imported today. | `tests/application/test_time.py::test_ac_time_03` |
| AC-TIME-04 | VT02 | PASSED | First releases and revisions reconstruct different eligible snapshots at the appropriate times. | `tests/application/test_time.py::test_ac_time_04` |
| AC-TIME-05 | VT02 | PASSED | One-, five-, and twenty-session labels mature only after their complete intervals and publication rules. | `tests/application/test_time.py::test_ac_time_05` |
| AC-TIME-06 | VT07 | PASSED | Episode confirmation lags, existing episodes, and right censoring are represented correctly. | `tests/application/test_time.py::test_ac_time_06` |
| AC-TIME-07 | VT11 | PASSED | Cross-fitted event forecasts and upstream ensembles respect chronology and shared-event groups. | `tests/application/test_time.py::test_ac_time_07` |
| AC-TIME-08 | VT10 | PASSED | Forecast completion and source arrival times prevent fictitious earlier entries or earlier knowledge. | `tests/application/test_time.py::test_ac_time_08` |
| AC-TIME-09 | VT20 | NOT_IMPLEMENTED | Reusing an examined holdout for a fresh confirmation claim is rejected by the experiment manifest. | `tests/application/test_time.py::test_ac_time_09` |
| AC-PROB-01 | VT01 | PASSED | Event probability, transmission probability, scenario mass, and expert weight have distinct typed fields. | `tests/application/test_prob.py::test_ac_prob_01` |
| AC-PROB-02 | VT03 | PASSED | Invalid conditional tables, non-normalized exclusive branches, and probabilities outside [0,1] fail validation. | `tests/application/test_prob.py::test_ac_prob_02` |
| AC-PROB-03 | VT09 | PASSED | Concurrent mechanisms are not normalized as though they were mutually exclusive outcomes. | `tests/application/test_prob.py::test_ac_prob_03` |
| AC-PROB-04 | VT03 | PASSED | Background B risk when A is absent is included in total probability calculations. | `tests/application/test_prob.py::test_ac_prob_04` |
| AC-PROB-05 | VT10 | PASSED | Predicted A cannot trigger the same update as independently observed/confirmed A. | `tests/application/test_prob.py::test_ac_prob_05` |
| AC-PROB-06 | VT09 | PASSED | Conflicting or unreliable observations do not silently create certainty. | `tests/application/test_prob.py::test_ac_prob_06` |
| AC-PROB-07 | VT03 | PASSED | Unknown dependence yields declared assumptions, bounds, or an unsupported result—not silent independence. | `tests/application/test_prob.py::test_ac_prob_07` |
| AC-PROB-08 | VT09 | PASSED | User assumptions and interventions remain separate from observations and conditional sensitivities. | `tests/application/test_prob.py::test_ac_prob_08` |
| AC-PROB-09 | VT05 | PASSED | Intervals over parameters and Monte Carlo error are not mislabeled as predictive outcome intervals. | `tests/application/test_prob.py::test_ac_prob_09` |
| AC-CASC-01 | VT03 | PASSED | Three independent 30% precursors produce P(any A)=0.657 in the reference graph. | `tests/application/test_casc.py::test_ac_casc_01` |
| AC-CASC-02 | VT03 | PASSED | The independent complete-set and A-and-B arithmetic in Section 10.3 matches exact enumeration. | `tests/application/test_casc.py::test_ac_casc_02` |
| AC-CASC-03 | VT03 | PASSED | Three perfectly coincident 30% triggers produce 0.30, not 0.657. | `tests/application/test_casc.py::test_ac_casc_03` |
| AC-CASC-04 | VT03 | PASSED | Three mutually exclusive 30% triggers produce 0.90. | `tests/application/test_casc.py::test_ac_casc_04` |
| AC-CASC-05 | VT03 | PASSED | A shared downstream B under the specified assumptions produces 0.55845 and is counted once. | `tests/application/test_casc.py::test_ac_casc_05` |
| AC-CASC-06 | VT03 | PASSED | Two conditional 85% marginals preserve joint bounds [0.70,0.85] without an independence assumption. | `tests/application/test_casc.py::test_ac_casc_06` |
| AC-CASC-07 | VT03 | PASSED | Both B-and-C and either B-or-C queries are distinct and independently tested. | `tests/application/test_casc.py::test_ac_casc_07` |
| AC-CASC-08 | VT03 | PASSED | Duplicating or renaming a source/scenario does not increase world probability or coverage. | `tests/application/test_casc.py::test_ac_casc_08` |
| AC-CASC-09 | VT12 | PASSED | AND interactions, inhibitory/buffering paths, mutually exclusive branches, and lagged feedback behave as declared. | `tests/application/test_casc.py::test_ac_casc_09` |
| AC-CASC-10 | VT12 | PASSED | Cancelled, postponed, expired, and non-propagating precursors update the correct future windows. | `tests/application/test_casc.py::test_ac_casc_10` |
| AC-CASC-11 | VT12 | PASSED | Sampled market episodes and derived variance paths cannot contradict each other in a joint-capable artifact. | `tests/application/test_casc.py::test_ac_casc_11` |
| AC-CASC-12 | VT12 | PASSED | Pruning/importance sampling preserves no-event and remainder mass with correct weights and uncertainty. | `tests/application/test_casc.py::test_ac_casc_12` |
| AC-DIST-01 | VT04 | PASSED | Identical point experts can retain nonzero predictive uncertainty through their outcome distributions. | `tests/application/test_dist.py::test_ac_dist_01` |
| AC-DIST-02 | VT01 | PASSED | Quantiles are ordered with valid support; sparse quantiles cannot silently imply full tails or joint paths. | `tests/application/test_dist.py::test_ac_dist_02` |
| AC-DIST-03 | VT05 | PASSED | A CDF mixture and a weighted-quantile average are distinguished on a known counterexample. | `tests/application/test_dist.py::test_ac_dist_03` |
| AC-DIST-04 | VT05 | PASSED | The empirical/analytic mixture CRPS identity matches a direct reference calculation. | `tests/application/test_dist.py::test_ac_dist_04` |
| AC-DIST-05 | VT07 | PASSED | Variance is nonnegative; cumulative variance equals path sums; annualized volatility is not forced monotone. | `tests/application/test_dist.py::test_ac_dist_05` |
| AC-DIST-06 | VT07 | PASSED | Marginal-only adapters cannot serve duration, joint-tail, or simultaneous multi-market queries. | `tests/application/test_dist.py::test_ac_dist_06` |
| AC-DIST-07 | VT07 | PASSED | A joint mixture preserves world/expert identity and shared dependence across its full path. | `tests/application/test_dist.py::test_ac_dist_07` |
| AC-DIST-08 | VT04 | PASSED | Unsupported/infinite required moments block the relevant score or payoff consumer with a specific reason. | `tests/application/test_dist.py::test_ac_dist_08` |
| AC-DIST-09 | VT04 | PASSED | Point/mean return-variance baselines do not silently masquerade as full intraday realized-variance distributions. | `tests/application/test_dist.py::test_ac_dist_09` |
| AC-DIST-10 | VT07 | PASSED | Independent calibration heads cannot be combined into an unverified coherent joint probability. | `tests/application/test_dist.py::test_ac_dist_10` |
| AC-ARB-01 | VT14 | PASSED | Equal/global/rolling/feature/event-stage policies can be evaluated on the identical forecast pool. | `tests/application/test_arb.py::test_ac_arb_01` |
| AC-ARB-02 | VT16 | NOT_IMPLEMENTED | Post-inference features cannot be used to claim pre-inference cost savings. | `tests/application/test_arb.py::test_ac_arb_02` |
| AC-ARB-03 | VT14 | PASSED | Feature and gate parameters are fitted only on eligible earlier observations and out-of-fold forecasts. | `tests/application/test_arb.py::test_ac_arb_03` |
| AC-ARB-04 | VT14 | PASSED | Loss-to-weight, FFORMA-inspired surrogate, and direct-mixture objectives have explicit distinct identifiers. | `tests/application/test_arb.py::test_ac_arb_04` |
| AC-ARB-05 | VT15 | PASSED | An unconditional expert is not multiplied by scenario probabilities twice. | `tests/application/test_arb.py::test_ac_arb_05` |
| AC-ARB-06 | VT15 | PASSED | An unsupported expert cannot be represented as a conditional-world forecaster. | `tests/application/test_arb.py::test_ac_arb_06` |
| AC-ARB-07 | VT06 | PASSED | An expert failure is credited to its named fallback, not the failed model. | `tests/application/test_arb.py::test_ac_arb_07` |
| AC-ARB-08 | VT09 | PASSED | A scenario change invalidates affected cache entries even when price history is unchanged. | `tests/application/test_arb.py::test_ac_arb_08` |
| AC-ARB-09 | VT05 | PASSED | Consensus or simulated ensemble medians cannot enter real performance updates. | `tests/application/test_arb.py::test_ac_arb_09` |
| AC-ARB-10 | VT15 | PASSED | Rare-context shrinkage and bounded weight updates are verified against their declared policy. | `tests/application/test_arb.py::test_ac_arb_10` |
| AC-EVT-01 | VT10 | PASSED | Event outcome rules are frozen independently of the observed market response. | `tests/application/test_evt.py::test_ac_evt_01` |
| AC-EVT-02 | VT10 | PASSED | Storage/macro first-release timing, original weather runs, and publication-lagged data obey their vintages. | `tests/application/test_evt.py::test_ac_evt_02` |
| AC-EVT-03 | VT11 | PASSED | A forecast future covariate is marginalized through scenarios rather than treated as a certain observation. | `tests/application/test_evt.py::test_ac_evt_03` |
| AC-EVT-04 | VT10 | PASSED | Own-model error is not relabeled market surprise without an eligible expectation source. | `tests/application/test_evt.py::test_ac_evt_04` |
| AC-EVT-05 | VT10 | PASSED | Event occurrence, information receipt, and market response can have different clocks. | `tests/application/test_evt.py::test_ac_evt_05` |
| AC-EVT-06 | VT10 | PASSED | Non-occurrence, cancellation, and uncertainty resolution remain possible outcomes. | `tests/application/test_evt.py::test_ac_evt_06` |
| AC-EVT-07 | VT11 | PASSED | An ESS graph and a plain numerical comparator receive matched eligible evidence. | `tests/application/test_evt.py::test_ac_evt_07` |
| AC-EVT-08 | VT12 | PASSED | Unobserved downstream response is distinguished from delayed or missing reporting. | `tests/application/test_evt.py::test_ac_evt_08` |
| AC-SEL-01 | VT02 | PASSED | A zero external-call budget produces no paid API call or implicit paid fallback. | `tests/application/test_sel.py::test_ac_sel_01` |
| AC-SEL-02 | VT02 | PASSED | Concurrent reservations, retries, cancellation, and failures cannot exceed the configured budget. | `tests/application/test_sel.py::test_ac_sel_02` |
| AC-SEL-03 | VT02 | PASSED | Capability and license ineligibility removes an expert before dispatch. | `tests/application/test_sel.py::test_ac_sel_03` |
| AC-SEL-04 | VT13 | PASSED | Selecting more monitors changes coverage, not the underlying event probabilities. | `tests/application/test_sel.py::test_ac_sel_04` |
| AC-SEL-05 | VT13 | PASSED | The coverage planner handles shared outcomes/common drivers and is compared with exact small-set enumeration. | `tests/application/test_sel.py::test_ac_sel_05` |
| AC-SEL-06 | VT02 | PASSED | Disabled networking, expired deadlines, and action limits produce explicit stop states. | `tests/application/test_sel.py::test_ac_sel_06` |
| AC-SEL-07 | VT17 | NOT_IMPLEMENTED | Acquisition scoring uses a same-time, same-future-target control rather than crediting elapsed time. | `tests/application/test_sel.py::test_ac_sel_07` |
| AC-SEL-08 | VT17 | NOT_IMPLEMENTED | Off-policy learning records supported action propensities and does not invent unobserved counterfactual rewards. | `tests/application/test_sel.py::test_ac_sel_08` |
| AC-LEARN-01 | VT05 | PASSED | Actual matured observations, simulated outcomes, critic scores, and assumptions are isolated in storage. | `tests/application/test_learn.py::test_ac_learn_01` |
| AC-LEARN-02 | VT18 | NOT_IMPLEMENTED | Every approved online update records its algorithm, training label IDs, and resulting state version. | `tests/application/test_learn.py::test_ac_learn_02` |
| AC-LEARN-03 | VT18 | NOT_IMPLEMENTED | Graph/model/prompt structural changes run in shadow until promotion approval. | `tests/application/test_learn.py::test_ac_learn_03` |
| AC-LEARN-04 | VT18 | NOT_IMPLEMENTED | A learner cannot change evaluation targets, splits, budgets, permissions, or entitlements. | `tests/application/test_learn.py::test_ac_learn_04` |
| AC-LEARN-05 | VT18 | NOT_IMPLEMENTED | Paired contribution credit is distinct from coalition success and model standalone accuracy. | `tests/application/test_learn.py::test_ac_learn_05` |
| AC-LEARN-06 | VT18 | NOT_IMPLEMENTED | Corrected outcomes produce a versioned correction/replay rather than silent history changes. | `tests/application/test_learn.py::test_ac_learn_06` |
| AC-LEARN-07 | VT18 | NOT_IMPLEMENTED | Rollback restores the declared model, gate, calibrator, graph, and online state. | `tests/application/test_learn.py::test_ac_learn_07` |
| AC-LEARN-08 | VT18 | NOT_IMPLEMENTED | An inconclusive or negative benchmark preserves the incumbent and cannot become a superiority badge. | `tests/application/test_learn.py::test_ac_learn_08` |
| AC-DATA-01 | VT02 | PASSED | Variance units, annualization, session coverage, estimator identity, and proxy labels remain consistent. | `tests/application/test_data.py::test_ac_data_01` |
| AC-DATA-02 | VT02 | PASSED | Missing intraday bars and stale observations are not interpreted as zero variance. | `tests/application/test_data.py::test_ac_data_02` |
| AC-DATA-03 | VT02 | PASSED | Splits and futures rolls do not create unmarked economic jumps. | `tests/application/test_data.py::test_ac_data_03` |
| AC-DATA-04 | VT02 | PASSED | Nonpositive commodity prices use an explicit valid target or unsupported status, not silent log clipping. | `tests/application/test_data.py::test_ac_data_04` |
| AC-DATA-05 | VT08 | PASSED | Paper replication and application-specific targets/horizons have separate task IDs. | `tests/application/test_data.py::test_ac_data_05` |
| AC-DATA-06 | VT02 | PASSED | Raw restricted datasets and model artifacts cannot be exported under the code license alone. | `tests/application/test_data.py::test_ac_data_06` |
| AC-DATA-07 | VT06 | PASSED | Pretraining overlap/unknown-cutoff limitations are retained in research reports and prospective gates. | `tests/application/test_data.py::test_ac_data_07` |
| AC-UI-01 | VT19 | NOT_IMPLEMENTED | Every numerical card exposes its target, conditioning, horizon, version, and synthetic/research/live status. | `tests/application/test_ui.py::test_ac_ui_01` |
| AC-UI-02 | VT19 | NOT_IMPLEMENTED | The graph editor changes validated numerical assumptions and creates a new branch, not merely a visual edge. | `tests/application/test_ui.py::test_ac_ui_02` |
| AC-UI-03 | VT19 | NOT_IMPLEMENTED | Empty, failed, unavailable, and unsupported states are visible without invented probabilities. | `tests/application/test_ui.py::test_ac_ui_03` |
| AC-UI-04 | VT19 | NOT_IMPLEMENTED | Coverage is labeled as research/monitoring coverage rather than profit probability. | `tests/application/test_ui.py::test_ac_ui_04` |
| AC-UI-05 | VT19 | NOT_IMPLEMENTED | Arbitration displays show actual run/failure/weight/cost lineage, not arbitrary model confidence. | `tests/application/test_ui.py::test_ac_ui_05` |
| AC-UI-06 | VT19 | NOT_IMPLEMENTED | All mandatory workflows can be reproduced through the CLI and inspected in the workbench. | `tests/application/test_ui.py::test_ac_ui_06` |
| AC-OPS-01 | VT05 | PASSED | Clean offline setup and a full synthetic vertical slice run without model downloads or external accounts. | `tests/application/test_ops.py::test_ac_ops_01` |
| AC-OPS-02 | VT06 | PASSED | Save/reload parity includes all fitted numerical and state artifacts, not configuration alone. | `tests/application/test_ops.py::test_ac_ops_02` |
| AC-OPS-03 | VT02 | PASSED | Idempotent replay/job recovery creates no duplicate evidence, forecasts, charges, or outcomes. | `tests/application/test_ops.py::test_ac_ops_03` |
| AC-OPS-04 | VT09 | PASSED | Graph text, retrieved documents, and serialized data cannot execute arbitrary code. | `tests/application/test_ops.py::test_ac_ops_04` |
| AC-OPS-05 | VT00 | PASSED | Credentials and private donor data are excluded from logs, artifacts, and the new repository. | `tests/application/test_ops.py::test_ac_ops_05` |
| AC-OPS-06 | VT02 | PASSED | Model/data licenses and capabilities are pinned and enforced independently. | `tests/application/test_ops.py::test_ac_ops_06` |
| AC-OPS-07 | VT06 | PASSED | CPU/reference and any accelerator paths have measured parity/resource tests with honest unsupported states. | `tests/application/test_ops.py::test_ac_ops_07` |
| AC-OPS-08 | VT23 | NOT_IMPLEMENTED | Release reports distinguish tests run, failed, blocked, synthetic-only, and not implemented. | `tests/application/test_ops.py::test_ac_ops_08` |
| AC-ECO-01 | VT22 | NOT_IMPLEMENTED | A high-variance path ending at the strike can lose the entire unhedged straddle premium. | `tests/application/test_eco.py::test_ac_eco_01` |
| AC-ECO-02 | VT22 | NOT_IMPLEMENTED | Payoff calculations use contract-specific multiplier, expiry, exercise/settlement, and eligible underlying prices. | `tests/application/test_eco.py::test_ac_eco_02` |
| AC-ECO-03 | VT22 | NOT_IMPLEMENTED | Entry/exit timing, bid/ask costs, financing where material, overlapping capital, and non-activations are retained. | `tests/application/test_eco.py::test_ac_eco_03` |
| AC-ECO-04 | VT22 | NOT_IMPLEMENTED | Missing quotes return NOT_ASSESSED; model valuations are never relabeled observed historical fills. | `tests/application/test_eco.py::test_ac_eco_04` |
| AC-ECO-05 | VT02 | PASSED | No brokerage credentials, execution endpoint, or autonomous trade action exists. | `tests/application/test_eco.py::test_ac_eco_05` |
| AC-CTRL-01 | VT00 | PASSED | The canonical goal is GOAL_UPD.md; all active entry points agree and archived specifications remain identifiable. | `tests/application/test_ctrl.py::test_ac_ctrl_01` |
| AC-CTRL-02 | VT02 | PASSED | Purpose, allowlist, timeout, reservation and completion controls exist before any external model/source call. | `tests/application/test_ctrl.py::test_ac_ctrl_02` |
| AC-CTRL-03 | VT05 | PASSED | A blocked external checkpoint cannot prevent a verified offline classical slice or be credited as tested. | `tests/application/test_ctrl.py::test_ac_ctrl_03` |
| AC-CTRL-04 | VT05 | PASSED | The first scored offline slice includes genuine baseline inference, sealed predictions, matured outcomes and proper scores. | `tests/application/test_ctrl.py::test_ac_ctrl_04` |
| AC-CTRL-05 | VT01 | PASSED | Numeric exponent overflow and nested nonfinite values fail safe serialization and contract validation. | `tests/application/test_ctrl.py::test_ac_ctrl_05` |
| AC-CTRL-06 | VT01 | PASSED | Student-t and every admitted family reject invalid scale, parameter sets, support and required moments. | `tests/application/test_ctrl.py::test_ac_ctrl_06` |
| AC-CTRL-07 | VT02 | PASSED | Nonexistent snapshot/model/calibrator references and missing or mismatched artifacts fail runtime integrity checks. | `tests/application/test_ctrl.py::test_ac_ctrl_07` |
| AC-CTRL-08 | VT02 | PASSED | Synthetic lineage propagates through mixed inputs and cannot be cleared by a forecast, branch or export. | `tests/application/test_ctrl.py::test_ac_ctrl_08` |
| AC-MON-01 | VT10 | PASSED | A monitor declares observation coverage, cadence, arrival/error/failure law and costs separately from event occurrence. | `tests/application/test_mon.py::test_ac_mon_01` |
| AC-MON-02 | VT13 | PASSED | Coverage credits only eligible usable alerts satisfying the frozen lead-time rule; late and failed alerts remain visible. | `tests/application/test_mon.py::test_ac_mon_02` |
| AC-MON-03 | VT13 | PASSED | Monitoring utility units, cost tradeoffs, candidate universe and constraints freeze before policy evaluation. | `tests/application/test_mon.py::test_ac_mon_03` |
| AC-MON-04 | VT13 | PASSED | Duplicate feeds may change detection resilience but cannot create independent precursor or outcome probability. | `tests/application/test_mon.py::test_ac_mon_04` |
| AC-MON-05 | VT10 | PASSED | Physical state, evidence/confirmation state and per-instrument propagation state are stored independently. | `tests/application/test_mon.py::test_ac_mon_05` |
| AC-MON-06 | VT12 | PASSED | Query episode deduplication and cross-origin evaluation clustering preserve each origin-specific target definition. | `tests/application/test_mon.py::test_ac_mon_06` |
| AC-SEL-09 | VT16 | NOT_IMPLEMENTED | An unrun expert has no realized counterfactual forecast score; missing forecasts never become zero loss. | `tests/application/test_sel.py::test_ac_sel_09` |
| AC-SEL-10 | VT16 | NOT_IMPLEMENTED | Full-pool audit forecasts and randomized selection propensities are recorded with their full compute/acquisition cost. | `tests/application/test_sel.py::test_ac_sel_10` |
| AC-CASC-13 | VT12 | PASSED | Failure in a conditional branch cannot silently discard its probability mass or renormalize background risk away. | `tests/application/test_casc.py::test_ac_casc_13` |
| AC-ARB-11 | VT15 | PASSED | Event/world probabilities remain independently resolvable and scored; expert weights cannot masquerade as event calibration. | `tests/application/test_arb.py::test_ac_arb_11` |
| AC-OPS-09 | VT00 | PASSED | Scaffold/package checks and application acceptance execution have separate counts and no unimplemented capability receives a pass. | `tests/application/test_ops.py::test_ac_ops_09` |
| AC-EVT-09 | VT10 | PASSED | The real event study verifies intersecting contract/target/weather-run/member/availability coverage before confirmatory evaluation. | `tests/application/test_evt.py::test_ac_evt_09` |
