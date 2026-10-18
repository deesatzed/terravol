from __future__ import annotations
from dataclasses import dataclass
import math

class ProvenanceError(ValueError): pass

@dataclass(frozen=True)
class Record:
    record_id: str
    kind: str
    value: float

class ProvenanceLedger:
    _allowed={"MATURED_OBSERVATION","SIMULATED_OUTCOME","ASSUMPTION","CRITIC_SCORE","CONSENSUS"}
    def __init__(self) -> None:
        self.records: dict[str,Record]={}
        self.performance_updates: list[str]=[]
    def record(self, record_id: str, *, kind: str, value: float) -> None:
        if not record_id or kind not in self._allowed or not math.isfinite(value): raise ProvenanceError("invalid provenance record")
        if record_id in self.records: raise ProvenanceError("record identity is immutable")
        self.records[record_id]=Record(record_id,kind,float(value))
    def real_performance_values(self) -> tuple[float,...]:
        return tuple(item.value for item in self.records.values() if item.kind=="MATURED_OBSERVATION")
    def record_performance_update(self, record_id: str) -> None:
        item=self.records.get(record_id)
        if item is None or item.kind!="MATURED_OBSERVATION": raise ProvenanceError("real performance updates require a matured observation")
        self.performance_updates.append(record_id)
