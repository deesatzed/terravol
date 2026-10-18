from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class EpisodeState:
 started_at:int|None
 ended_at:int|None
 right_censored:bool
def derive_episode(values:tuple[float,...],*,upper:float,lower:float)->EpisodeState:
 start=None; end=None
 for i in range(1,len(values)):
  if start is None and values[i-1]>upper and values[i]>upper: start=i-1
  if start is not None and values[i-1]<lower and values[i]<lower: end=i-1; break
 return EpisodeState(start,end,start is not None and end is None)
