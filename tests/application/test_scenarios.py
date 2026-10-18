from __future__ import annotations
import unittest
class ScenarioTests(unittest.TestCase):
 def test_assumptions_conflicts_and_cache_versions(self):
  from volterra.scenarios import Scenario, ScenarioError
  s=Scenario(observations={"x":"CONFLICTING"},assumptions={"policy":"high"})
  self.assertEqual(s.probability("x"),None)
  self.assertNotEqual(s.cache_key(),s.with_assumption("policy","low").cache_key())
  with self.assertRaises(ScenarioError): s.execute_graph_text("import os")
