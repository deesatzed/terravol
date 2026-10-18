from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class MatchedEvidenceComparator:
 ess_evidence:tuple[str,...]
 numerical_evidence:tuple[str,...]
 def compare(self):
  if set(self.ess_evidence)!=set(self.numerical_evidence):raise ValueError("ESS and numerical control require matched eligible evidence")
  return "COMPARABLE"
def future_covariate_mean(scenarios:tuple[tuple[float,float],...]):
 if not scenarios or abs(sum(w for w,_ in scenarios)-1)>1e-12:raise ValueError("future covariate requires weighted scenarios")
 return sum(w*x for w,x in scenarios)
