from __future__ import annotations
from dataclasses import dataclass
class OptionsResearchError(ValueError):pass
@dataclass(frozen=True)
class StraddleContract:
 strike:float;multiplier:float;premium_per_leg:float
 def __post_init__(self):
  if self.strike<=0 or self.multiplier<=0 or self.premium_per_leg<0:raise OptionsResearchError('invalid read-only contract')
def straddle_payoff(contract:StraddleContract,settlement:float)->float:
 if settlement<0:raise OptionsResearchError('invalid settlement')
 return (abs(settlement-contract.strike)-2*contract.premium_per_leg)*contract.multiplier
@dataclass(frozen=True)
class QuoteAssessment:
 quote:float|None
 @property
 def status(self):return 'NOT_ASSESSED' if self.quote is None else 'OBSERVED_QUOTE'
