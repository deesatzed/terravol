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
def downstream_status(*,observed:bool,report_due:bool)->str:
    if observed:return "OBSERVED_RESPONSE"
    return "MISSING_REPORT" if report_due else "REPORTING_DELAY"
def interaction(kind:str,left:bool,right:bool)->bool:
    if kind=="AND":return left and right
    if kind=="INHIBIT":return left and not right
    if kind=="EXCLUSIVE":return left != right
    raise ValueError("declared interaction kind required")
def joint_artifact(*,episode:bool,variance_path:tuple[float,...]):
    if episode and not any(variance_path):raise ValueError("episode contradicts zero sampled variance path")
    return {"episode":episode,"variance_path":variance_path}
def preserved_mass(*,retained:float,remainder:float,no_event:float):
    total=retained+remainder+no_event
    if abs(total-1)>1e-12:raise ValueError("pruning must retain remainder and no-event mass")
    return total
