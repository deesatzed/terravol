"""VT02 observation-state and synthetic-lineage acceptance tests."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest


UTC = timezone.utc


class DataContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
