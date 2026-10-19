from __future__ import annotations
class ExperimentError(ValueError):pass
class ExperimentManifest:
 def __init__(self,experiment_id,holdout_ids):
  if not experiment_id or not holdout_ids or len(set(holdout_ids))!=len(holdout_ids):raise ExperimentError('experiment requires unique holdouts')
  self.experiment_id=experiment_id;self.holdout_ids=set(holdout_ids);self.consumed={}
 def consume_holdout(self,holdout_id,purpose):
  if holdout_id not in self.holdout_ids or purpose not in {'exploratory','confirmation'}:raise ExperimentError('invalid holdout use')
  if holdout_id in self.consumed:raise ExperimentError('examined holdout cannot support a fresh confirmation claim')
  self.consumed[holdout_id]=purpose
