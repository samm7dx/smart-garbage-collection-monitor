from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from ..database import get_db

router = APIRouter()

@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    total_bins = db.query(models.GarbageBin).count()
    on_time = db.query(models.CollectionRecord).filter(models.CollectionRecord.status == models.CollectionStatus.ON_TIME).count()
    delayed = db.query(models.CollectionRecord).filter(models.CollectionRecord.status == models.CollectionStatus.DELAYED).count()
    missed = db.query(models.CollectionRecord).filter(models.CollectionRecord.status == models.CollectionStatus.MISSED).count()
    high_risk = db.query(models.GarbageBin).filter(models.GarbageBin.status == models.BinStatus.OVERFLOW_RISK).count()
    open_complaints = db.query(models.Complaint).filter(models.Complaint.status == models.ComplaintStatus.OPEN).count()

    return {
        "total_bins": total_bins,
        "on_time_collections": on_time,
        "delayed_collections": delayed,
        "missed_collections": missed,
        "high_risk_bins": high_risk,
        "open_complaints": open_complaints
    }
