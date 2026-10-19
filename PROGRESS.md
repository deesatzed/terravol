# VOLTERRA progress

**Current authority:** [GOAL_UPD.md](GOAL_UPD.md) v2.1. **Current implementation status:** bounded local/synthetic components exist through VT15; the full application remains NOT_IMPLEMENTED. The machine control records 96/120 executed application acceptance requirements. VT16 is next.

## 2026-10-19 — VT15 conditional-world fusion

**Ticket:** conditional fusion now keeps world masses (`q`) distinct from expert weights (`w`), mixes each declared conditional expert once inside each world, and applies outer world mass once. Marginal experts must be explicitly invariant across all worlds; incomplete conditional maps are rejected. Rare-context updates use bounded shrinkage toward a declared baseline.

**Validation:** missing APIs first produced 3 focused import errors. The final suite passed 126 tests. Receipts: [application acceptance](reports/vt15/application-acceptance.json) and [ticket verification](reports/vt15/ticket-verification.json). AC-ARB-05, AC-ARB-06, AC-ARB-10, and AC-ARB-11 are satisfied.

**Limits / next work:** this is local distribution fusion only; it does not establish joint-path switching or an event forecast. VT16 is next.

**Current authority:** [GOAL_UPD.md](GOAL_UPD.md) v2.1. **Current implementation status:** bounded local/synthetic components exist through VT14; the full application remains NOT_IMPLEMENTED. The machine control records 92/120 executed application acceptance requirements. VT15 is next.

## 2026-10-18 — VT14 same-pool arbitration controls

**Ticket:** VT14 adds `volterra.arbitration`: immutable same-pool rows with matured out-of-fold labels, origin-available features, and discrete expert distributions. Equal, global regularized, rolling regularized, loss-to-weight, FFORMA-inspired, and direct-mixture gate identities are explicit. The lightweight feature gate fits an eligible-only loss regression rather than relabeling a global mixture.

**Safeguards:** every training row has the identical expert pool, a mature label no later than the fit as-of, and features available at its own origin; future feature availability and in-fold rows are rejected. The current path is post-inference arbitration only and contains no model selection/cost claim.

**Validation:** tests first failed because `volterra.arbitration` was absent (3 errors). The focused four tests and full command `PYTHONPATH=src .venv/bin/python -B -m unittest discover -s tests -p 'test_*.py' -q` then passed: 122 tests. Receipts: [application acceptance](reports/vt14/application-acceptance.json), [ticket verification](reports/vt14/ticket-verification.json). Acceptance IDs: AC-ARB-01, AC-ARB-03, AC-ARB-04.

**Limits / next work:** no event-stage or conditional-world fusion, promotion, external model, or performance-improvement claim exists. VT15 is next.

**Current authority:** [GOAL_UPD.md](GOAL_UPD.md) v2.1. **Current implementation status:** bounded local/synthetic components exist through VT13; the full application remains NOT_IMPLEMENTED. The machine control records 89/120 executed application acceptance requirements. VT14 is next.

## 2026-10-18 — VT13 coverage planning and conditional research watches

**Ticket:** VT13 completed locally with deterministic, offline coverage planning in `volterra.coverage`. `CoveragePolicy` freezes query, graph version, utility unit, minimum useful lead time, cost tradeoffs, budget and candidate universe. `MonitorCandidate` supplies conditional detection reliability only; it cannot change an `Outcome` world probability.

**Behavior and safeguards:** selected monitors are bounded by the frozen candidate set/budget. Coverage is deduplicated by canonical downstream outcome; multiple feeds improve conditional detection resilience under a declared conditional-independence calculation but never create independent precursor/outcome mass. `AlertReceipt` retains `USABLE`, `LATE`, `FAILED`, and ineligible states. `ConditionalResearchWatch` is a local data object whose external job flag is permanently false. Exact enumeration is limited to 16 candidates and serves only as the small-set correctness comparator.

**Tests and receipts:** tests were first run before implementation and failed with `ModuleNotFoundError: volterra.coverage` (7 errors in the focused group). After implementation, the focused 14 tests passed. Full validation: `PYTHONPATH=src .venv/bin/python -B -m unittest discover -s tests -p 'test_*.py' -v` — 118 passed. Receipt files: [application acceptance](reports/vt13/application-acceptance.json) and [ticket verification](reports/vt13/ticket-verification.json). Acceptance IDs: AC-SEL-04, AC-SEL-05, AC-MON-02, AC-MON-03, AC-MON-04.

