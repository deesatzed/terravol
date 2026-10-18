"""VT02 observation-state and synthetic-lineage acceptance tests."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest


UTC = timezone.utc


class DataContractTests(unittest.TestCase):
    def test_ac_data_01_variance_target_requires_measurement_identity(self) -> None:
        try:
            from volterra.storage import EvidenceLedger, LedgerError, MeasurementSpec, TargetDefinition
        except ImportError as exc:
            self.fail(f"VT02 measurement contracts are not implemented: {exc}")
        with self.assertRaises(LedgerError):
            MeasurementSpec("squared_decimal_return", 0, "XNYS", "FULL_SESSION", "close_to_close", "SPLIT_ADJUSTED", "NOT_APPLICABLE")
        measurement = MeasurementSpec(
            "squared_decimal_return", 252, "XNYS", "FULL_SESSION", "close_to_close", "SPLIT_ADJUSTED", "NOT_APPLICABLE",
        )
        target = TargetDefinition("rv-1", 1, "realized_variance_v1", measurement)
        with tempfile.TemporaryDirectory(prefix="volterra-measurement-") as directory:
            ledger = EvidenceLedger(Path(directory) / "ledger.sqlite")
            self.addCleanup(ledger.close)
            ledger.register_target(target)
            with self.assertRaises(LedgerError):
                ledger.register_target(TargetDefinition(
                    "rv-1", 1, "realized_variance_v1",
                    MeasurementSpec("squared_decimal_return", 365, "XNYS", "FULL_SESSION", "close_to_close", "SPLIT_ADJUSTED", "NOT_APPLICABLE"),
                ))

    def test_ac_data_02_missing_or_stale_is_not_zero_observation(self) -> None:
        try:
            from volterra.storage import EvidenceInput, EvidenceLedger, LedgerError
        except ImportError as exc:
            self.fail(f"VT02 observation controls are not implemented: {exc}")
        moment = datetime(2026, 1, 1, tzinfo=UTC)
        with tempfile.TemporaryDirectory(prefix="volterra-data-") as directory:
            ledger = EvidenceLedger(Path(directory) / "ledger.sqlite")
            self.addCleanup(ledger.close)
            with self.assertRaises(LedgerError):
                ledger.append_evidence(EvidenceInput("missing", "synthetic", 0.0, moment, moment, moment, moment,
                                                     "MISSING", True))
            with self.assertRaises(LedgerError):
                ledger.append_evidence(EvidenceInput("observed", "synthetic", None, moment, moment, moment, moment,
                                                     "OBSERVED", True))
            revision = ledger.append_evidence(EvidenceInput("stale", "synthetic", None, moment, moment, moment, moment,
                                                             "STALE", True))
            self.assertIsInstance(revision, str)

    def test_ac_data_03_target_requires_declared_split_or_roll_policy(self) -> None:
        try:
            from volterra.storage import LedgerError, MeasurementSpec
        except ImportError as exc:
            self.fail(f"VT02 adjustment contract is not implemented: {exc}")
        with self.assertRaises(LedgerError):
            MeasurementSpec("squared_decimal_return", 252, "XNYS", "FULL_SESSION", "close_to_close", "", "NOT_APPLICABLE")
        adjusted = MeasurementSpec(
            "squared_decimal_return", 252, "XNYS", "FULL_SESSION", "close_to_close", "SPLIT_ADJUSTED", "NOT_APPLICABLE",
        )
        rolled = MeasurementSpec(
            "squared_decimal_return", 252, "CME", "FULL_SESSION", "close_to_close", "BACK_ADJUSTED_ROLL", "NOT_APPLICABLE",
        )
        self.assertNotEqual(adjusted.canonical(), rolled.canonical())

    def test_ac_data_04_nonpositive_price_policy_is_explicit(self) -> None:
        try:
            from volterra.storage import LedgerError, MeasurementSpec
        except ImportError as exc:
            self.fail(f"VT02 nonpositive-price contract is not implemented: {exc}")
        with self.assertRaises(LedgerError):
            MeasurementSpec("log_return", 252, "CME", "FULL_SESSION", "settlement", "BACK_ADJUSTED_ROLL", "")
        unsupported = MeasurementSpec(
            "log_return", 252, "CME", "FULL_SESSION", "settlement", "BACK_ADJUSTED_ROLL", "UNSUPPORTED",
        )
        alternative = MeasurementSpec(
            "arithmetic_return", 252, "CME", "FULL_SESSION", "settlement", "BACK_ADJUSTED_ROLL", "ARITHMETIC_RETURN",
        )
        self.assertNotEqual(unsupported.canonical(), alternative.canonical())

    def test_synthetic_lineage_cannot_be_cleared_by_a_derived_record(self) -> None:
        try:
            from volterra.storage import EvidenceInput, EvidenceLedger
        except ImportError as exc:
            self.fail(f"VT02 lineage controls are not implemented: {exc}")
        moment = datetime(2026, 1, 1, tzinfo=UTC)
        with tempfile.TemporaryDirectory(prefix="volterra-lineage-") as directory:
            ledger = EvidenceLedger(Path(directory) / "ledger.sqlite")
            self.addCleanup(ledger.close)
            synthetic = ledger.append_evidence(EvidenceInput("synthetic", "fixture", 1.0, moment, moment, moment, moment,
                                                              "OBSERVED", True))
            observed = ledger.append_evidence(EvidenceInput("observed", "fixture", 2.0, moment, moment, moment, moment,
                                                             "OBSERVED", False))
            self.assertTrue(ledger.derive_synthetic_lineage((synthetic, observed), declared_synthetic=False))
            self.assertFalse(ledger.derive_synthetic_lineage((observed,), declared_synthetic=False))


if __name__ == "__main__":
    unittest.main()
