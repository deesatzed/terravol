from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckpointResult:
    status: str
    failure_model_id: str
    credited_model_id: str | None
    reason: str | None

@dataclass(frozen=True)
class CheckpointGate:
    model_id: str
    available: bool
    fallback_id: str | None = None
    def run(self) -> CheckpointResult:
        if self.available: return CheckpointResult("AVAILABLE",self.model_id,self.model_id,None)
        return CheckpointResult("BLOCKED",self.model_id,self.fallback_id,"EXACT_ARTIFACT_OR_LICENSE_NOT_VERIFIED")
