# Source ownership and current implementation

Only package metadata, `__main__.py` and `scaffold.py` implement behavior in this scaffold. Their purpose is project/control inspection. No forecasting adapter, inference engine or data store is implied by this directory.

Create application modules as their tickets become eligible, using [architecture ownership](../../docs/ARCHITECTURE.md) and [the active queue](../../TASK_QUEUE.md). Do not create empty adapters that return fabricated forecasts or create a package per future component merely to claim completeness. Keep numerical libraries out of control contracts and isolate incompatible ML workers when necessary.
