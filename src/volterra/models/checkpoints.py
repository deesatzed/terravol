from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckpointResult:
    status: str
    failure_model_id: str
    credited_model_id: str | None
    reason: str | None

@dataclass(frozen=True)
class ExecutionCapability:
    model_id: str
    path: str
    status: str
    milliseconds: float | None
    reason: str | None
    @classmethod
    def reference_cpu(cls, model_id: str, *, milliseconds: float) -> "ExecutionCapability":
        if milliseconds < 0: raise ValueError("milliseconds must be nonnegative")
        return cls(model_id,"cpu_reference","MEASURED",milliseconds,None)
    @classmethod
    def unsupported(cls, model_id: str, *, path: str, reason: str) -> "ExecutionCapability":
        return cls(model_id,path,"UNSUPPORTED",None,reason)

@dataclass(frozen=True)
class ResearchModelLimit:
    model_id: str
    pretraining_cutoff: str | None
    @property
    def prospective_gate(self) -> str:
        return "PRETRAINING_CUTOFF_UNKNOWN" if self.pretraining_cutoff is None else "OVERLAP_REVIEW_REQUIRED"
    def research_note(self) -> str:
        return f"{self.model_id}: pretraining cutoff is unknown; historical performance may overlap pretraining data."

@dataclass(frozen=True)
class CheckpointGate:
    model_id: str
    available: bool
    fallback_id: str | None = None
    def run(self) -> CheckpointResult:
        if self.available: return CheckpointResult("AVAILABLE",self.model_id,self.model_id,None)
        return CheckpointResult("BLOCKED",self.model_id,self.fallback_id,"EXACT_ARTIFACT_OR_LICENSE_NOT_VERIFIED")
