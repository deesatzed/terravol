from __future__ import annotations
from dataclasses import dataclass,replace
import hashlib,json,math
class WorkbenchError(ValueError):pass
@dataclass(frozen=True)
class NumericalCard:
 target:str; conditioning:str; horizon_sessions:int; version:str; data_mode:str; value:float|None; status:str='AVAILABLE'
 def __post_init__(self):
  if not all((self.target,self.conditioning,self.version)) or self.horizon_sessions<=0 or self.data_mode not in {'SYNTHETIC','RESEARCH','LIVE'} or self.status not in {'AVAILABLE','EMPTY','FAILED','UNAVAILABLE','UNSUPPORTED'}:raise WorkbenchError('invalid numerical card')
  if self.status=='AVAILABLE' and (self.value is None or not math.isfinite(self.value)):raise WorkbenchError('available card needs finite value')
  if self.status!='AVAILABLE' and self.value is not None:raise WorkbenchError('unavailable card cannot invent value')
@dataclass(frozen=True)
class ScenarioBranch:
 branch_id:str; assumptions:dict[str,object]
 def edit(self,key:str,value:object):
  if not key or isinstance(value,(dict,list,set)):raise WorkbenchError('branch edit must be scalar')
  a=dict(self.assumptions);a[key]=value;digest=hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()[:12];return ScenarioBranch(f'{self.branch_id}-{digest}',a)
@dataclass(frozen=True)
class CoverageView:
 coverage:float
 @property
 def label(self):return 'RESEARCH_MONITORING_COVERAGE'
@dataclass(frozen=True)
class ArbitrationView:
 actual_runs:tuple[str,...]; failures:tuple[str,...]; weights:dict[str,float]; total_cost_usd:float
