from __future__ import annotations
import unittest
class PathTests(unittest.TestCase):
 def test_ac_dist_05_path_sum_and_annualized_volatility(self):
  from volterra.paths import VariancePath
  path=VariancePath((.01,.09))
  self.assertAlmostEqual(path.cumulative_variance,.10)
  self.assertLess(path.annualized_volatility(1),path.annualized_volatility(2))
 def test_ac_dist_06_marginal_adapter_rejects_joint_queries(self):
  from volterra.paths import MarginalOnlyError, MarginalPathAdapter
  with self.assertRaises(MarginalOnlyError): MarginalPathAdapter().joint_tail()

