from __future__ import annotations
from dataclasses import dataclass
import math

class UncertaintyError(ValueError): pass

@dataclass(frozen=True)
class Interval:
    lower: float
    upper: float
    kind: str
    def __post_init__(self) -> None:
        if self.kind not in {"PREDICTIVE_OUTCOME", "PARAMETER", "MONTE_CARLO_ERROR"}: raise UncertaintyError("unsupported interval kind")
        if not math.isfinite(self.lower) or not math.isfinite(self.upper) or self.lower > self.upper: raise UncertaintyError("invalid interval bounds")
    @property
    def is_predictive_outcome(self) -> bool: return self.kind == "PREDICTIVE_OUTCOME"
    def as_predictive_outcome(self) -> "Interval":
        if not self.is_predictive_outcome: raise UncertaintyError("parameter or Monte Carlo interval is not predictive outcome uncertainty")
        return self
