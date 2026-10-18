from __future__ import annotations
import unittest


class ProvenanceTests(unittest.TestCase):
    def test_ac_learn_01_and_arb_09_real_performance_accepts_only_matured_observations(self) -> None:
        from volterra.learning import ProvenanceLedger, ProvenanceError
        ledger = ProvenanceLedger()
        ledger.record("actual-1", kind="MATURED_OBSERVATION", value=0.2)
        ledger.record("sim-1", kind="SIMULATED_OUTCOME", value=0.9)
        ledger.record("consensus-1", kind="CONSENSUS", value=0.7)
        self.assertEqual(ledger.real_performance_values(), (0.2,))
        with self.assertRaises(ProvenanceError): ledger.record_performance_update("sim-1")
        with self.assertRaises(ProvenanceError): ledger.record_performance_update("consensus-1")
        ledger.record_performance_update("actual-1")

