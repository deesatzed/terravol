"""Classical, deterministic variance baselines."""

from volterra.baselines.variance import (
    EWMAVarianceBaseline, GJRGARCHVarianceBaseline, LogHARVarianceBaseline, NormalVarianceOutcomeDistribution,
    PersistenceVarianceBaseline, PointVarianceForecast, VarianceForecastContext,
)

__all__ = [
    "EWMAVarianceBaseline", "GJRGARCHVarianceBaseline", "LogHARVarianceBaseline",
    "NormalVarianceOutcomeDistribution", "PersistenceVarianceBaseline", "PointVarianceForecast",
    "VarianceForecastContext",
]
