from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class MatchedEvidenceComparator:
 ess_evidence:tuple[str,...]
 numerical_evidence:tuple[str,...]
 def compare(self):
  if set(self.ess_evidence)!=set(self.numerical_evidence):raise ValueError("ESS and numerical control require matched eligible evidence")
  return "COMPARABLE"
