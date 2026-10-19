from __future__ import annotations
import unittest
class LearningStateTests(unittest.TestCase):
 def test_ac_learn_02_update_records_algorithm_labels_and_version(self):
  from volterra.learning import LearningState
  s=LearningState('v1');u=s.update('ewma',['mature-1']);self.assertEqual((u.algorithm,u.label_ids,u.state_version),('ewma',('mature-1',),'v2'))
 def test_ac_learn_03_and_04_structural_changes_stay_shadow_and_controls_immutable(self):
  from volterra.learning import LearningError,LearningState
  s=LearningState('v1');self.assertEqual(s.propose_structural('graph-v2').lane,'SHADOW')
  with self.assertRaises(LearningError):s.change_control('budget','more')
 def test_ac_learn_06_07_08_correction_rollback_and_inconclusive_retain_incumbent(self):
  from volterra.learning import LearningState
  s=LearningState('v1');c=s.correct('outcome-1');self.assertEqual(c.state_version,'v1-correction-1');self.assertEqual(s.resolve_benchmark('INCONCLUSIVE'),'v1');self.assertEqual(s.rollback('v0'),'v0')
