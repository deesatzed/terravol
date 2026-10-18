from __future__ import annotations
from dataclasses import dataclass
import math
class MarginalOnlyError(ValueError): pass
class IndependentHeadError(ValueError): pass
@dataclass(frozen=True)
class VariancePath:
 increments: tuple[float,...]
 def __post_init__(self):
  if not self.increments or any(not math.isfinite(x) or x<0 for x in self.increments): raise ValueError("variance increments must be finite and nonnegative")
 @property
 def cumulative_variance(self): return sum(self.increments)
 def annualized_volatility(self,horizon,annualization=252):
  if not 1<=horizon<=len(self.increments): raise ValueError("invalid horizon")
  return math.sqrt(annualization*sum(self.increments[:horizon])/horizon)
class MarginalPathAdapter:
 def joint_tail(self): raise MarginalOnlyError("marginal-only adapter cannot answer joint-tail query")
@dataclass(frozen=True)
class JointPathMixture:
 worlds: tuple[tuple[float,tuple[float,...]],...]
 def __post_init__(self):
  if not self.worlds or abs(sum(p for p,_ in self.worlds)-1)>1e-12: raise ValueError("world masses must sum to one")
 def support(self): return {path for _,path in self.worlds}
def independent_heads_joint_probability(*_: float) -> float:
 raise IndependentHeadError("independently calibrated heads do not establish a coherent joint probability")
