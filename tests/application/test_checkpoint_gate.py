from __future__ import annotations
import unittest

class CheckpointGateTests(unittest.TestCase):
    def test_ac_arb_07_unavailable_checkpoint_credits_named_fallback(self) -> None:
        from volterra.models import CheckpointGate
        result=CheckpointGate("timestral_209m",available=False,fallback_id="ewma_variance").run()
        self.assertEqual(result.status,"BLOCKED")
        self.assertEqual(result.credited_model_id,"ewma_variance")
        self.assertEqual(result.failure_model_id,"timestral_209m")

