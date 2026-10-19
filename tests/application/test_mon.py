from __future__ import annotations
from datetime import datetime, timedelta, timezone
import unittest

class MonitoringAcceptanceTests(unittest.TestCase):
    def test_ac_mon_02_eligible_usable_alerts_only(self) -> None:
        from volterra.coverage import AlertReceipt, CoveragePolicy
        policy=CoveragePolicy("q","g1","episode",timedelta(minutes=20),1,0,1,("m",))
        alert=AlertReceipt("m","outcome",datetime(2026,1,1,tzinfo=timezone.utc),datetime(2026,1,1,0,10,tzinfo=timezone.utc),True,True)
        self.assertEqual(policy.alert_status(alert),"LATE")

    def test_ac_mon_03_policy_freezes_units_costs_candidates_and_constraints(self) -> None:
        from volterra.coverage import CoveragePolicy
        policy=CoveragePolicy("q","graph-v1","episodes",timedelta(minutes=20),2,0.1,3,("m1","m2"))
        self.assertEqual(policy.utility_unit,"episodes")
        self.assertEqual(policy.candidate_universe,("m1","m2"))

    def test_ac_mon_04_duplicate_feeds_add_resilience_not_event_mass(self) -> None:
        from volterra.coverage import CoveragePolicy, MonitorCandidate, Outcome, plan_coverage
        policy=CoveragePolicy("q","g1","episode",timedelta(minutes=1),1,0,2,("one","two"))
        result=plan_coverage(policy,(Outcome("e",0.4),),(MonitorCandidate("one",{"e":.5},1,"a"),MonitorCandidate("two",{"e":.5},1,"b")),("one","two"))
        self.assertEqual(result.outcome_probabilities,{"e":.4})
        self.assertAlmostEqual(result.expected_coverage,.3)
