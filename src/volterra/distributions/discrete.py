from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class DiscreteDistribution:
    atoms: tuple[tuple[float, float], ...]
    def __post_init__(self) -> None:
        if not self.atoms or any(not math.isfinite(x) or not math.isfinite(p) or p < 0 for x,p in self.atoms):
            raise ValueError("atoms require finite values and nonnegative mass")
        if abs(sum(p for _,p in self.atoms)-1.0)>1e-12: raise ValueError("atom mass must sum to one")
    def cdf(self, value: float) -> float: return sum(p for x,p in self.atoms if x <= value)
    def quantile(self, probability: float) -> float:
        total=0.0
        for x,p in sorted(self.atoms):
            total += p
            if total >= probability: return x
        return max(x for x,_ in self.atoms)
    def crps(self, observation: float) -> float:
        first=sum(p*abs(x-observation) for x,p in self.atoms)
        second=sum(p*q*abs(x-y) for x,p in self.atoms for y,q in self.atoms)
        return first-0.5*second

def cdf_mixture(parts: tuple[tuple[float, DiscreteDistribution], ...]) -> DiscreteDistribution:
    atoms=[]
    for weight, dist in parts:
        atoms.extend((x,weight*p) for x,p in dist.atoms)
    merged={}
    for x,p in atoms: merged[x]=merged.get(x,0.0)+p
    return DiscreteDistribution(tuple(merged.items()))

def weighted_quantile_average(parts: tuple[tuple[float, DiscreteDistribution], ...], probability: float) -> float:
    return sum(weight*dist.quantile(probability) for weight,dist in parts)
