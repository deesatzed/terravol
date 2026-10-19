from __future__ import annotations
import unittest
class CoverageTests(unittest.TestCase):
 def test_confirmatory_evaluation_requires_full_intersection(self):
  from volterra.events import confirmatory_coverage
  self.assertFalse(confirmatory_coverage(contract=True,target=True,weather_run=True,member=False,availability=True))
  self.assertTrue(confirmatory_coverage(contract=True,target=True,weather_run=True,member=True,availability=True))

class CoveragePlannerTests(unittest.TestCase):
 def test_usable_alerts_require_frozen_lead_time_and_failed_alerts_remain_visible(self):
  from datetime import datetime, timedelta, timezone
  from volterra.coverage import AlertReceipt, CoveragePolicy
  now=datetime(2026,1,1,12,tzinfo=timezone.utc)
  policy=CoveragePolicy(query_id="q",graph_version="g1",utility_unit="qualified_episode",minimum_lead_time=timedelta(minutes=30),monetary_cost_weight=1,latency_cost_per_minute=0,budget_usd=4,candidate_universe=("m1",))
  eligible=AlertReceipt("m1","outcome",now,now+timedelta(minutes=45),True,True)
  late=AlertReceipt("m1","outcome",now,now+timedelta(minutes=10),True,True)
  failed=AlertReceipt("m1","outcome",now,now+timedelta(minutes=45),False,True)
  self.assertEqual(policy.alert_status(eligible),"USABLE")
  self.assertEqual(policy.alert_status(late),"LATE")
  self.assertEqual(policy.alert_status(failed),"FAILED")

 def test_watch_is_a_local_plan_and_never_enables_a_job(self):
  from volterra.coverage import ConditionalResearchWatch, CoveragePolicy
  from datetime import timedelta
  policy=CoveragePolicy("q","g1","qualified_episode",timedelta(minutes=1),1,0,4,("m1",))
  watch=ConditionalResearchWatch("watch",policy,("m1",),"event-1","forecast-1")
  self.assertFalse(watch.external_job_enabled)
