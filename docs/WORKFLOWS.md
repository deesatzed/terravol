# Workflow and command status

Application scope: [GOAL_UPD.md](../GOAL_UPD.md). The currently supplied commands are read-only scaffold controls:

```bash
PYTHONPATH=src python3.12 -B -m volterra doctor --profile offline
PYTHONPATH=src python3.12 -B -m volterra scaffold validate
```

With the locked development environment installed, use `uv run volterra doctor --profile offline` and `uv run volterra scaffold validate`. Both accept `--root PATH`; defaults use the current directory. Exit 0 means scaffold controls validate, **not** that the forecasting application is implemented. Invalid controls return exit 2. No external call or runtime data write occurs. Other commands are explicitly unavailable.

| Workflow | Planned result | Ticket range | Current application status |
|---|---|---|---|
| W01 | Instrument/horizon/as-of forecast, selection, actual outputs, pooling, seal and provenance | VT02–VT08, VT14–VT16 | NOT_IMPLEMENTED |
| W02 | Defined external event, expectations/worlds and conditional volatility versus controls | VT10–VT11 | NOT_IMPLEMENTED |
| W03 | Explicit joint cascade query with shared-driver/outcome identity | VT03, VT12 | NOT_IMPLEMENTED |
| W04 | Conditional watch and observation-aware precursor monitor selection | VT13 | NOT_IMPLEMENTED |
| W05 | New evidence/contradiction/non-propagation, new snapshot and forecast lineage | VT10–VT12 | NOT_IMPLEMENTED |
| W06 | Manual numerical graph branch with conditional/intervention distinction | VT09 | NOT_IMPLEMENTED |
| W07 | Same-pool global/rolling/feature/event arbitration comparison | VT14–VT15 | NOT_IMPLEMENTED |
| W08 | Permitted acquisition with reservation, stopping and time-matched scoring | VT17 | NOT_IMPLEMENTED |
| W09 | Matured updates, shadow challenger, evidence-backed promotion/rollback | VT18 | NOT_IMPLEMENTED |
| W10 | Optional actual-quote/contract-based economic research and no-edge states | VT22 | NOT_IMPLEMENTED |

Goal §23 names future CLI contracts. Do not document them as runnable before their implementation and success/failure tests exist. Preparing W04 cannot enable an external recurring job/cadence/budget; that is a separately recorded operator action.
