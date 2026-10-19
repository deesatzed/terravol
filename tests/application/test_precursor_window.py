from __future__ import annotations
import unittest
class PrecursorWindowTests(unittest.TestCase):
 def test_cancelled_precursor_does_not_propagate(self):
  from volterra.cascades import future_window_active
  self.assertFalse(future_window_active("CANCELLED"))
