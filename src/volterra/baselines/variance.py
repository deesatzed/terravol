"""Measurement-explicit point variance baselines, not intraday distributions."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math

from volterra.storage import TargetDefinition


def _history(values: tuple[float, ...]) -> tuple[float, ...]:
    if not values:
        raise ValueError("variance history is required")
    normalized = tuple(float(value) for value in values)
    if any(not math.isfinite(value) or value <= 0.0 for value in normalized):
        raise ValueError("variance history must be finite and strictly positive")
    return normalized


@dataclass(frozen=True)
class VarianceForecastContext:
    """The complete admissible context for a pre-outcome baseline forecast.

    The realized target and post-origin features deliberately have no field here.
    A caller must create a new immutable context after sealing an eligible snapshot.
    """
    snapshot_id: str
    target_id: str
    origin_at: datetime
    variance_history: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.snapshot_id or not self.target_id:
            raise ValueError("forecast context requires sealed snapshot and target identity")
        if self.origin_at.tzinfo is None:
            raise ValueError("forecast context origin_at must be timezone-aware")
        object.__setattr__(self, "variance_history", _history(self.variance_history))


@dataclass(frozen=True)
class PointVarianceForecast:
    model_id: str
    mean_variance: float
    is_intraday_realized_variance_distribution: bool = False

    def __post_init__(self) -> None:
        if not self.model_id or not math.isfinite(self.mean_variance) or self.mean_variance <= 0.0:
            raise ValueError("point variance forecast requires identity and positive finite variance")


@dataclass(frozen=True)
class NormalVarianceOutcomeDistribution:
    """A residual uncertainty contract around a point variance forecast.

    This describes a forecast outcome distribution, not an intraday realized-variance distribution.
    """
    target_id: str
    measurement_identity: str
    mean_variance: float
    residual_scale: float
    is_intraday_realized_variance_distribution: bool = False

    def __post_init__(self) -> None:
        if not self.target_id or not self.measurement_identity:
            raise ValueError("outcome distribution requires target and measurement identity")
        if not math.isfinite(self.mean_variance) or self.mean_variance <= 0.0:
            raise ValueError("mean_variance must be finite and positive")
        if not math.isfinite(self.residual_scale) or self.residual_scale <= 0.0:
            raise ValueError("residual_scale must be finite and positive")

    @property
    def variance(self) -> float:
        return self.residual_scale ** 2

    @classmethod
    def for_target(cls, target: TargetDefinition, *, mean_variance: float, residual_scale: float) -> "NormalVarianceOutcomeDistribution":
        return cls(
            target_id=target.target_id,
            measurement_identity=target.measurement.canonical(),
            mean_variance=mean_variance,
            residual_scale=residual_scale,
        )


@dataclass(frozen=True)
class PersistenceVarianceBaseline:
    def forecast(self, history: tuple[float, ...]) -> PointVarianceForecast:
        return PointVarianceForecast("persistence_variance", _history(history)[-1])

    def forecast_context(self, context: VarianceForecastContext) -> PointVarianceForecast:
        return self.forecast(context.variance_history)


@dataclass(frozen=True)
class EWMAVarianceBaseline:
    decay: float = 0.94

    def __post_init__(self) -> None:
        if not math.isfinite(self.decay) or not 0.0 <= self.decay < 1.0:
            raise ValueError("decay must be finite and within [0, 1)")

    def forecast(self, history: tuple[float, ...]) -> PointVarianceForecast:
        values = _history(history)
        estimate = values[0]
        for value in values[1:]:
            estimate = self.decay * estimate + (1.0 - self.decay) * value
        return PointVarianceForecast("ewma_variance", estimate)

    def forecast_context(self, context: VarianceForecastContext) -> PointVarianceForecast:
        return self.forecast(context.variance_history)


@dataclass(frozen=True)
class LogHARVarianceBaseline:
    """Configured log-HAR inference over pre-origin realized-variance history.

    Parameter estimation is deliberately outside this primitive: callers must record a
    fit artifact and its as-of snapshot before constructing the configured baseline.
    """
    intercept: float
    daily_coefficient: float
    weekly_coefficient: float
    monthly_coefficient: float

    def __post_init__(self) -> None:
        coefficients = (
            self.intercept,
            self.daily_coefficient,
            self.weekly_coefficient,
            self.monthly_coefficient,
        )
        if any(not math.isfinite(value) for value in coefficients):
            raise ValueError("Log-HAR coefficients must be finite")

    def forecast(self, history: tuple[float, ...]) -> PointVarianceForecast:
        values = _history(history)
        if len(values) < 22:
            raise ValueError("Log-HAR requires at least 22 pre-origin variance observations")
        daily = math.log(values[-1])
        weekly = sum(math.log(value) for value in values[-5:]) / 5.0
        monthly = sum(math.log(value) for value in values[-22:]) / 22.0
        log_forecast = (
            self.intercept
            + self.daily_coefficient * daily
            + self.weekly_coefficient * weekly
            + self.monthly_coefficient * monthly
        )
        if not math.isfinite(log_forecast) or log_forecast > math.log(float.fromhex("0x1.fffffffffffffp+1023")):
            raise ValueError("Log-HAR forecast is not representable as finite variance")
        return PointVarianceForecast("log_har_variance", math.exp(log_forecast))

    def forecast_context(self, context: VarianceForecastContext) -> PointVarianceForecast:
        return self.forecast(context.variance_history)


@dataclass(frozen=True)
class GJRGARCHVarianceBaseline:
    """Configured GJR-GARCH(1,1) recursion over pre-origin returns."""
    omega: float
    alpha: float
    gamma: float
    beta: float

    def __post_init__(self) -> None:
        parameters = (self.omega, self.alpha, self.gamma, self.beta)
        if any(not math.isfinite(value) for value in parameters) or self.omega <= 0.0:
            raise ValueError("GJR-GARCH parameters must be finite and omega positive")
        if any(value < 0.0 for value in (self.alpha, self.gamma, self.beta)):
            raise ValueError("GJR-GARCH alpha, gamma, and beta must be nonnegative")
        if self.alpha + 0.5 * self.gamma + self.beta >= 1.0:
            raise ValueError("GJR-GARCH parameters require alpha + gamma/2 + beta < 1")

    def forecast(self, returns: tuple[float, ...]) -> PointVarianceForecast:
        if not returns:
            raise ValueError("GJR-GARCH return history is required")
        values = tuple(float(value) for value in returns)
        if any(not math.isfinite(value) for value in values):
            raise ValueError("GJR-GARCH returns must be finite")
        variance = self.omega / (1.0 - self.alpha - 0.5 * self.gamma - self.beta)
        for value in values:
            innovation = value * value
            asymmetric = innovation if value < 0.0 else 0.0
            variance = self.omega + self.alpha * innovation + self.gamma * asymmetric + self.beta * variance
        return PointVarianceForecast("gjr_garch_variance", variance)
