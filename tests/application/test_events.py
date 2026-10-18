from __future__ import annotations
from datetime import datetime,timezone
import unittest
class EventTests(unittest.TestCase):
 def test_event_occurrence_receipt_and_response_clocks_are_distinct(self):
  from volterra.events import EventClock
  t=lambda h:datetime(2026,1,1,h,tzinfo=timezone.utc)
  clock=EventClock(t(1),t(2),t(3),outcome="CANCELLED")
  self.assertEqual(clock.outcome,"CANCELLED")
  self.assertLess(clock.occurred_at,clock.received_at)
  self.assertLess(clock.received_at,clock.market_response_at)
 def test_monitor_declares_observation_law_separately(self):
  from volterra.events import MonitorContract
  monitor=MonitorContract("weather",cadence_minutes=60,cost_usd=.1,arrival_law="LAGGED",failure_law="MISSING")
  self.assertEqual(monitor.coverage,"weather")
 def test_predicted_event_cannot_confirm_itself(self):
  from volterra.events import EventUpdate
  predicted=EventUpdate("A",source="PREDICTED")
  self.assertFalse(predicted.can_confirm)
