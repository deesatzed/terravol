from __future__ import annotations
from datetime import datetime, timedelta, timezone
import unittest

UTC = timezone.utc


def rows():
    from volterra.arbitration import ArbitrationRow
    from volterra.distributions import DiscreteDistribution
    start = datetime(2026, 1, 1, tzinfo=UTC)
    return tuple(
        ArbitrationRow(
            origin_at=start + timedelta(days=index),
            matured_at=start + timedelta(days=index + 1),
            event_group=f"event-{index}",
            outcome=float(index % 2),
            forecasts={
                "steady": DiscreteDistribution(((0.0, .8), (1.0, .2))),
                "reactive": DiscreteDistribution(((0.0, .2), (1.0, .8))),
            },
            features={"calendar_distance": float(index)},
            feature_available_at=start + timedelta(days=index),
            out_of_fold=True,
        )
        for index in range(4)
    )


class ArbitrationTests(unittest.TestCase):
    def test_ac_arb_01_same_pool_controls_produce_mixtures(self) -> None:
        from volterra.arbitration import SamePoolArbitrator
        pool = rows()
        arbitrator = SamePoolArbitrator(pool)
        origin = datetime(2026, 1, 5, tzinfo=UTC)
        equal = arbitrator.predict_equal(pool[-1])
        global_result = arbitrator.fit_global(as_of=origin).predict(pool[-1])
        rolling = arbitrator.fit_rolling(as_of=origin, window=2).predict(pool[-1])
        self.assertEqual(equal.expert_ids, global_result.expert_ids)
        self.assertEqual(global_result.expert_ids, rolling.expert_ids)
        self.assertAlmostEqual(sum(global_result.weights.values()), 1.0)

    def test_ac_arb_03_training_rejects_future_or_non_oof_features_and_labels(self) -> None:
        from volterra.arbitration import ArbitrationError, SamePoolArbitrator
        pool = list(rows())
        future = pool[-1]
        with self.assertRaises(ArbitrationError):
            SamePoolArbitrator(tuple(pool[:-1] + [future.__class__(
                future.origin_at, future.matured_at, future.event_group, future.outcome,
                future.forecasts, future.features, future.origin_at + timedelta(days=1), True,
            )]))
        with self.assertRaises(ArbitrationError):
            SamePoolArbitrator(tuple(pool[:-1] + [future.__class__(
                future.origin_at, future.matured_at, future.event_group, future.outcome,
                future.forecasts, future.features, future.feature_available_at, False,
            )]))

    def test_ac_arb_04_objectives_have_distinct_declared_identities(self) -> None:
        from volterra.arbitration import SUPPORTED_OBJECTIVES, SamePoolArbitrator
        a = SamePoolArbitrator(rows())
        self.assertEqual(set(SUPPORTED_OBJECTIVES), {"equal_mixture", "global_regularized", "rolling_regularized", "loss_to_weight", "fforma_inspired", "direct_mixture_gate"})
        self.assertEqual(a.fit_feature_gate(as_of=datetime(2026, 1, 5, tzinfo=UTC), objective="loss_to_weight").objective, "loss_to_weight")
        self.assertEqual(a.fit_feature_gate(as_of=datetime(2026, 1, 5, tzinfo=UTC), objective="fforma_inspired").objective, "fforma_inspired")
        self.assertEqual(a.fit_feature_gate(as_of=datetime(2026, 1, 5, tzinfo=UTC), objective="direct_mixture_gate").objective, "direct_mixture_gate")

    def test_feature_gate_changes_weights_from_available_feature_only(self) -> None:
        from volterra.arbitration import SamePoolArbitrator
        pool = rows()
        gate = SamePoolArbitrator(pool).fit_feature_gate(as_of=datetime(2026, 1, 5, tzinfo=UTC), objective="loss_to_weight")
        low = gate.predict(pool[0])
        high = gate.predict(pool[-1])
        self.assertNotEqual(low.weights, high.weights)

class ConditionalFusionTests(unittest.TestCase):
    def test_ac_arb_05_unconditional_is_not_double_weighted(self) -> None:
        from volterra.arbitration import conditional_fuse
        from volterra.distributions import DiscreteDistribution
        baseline = DiscreteDistribution(((0.0, 1.0),))
        result = conditional_fuse({"no": .7, "yes": .3}, {"base": baseline}, {"base": 1.0})
        self.assertEqual(result.distribution.atoms, ((0.0, 1.0),))
        self.assertEqual(result.world_masses, {"no": .7, "yes": .3})

    def test_ac_arb_06_marginal_expert_cannot_pose_as_conditional(self) -> None:
        from volterra.arbitration import ArbitrationError, conditional_fuse
        from volterra.distributions import DiscreteDistribution
        with self.assertRaises(ArbitrationError):
            conditional_fuse({"no": .5, "yes": .5}, {"only_no": {"no": DiscreteDistribution(((0.0, 1.0),))}}, {"only_no": 1.0})

    def test_ac_arb_10_shrinkage_is_bounded_toward_baseline(self) -> None:
        from volterra.arbitration import shrink_weights
        weights=shrink_weights({"a":1.0,"b":0.0},{"a":.5,"b":.5},strength=.8,max_change=.2)
        self.assertEqual(weights,{"a":.7,"b":.3})

    def test_ac_arb_11_world_mass_is_distinct_from_expert_weight(self) -> None:
        from volterra.arbitration import conditional_fuse
        from volterra.distributions import DiscreteDistribution
        result=conditional_fuse({"no":.9,"yes":.1},{"a":DiscreteDistribution(((0.0,1.0),)),"b":DiscreteDistribution(((1.0,1.0),))},{"a":.25,"b":.75})
        self.assertEqual(result.world_masses,{"no":.9,"yes":.1})
        self.assertNotEqual(result.world_masses,{"a":.25,"b":.75})

    def test_ac_arb_02_post_inference_features_cannot_drive_selection(self) -> None:
        from volterra.selection import CheapFeature, SelectionError, select_experts
        now=datetime(2026,1,1,tzinfo=UTC)
        with self.assertRaises(SelectionError): select_experts(("a","b"),("a",),(CheapFeature("spread",1.0,now,True),),now)
