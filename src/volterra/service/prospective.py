from __future__ import annotations
from dataclasses import dataclass
class ProspectiveError(ValueError):pass
@dataclass(frozen=True)
class JobState:
 enabled:bool=False
 @property
 def status(self):return 'NOT_ENABLED' if not self.enabled else 'ENABLED'
@dataclass(frozen=True)
class ProspectiveProtocol:
 protocol_id:str; observation_fields:tuple[str,...]; job:JobState=JobState()
 def __post_init__(self):
  if not self.protocol_id or not self.observation_fields or not all(isinstance(x,str) and x for x in self.observation_fields):raise ProspectiveError('protocol requires frozen observation fields')