**Limits / next work:** this is not a live monitor, job scheduler, data provider integration, calibrated event model, or proof of monitoring value. Detection independence is explicit and only conditional on an already declared outcome. VT14 (same-pool arbitration) is now dependency-eligible.

**Current authority:** [GOAL_UPD.md](GOAL_UPD.md) v2.1. The entries below retain earlier observations and scope as history. The consolidated scaffold is validated; the forecasting application remains NOT_IMPLEMENTED, with 41/120 application acceptance requirements executed. VT05 is the next application ticket for the first scored offline slice.

## 2026-10-18 — ANALYSIS-VOLTUPD

**Requested work:** read `voltupd.md`, examine this codebase, and develop a gap analysis. Analysis completed in [VOLTUPD_GAP_ANALYSIS.md](VOLTUPD_GAP_ANALYSIS.md); execution evidence is in [verification.json](reports/voltupd-gap-analysis/verification.json).

**Scope and assumptions:** audited this directory only. It is a specification package, and Git reported no repository. No neighboring application checkout was inferred. The update includes both event/transmission forecasting and cascade/coverage planning. Proposed resolutions preserve the existing T00–T03 first assignment and equity integrity gate before natural gas; broader scope changes remain proposals.

**Implemented application work:** none. No T00–T22 ticket is marked complete. Existing original specs, schemas, fixtures, validator, configuration, manifest and package-validation receipt were preserved.

**Checks executed:** original validator against temporary fixture/config/schema copies using Python 3.12.15 and jsonschema 4.25.1: 28/28 package-only checks passed; 0/78 planned application acceptance requirements executed. All 26 original manifest hashes matched and remained unchanged. Eight focused probes documented runtime gaps, a schema/prose mismatch, two validation defects and a functioning unit-conversion rejection control. Arithmetic references were recalculated directly; no cascade engine or fitted forecasting model was run.

**Failures and mitigation:** default Python 3.15 lacked jsonschema. uv runtime discovery initially could not access its cache under sandbox restrictions; an escalated read succeeded. Validation then used an isolated Python 3.12 environment with a pinned jsonschema version. The validator currently accepts a negative Student-t scale and JSON numeric exponent overflow to infinity; these defects are documented and remain unfixed.

**Interface changes:** none. Proposed contracts, modules, tickets and tests are recommendations in the analysis, not implemented APIs.

**Resource evidence:** interpreter/package versions and arm64 architecture recorded. No application memory/latency measurements, forecasting performance, provider payload tests or real-market evaluations performed. No paid provider calls or model downloads.

**Remaining work / next eligible ticket:** T00 closure, followed by T01–T03 in order. New VU/NG tickets and architecture decisions in the report require integration into the governing specification before broader implementation. Real historical data coverage, as-issued weather ensembles, contract observations, consensus rights and model compatibility remain unverified.

## 2026-10-18 — ANALYSIS-GOAL-V2

**Requested work:** assess `VOLTERRA GOAL v2.txt`, `GOALn.md`, this progress log and the gap analysis, then continue brainstorming. Read all four and recorded the cross-document assessment in [GOAL_V2_ASSESSMENT.md](GOAL_V2_ASSESSMENT.md). Added a historical-scope notice to the earlier gap analysis.

**Findings:** v2 adds explicit pre-selection/post-arbitration, matched expert-pool experiments, distinct weighting objectives, conditional-world fusion and time-matched acquisition controls. Remaining design issues include conflicting goal authority, the first scored slice versus milestone labels, late placement of minimal external-call controls, monitoring observation/latency semantics, event-state dimensions, selective-expert feedback, episode identity and real-data intersection.

**Checks executed:** parsed 100 unique acceptance IDs, 24 VT tickets and 10 workflows; listed dependencies have no undefined VT identifier or cycle. Direct finite-distribution arithmetic verified the proposed mixture CRPS identity and its difference from average individual expert scores. These are document/reference calculations, not application tests. Focused primary-source checks support selected v2 model/method statements; no model installed or benchmark reproduced.

