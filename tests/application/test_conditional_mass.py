from __future__ import annotations
import unittest
class ConditionalMassTests(unittest.TestCase):
 def test_failed_branch_retains_probability_mass(self):
  from volterra.cascades import retain_failed_branch_mass
  result=retain_failed_branch_mass(.3,background=.7)
  self.assertEqual(result["failed_branch"],.3)
  self.assertEqual(sum(result.values()),1.0)
