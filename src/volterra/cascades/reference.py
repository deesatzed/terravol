"""Small exact reference functions; no fitted or learned assumptions."""
from __future__ import annotations

import math


def independent_any_probability(probabilities: tuple[float, ...]) -> float:
    """Return P(any event), explicitly under independent Bernoulli assumptions."""
    remaining = 1.0
    for probability in probabilities:
        if not isinstance(probability, (int, float)) or isinstance(probability, bool) or not math.isfinite(probability):
            raise ValueError("probabilities must be finite numbers")
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probabilities must be within [0, 1]")
        remaining *= 1.0 - probability
    return 1.0 - remaining
