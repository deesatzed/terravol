from __future__ import annotations
import unittest
class EventStateTests(unittest.TestCase):
 def test_physical_evidence_and_instrument_states_are_independent(self):
  from volterra.events import EventState
  state=EventState("storm","CONFIRMED",{"SPY":"PENDING","NG":"TRANSMITTED"})
  self.assertEqual(state.physical_state,"storm")
  self.assertEqual(state.instrument_states["SPY"],"PENDING")
