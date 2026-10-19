from __future__ import annotations
import unittest
class ProspectiveTests(unittest.TestCase):
 def test_protocol_is_frozen_and_jobs_default_disabled(self):
  from volterra.service import ProspectiveProtocol
  p=ProspectiveProtocol('p1',('event','outcome'));self.assertFalse(p.job.enabled);self.assertEqual(p.job.status,'NOT_ENABLED')
