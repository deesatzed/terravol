"""Application operational-boundary acceptance tests."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class OperationsAcceptanceTests(unittest.TestCase):
    def test_ac_ops_06_dispatch_requires_pinned_capability_and_license_authorization(self) -> None:
        try:
            from volterra.policy import Authorization, DispatchPolicy, DispatchRequest, ReservationLedger
        except ImportError as exc:
            self.fail(f"VT02 authorization registry is not implemented: {exc}")
        from datetime import datetime, timedelta, timezone
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        approved = Authorization("forecast-adapter", "1.2.0", "provider-terms", "2026-01")
        policy = DispatchPolicy(True, ("api.example.test",), ("forecast",), 1.0, 1, (approved,))
        denied = ReservationLedger(policy).reserve(DispatchRequest(
            "unapproved", "api.example.test", "forecast", 0.1, now + timedelta(minutes=1), authorization=None,
        ), now=now)
        allowed = ReservationLedger(policy).reserve(DispatchRequest(
            "approved", "api.example.test", "forecast", 0.1, now + timedelta(minutes=1),
            capability_verified=True, license_verified=True, authorization=approved,
        ), now=now)
        self.assertEqual(denied.reason, "AUTHORIZATION_UNVERIFIED")
        self.assertEqual(allowed.status, "RESERVED")

    def test_ac_ops_05_donor_and_sensitive_runtime_paths_are_excluded(self) -> None:
        ignored = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/aXc-ace-forecaster/", ignored)
        self.assertIn(".env", ignored)
        self.assertIn("*.pkl", ignored)
        self.assertIn("/data/", ignored)

    def test_ac_ops_09_application_matrix_never_counts_scaffold_results(self) -> None:
        matrix = json.loads((ROOT / "config/acceptance_matrix.json").read_text())
        self.assertEqual(matrix["scope"], "APPLICATION_REQUIREMENTS_NOT_SCAFFOLD_TEST_RESULTS")
        scaffold = json.loads((ROOT / "reports/scaffold/verification.json").read_text())
        self.assertEqual(scaffold["application_acceptance_executed"], 0)
        self.assertTrue(all("reports/scaffold/" not in reference
                            for row in matrix["requirements"]
                            for reference in row["evidence_refs"]))

    def test_ac_ops_03_idempotent_job_claim_prevents_duplicate_replay_work(self) -> None:
        try:
            from volterra.storage import EvidenceLedger
        except ImportError as exc:
            self.fail(f"VT02 job ledger is not implemented: {exc}")
        with tempfile.TemporaryDirectory(prefix="volterra-job-") as directory:
            ledger = EvidenceLedger(Path(directory) / "ledger.sqlite")
            self.addCleanup(ledger.close)
            self.assertTrue(ledger.claim_job("replay", "run-001"))
            self.assertFalse(ledger.claim_job("replay", "run-001"))
            ledger.complete_job("replay", "run-001")
            self.assertEqual(ledger.job_status("replay", "run-001"), "COMPLETED")


if __name__ == "__main__":
    unittest.main()
