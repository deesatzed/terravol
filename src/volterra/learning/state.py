from __future__ import annotations
from dataclasses import dataclass
class LearningError(ValueError):pass
@dataclass(frozen=True)
class UpdateRecord: algorithm:str; label_ids:tuple[str,...]; state_version:str
@dataclass(frozen=True)
class StructuralProposal: candidate_id:str; lane:str
@dataclass(frozen=True)
class Correction: outcome_id:str; state_version:str
class LearningState:
 def __init__(self,incumbent:str):
  if not incumbent:raise LearningError('incumbent required')
  self.incumbent=incumbent;self._updates=0;self._corrections=0
 def update(self,algorithm,label_ids):
  if not algorithm or not label_ids or not all(isinstance(x,str) and x for x in label_ids):raise LearningError('approved update requires algorithm and matured label ids')
  self._updates+=1;version=f'v{self._updates+1}';self.incumbent=version;return UpdateRecord(algorithm,tuple(label_ids),version)
 def propose_structural(self,candidate_id):
  if not candidate_id:raise LearningError('candidate required')
  return StructuralProposal(candidate_id,'SHADOW')
 def change_control(self,*_):raise LearningError('learners cannot change evaluation controls, budgets, permissions, or entitlements')
 def correct(self,outcome_id):
  if not outcome_id:raise LearningError('outcome required')
  self._corrections+=1;return Correction(outcome_id,f'{self.incumbent}-correction-{self._corrections}')
 def rollback(self,declared_version):
  if not declared_version:raise LearningError('rollback version required')
  self.incumbent=declared_version;return declared_version
 def resolve_benchmark(self,status):
  if status not in {'INCONCLUSIVE','NEGATIVE','SUPERIOR'}:raise LearningError('unknown benchmark status')
  return self.incumbent
