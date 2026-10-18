from __future__ import annotations
import unittest

class CheckpointGateTests(unittest.TestCase):
    def test_ac_arb_07_unavailable_checkpoint_credits_named_fallback(self) -> None:
        from volterra.models import CheckpointGate
        result=CheckpointGate("timestral_209m",available=False,fallback_id="ewma_variance").run()
        self.assertEqual(result.status,"BLOCKED")
        self.assertEqual(result.credited_model_id,"ewma_variance")
        self.assertEqual(result.failure_model_id,"timestral_209m")

    def test_ac_ops_07_unsupported_accelerator_is_honest(self) -> None:
        from volterra.models import ExecutionCapability
        cpu=ExecutionCapability.reference_cpu("ewma_variance",milliseconds=1.5)
        unsupported=ExecutionCapability.unsupported("timestral_209m",path="accelerator",reason="NOT_INSTALLED")
        self.assertEqual(cpu.status,"MEASURED")
        self.assertEqual(unsupported.status,"UNSUPPORTED")
        self.assertEqual(unsupported.reason,"NOT_INSTALLED")

