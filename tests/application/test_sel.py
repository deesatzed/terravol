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
