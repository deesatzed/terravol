"""Finite, immutable contracts with no implicit probability semantics."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from typing import Any, ClassVar


class ContractError(ValueError):
    """A value violates a declared runtime contract."""


def _finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{name} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ContractError(f"{name} must be finite")
    return number


def _finite_tree(value: Any, path: str = "value") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError(f"{path} must be finite")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ContractError("JSON object keys must be strings")
            _finite_tree(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _finite_tree(child, f"{path}[{index}]")
    elif not isinstance(value, (str, int, float, bool, type(None))):
        raise ContractError(f"{path} has unsupported serialized type {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return deterministic JSON after recursively rejecting non-finite values."""
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    _finite_tree(value)
    try:
        return json.dumps(value, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ContractError(f"cannot serialize contract: {exc}") from exc


@dataclass(frozen=True)
class _Probability:
    value: float
    _kind: ClassVar[str] = "probability"

    def __post_init__(self) -> None:
        value = _finite_number(self.value, self._kind)
        if not 0.0 <= value <= 1.0:
            raise ContractError(f"{self._kind} must be within [0, 1]")
        object.__setattr__(self, "value", value)


@dataclass(frozen=True)
class EventProbability(_Probability):
    _kind: ClassVar[str] = "event probability"


@dataclass(frozen=True)
class TransmissionProbability(_Probability):
    _kind: ClassVar[str] = "transmission probability"


@dataclass(frozen=True)
class ScenarioProbability(_Probability):
    _kind: ClassVar[str] = "scenario probability"


@dataclass(frozen=True)
class ExpertWeight(_Probability):
    _kind: ClassVar[str] = "expert weight"


@dataclass(frozen=True)
class QuantileForecast:
    """A marginal quantile representation; it is neither a full CDF nor a path model."""

    pairs: tuple[tuple[float, float], ...]
    has_full_cdf: bool = False
    has_joint_paths: bool = False

    @classmethod
    def from_pairs(cls, pairs: tuple[tuple[float, float], ...]) -> "QuantileForecast":
        normalized: list[tuple[float, float]] = []
        for index, pair in enumerate(pairs):
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise ContractError(f"quantile pair {index} must contain probability and value")
            probability = _finite_number(pair[0], f"quantile probability {index}")
            value = _finite_number(pair[1], f"quantile value {index}")
            if not 0.0 < probability < 1.0:
                raise ContractError("quantile probabilities must be strictly inside (0, 1)")
            normalized.append((probability, value))
        if len(normalized) < 2:
            raise ContractError("at least two quantiles are required")
        if any(left[0] >= right[0] or left[1] > right[1]
               for left, right in zip(normalized, normalized[1:])):
            raise ContractError("quantile probabilities and values must be strictly/weakly ordered")
        return cls(tuple(normalized))


@dataclass(frozen=True)
class StudentTSpec:
    degrees_of_freedom: float
    location: float
    scale: float

    def __post_init__(self) -> None:
        degrees = _finite_number(self.degrees_of_freedom, "degrees_of_freedom")
        location = _finite_number(self.location, "location")
        scale = _finite_number(self.scale, "scale")
        if degrees <= 0.0:
            raise ContractError("degrees_of_freedom must be positive")
        if scale <= 0.0:
            raise ContractError("scale must be positive")
        object.__setattr__(self, "degrees_of_freedom", degrees)
        object.__setattr__(self, "location", location)
        object.__setattr__(self, "scale", scale)

    def require_finite_variance(self) -> None:
        self.require_finite_moment(2, consumer="variance")

    def require_finite_moment(self, order: int, *, consumer: str) -> None:
        if isinstance(order, bool) or not isinstance(order, int) or order <= 0:
            raise ContractError("moment order must be a positive integer")
        if not consumer:
            raise ContractError("moment consumer identity is required")
        if self.degrees_of_freedom <= order:
            raise ContractError(
                f"{consumer} requires finite moment order {order}; "
                f"Student-t degrees_of_freedom must exceed {order}"
            )


@dataclass(frozen=True)
class CapabilityManifest:
    """A minimal static claim set; runtime integration checks belong to later tickets."""

    model_id: str
    model_revision: str
    artifact_sha256: str | None
    output_kind: str
    supports_joint_paths: bool

    def __post_init__(self) -> None:
        if not self.model_id or not self.model_revision:
            raise ContractError("model_id and model_revision are required")
        if self.output_kind not in {"point", "quantiles", "cdf", "samples"}:
            raise ContractError("output_kind is unsupported")
        if self.supports_joint_paths and self.output_kind != "samples":
            raise ContractError("joint-path support requires declared sample output")