**Current-state qualification:** read-only donor Git metadata identifies commit `3bd39789c3811a5b437baf60a65de480aa0486bf` and tracked working-tree deletions. Donor contents were not restored or modified, and no donor script, restricted dataset, environment contents or serialized model was loaded. Excluding the donor subtree, the VOLTERRA Python inventory remains the fixture validator.

**Brainstorm status:** three first-proof approaches proposed: event-to-volatility chain, arbitration laboratory, or cascade workbench. An optional preference question was presented; no response or design approval is inferred. The full v2 roster and eventual capabilities remain visible. Assessment documents only; no canonical goal replacement, application implementation or completed T/VT ticket.

## 2026-10-18 — SCAFFOLD-2.1

**Requested work:** create updated scaffolding and `GOAL_UPD.md` to consolidate the best version of the application. Delivered the canonical goal, active engineering/control documents, complete ticket/acceptance map, package boundary and executable scaffold inspection. The user request authorizes this consolidation; application forecasting is a subsequent implementation phase.

**Authority and assumptions:** `GOAL.md` now points to `GOAL_UPD.md`; the exact 26 original manifest entries and original manifest are preserved under `docs/archive/spec-v1/`. Candidate goals and narratives remain unchanged provenance. The event-to-volatility chain is the documented first research proof, retaining the full cascade/arbitration/monitoring program. The old T00–T03 cap becomes an integrity checkpoint; the first scored offline slice ends at VT05. VT02 owns early external-call enforcement. Foundation-checkpoint feasibility does not block the independent offline path. TTM, Chronos-2 and TimesFM 2.5 remain the committed challengers; none is installed or verified.

**Interfaces and implementation:** added the installable `volterra-research` package with only `volterra doctor --profile offline` and `volterra scaffold validate`. These read project controls, reject contradictory claims/defaults and report actual application status; they do not forecast, retrieve evidence, run monitoring or learn. Added 24 machine-readable tickets and 120 planned application requirements, retaining all 100 v2 acceptance IDs and adding 20 assessed-gap controls. Four optional economic requirements belong to VT22; the prohibition on brokerage execution is mandatory at VT02. Only VT00 is PARTIAL; no application ticket is complete.

**Verification:** 30 scaffold tests passed, including malformed inputs, finite-number overflow, dependency drift/cycles, false or mismatched execution receipts, optional-lane scheduling, disabled external defaults, archive integrity and read-only CLI behavior. Red-first tests exposed the defects before their fixes. Both installed CLI commands passed and reported 0/120 application acceptance executed. The archived v1 validator independently passed 28/28 package-only checks in temporary copies. Archive hashes, preserved input hashes and active local document links were checked. Exact commands, environment, outputs and scope are recorded in [verification.json](reports/scaffold/verification.json); the legacy result is [separate](reports/scaffold/legacy-package-validation.json).

**Review and failures:** a bounded read-only reviewer found receipt-binding, malformed-field, execution-count, dependency-completion, offline-policy and optional-lane issues. All were accepted and fixed with regressions; a second pass found malformed owner and ticket-receipt holes, also fixed. Final recheck confirmed 30 tests passing with no remaining material finding from that review. [Adjudication](docs/reviews/scaffold-review.md) records scope and limits. The original legacy validator's Student-t and exponent-overflow defects remain historical defects; VT01 must fix the application contracts. An early chained regression command stopped after the first expected failure; the second regression was run independently before its fix. The initial Git whitespace check reported preserved-source whitespace in `GOALn.md` and `voltupd.md`; these exact provenance files were retained, and the remaining staged files passed the scoped whitespace check.

**Reproducibility and boundaries:** tested Python 3.12.15; pinned and installed the development/build environment with `uv.lock`. No numerical/ML dependency intersection is claimed. Initialized isolated VOLTERRA version control with donor/environment/runtime exclusions. The donor was neither staged nor modified, and no donor script, private data, credentials or serialized model was loaded. Development dependency downloads do not grant application network permissions. No paid provider calls, model downloads, application resource benchmark, real-market evaluation or performance/profitability claim.

