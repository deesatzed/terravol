"""Small exact reference functions; no fitted or learned assumptions."""
from __future__ import annotations

import math
from dataclasses import dataclass


def _validated(probabilities: tuple[float, ...]) -> tuple[float, ...]:
    values = tuple(probabilities)
    for probability in values:
        if not isinstance(probability, (int, float)) or isinstance(probability, bool) or not math.isfinite(probability):
            raise ValueError("probabilities must be finite numbers")
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probabilities must be within [0, 1]")
    return values


def independent_any_probability(probabilities: tuple[float, ...]) -> float:
    """Return P(any event), explicitly under independent Bernoulli assumptions."""
    remaining = 1.0
    for probability in _validated(probabilities):
        remaining *= 1.0 - probability
    return 1.0 - remaining


def coincident_any_probability(probabilities: tuple[float, ...]) -> float:
    """Return the union when events are declared perfectly coincident."""
    values = _validated(probabilities)
    if values and any(value != values[0] for value in values[1:]):
        raise ValueError("perfectly coincident events require equal marginal probabilities")
    return values[0] if values else 0.0


def exclusive_any_probability(probabilities: tuple[float, ...]) -> float:
    """Return the union for explicitly mutually exclusive events."""
    total = sum(_validated(probabilities))
    if total > 1.0 + 1e-12:
        raise ValueError("mutually exclusive event probabilities cannot exceed one")
    return total


def joint_probability_bounds(first: float, second: float) -> tuple[float, float]:
    """Return Fréchet bounds when no dependence model has been admitted."""
    left, right = _validated((first, second))
    return (round(max(0.0, left + right - 1.0), 12), min(left, right))


def unique_source_probabilities(sources: tuple[tuple[str, float], ...]) -> tuple[float, ...]:
    """Validate stable source identities before any exact world arithmetic."""
    identifiers = tuple(source_id for source_id, _ in sources)
    if not all(isinstance(source_id, str) and source_id for source_id in identifiers):
        raise ValueError("source identities must be nonempty strings")
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("a source identity may appear only once in a scenario")
    return _validated(tuple(probability for _, probability in sources))


@dataclass(frozen=True)
class ExclusiveBranchTable:
    """A named, exhaustive mutually exclusive branch distribution."""
    branches: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        names = tuple(name for name, _ in self.branches)
        if not names or not all(isinstance(name, str) and name for name in names):
            raise ValueError("exclusive branches require nonempty names")
        if len(set(names)) != len(names):
            raise ValueError("exclusive branch names must be unique")
        values = _validated(tuple(value for _, value in self.branches))
        if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("exclusive branch probabilities must sum to one")

    def probability_of(self, name: str) -> float:
        for branch, probability in self.branches:
            if branch == name:
                return probability
        raise KeyError(name)
