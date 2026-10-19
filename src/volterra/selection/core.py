"""Pre-inference expert selection records; no expert execution occurs here."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import math
from typing import Mapping, Sequence
class SelectionError(ValueError): pass
@dataclass(frozen=True)
class CheapFeature:
 name:str; value:float; available_at:datetime; post_inference:bool
@dataclass(frozen=True)
class SelectionDecision:
 eligible_experts:tuple[str,...]; selected_experts:tuple[str,...]; excluded_reasons:dict[str,str]; feature_names:tuple[str,...]
 def realized_loss(self,expert_id:str)->float|None:
  return None if expert_id not in self.selected_experts else None
@dataclass(frozen=True)
class FullPoolAudit:
 decision:SelectionDecision; cost_by_expert:dict[str,float]; total_cost_usd:float; selection_propensity:float
def _validate(eligible:Sequence[str],selected:Sequence[str],features:Sequence[CheapFeature],origin:datetime):
 if origin.tzinfo is None:raise SelectionError('origin must be timezone-aware')
 e=tuple(eligible);s=tuple(selected)
 if not e or len(set(e))!=len(e) or not all(isinstance(x,str) and x for x in e):raise SelectionError('eligible experts must be unique')
 if not set(s).issubset(e) or len(set(s))!=len(s):raise SelectionError('selected experts must be unique eligible experts')
 for f in features:
  if f.available_at.tzinfo is None or f.available_at>origin or f.post_inference:raise SelectionError('selection requires origin-available pre-inference features')
 return e,s
def select_experts(eligible,selected,features,origin):
 e,s=_validate(eligible,selected,features,origin)
 return SelectionDecision(e,s,{x:'NOT_SELECTED' for x in e if x not in s},tuple(f.name for f in features))
def full_pool_audit(eligible,features,origin,cost_by_expert:Mapping[str,float],*,selection_propensity:float):
 e,_,=_validate(eligible,eligible,features,origin);costs=dict(cost_by_expert)
 if set(costs)!=set(e) or any(not math.isfinite(v) or v<0 for v in costs.values()):raise SelectionError('audit costs must cover every expert')
 if not isinstance(selection_propensity,(int,float)) or not 0<selection_propensity<=1:raise SelectionError('propensity must be in (0,1]')
 decision=select_experts(e,e,features,origin)
 return FullPoolAudit(decision,costs,sum(costs.values()),float(selection_propensity))
