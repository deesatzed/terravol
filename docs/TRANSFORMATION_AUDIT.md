# Transformation audit — scaffold baseline

**Date:** October 18, 2026. **Scope:** VOLTERRA package and read-only donor metadata. **VT00 status:** COMPLETE for the bounded local audit; it freezes synthetic target declarations and identifies external feasibility as unverified/blocked. It does not establish real data/model availability or implement forecasting.

| Capability | Observed state | Evidence / remaining work |
|---|---|---|
| Canonical design/control scaffold | Prepared; verification receipt recorded after checks | GOAL_UPD, standards/decisions/queue, machine controls and acceptance traceability |
| VT00 local boundary/feasibility audit | Complete within declared offline/synthetic scope | `config/synthetic_targets.json`, `config/feasibility_matrix.json`, `reports/vt00/` |
| Executable scaffold inspection | Implemented in this increment; test result belongs to scaffold receipt | `src/volterra/scaffold.py`, package entry point, `tests/scaffold/` |
| Original fixture validator | Present; limited package-only behavior | Exact v1 archive; fresh 28/28 temporary-copy check in the separate scaffold legacy receipt is not application acceptance |
| Safe runtime distribution/numeric contracts | Implemented local VT01 primitives | Typed finite serialization, probability concepts, marginal quantiles and Student-t parameter/moment guards; broader runtime/persistence contracts remain VT02+ |
| Ledger/as-of/targets/maturity/dispatch | ABSENT runtime | VT02 |
| Seeded worlds/exact reference | ABSENT runtime | Hand-authored v1 records do not implement VT03 |
| Forecasting/scoring/replay/path models | ABSENT runtime | VT04–VT08 |
| Event/expectation/transmission/cascade/watch | ABSENT runtime | VT09–VT13 |
| Arbitration/selector/acquisition/learning | ABSENT runtime | VT14–VT18 |
| Computed workbench/research/forward/bridge | ABSENT runtime | VT19–VT23; quotes and future outcomes independently gated |
| Local donor checkout | Present, matching pin; dirty working tree | Prior read-only metadata found `3bd39789c3811a5b437baf60a65de480aa0486bf`; no restored files, script execution or private import |

## Preserved inputs

`docs/archive/spec-v1/` contains exact original files and manifest. The candidate `GOALn.md`, narrative `voltupd.md`, donor-oriented `aXcupd.md`, v2 summary and assessment reports remain provenance. Claims in those texts are not inherited performance or compatibility evidence.

The source root initially had no VOLTERRA Git repository; the donor is a distinct nested repository. This increment initialized isolated VOLTERRA version control with donor/private/runtime exclusions. No donor contents are included. Preserve these boundaries and unrelated work in later increments.

## External feasibility remains unresolved

The local audit freezes synthetic targets and records the project boundary. Real source selection, archived member/run availability, exact contract coverage, consensus rights, model artifact/license intersection and sample support remain `UNVERIFIED`; paid/live access is `BLOCKED` by the offline profile. Missing external feasibility is a capability state, not a reason to invent inputs or block independent offline work.

Execution evidence for this scaffold is [verification.json](../reports/scaffold/verification.json) once generated. The scaffold-only result must never populate the application acceptance matrix as 120 passing tests.
