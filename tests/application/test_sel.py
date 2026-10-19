"""VT02 deterministic dispatch-policy acceptance tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest


UTC = timezone.utc


class DispatchPolicyTests(unittest.TestCase):
    def test_ac_sel_01_zero_budget_denies_paid_request_without_fallback(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        policy = DispatchPolicy(
            allow_network=True, allowed_domains=("api.example.test",), allowed_purposes=("forecast",),
            max_external_usd=0.0, action_limit=1,
        )
        decision = ReservationLedger(policy).reserve(DispatchRequest(
            request_id="paid", domain="api.example.test", purpose="forecast", worst_case_usd=0.01,
            deadline_at=datetime.now(UTC) + timedelta(minutes=1), capability_verified=True, license_verified=True,
        ), now=datetime.now(UTC))
        self.assertEqual(decision.status, "DENIED")
        self.assertEqual(decision.reason, "BUDGET_ZERO")

    def test_ac_sel_02_concurrent_reservations_cannot_exceed_budget_and_cancel_releases(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        now = datetime(2026, 1, 1, tzinfo=UTC)
        policy = DispatchPolicy(True, ("api.example.test",), ("forecast",), 1.0, 2)
        ledger = ReservationLedger(policy)
        request = lambda identifier: DispatchRequest(identifier, "api.example.test", "forecast", 0.6,
                                                       now + timedelta(minutes=1), True, True)
        first = ledger.reserve(request("one"), now=now)
        second = ledger.reserve(request("two"), now=now)
        self.assertEqual(first.status, "RESERVED")
        self.assertEqual(second.reason, "BUDGET_EXCEEDED")
        ledger.cancel("one")
        self.assertEqual(ledger.reserve(request("two"), now=now).status, "RESERVED")

    def test_failed_reservation_releases_budget_without_reclassifying_it_as_success(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        now = datetime(2026, 1, 1, tzinfo=UTC)
        ledger = ReservationLedger(DispatchPolicy(True, ("api.example.test",), ("forecast",), 0.5, 1))
        request = lambda identifier: DispatchRequest(identifier, "api.example.test", "forecast", 0.5,
                                                       now + timedelta(minutes=1), True, True)
        self.assertEqual(ledger.reserve(request("failed"), now=now).status, "RESERVED")
        ledger.fail("failed")
        self.assertEqual(ledger.reserve(request("retry"), now=now).status, "RESERVED")

    def test_ac_sel_03_and_06_ineligible_or_expired_requests_have_explicit_denials(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        now = datetime(2026, 1, 1, tzinfo=UTC)
        policy = DispatchPolicy(False, (), (), 1.0, 1)
        ledger = ReservationLedger(policy)
        expired = ledger.reserve(DispatchRequest("expired", "api.example.test", "forecast", 0.1, now, True, True), now=now)
        ineligible = ledger.reserve(DispatchRequest("ineligible", "api.example.test", "forecast", 0.1,
                                                     now + timedelta(minutes=1), False, False), now=now)
        self.assertEqual(expired.reason, "DEADLINE_EXPIRED")
        self.assertEqual(ineligible.reason, "NETWORK_DISABLED")

    def test_brokerage_or_trade_purpose_is_never_dispatchable(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        now = datetime(2026, 1, 1, tzinfo=UTC)
        policy = DispatchPolicy(True, ("api.example.test",), ("brokerage",), 1.0, 1)
        decision = ReservationLedger(policy).reserve(DispatchRequest(
            "trade", "api.example.test", "brokerage", 0.1, now + timedelta(minutes=1), True, True
        ), now=now)
        self.assertEqual(decision.status, "DENIED")
        self.assertEqual(decision.reason, "FORBIDDEN_PURPOSE")

    def test_completed_reservation_retains_actual_cost_for_reconciliation(self) -> None:
        try:
            from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 dispatch policy is not implemented: {exc}")
        now = datetime(2026, 1, 1, tzinfo=UTC)
        ledger = ReservationLedger(DispatchPolicy(True, ("api.example.test",), ("forecast",), 1.0, 1))
        request = DispatchRequest("completed", "api.example.test", "forecast", 0.5,
                                  now + timedelta(minutes=1), True, True)
        self.assertEqual(ledger.reserve(request, now=now).status, "RESERVED")
        ledger.complete("completed", actual_usd=0.37)
        record = ledger.reservation_record("completed")
        self.assertEqual(record.status, "COMPLETED")
        self.assertEqual(record.worst_case_usd, 0.5)
        self.assertEqual(record.actual_usd, 0.37)

class CoverageSelectionTests(unittest.TestCase):
    def test_ac_sel_04_monitor_selection_changes_coverage_not_world_probability(self) -> None:
        from datetime import timedelta
        from volterra.coverage import CoveragePolicy, MonitorCandidate, Outcome, plan_coverage
        policy = CoveragePolicy("query", "g1", "qualified_episode", timedelta(minutes=30), 1.0, 0.0, 3.0, ("a", "b"))
        outcomes = (Outcome("episode", 0.6),)
        candidates = (
            MonitorCandidate("a", {"episode": 0.5}, 1.0, "feed-a"),
            MonitorCandidate("b", {"episode": 0.5}, 1.0, "feed-b"),
        )
        one = plan_coverage(policy, outcomes, candidates, ("a",))
        both = plan_coverage(policy, outcomes, candidates, ("a", "b"))
        self.assertEqual(one.outcome_probabilities, both.outcome_probabilities)
        self.assertGreater(both.expected_coverage, one.expected_coverage)

    def test_ac_sel_05_shared_outcomes_are_deduplicated_and_exact_small_set_matches(self) -> None:
        from datetime import timedelta
        from volterra.coverage import CoveragePolicy, MonitorCandidate, Outcome, exact_small_set_plan, plan_coverage
        policy = CoveragePolicy("query", "g1", "qualified_episode", timedelta(minutes=5), 1.0, 0.0, 2.0, ("a", "b"))
        outcomes = (Outcome("shared", 0.8),)
        candidates = (
            MonitorCandidate("a", {"shared": 0.5}, 0.1, "driver-a"),
            MonitorCandidate("b", {"shared": 0.5}, 0.1, "driver-b"),
        )
        direct = plan_coverage(policy, outcomes, candidates, ("a", "b"))
        exact = exact_small_set_plan(policy, outcomes, candidates)
        self.assertAlmostEqual(direct.expected_coverage, 0.6)
        self.assertEqual(exact.selected_monitor_ids, ("a", "b"))
        self.assertAlmostEqual(exact.expected_coverage, direct.expected_coverage)

class SelectionAuditTests(unittest.TestCase):
    def test_ac_sel_09_unrun_expert_has_no_counterfactual_loss(self) -> None:
        from datetime import datetime, timezone
        from volterra.selection import CheapFeature, select_experts
        now=datetime(2026,1,1,tzinfo=timezone.utc)
        decision=select_experts(("a","b"),("a",),(CheapFeature("lag",1.0,now,False),),now)
        self.assertIsNone(decision.realized_loss("b"))
        self.assertEqual(decision.excluded_reasons["b"],"NOT_SELECTED")

    def test_ac_sel_10_full_pool_audit_records_cost_and_propensity(self) -> None:
        from datetime import datetime, timezone
        from volterra.selection import CheapFeature, full_pool_audit
        now=datetime(2026,1,1,tzinfo=timezone.utc)
        audit=full_pool_audit(("a","b"),(CheapFeature("lag",1.0,now,False),),now,{"a":.2,"b":.3},selection_propensity=.5)
        self.assertEqual(audit.total_cost_usd,.5)
        self.assertEqual(audit.selection_propensity,.5)
