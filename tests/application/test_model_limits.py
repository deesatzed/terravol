from __future__ import annotations
import unittest
class ModelLimitsTests(unittest.TestCase):
 def test_ac_data_07_unknown_pretraining_cutoff_is_retained(self):
  from volterra.models import ResearchModelLimit
  limit=ResearchModelLimit("timestral_209m",pretraining_cutoff=None)
  self.assertEqual(limit.prospective_gate,"PRETRAINING_CUTOFF_UNKNOWN")
  self.assertIn("unknown",limit.research_note().lower())
