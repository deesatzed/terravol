from __future__ import annotations
import unittest
class ScenarioTests(unittest.TestCase):
 def test_assumptions_conflicts_and_cache_versions(self):
  from volterra.scenarios import Scenario, ScenarioError
  s=Scenario(observations={"x":"CONFLICTING"},assumptions={"policy":"high"})
  self.assertEqual(s.probability("x"),None)
  self.assertNotEqual(s.cache_key(),s.with_assumption("policy","low").cache_key())
  with self.assertRaises(ScenarioError): s.execute_graph_text("import os")
 def test_ac_prob_03_concurrent_mechanisms_are_not_normalized(self):
  from volterra.scenarios import concurrent_mechanisms
  self.assertEqual(concurrent_mechanisms((.7,.8)),(.7,.8))
