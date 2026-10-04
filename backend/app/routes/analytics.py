from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..status_utils import refresh_collection_record, get_bin_status_from_latest_collection

router = APIRouter()

@router.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    total_bins = db.query(models.GarbageBin).count()

    collections = db.query(models.CollectionRecord).all()
    bins = db.query(models.GarbageBin).all()
    latest_by_bin: dict[int, models.CollectionRecord] = {}
    changed = False

    on_time = 0
    delayed = 0
    missed = 0
    for record in collections:
        if refresh_collection_record(record):
            changed = True
        if record.status == models.CollectionStatus.ON_TIME:
            on_time += 1
        elif record.status == models.CollectionStatus.DELAYED:
            delayed += 1
        elif record.status == models.CollectionStatus.MISSED:
            missed += 1

        current = latest_by_bin.get(record.bin_id)
        if current is None or record.scheduled_date > current.scheduled_date:
            latest_by_bin[record.bin_id] = record

    high_risk = 0
    for db_bin in bins:
        status = get_bin_status_from_latest_collection(db_bin, latest_by_bin.get(db_bin.id))
        if db_bin.status != status:
            db_bin.status = status
            changed = True
        if status == models.BinStatus.OVERFLOW_RISK:
            high_risk += 1

    open_complaints = db.query(models.Complaint).filter(models.Complaint.status == models.ComplaintStatus.OPEN).count()

    if changed:
        db.commit()

    return {
        "total_bins": total_bins,
        "on_time_collections": on_time,
        "delayed_collections": delayed,
        "missed_collections": missed,
        "high_risk_bins": high_risk,
        "open_complaints": open_complaints
    }
