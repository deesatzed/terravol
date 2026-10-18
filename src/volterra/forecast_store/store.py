"""Local immutable forecasts with maturity-gated proper scoring."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sqlite3

from volterra.baselines import NormalVarianceOutcomeDistribution
from volterra.contracts import canonical_json
from volterra.storage import EvidenceLedger, TargetDefinition


class ForecastStoreError(ValueError):
    """A forecast mutation or score violates the delayed-score contract."""


def _utc(value: datetime, field: str) -> str:
    if value.tzinfo is None:
        raise ForecastStoreError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat()


@dataclass(frozen=True)
class ForecastRecord:
    forecast_id: str
    snapshot_id: str
    target_id: str
    measurement_identity: str
    origin_at: datetime
    model_id: str
    mean_variance: float
    residual_scale: float
    synthetic: bool


@dataclass(frozen=True)
class ForecastScore:
    forecast_id: str
    outcome_id: str
    crps: float
    scored_at: datetime


def normal_crps(*, mean: float, scale: float, observation: float) -> float:
    """CRPS for a Normal forecast; finite scale and outcome are required."""
    if not all(math.isfinite(value) for value in (mean, scale, observation)) or scale <= 0.0:
        raise ForecastStoreError("Normal CRPS requires finite mean, observation, and positive scale")
    z = (observation - mean) / scale
    phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
    Phi = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    return scale * (z * (2.0 * Phi - 1.0) + 2.0 * phi - 1.0 / math.sqrt(math.pi))


class ForecastStore:
    def __init__(self, path: Path) -> None:
        self.connection = sqlite3.connect(path)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS forecasts (
              forecast_id TEXT PRIMARY KEY, snapshot_id TEXT NOT NULL, target_id TEXT NOT NULL,
              measurement_identity TEXT NOT NULL, origin_at TEXT NOT NULL, model_id TEXT NOT NULL,
              mean_variance REAL NOT NULL, residual_scale REAL NOT NULL, synthetic INTEGER NOT NULL
            )
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS forecast_scores (
              forecast_id TEXT PRIMARY KEY REFERENCES forecasts(forecast_id), outcome_id TEXT NOT NULL,
              crps REAL NOT NULL, scored_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def seal_normal_forecast(self, *, snapshot_id: str, origin_at: datetime, target: TargetDefinition,
                             model_id: str, distribution: NormalVarianceOutcomeDistribution,
                             synthetic: bool) -> str:
        if not snapshot_id or not model_id:
            raise ForecastStoreError("forecast requires snapshot and model identity")
        if distribution.target_id != target.target_id or distribution.measurement_identity != target.measurement.canonical():
            raise ForecastStoreError("forecast distribution target measurement does not match declared target")
        origin = _utc(origin_at, "origin_at")
        frozen = canonical_json({
            "snapshot_id": snapshot_id, "target_id": target.target_id,
            "measurement_identity": target.measurement.canonical(), "origin_at": origin, "model_id": model_id,
            "mean_variance": distribution.mean_variance, "residual_scale": distribution.residual_scale,
            "synthetic": synthetic,
        })
        forecast_id = hashlib.sha256(frozen.encode()).hexdigest()
        with self.connection:
            existing = self.connection.execute("SELECT forecast_id FROM forecasts WHERE forecast_id = ?", (forecast_id,)).fetchone()
            if existing is not None:
                raise ForecastStoreError("forecast is already sealed")
            self.connection.execute(
                "INSERT INTO forecasts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (forecast_id, snapshot_id, target.target_id, target.measurement.canonical(), origin, model_id,
                 distribution.mean_variance, distribution.residual_scale, int(synthetic)),
            )
        return forecast_id

    def get_forecast(self, forecast_id: str) -> ForecastRecord:
        row = self.connection.execute("SELECT * FROM forecasts WHERE forecast_id = ?", (forecast_id,)).fetchone()
        if row is None:
            raise ForecastStoreError("forecast_id does not exist")
        return ForecastRecord(row[0], row[1], row[2], row[3], datetime.fromisoformat(row[4]), row[5], row[6], row[7], bool(row[8]))

    def score_mature_outcome(self, forecast_id: str, *, ledger: EvidenceLedger, outcome_id: str,
                             as_of: datetime) -> ForecastScore:
        forecast = self.get_forecast(forecast_id)
        if not ledger.is_outcome_mature(outcome_id, as_of):
            raise ForecastStoreError("outcome is not mature at scoring time")
        outcome = ledger.get_outcome(outcome_id)
        if outcome.target_id != forecast.target_id or outcome.origin_at != forecast.origin_at:
            raise ForecastStoreError("outcome does not match sealed forecast target and origin")
        if outcome.synthetic != forecast.synthetic:
            raise ForecastStoreError("synthetic and observed outcomes may not be mixed")
        if isinstance(outcome.value, bool) or not isinstance(outcome.value, (int, float)):
            raise ForecastStoreError("outcome value must be a finite scalar for Normal CRPS")
        crps = normal_crps(mean=forecast.mean_variance, scale=forecast.residual_scale, observation=float(outcome.value))
        scored_at = _utc(as_of, "as_of")
        with self.connection:
            existing = self.connection.execute("SELECT outcome_id, crps, scored_at FROM forecast_scores WHERE forecast_id = ?", (forecast_id,)).fetchone()
            if existing is not None:
                if tuple(existing) != (outcome_id, crps, scored_at):
                    raise ForecastStoreError("forecast score is immutable once recorded")
            else:
                self.connection.execute("INSERT INTO forecast_scores VALUES (?, ?, ?, ?)", (forecast_id, outcome_id, crps, scored_at))
        return ForecastScore(forecast_id, outcome_id, crps, datetime.fromisoformat(scored_at))
