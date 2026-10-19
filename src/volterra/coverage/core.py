"""Deterministic, offline coverage planning for explicitly declared event worlds.

This module never updates event-world probabilities or starts monitoring jobs.  It
only evaluates the information value of a frozen candidate set.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations
import math
from typing import Mapping, Sequence


class CoverageError(ValueError):
    """Raised for unsupported or internally inconsistent coverage requests."""


def _finite_nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise CoverageError(f"{name} must be a finite nonnegative number")
    return float(value)


def _probability(value: float, name: str) -> float:
    result = _finite_nonnegative(value, name)
    if result > 1:
        raise CoverageError(f"{name} must be within [0, 1]")
    return result


@dataclass(frozen=True)
class Outcome:
    """A canonical downstream episode and its already-declared world probability."""

    outcome_id: str
    probability: float

    def __post_init__(self) -> None:
        if not isinstance(self.outcome_id, str) or not self.outcome_id:
            raise CoverageError("outcome_id is required")
        object.__setattr__(self, "probability", _probability(self.probability, "outcome probability"))


@dataclass(frozen=True)
class MonitorCandidate:
    """An offline monitor candidate with conditional detection probabilities by outcome."""

    monitor_id: str
    detection_by_outcome: Mapping[str, float]
    cost_usd: float
    dependency_group: str

    def __post_init__(self) -> None:
        if not isinstance(self.monitor_id, str) or not self.monitor_id:
            raise CoverageError("monitor_id is required")
        if not isinstance(self.dependency_group, str) or not self.dependency_group:
            raise CoverageError("dependency_group is required")
        values = dict(self.detection_by_outcome)
        if not values or not all(isinstance(key, str) and key for key in values):
            raise CoverageError("detection_by_outcome requires nonempty outcome identifiers")
        object.__setattr__(self, "detection_by_outcome", {key: _probability(value, "detection probability") for key, value in values.items()})
        object.__setattr__(self, "cost_usd", _finite_nonnegative(self.cost_usd, "cost_usd"))


@dataclass(frozen=True)
class CoveragePolicy:
    """Frozen query-local scoring rules and bounded candidate universe."""

    query_id: str
    graph_version: str
    utility_unit: str
    minimum_lead_time: timedelta
    monetary_cost_weight: float
    latency_cost_per_minute: float
    budget_usd: float
    candidate_universe: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all(isinstance(value, str) and value for value in (self.query_id, self.graph_version, self.utility_unit)):
            raise CoverageError("query_id, graph_version and utility_unit are required")
        if not isinstance(self.minimum_lead_time, timedelta) or self.minimum_lead_time < timedelta(0):
            raise CoverageError("minimum_lead_time must be nonnegative")
        for name in ("monetary_cost_weight", "latency_cost_per_minute", "budget_usd"):
            object.__setattr__(self, name, _finite_nonnegative(getattr(self, name), name))
        if not self.candidate_universe or not all(isinstance(item, str) and item for item in self.candidate_universe):
            raise CoverageError("candidate_universe requires monitor identifiers")
        if len(set(self.candidate_universe)) != len(self.candidate_universe):
            raise CoverageError("candidate_universe contains duplicates")

    def alert_status(self, receipt: "AlertReceipt") -> str:
        if receipt.monitor_id not in self.candidate_universe:
            return "INELIGIBLE_MONITOR"
        if not receipt.evidence_eligible:
            return "INELIGIBLE_EVIDENCE"
        if not receipt.successful:
            return "FAILED"
        if receipt.outcome_at - receipt.alert_at < self.minimum_lead_time:
            return "LATE"
        return "USABLE"


@dataclass(frozen=True)
class AlertReceipt:
    """Observed alert result retained even when it earns no coverage credit."""

    monitor_id: str
    outcome_id: str
    alert_at: datetime
    outcome_at: datetime
    successful: bool
    evidence_eligible: bool

    def __post_init__(self) -> None:
        if not all(isinstance(value, str) and value for value in (self.monitor_id, self.outcome_id)):
            raise CoverageError("alert identity is required")
        if any(value.tzinfo is None for value in (self.alert_at, self.outcome_at)):
            raise CoverageError("alert timestamps must be timezone-aware")


@dataclass(frozen=True)
class CoveragePlan:
    query_id: str
    selected_monitor_ids: tuple[str, ...]
    outcome_probabilities: dict[str, float]
    expected_coverage: float
    monitoring_cost_usd: float
    utility: float
    overlap_diagnostics: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class ConditionalResearchWatch:
    """A stored local plan; runtime scheduling remains disabled by construction."""

    watch_id: str
    policy: CoveragePolicy
    selected_monitor_ids: tuple[str, ...]
    event_id: str
    forecast_id: str
    external_job_enabled: bool = False

    def __post_init__(self) -> None:
        if not all(isinstance(value, str) and value for value in (self.watch_id, self.event_id, self.forecast_id)):
            raise CoverageError("watch, event and forecast identities are required")
        if self.external_job_enabled:
            raise CoverageError("a research watch cannot enable an external job")
        if not set(self.selected_monitor_ids).issubset(self.policy.candidate_universe):
            raise CoverageError("watch selects monitor outside frozen candidate universe")


def _validated_inputs(policy: CoveragePolicy, outcomes: Sequence[Outcome], candidates: Sequence[MonitorCandidate], selected_ids: Sequence[str]) -> tuple[dict[str, Outcome], dict[str, MonitorCandidate], tuple[str, ...]]:
    outcome_by_id = {outcome.outcome_id: outcome for outcome in outcomes}
    if len(outcome_by_id) != len(outcomes) or not outcome_by_id:
        raise CoverageError("outcomes must have unique identities")
    candidate_by_id = {candidate.monitor_id: candidate for candidate in candidates}
    if len(candidate_by_id) != len(candidates):
        raise CoverageError("candidates must have unique identities")
    if set(candidate_by_id) != set(policy.candidate_universe):
        raise CoverageError("candidates must exactly match the frozen candidate universe")
    selected = tuple(selected_ids)
    if len(set(selected)) != len(selected) or not set(selected).issubset(candidate_by_id):
        raise CoverageError("selected monitors must be unique frozen candidates")
    if any(outcome_id not in outcome_by_id for candidate in candidates for outcome_id in candidate.detection_by_outcome):
        raise CoverageError("candidate references unknown outcome")
    return outcome_by_id, candidate_by_id, selected


def plan_coverage(policy: CoveragePolicy, outcomes: Sequence[Outcome], candidates: Sequence[MonitorCandidate], selected_ids: Sequence[str]) -> CoveragePlan:
    """Evaluate deduplicated outcome coverage under explicit conditional detection independence.

    Detection independence is an assumption about feeds conditional on an existing
    outcome; the outcome's world probability is copied unchanged into the result.
    """
    outcome_by_id, candidate_by_id, selected = _validated_inputs(policy, outcomes, candidates, selected_ids)
    selected_candidates = tuple(candidate_by_id[identifier] for identifier in selected)
    cost = sum(candidate.cost_usd for candidate in selected_candidates)
    if cost > policy.budget_usd + 1e-12:
        raise CoverageError("selected monitors exceed frozen budget")
    coverage = 0.0
    overlaps: dict[str, tuple[str, ...]] = {}
    for outcome_id, outcome in outcome_by_id.items():
        monitors = tuple(candidate.monitor_id for candidate in selected_candidates if outcome_id in candidate.detection_by_outcome)
        if monitors:
            no_detection = math.prod(1.0 - candidate_by_id[monitor].detection_by_outcome[outcome_id] for monitor in monitors)
            coverage += outcome.probability * (1.0 - no_detection)
            if len(monitors) > 1:
                overlaps[outcome_id] = monitors
    utility = coverage - policy.monetary_cost_weight * cost
    return CoveragePlan(policy.query_id, selected, {key: item.probability for key, item in outcome_by_id.items()}, coverage, cost, utility, overlaps)


def exact_small_set_plan(policy: CoveragePolicy, outcomes: Sequence[Outcome], candidates: Sequence[MonitorCandidate]) -> CoveragePlan:
    """Enumerate the bounded candidate set for a correctness comparator, never a live job."""
    if len(candidates) > 16:
        raise CoverageError("exact enumeration is limited to 16 candidates")
    _, candidate_by_id, _ = _validated_inputs(policy, outcomes, candidates, ())
    identifiers = tuple(candidate_by_id)
    feasible: list[CoveragePlan] = []
    for count in range(len(identifiers) + 1):
        for subset in combinations(identifiers, count):
            if sum(candidate_by_id[item].cost_usd for item in subset) <= policy.budget_usd + 1e-12:
                feasible.append(plan_coverage(policy, outcomes, candidates, subset))
    return max(feasible, key=lambda result: (result.utility, result.expected_coverage, tuple(reversed(result.selected_monitor_ids))))
