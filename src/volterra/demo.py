"""A fully local synthetic VT05 vertical slice."""
from datetime import datetime, timezone
from pathlib import Path
import tempfile
from volterra.baselines import EWMAVarianceBaseline, NormalVarianceOutcomeDistribution
from volterra.forecast_store import ForecastStore
from volterra.storage import EvidenceLedger, MeasurementSpec, TargetDefinition

def run_offline_slice() -> dict[str, object]:
    utc=timezone.utc
    at=lambda day: datetime(2026,3,day,tzinfo=utc)
    target=TargetDefinition("synthetic-demo-v1",1,"synthetic_variance",MeasurementSpec("variance",252,"SYNTHETIC","FULL","synthetic","none","UNSUPPORTED"))
    with tempfile.TemporaryDirectory(prefix="volterra-demo-") as directory:
        root=Path(directory); ledger=EvidenceLedger(root/"ledger.sqlite"); store=ForecastStore(root/"forecasts.sqlite")
        try:
            ledger.register_target(target); snapshot=ledger.create_snapshot("demo-origin",at(1),policy="live")
            mean=EWMAVarianceBaseline(decay=.5).forecast((.01,.09)).mean_variance
            distribution=NormalVarianceOutcomeDistribution.for_target(target,mean_variance=mean,residual_scale=.01)
            forecast_id=store.seal_normal_forecast(snapshot_id=snapshot.snapshot_id,origin_at=at(1),target=target,model_id="ewma_variance",distribution=distribution,synthetic=True)
            outcome_id=ledger.record_outcome(target_id=target.target_id,origin_at=at(1),completed_sessions=1,target_end_at=at(2),first_public_at=at(3),value=.06,synthetic=True)
            score=store.score_mature_outcome(forecast_id,ledger=ledger,outcome_id=outcome_id,as_of=at(3))
            return {"synthetic":True,"model_id":"ewma_variance","crps":score.crps,"external_calls":0}
        finally:
            store.close(); ledger.close()