**Remaining work:** close VT00 with frozen synthetic targets and the source/data feasibility matrix; implement VT01 typed safe contracts and then VT02 ledger/as-of/maturity/policy, VT03 seeded worlds, VT04 baseline distributions and VT05 sealed forecasts/proper scoring. All 120 application acceptance rows remain NOT_IMPLEMENTED. Source rights, historical overlap, weather member archives, exact contract observations and model artifact/license feasibility require evidence before the relevant integrations. The full dependency-ordered path is in [TASK_QUEUE.md](TASK_QUEUE.md).

## 2026-10-18 — VT00–VT01 integrity foundation

**Implemented:** VT00 now freezes two explicit synthetic targets and an external feasibility matrix. Five data/model dependencies are `UNVERIFIED`; paid/live access is `BLOCKED` by the offline profile. VT01 adds `volterra.audit` and `volterra.contracts`: finite recursive serialization, distinct event/transmission/scenario/weight types, marginal-only quantile records, Student-t parameter and finite-variance guards, and a static capability-manifest primitive. No persistence, forecast, external call, data retrieval, model artifact, or numerical market result was added.

**Verification:** the VT00 application boundary suite passed 6 tests; the combined application suite passed 10; the complete test suite passed 40. The initial full discovery attempt found zero tests because directories lacked package markers; adding the markers exposed the scaffold fixture gap, which was fixed by copying the referenced reports and test paths into its temporary workspace. Final receipts are [VT00](reports/vt00/ticket-verification.json) and [VT01](reports/vt01/ticket-verification.json). The scaffold validator reports 7/120 application acceptance requirements executed and selects VT02 as next eligible work.

**Acceptance evidence:** VT00 executed AC-OPS-05, AC-CTRL-01 and AC-OPS-09. VT01 executed AC-PROB-01, AC-DIST-02, AC-CTRL-05 and AC-CTRL-06. Every other requirement remains `NOT_IMPLEMENTED`; a capability-manifest type is not proof of a real model/artifact integration.

**Next work:** VT02 adds durable as-of evidence/target/maturity stores, artifact integrity, idempotent jobs, and deterministic external-call policy/reservation controls. It remains offline and synthetic-only until specific data/model feasibility receives real evidence.

## 2026-10-18 — VT02 in progress: evidence snapshots

**Implemented so far:** a local SQLite `EvidenceLedger` accepts only finite, typed payload serialization; appends evidence revisions; requires same-logical-ID supersession; and seals immutable snapshot membership. A live snapshot requires receipt by origin, while certified historical replay uses recorded availability without treating today’s import time as past live receipt. The ledger performs no network or provider action.

**Verification:** four new time-integrity tests now cover later-revision invariance, historical/live policy divergence, revision selection at the correct origin, and 1/5/20-session outcome maturity after publication. VT02 is still `NOT_IMPLEMENTED`: artifact integrity, jobs and external-call reservation controls remain next.

**Additional VT02 progress:** content-addressed artifacts now verify SHA-256 and reject absent references. The deterministic local reservation ledger denies expired, disabled-network, unallowlisted, unlicensed, capability-unverified, zero-budget and over-budget requests before dispatch; it safely releases cancelled and failed reservations. Five focused policy/integrity tests and the full 49-test suite pass. Idempotent jobs, richer observation/data-status handling, lineage propagation, and receipt-backed VT02 completion remain pending.

**Latest VT02 progress:** idempotent local job claims now persist `RUNNING`/`COMPLETED` state and reject duplicate replay claims, preventing duplicate work from recovery/retry. The full suite now passes 50 tests. Richer observation/data-status handling, lineage propagation, and receipt-backed VT02 completion remain pending.

**Current VT02 policy increment:** the local-only dispatch ledger now retains a completed reservation's actual charge separately from its reserved maximum, and exposes that immutable completion record for reconciliation. Brokerage, trade, trading, order-placement, and account-control purposes are hard-denied even if callers put them in an allowlist. The full suite passes 54 tests. Completion records are policy evidence only: no provider, brokerage endpoint, credentials, downloads, or external action exists.

**Current VT02 measurement increment:** every persisted variance target now requires immutable measurement identity: units, annualization sessions, session calendar, coverage policy, estimator ID, and proxy label. Registering the same target ID with changed metadata fails, preventing a target name from silently retaining a different economic meaning. The full suite passes 55 tests. Split/roll adjustment policy, explicit nonpositive-price target support, and license-policy enforcement remain VT02 work.

