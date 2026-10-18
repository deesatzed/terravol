from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class EventClock:
 occurred_at:datetime
 received_at:datetime
 market_response_at:datetime
 outcome:str
 def __post_init__(self):
  if self.outcome not in {"OCCURRED","NON_OCCURRENCE","CANCELLED","UNCERTAIN"}:raise ValueError("invalid outcome")
  if any(x.tzinfo is None for x in (self.occurred_at,self.received_at,self.market_response_at)):raise ValueError("clocks timezone-aware")
  if self.received_at<self.occurred_at or self.market_response_at<self.received_at:raise ValueError("clocks must not reverse")
