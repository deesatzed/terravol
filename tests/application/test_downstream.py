from __future__ import annotations
import unittest
class DownstreamTests(unittest.TestCase):
 def test_unobserved_and_delayed_are_distinct(self):
  from volterra.cascades import downstream_status
  self.assertNotEqual(downstream_status(observed=False,report_due=False),downstream_status(observed=False,report_due=True))
