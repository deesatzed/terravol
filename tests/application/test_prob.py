"""VT01 probability contract acceptance tests."""
from __future__ import annotations

import unittest


class ProbabilityContractTests(unittest.TestCase):
    def test_ac_prob_01_probability_concepts_have_distinct_types(self) -> None:
        try:
            from volterra.contracts import (
                EventProbability,
                ExpertWeight,
                ScenarioProbability,
                TransmissionProbability,
            )
        except ImportError as exc:
            self.fail(f"VT01 probability contracts are not implemented: {exc}")
        concepts = (
            EventProbability(0.25),
            TransmissionProbability(0.25),
            ScenarioProbability(0.25),
            ExpertWeight(0.25),
        )
        self.assertEqual([item.value for item in concepts], [0.25] * 4)
        self.assertEqual(len({type(item) for item in concepts}), 4)


if __name__ == "__main__":
    unittest.main()
