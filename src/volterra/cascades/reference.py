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


def background_probability(precursor_probability: float, given_precursor: float, given_absence: float) -> float:
    """Apply total probability without deleting background risk when A is absent."""
    precursor, present, absent = _validated((precursor_probability, given_precursor, given_absence))
    return precursor * present + (1.0 - precursor) * absent


def complete_set_probability(precursor_probability: float, first_given_precursor: float,
                             second_given_precursor: float, *, scenario_sets: int = 1) -> float:
    """Exact complete A-B-C probability, optionally across independent complete sets."""
    precursor, first, second = _validated((precursor_probability, first_given_precursor, second_given_precursor))
    if isinstance(scenario_sets, bool) or not isinstance(scenario_sets, int) or scenario_sets <= 0:
        raise ValueError("scenario_sets must be a positive integer")
    complete = precursor * first * second
    return 1.0 - (1.0 - complete) ** scenario_sets


def shared_downstream_probability(precursor_probabilities: tuple[float, ...], given_any_precursor: float,
                                  given_no_precursor: float) -> float:
    """Count one shared downstream outcome once across independent precursor routes."""
    given_any, given_none = _validated((given_any_precursor, given_no_precursor))
    any_precursor = independent_any_probability(precursor_probabilities)
    return any_precursor * given_any + (1.0 - any_precursor) * given_none


def conditional_both_or_either(first: float, second: float, *, joint_probability: float) -> tuple[float, float]:
    """Return separate `both` and `either` values for declared conditional joint mass."""
    left, right, joint = _validated((first, second, joint_probability))
    lower, upper = joint_probability_bounds(left, right)
    if joint < lower or joint > upper:
        raise ValueError("joint_probability violates the supplied marginal bounds")
    return joint, left + right - joint


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
