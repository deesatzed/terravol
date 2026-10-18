from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class EvaluationTask:
 task_id:str
 horizon_sessions:int
 target_id:str
 def __post_init__(self):
  if not self.task_id or not self.target_id or self.horizon_sessions<=0: raise ValueError("task identity, target, and horizon required")
  if self.task_id.startswith("application-") and self.horizon_sessions not in {1,5,20}: raise ValueError("application horizons are fixed; paper replication needs a separate task id")
