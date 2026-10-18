from __future__ import annotations
from datetime import datetime,timezone
import unittest
class VintageTests(unittest.TestCase):
 def test_vintage_is_unavailable_before_publication(self):
  from volterra.events import Vintage
  t=lambda d:datetime(2026,1,d,tzinfo=timezone.utc)
  vintage=Vintage(t(1),t(3))
  self.assertFalse(vintage.available_at(t(2)))
  self.assertTrue(vintage.available_at(t(3)))
