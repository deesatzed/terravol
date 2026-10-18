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
@dataclass(frozen=True)
class MonitorContract:
 coverage:str
 cadence_minutes:int
 cost_usd:float
 arrival_law:str
 failure_law:str
 def __post_init__(self):
  if not self.coverage or self.cadence_minutes<=0 or self.cost_usd<0 or not self.arrival_law or not self.failure_law:raise ValueError("monitor requires coverage cadence costs and observation laws")
@dataclass(frozen=True)
class EventUpdate:
 event_id:str
 source:str
 @property
 def can_confirm(self):return self.source=="OBSERVED_CONFIRMATION"
@dataclass(frozen=True)
class EventState:
 physical_state:str
 evidence_state:str
 instrument_states:dict[str,str]
@dataclass(frozen=True)
class Vintage:
 observation_at:datetime
 published_at:datetime
 def available_at(self,as_of:datetime):return as_of>=self.published_at
def confirmatory_coverage(**coverage:bool):return all(coverage.values())
def classify_surprise(*,own_model_error:float,expectation_source:str|None):
 return "OWN_MODEL_ERROR" if expectation_source is None else "MARKET_SURPRISE"
