from __future__ import annotations
from dataclasses import dataclass,replace
import hashlib,json
class ScenarioError(ValueError):pass
def concurrent_mechanisms(values:tuple[float,...])->tuple[float,...]:
 if any(not 0<=value<=1 for value in values):raise ScenarioError("mechanism probabilities must be marginals")
 return values
@dataclass(frozen=True)
class Scenario:
 observations:dict[str,str]
 assumptions:dict[str,str]
 def probability(self,key:str):
  state=self.observations.get(key)
  if state in {"CONFLICTING","UNRELIABLE",None}:return None
  raise ScenarioError("observations require a separately calibrated probability")
 def with_assumption(self,key:str,value:str):
  values=dict(self.assumptions);values[key]=value;return replace(self,assumptions=values)
 def cache_key(self):return hashlib.sha256(json.dumps({"observations":self.observations,"assumptions":self.assumptions},sort_keys=True).encode()).hexdigest()
 def execute_graph_text(self,text:str):raise ScenarioError("graph text is data and cannot execute")
