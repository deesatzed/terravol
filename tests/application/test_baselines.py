"""VT04 classical baseline tests over synthetic variance histories."""
from __future__ import annotations

from dataclasses import fields
from datetime import datetime, timezone
import unittest

from volterra.storage import MeasurementSpec, TargetDefinition


def _synthetic_variance_target() -> TargetDefinition:
    return TargetDefinition(
        target_id="synthetic-variance-5-session-v1",
        horizon_sessions=5,
        estimator_id="synthetic-realized-variance",
        measurement=MeasurementSpec(
            units="variance", annualization_sessions=252, session_calendar_id="SYNTHETIC",
            coverage_policy="complete", proxy_label="synthetic", adjustment_policy="none",
            nonpositive_price_policy="UNSUPPORTED",
        ),
    )


class ClassicalBaselineTests(unittest.TestCase):
    def test_ac_dist_01_identical_point_experts_can_retain_residual_uncertainty(self) -> None:
        try:
            from volterra.baselines import NormalVarianceOutcomeDistribution
        except ImportError as exc:
            self.fail(f"VT04 outcome distribution is not implemented: {exc}")
        target = _synthetic_variance_target()
        first = NormalVarianceOutcomeDistribution.for_target(target, mean_variance=0.04, residual_scale=0.01)
        second = NormalVarianceOutcomeDistribution.for_target(target, mean_variance=0.04, residual_scale=0.02)
        self.assertEqual(first.mean_variance, second.mean_variance)
        self.assertNotEqual(first.residual_scale, second.residual_scale)
        self.assertGreater(first.variance, 0.0)

    def test_residual_distribution_carries_immutable_target_measurement_identity(self) -> None:
        from volterra.baselines import NormalVarianceOutcomeDistribution
        target = _synthetic_variance_target()
        distribution = NormalVarianceOutcomeDistribution.for_target(target, mean_variance=0.04, residual_scale=0.01)
        self.assertEqual(distribution.target_id, target.target_id)
        self.assertEqual(distribution.measurement_identity, target.measurement.canonical())
        with self.assertRaises(ValueError):
            NormalVarianceOutcomeDistribution(
                target_id="", measurement_identity="", mean_variance=0.04, residual_scale=0.01
            )

    def test_ac_dist_08_blocks_a_consumer_that_requires_an_unsupported_moment(self) -> None:
        from volterra.contracts import ContractError, StudentTSpec
        heavy_tailed = StudentTSpec(degrees_of_freedom=2.0, location=0.0, scale=1.0)
        with self.assertRaisesRegex(ContractError, "tail-payoff requires finite moment order 2"):
            heavy_tailed.require_finite_moment(2, consumer="tail-payoff")
        StudentTSpec(degrees_of_freedom=3.0, location=0.0, scale=1.0).require_finite_moment(
            2, consumer="tail-payoff"
        )

    def test_ac_time_02_baseline_context_excludes_realized_target_and_future_features(self) -> None:
        from volterra.baselines import EWMAVarianceBaseline, VarianceForecastContext
        context = VarianceForecastContext(
            snapshot_id="sealed-origin-1",
            target_id="synthetic-variance-5-session-v1",
            origin_at=datetime(2026, 1, 5, tzinfo=timezone.utc),
            variance_history=(0.01, 0.09),
        )
        forecast = EWMAVarianceBaseline(decay=0.5).forecast_context(context)
        self.assertAlmostEqual(forecast.mean_variance, 0.05)
        field_names = {field.name for field in fields(VarianceForecastContext)}
        self.assertNotIn("realized_target", field_names)
        self.assertNotIn("future_features", field_names)
        with self.assertRaises(TypeError):
            VarianceForecastContext(
                snapshot_id="sealed-origin-1", target_id="synthetic-variance-5-session-v1",
                origin_at=datetime(2026, 1, 5, tzinfo=timezone.utc), variance_history=(0.01, 0.09),
                realized_target=0.50,
            )

    def test_ac_dist_09_persistence_is_explicit_point_variance_not_intraday_distribution(self) -> None:
        try:
            from volterra.baselines import PersistenceVarianceBaseline
        except ImportError as exc:
            self.fail(f"VT04 persistence baseline is not implemented: {exc}")
        forecast = PersistenceVarianceBaseline().forecast((0.01, 0.04, 0.09))
        self.assertEqual(forecast.mean_variance, 0.09)
        self.assertEqual(forecast.model_id, "persistence_variance")
        self.assertFalse(forecast.is_intraday_realized_variance_distribution)

    def test_ewma_uses_only_pre_origin_history_and_positive_finite_variance(self) -> None:
        try:
            from volterra.baselines import EWMAVarianceBaseline
        except ImportError as exc:
            self.fail(f"VT04 EWMA baseline is not implemented: {exc}")
        forecast = EWMAVarianceBaseline(decay=0.5).forecast((0.01, 0.09))
        self.assertAlmostEqual(forecast.mean_variance, 0.05)
        with self.assertRaises(ValueError):
            EWMAVarianceBaseline().forecast((0.01, 0.0))

    def test_log_har_uses_configured_lag_windows_without_fitting_on_future_data(self) -> None:
        try:
            from volterra.baselines import LogHARVarianceBaseline
        except ImportError as exc:
            self.fail(f"VT04 Log-HAR baseline is not implemented: {exc}")
        forecast = LogHARVarianceBaseline(
            intercept=0.0, daily_coefficient=1.0, weekly_coefficient=0.0, monthly_coefficient=0.0
        ).forecast((0.04,) * 22)
        self.assertAlmostEqual(forecast.mean_variance, 0.04)
        self.assertEqual(forecast.model_id, "log_har_variance")

    def test_gjr_garch_preserves_positive_variance_and_rejects_nonstationary_parameters(self) -> None:
        try:
            from volterra.baselines import GJRGARCHVarianceBaseline
        except ImportError as exc:
            self.fail(f"VT04 GJR-GARCH baseline is not implemented: {exc}")
        forecast = GJRGARCHVarianceBaseline(
            omega=0.001, alpha=0.1, gamma=0.1, beta=0.7
        ).forecast((-0.1, 0.1))
        self.assertGreater(forecast.mean_variance, 0.0)
        self.assertEqual(forecast.model_id, "gjr_garch_variance")
        with self.assertRaises(ValueError):
            GJRGARCHVarianceBaseline(omega=0.001, alpha=0.5, gamma=0.4, beta=0.4)

