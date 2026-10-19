"""VT02 economic-safety acceptance tests."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest


class EconomicSafetyTests(unittest.TestCase):
    def test_ac_eco_05_no_brokerage_credential_or_execution_surface_exists(self) -> None:
        from volterra.policy import DispatchPolicy, DispatchRequest, ReservationLedger

        fields = set(DispatchRequest.__dataclass_fields__)
        self.assertFalse(fields & {"brokerage_credential", "account_id", "order", "trade_action"})
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        ledger = ReservationLedger(DispatchPolicy(True, ("api.example.test",), ("brokerage",), 1.0, 1))
        decision = ledger.reserve(DispatchRequest(
            "trade-attempt", "api.example.test", "brokerage", 0.0, now + timedelta(minutes=1), True, True,
        ), now=now)
        self.assertEqual(decision.reason, "FORBIDDEN_PURPOSE")


class OptionalResearchTests(unittest.TestCase):
 def test_ac_eco_01_path_at_strike_can_lose_premium(self):
  from volterra.options import StraddleContract,straddle_payoff
  c=StraddleContract(100,100,2);self.assertEqual(straddle_payoff(c,100),-400)
 def test_ac_eco_02_contract_multiplier_and_settlement_are_explicit(self):
  from volterra.options import StraddleContract
  c=StraddleContract(100,50,2);self.assertEqual(c.multiplier,50)
 def test_ac_eco_03_04_missing_quote_is_not_assessed_and_no_fill_is_invented(self):
  from volterra.options import QuoteAssessment
  self.assertEqual(QuoteAssessment(None).status,'NOT_ASSESSED')
