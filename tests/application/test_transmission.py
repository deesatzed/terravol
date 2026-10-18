from __future__ import annotations
import unittest
class TransmissionTests(unittest.TestCase):
 def test_ess_and_numerical_control_require_matched_evidence(self):
  from volterra.transmission import MatchedEvidenceComparator
  result=MatchedEvidenceComparator(("a","b"),("a","b")).compare()
  self.assertEqual(result,"COMPARABLE")
  with self.assertRaises(ValueError):MatchedEvidenceComparator(("a",),("b",)).compare()
 def test_future_covariate_is_scenario_weighted(self):
  from volterra.transmission import future_covariate_mean
  self.assertEqual(future_covariate_mean(((.5,0),(.5,2))),1)
