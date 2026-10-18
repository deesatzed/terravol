# VOLTERRA implementation workflow

Read [GOAL_UPD.md](GOAL_UPD.md), [STANDARDS.md](STANDARDS.md), [DECISIONS.md](DECISIONS.md), [PROGRESS.md](PROGRESS.md) and [TASK_QUEUE.md](TASK_QUEUE.md). The machine sources are `config/implementation_queue.json` and `config/acceptance_matrix.json`.

## Working method

1. Reconcile the current workspace/dirty state, active entry points, exact environment and previously executed receipts. Do not assume this scaffold is a functioning forecaster.
2. Select the first unmet dependency. Use one implementing agent by default; a bounded reviewer/worker may be used only under the session's delegation authorization. Never delegate secrets or broad donor rewrites.
3. Write the increment's concrete contract, owned files, meaningful failing test, expected failure, implementation steps, verification commands and exit evidence. Keep scope small enough to inspect.
4. Implement the minimal real behavior, run the focused checks, then required integration/adversarial/replay checks. Inspect an actual success and failure path.
5. Review correctness, leakage, probability semantics, permissions and resource accounting. Record accepted/rejected second-opinion findings if delegation is used.
6. Update the machine queue and acceptance evidence, progress and affected docs. Continue eligible work after reporting a milestone; stop only for a real external/unsafe/scope blocker.

## Upfront reconnaissance still required at VT00

The scaffold audit is a starting record, not full closure. Confirm the new VOLTERRA repository boundary and dirty state, tested Python/dependency environment, package/schema/test inventory, synthetic target definitions and data feasibility. Record exact donor commit/state metadata without running donor scripts. Maintain source/license attribution for any later copied helper.

Record unresolved historical contract/weather/consensus coverage as specific feasibility gaps. No paid-data purchase or model download is implied by a model roster. Unavailable external integrations cannot stop independent offline work.

## Build phases

| Gate | Work | Exit |
|---|---|---|
| M0 | VT00–VT03 | Typed contracts, immutable as-of/target/maturity/policy stores, seeded worlds and exact finite-state reference |
| M1a | VT04–VT05 | First genuine scored offline forecasting/cascade slice, repeatable from one manifest |
| M1b | VT07–VT08 | Coherent numerical/path lab and replay CLI; offline path independent of checkpoint availability |
| Checkpoints | VT06 | Actual TTM/Chronos-2/TimesFM 2.5 integrations with exact artifacts, terms and resource/reload receipts |
| M2 | VT09–VT11 | Numerical ESS, exact gas-contract/weather feasibility, event beliefs/clocks/expectations/monitor observations, transmission versus numerical control |
| M3 | VT12–VT13 | Fitted dependent cascades, query deduplication, observation-aware coverage and conditional research watches |
| M4 | VT14–VT16 | Same-pool arbitration, conditional-world fusion, cheap selection and costed reliability audits |
| M5 | VT17–VT18 | Bounded acquisition, time-matched revisions, matured adaptation and promotion/rollback |
| M6 | VT19–VT20 | Real computed workbench and preregistered ablation reports |
| M7 | VT21; optional VT22 | Prospective collection and separately gated quote/contract-based economic research |
| M8 | VT23 | Evidence-backed engineering release; research/forward/economic claims remain separately gated |

VT02 owns the first external-call guard; VT16 does not defer it. Design benchmark targets/splits and logging before fitting, even though the consolidated report is VT20. VT14 can first use a fixed classical pool; checkpoint expansion is a separate experiment. Preserve all mandatory integrations and report their blocked state honestly.

## Atomic task template

```text
Ticket/subtask:
User-visible or numerical behavior:
Dependencies and observed evidence:
Owned files / interfaces / migrations:
Assumptions and permission envelope:
Failing success/failure regression and expected reason:
Minimal implementation:
Commands executed / actual results / artifact paths:
Resources, unsupported states and remaining work:
Acceptance IDs satisfied by real evidence:
```

## First application increment after this scaffold

Close VT00, then VT01 safe parsing/typed contracts. Start with regressions for numeric `1e999` overflow and invalid Student-t scale/parameter/support combinations. Preserve the old validator under v1 as historical evidence; runtime v2 contracts must reject those cases. Do not port a model before the one-step target-leakage regression exists.

VT02 adds append-only SQLite evidence/revision reconstruction, an origin snapshot with fitted-transform cutoffs, target definitions/maturity, idempotent jobs and transactional external-call accounting. VT03 supplies known synthetic worlds and exact enumeration. VT04–VT05 produce distributions, seal predictions, advance the controlled replay clock, reveal matured outcomes and compute proper scores. A final command must demonstrate future-mutation invariance without network access or ML weights.

Detailed scaffold design and executed preparation plan: [design](docs/plans/2026-10-18-consolidated-scaffold-design.md), [plan](docs/plans/2026-10-18-updated-scaffold-implementation.md).

## Risks and decisions

Highest risks: leakage in cross-fitted upstream stages, incompatible measurement targets, insufficient independent events, unknown archive availability, model/weight/data rights, conditional-world inconsistency, selective-feedback bias and elapsed-time acquisition credit. The deterministic boundary, controls and removal ablations are required regardless of which model wins. Remaining open decisions are listed in [DECISIONS.md](DECISIONS.md); make safe assumptions and log them while progressing independently.
