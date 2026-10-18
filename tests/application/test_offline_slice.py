"""VT05 sealed synthetic forecast and delayed-score tests."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from volterra.storage import EvidenceLedger, MeasurementSpec, TargetDefinition


UTC = timezone.utc


def instant(day: int) -> datetime:
    return datetime(2026, 2, day, tzinfo=UTC)


def target() -> TargetDefinition:
    return TargetDefinition(
        "synthetic-variance-1-session-v1", 1, "synthetic_variance",
        MeasurementSpec("variance", 252, "SYNTHETIC", "FULL", "synthetic", "none", "UNSUPPORTED"),
    )


class OfflineSliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="volterra-vt05-")
        self.addCleanup(self.temp.cleanup)
        self.ledger = EvidenceLedger(Path(self.temp.name) / "ledger.sqlite")
        self.addCleanup(self.ledger.close)
        self.ledger.register_target(target())

    def test_ac_ctrl_04_sealed_forecast_scores_only_after_matching_mature_outcome(self) -> None:
        from volterra.baselines import NormalVarianceOutcomeDistribution
        from volterra.forecast_store import ForecastStore, ForecastStoreError
        snapshot = self.ledger.create_snapshot("origin", instant(1), policy="live")
        store = ForecastStore(Path(self.temp.name) / "forecasts.sqlite")
        self.addCleanup(store.close)
        forecast_id = store.seal_normal_forecast(
            snapshot_id=snapshot.snapshot_id, origin_at=instant(1), target=target(), model_id="persistence_variance",
            distribution=NormalVarianceOutcomeDistribution.for_target(target(), mean_variance=0.04, residual_scale=0.01),
            synthetic=True,
        )
        outcome_id = self.ledger.record_outcome(
            target_id=target().target_id, origin_at=instant(1), completed_sessions=1,
            target_end_at=instant(2), first_public_at=instant(3), value=0.05, synthetic=True,
        )
        with self.assertRaises(ForecastStoreError):
            store.score_mature_outcome(forecast_id, ledger=self.ledger, outcome_id=outcome_id, as_of=instant(2))
        score = store.score_mature_outcome(forecast_id, ledger=self.ledger, outcome_id=outcome_id, as_of=instant(3))
        self.assertGreater(score.crps, 0.0)
        self.assertEqual(store.get_forecast(forecast_id).forecast_id, forecast_id)
        with self.assertRaises(ForecastStoreError):
            store.seal_normal_forecast(
                snapshot_id=snapshot.snapshot_id, origin_at=instant(1), target=target(), model_id="persistence_variance",
                distribution=NormalVarianceOutcomeDistribution.for_target(target(), mean_variance=0.04, residual_scale=0.01),
                synthetic=True,
            )

