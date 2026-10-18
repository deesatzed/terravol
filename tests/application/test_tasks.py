from __future__ import annotations
import unittest
class TaskTests(unittest.TestCase):
 def test_ac_data_05_replication_and_application_targets_are_distinct(self):
  from volterra.evaluation import EvaluationTask
  app=EvaluationTask("application-v1",horizon_sessions=20,target_id="variance-20")
  paper=EvaluationTask("paper-foo-v1",horizon_sessions=22,target_id="paper-target")
  self.assertNotEqual(app.task_id,paper.task_id)
  with self.assertRaises(ValueError): EvaluationTask("application-v1",horizon_sessions=22,target_id="variance-20")
