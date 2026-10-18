# VOLTERRA implementation queue

Canonical scope: [GOAL_UPD.md](GOAL_UPD.md). Machine source: [implementation_queue.json](config/implementation_queue.json). VT00–VT03 are closed within their bounded local/synthetic scopes; VT04 is in progress and remains the next ticket. Scaffold work remains separate from application implementation.

| Ticket | Dependencies | Status | Deliverable |
|---|---|---|---|
| VT00 | None | COMPLETE | Bounded local/synthetic current-state and source/data feasibility audit |
| VT01 | VT00 | COMPLETE | Typed finite contracts, safe serialization and capability-manifest primitives |
| VT02 | VT01 | COMPLETE | As-of evidence, targets, maturity and early deterministic call controls |
| VT03 | VT01, VT02 | COMPLETE | Seeded market/event worlds and exact cascade reference |
| VT04 | VT02, VT03 | IN_PROGRESS | Classical forecasts and measurement-compatible distributions |
| VT05 | VT04 | NOT_IMPLEMENTED | Sealed forecasts, delayed proper scoring and first offline slice |
| VT06 | VT02, VT05 | NOT_IMPLEMENTED | TTM, Chronos-2 and TimesFM 2.5 adapters |
| VT07 | VT05 | NOT_IMPLEMENTED | Joint paths and episode derivation |
| VT08 | VT05, VT07 | NOT_IMPLEMENTED | Numerical CLI replay and chronological benchmark |
| VT09 | VT01, VT03, VT05 | NOT_IMPLEMENTED | ESS rules, inference and immutable scenarios |
| VT10 | VT02, VT09 | NOT_IMPLEMENTED | External events, clocks, expectations and monitor observation contracts |
| VT11 | VT07, VT09, VT10 | NOT_IMPLEMENTED | Transmission specialist and same-information numerical control |
| VT12 | VT03, VT07, VT11 | NOT_IMPLEMENTED | Fitted dependency-aware cascades and joint-world queries |
| VT13 | VT10, VT12 | NOT_IMPLEMENTED | Coverage planning and conditional research watches |
| VT14 | VT05, VT08 | NOT_IMPLEMENTED | Same-pool global/rolling/feature arbitration |
| VT15 | VT10, VT11, VT12, VT14 | NOT_IMPLEMENTED | Event-stage gates and conditional-world fusion |
| VT16 | VT02, VT14, VT15 | NOT_IMPLEMENTED | Cheap pre-inference selector and charged reliability audits |
| VT17 | VT10, VT13, VT16 | NOT_IMPLEMENTED | Bounded investigation and time-matched revisions |
| VT18 | VT05, VT15, VT17 | NOT_IMPLEMENTED | Matured-outcome memory, shadow promotion and rollback |
| VT19 | VT08, VT09, VT12, VT13, VT15, VT18 | NOT_IMPLEMENTED | Computed local workbench for W01-W09 |
| VT20 | VT11, VT12, VT15, VT18 | NOT_IMPLEMENTED | Full ablation and negative-result research report |
| VT21 | VT20 | NOT_IMPLEMENTED | Prospective collection protocol and jobs |
| VT22 | VT07, VT08, VT12, VT20 | NOT_IMPLEMENTED | Optional contract-aware options research W10 |
| VT23 | VT19, VT20, VT21 | NOT_IMPLEMENTED | Evidence-backed engineering release |

First scored offline result: VT05. Early external-call guards: VT02. Offline VT08 does not depend on external checkpoint availability. VT22 is optional. Complete one ticket with real receipts before claiming it passed; continue independent work when a particular external integration is blocked.
