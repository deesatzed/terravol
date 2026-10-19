from __future__ import annotations
import unittest
class ExperimentTests(unittest.TestCase):
 def test_ac_time_09_rejects_reused_holdout_confirmation(self):
  from volterra.evaluation import ExperimentManifest,ExperimentError
  m=ExperimentManifest('x',('h1',));m.consume_holdout('h1','exploratory')
  with self.assertRaises(ExperimentError):m.consume_holdout('h1','confirmation')
