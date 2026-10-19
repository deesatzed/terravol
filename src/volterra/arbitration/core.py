"""Chronology-safe post-inference arbitration over one immutable expert pool."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math
from typing import Mapping, Sequence

from volterra.distributions import DiscreteDistribution, cdf_mixture

SUPPORTED_OBJECTIVES = (
    "equal_mixture", "global_regularized", "rolling_regularized",
    "loss_to_weight", "fforma_inspired", "direct_mixture_gate",
)


class ArbitrationError(ValueError):
    pass


def _utc(value: datetime, field: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ArbitrationError(f"{field} must be timezone-aware")


def _weights_from_losses(losses: Mapping[str, float]) -> dict[str, float]:
    if not losses or any(not math.isfinite(loss) or loss < 0 for loss in losses.values()):
        raise ArbitrationError("losses must be finite nonnegative values")
    raw = {expert: math.exp(-loss) for expert, loss in losses.items()}
    total = sum(raw.values())
    return {expert: value / total for expert, value in raw.items()}


@dataclass(frozen=True)
class ArbitrationRow:
    """A matured, out-of-fold label plus every expert output from one frozen pool."""

    origin_at: datetime
    matured_at: datetime
    event_group: str
    outcome: float
    forecasts: Mapping[str, DiscreteDistribution]
    features: Mapping[str, float]
    feature_available_at: datetime
    out_of_fold: bool

    def __post_init__(self) -> None:
        _utc(self.origin_at, "origin_at")
        _utc(self.matured_at, "matured_at")
        _utc(self.feature_available_at, "feature_available_at")
        if self.matured_at < self.origin_at:
            raise ArbitrationError("matured_at precedes origin_at")
        if self.feature_available_at > self.origin_at:
            raise ArbitrationError("features were unavailable at forecast origin")
        if not self.out_of_fold:
            raise ArbitrationError("arbitration rows require out-of-fold expert forecasts")
        if not isinstance(self.event_group, str) or not self.event_group:
            raise ArbitrationError("event_group is required")
        if not isinstance(self.outcome, (int, float)) or isinstance(self.outcome, bool) or not math.isfinite(self.outcome):
            raise ArbitrationError("outcome must be finite")
        forecasts = dict(self.forecasts)
        if len(forecasts) < 2 or not all(isinstance(key, str) and key and isinstance(value, DiscreteDistribution) for key, value in forecasts.items()):
            raise ArbitrationError("a same-pool row requires two named discrete expert forecasts")
        if not all(isinstance(key, str) and key and isinstance(value, (int, float)) and math.isfinite(value)
                       for key, value in self.features.items()):
            raise ArbitrationError("features must be finite named values")
        object.__setattr__(self, "forecasts", forecasts)
        object.__setattr__(self, "features", dict(self.features))


@dataclass(frozen=True)
class ArbitrationResult:
    objective: str
    expert_ids: tuple[str, ...]
    weights: dict[str, float]
    distribution: DiscreteDistribution
    trained_through: datetime | None


@dataclass(frozen=True)
class FittedArbitrator:
    objective: str
    weights: dict[str, float]
    trained_through: datetime
    feature_name: str | None = None
    loss_intercepts: dict[str, float] | None = None
    loss_slopes: dict[str, float] | None = None

    def predict(self, row: ArbitrationRow) -> ArbitrationResult:
        if tuple(sorted(row.forecasts)) != tuple(sorted(self.weights)):
            raise ArbitrationError("prediction pool differs from fitted expert pool")
        weights = dict(self.weights)
        if self.feature_name is not None:
            if self.feature_name not in row.features or self.loss_intercepts is None or self.loss_slopes is None:
                raise ArbitrationError("prediction lacks the fitted gate feature")
            value = row.features[self.feature_name]
            losses = {expert: max(0.0, self.loss_intercepts[expert] + self.loss_slopes[expert] * value)
                      for expert in self.weights}
            weights = _weights_from_losses(losses)
        distribution = cdf_mixture(tuple((weights[expert], row.forecasts[expert]) for expert in sorted(weights)))
        return ArbitrationResult(self.objective, tuple(sorted(weights)), weights, distribution, self.trained_through)


class SamePoolArbitrator:
    """Fits only on matured rows whose frozen full expert pool is identical."""

    def __init__(self, rows: Sequence[ArbitrationRow]) -> None:
        self.rows = tuple(rows)
        if not self.rows:
            raise ArbitrationError("same-pool arbitration requires rows")
        first = tuple(sorted(self.rows[0].forecasts))
        if any(tuple(sorted(row.forecasts)) != first for row in self.rows):
            raise ArbitrationError("all rows must use the identical expert pool")
        self.expert_ids = first

    def _eligible(self, as_of: datetime, window: int | None = None) -> tuple[ArbitrationRow, ...]:
        _utc(as_of, "as_of")
        eligible = tuple(row for row in self.rows if row.origin_at < as_of and row.matured_at <= as_of)
        if not eligible:
            raise ArbitrationError("no matured rows eligible at as_of")
        eligible = tuple(sorted(eligible, key=lambda row: row.origin_at))
        if window is not None:
            if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
                raise ArbitrationError("window must be a positive integer")
            eligible = eligible[-window:]
        return eligible

    def predict_equal(self, row: ArbitrationRow) -> ArbitrationResult:
        weights = {expert: 1.0 / len(self.expert_ids) for expert in self.expert_ids}
        return FittedArbitrator("equal_mixture", weights, row.origin_at).predict(row)

    def _fit(self, as_of: datetime, objective: str, window: int | None = None) -> FittedArbitrator:
        if objective not in SUPPORTED_OBJECTIVES or objective == "equal_mixture":
            raise ArbitrationError("fit requires a declared trainable objective")
        eligible = self._eligible(as_of, window)
        losses = {expert: sum(row.forecasts[expert].crps(row.outcome) for row in eligible) / len(eligible) for expert in self.expert_ids}
        return FittedArbitrator(objective, _weights_from_losses(losses), as_of)

    def fit_global(self, *, as_of: datetime) -> FittedArbitrator:
        return self._fit(as_of, "global_regularized")

    def fit_rolling(self, *, as_of: datetime, window: int) -> FittedArbitrator:
        return self._fit(as_of, "rolling_regularized", window)

    def fit_feature_gate(self, *, as_of: datetime, objective: str) -> FittedArbitrator:
        """A labeled low-capacity challenger; feature fitting uses only eligible OOF rows.

        This foundation stores a global loss-to-weight estimate.  A later artifact may
        supply a genuine feature model only while preserving this chronology contract.
        """
        if objective not in {"loss_to_weight", "fforma_inspired", "direct_mixture_gate"}:
            raise ArbitrationError("unsupported feature-gate objective")
        eligible = self._eligible(as_of)
        feature_names = set(eligible[0].features)
        if not feature_names or any(set(row.features) != feature_names for row in eligible):
            raise ArbitrationError("feature gate requires one stable nonempty feature schema")
        feature_name = sorted(feature_names)[0]
        values = [row.features[feature_name] for row in eligible]
        mean_value = sum(values) / len(values)
        denominator = sum((value - mean_value) ** 2 for value in values)
        intercepts: dict[str, float] = {}
        slopes: dict[str, float] = {}
        for expert in self.expert_ids:
            losses = [row.forecasts[expert].crps(row.outcome) for row in eligible]
            mean_loss = sum(losses) / len(losses)
            slope = 0.0 if denominator == 0.0 else sum((value - mean_value) * (loss - mean_loss) for value, loss in zip(values, losses)) / denominator
            slopes[expert] = slope
            intercepts[expert] = mean_loss - slope * mean_value
        base = _weights_from_losses({expert: max(0.0, intercepts[expert]) for expert in self.expert_ids})
        return FittedArbitrator(objective, base, as_of, feature_name, intercepts, slopes)
