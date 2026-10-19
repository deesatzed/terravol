from __future__ import annotations
from datetime import datetime,timedelta,timezone
import unittest
class AcquisitionTests(unittest.TestCase):
 def test_ac_sel_07_requires_time_matched_same_target_control(self):
  from volterra.acquisition import RevisionContract,compare_acquisition,AcquisitionError
  t=datetime(2026,1,1,tzinfo=timezone.utc)
  c=RevisionContract('r','forecast','target',t+timedelta(days=5),t+timedelta(hours=1),.1,.01)
  self.assertAlmostEqual(compare_acquisition(c,reissued_at=t+timedelta(hours=1),control_target_id='target',control_reissued_at=t+timedelta(hours=1),acquired_score=.2,control_score=.3),.09)
  with self.assertRaises(AcquisitionError):compare_acquisition(c,reissued_at=t+timedelta(hours=1),control_target_id='other',control_reissued_at=t+timedelta(hours=1),acquired_score=.2,control_score=.3)
 def test_ac_sel_08_off_policy_requires_observed_reward_and_propensity(self):
  from volterra.acquisition import AcquisitionError,OffPolicyRecord
  t=datetime(2026,1,1,tzinfo=timezone.utc)
  self.assertEqual(OffPolicyRecord('a',.5,.2,t).reward,.2)
  with self.assertRaises(AcquisitionError):OffPolicyRecord('a',.5,None,t)