**Current VT02 authorization increment:** policy may now require a pinned `Authorization` record containing capability and license identifiers plus their versions. A request lacking the exact approved record is denied before reservation. The full suite passes 56 tests. Existing boolean fields remain only for the already-local compatibility path; any policy configured with authorization records enforces the immutable records independently.

**Current VT02 adjustment increment:** measurement identity now also requires an explicit split/futures-roll adjustment policy. Adjustment policy participates in the immutable target definition hash, so adjusted and unadjusted series cannot silently share a target. The full suite passes 57 tests. Nonpositive-price handling and receipt-backed ticket completion remain pending.

**Current VT02 nonpositive-price increment:** target measurement identity now requires a declared nonpositive-price policy, such as `UNSUPPORTED` or an explicitly supported arithmetic-return definition. Silent log clipping is not representable. The full suite passes 58 tests.

## 2026-10-18 — VT02 complete: offline evidence and control foundation

**Implemented:** VT02 now provides a local append-only evidence ledger with sealed as-of snapshots, target maturity, content-addressed artifacts, idempotent jobs, monotone synthetic lineage, explicit measurement/adjustment/nonpositive-price policies, and artifact export classifications. Dispatch policy enforces network/domain/purpose/deadline/budget/action limits, pinned authorizations, actual-cost completion records, and a hard brokerage/trading prohibition. No provider client, data retrieval, credentials, model inference, forecast, or trade execution was added.

**Verification:** 60 tests passed; the 30-test application suite exercised the VT02 controls. [Application receipt](reports/vt02/application-acceptance.json) binds 19 VT02 requirement IDs to that run, and [ticket receipt](reports/vt02/ticket-verification.json) passed scaffold validation. The scaffold reports 26/120 application requirements executed and selects VT03 as next eligible work.

## 2026-10-18 — VT03 complete: exact cascade references

**Implemented:** VT03 supplies deterministic finite-state cascade references for independent, coincident, and exclusive branches; background/no-event mass; complete-set arithmetic; shared-downstream de-duplication; joint-probability bounds; and explicit logical queries. It rejects duplicate source identities and invalid exclusive branch tables. The work operates only on supplied finite probabilities and does not fit, retrieve, or validate a real-world causal graph.

**Verification:** 68 total tests passed at completion. The 38-test application suite produced [application evidence](reports/vt03/application-acceptance.json) for 11 requirements and a [VT03 ticket receipt](reports/vt03/ticket-verification.json); scaffold validation selected VT04 next.

## 2026-10-18 — VT04 complete: measurement-bound classical baselines

**Implemented so far:** Persistence, EWMA, configured Log-HAR, and configured GJR-GARCH produce explicit point-variance forecasts from supplied pre-origin synthetic histories. A residual Normal outcome distribution binds to the immutable target measurement identity, and named consumers reject Student-t distributions without the required finite moment. The classical primitives do not fit parameters, infer intraday realized-variance distributions, retrieve external data, or score forecasts.

**Verification:** the 46-test application suite passed; [application evidence](reports/vt04/application-acceptance.json) binds AC-TIME-02, AC-DIST-01, AC-DIST-08, and AC-DIST-09. The 76-test full suite and [ticket receipt](reports/vt04/ticket-verification.json) close VT04. Scaffold validation reports 41/120 requirements executed and selects VT05 for sealed forecasts, mature outcomes, and delayed proper scoring.

## 2026-10-18 — VT05 in progress: sealed forecast and mature-outcome score seam

**Implemented so far:** a local `ForecastStore` seals a Normal variance forecast using its snapshot, immutable target measurement identity, origin, model identity, distribution parameters, and synthetic lineage. It rejects duplicate seals and allows CRPS only once a same-target, same-origin outcome from the ledger has matured; scoring again cannot replace the original score. Ledger outcome retrieval now preserves its stored synthetic identity.

**Verification:** the new focused test covers early-score denial, matching mature-outcome scoring, immutable forecast identity, and a nonzero CRPS. The complete suite passes 77 tests. This is an in-progress seam, not the completed VT05 offline slice: mixture scoring, provenance isolation, a runnable synthetic pipeline, and the remaining acceptance evidence are still required.
