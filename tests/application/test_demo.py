from __future__ import annotations
import unittest

class DemoTests(unittest.TestCase):
    def test_ac_ops_01_and_ctrl_03_offline_classical_slice_runs_without_checkpoint(self) -> None:
        from volterra.demo import run_offline_slice
        result=run_offline_slice()
        self.assertTrue(result["synthetic"])
        self.assertGreater(result["crps"],0.0)
        self.assertEqual(result["model_id"],"ewma_variance")
        self.assertEqual(result["external_calls"],0)

