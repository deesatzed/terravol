"""Exact, assumption-explicit cascade reference arithmetic."""

from volterra.cascades.reference import (
    ExclusiveBranchTable, background_probability, coincident_any_probability, complete_set_probability, conditional_both_or_either, exclusive_any_probability, independent_any_probability, joint_probability_bounds,
    shared_downstream_probability,
    unique_source_probabilities,
)

__all__ = ["ExclusiveBranchTable", "background_probability", "coincident_any_probability", "complete_set_probability", "conditional_both_or_either", "exclusive_any_probability", "independent_any_probability", "joint_probability_bounds", "shared_downstream_probability", "unique_source_probabilities"]
def retain_failed_branch_mass(branch_mass:float,*,background:float)->dict[str,float]:
    if branch_mass<0 or background<0 or abs(branch_mass+background-1)>1e-12: raise ValueError("mass must form a partition")
    return {"failed_branch":branch_mass,"background":background}
