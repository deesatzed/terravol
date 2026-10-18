"""VT02 evidence-time and snapshot acceptance tests."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest


UTC = timezone.utc


def instant(day: int) -> datetime:
    return datetime(2026, 1, day, tzinfo=UTC)


class EvidenceTimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="volterra-ledger-")
        self.addCleanup(self.temp.cleanup)
        try:
            from volterra.storage import EvidenceInput, EvidenceLedger
        except ImportError as exc:
            self.fail(f"VT02 evidence ledger is not implemented: {exc}")
        self.EvidenceInput = EvidenceInput
        self.ledger = EvidenceLedger(Path(self.temp.name) / "ledger.sqlite")
        self.addCleanup(self.ledger.close)

    def append(self, logical_id: str, published_day: int, received_day: int, payload: object,
               *, supersedes: str | None = None) -> str:
        return self.ledger.append_evidence(self.EvidenceInput(
            logical_id=logical_id,
            source_id="synthetic-source",
            payload=payload,
            event_at=instant(published_day),
            published_at=instant(published_day),
            available_at=instant(published_day),
            received_at=instant(received_day),
            observation_state="OBSERVED",
            synthetic=True,
            supersedes_revision_id=supersedes,
        ))

    def test_ac_time_01_future_revision_cannot_change_sealed_snapshot(self) -> None:
        first = self.append("storage", 1, 1, {"value": 10})
        before = self.ledger.create_snapshot("before", instant(2), policy="live")
        self.append("storage", 3, 3, {"value": 11}, supersedes=first)
        after = self.ledger.create_snapshot("after", instant(4), policy="live")
        self.assertEqual(before.revision_ids, (first,))
        self.assertNotEqual(after.revision_ids, before.revision_ids)
        self.assertEqual(self.ledger.get_snapshot("before").revision_ids, (first,))

    def test_ac_time_03_certified_historical_policy_is_not_live_receipt_policy(self) -> None:
        imported = self.append("archive", 1, 5, {"value": 4})
        live = self.ledger.create_snapshot("live", instant(2), policy="live")
        replay = self.ledger.create_snapshot("replay", instant(2), policy="certified_historical")
        self.assertNotIn(imported, live.revision_ids)
        self.assertIn(imported, replay.revision_ids)

    def test_ac_time_04_revision_selection_changes_only_after_eligible_revision(self) -> None:
        first = self.append("weather", 1, 1, {"run": "first"})
        second = self.append("weather", 3, 3, {"run": "revision"}, supersedes=first)
        old = self.ledger.create_snapshot("old", instant(2), policy="live")
        new = self.ledger.create_snapshot("new", instant(3), policy="live")
        self.assertEqual(old.revision_ids, (first,))
        self.assertEqual(new.revision_ids, (second,))

    def test_ac_time_05_outcomes_mature_only_after_horizon_and_publication(self) -> None:
        try:
            from volterra.storage import TargetDefinition
        except ImportError as exc:
            self.fail(f"VT02 target maturity is not implemented: {exc}")
        targets = (
            TargetDefinition("one", 1, "synthetic_variance", "squared_decimal_return"),
            TargetDefinition("five", 5, "synthetic_variance", "squared_decimal_return"),
            TargetDefinition("twenty", 20, "synthetic_variance", "squared_decimal_return"),
        )
        for target in targets:
            self.ledger.register_target(target)
            outcome_id = self.ledger.record_outcome(
                target_id=target.target_id,
                origin_at=instant(1),
                completed_sessions=target.horizon_sessions,
                target_end_at=instant(1 + target.horizon_sessions),
                first_public_at=instant(2 + target.horizon_sessions),
                value=0.03,
                synthetic=True,
            )
            self.assertFalse(self.ledger.is_outcome_mature(outcome_id, instant(1 + target.horizon_sessions)))
            self.assertTrue(self.ledger.is_outcome_mature(outcome_id, instant(2 + target.horizon_sessions)))


if __name__ == "__main__":
    unittest.main()
