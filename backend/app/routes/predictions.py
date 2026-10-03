from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..ml.predict import predict_overflow_risk
import datetime

router = APIRouter()

@router.get("/predictions")
def get_all_predictions():
    return {"message": "Use /predictions/bin/{id} to predict for a specific bin"}

@router.post("/predictions/bin/{id}")
def predict_bin_risk(id: int, db: Session = Depends(get_db)):
    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == id).first()
    if not db_bin:
        raise HTTPException(status_code=404, detail="Bin not found")
    
    fill_percentage = db_bin.current_fill_percentage
    
    collections = db.query(models.CollectionRecord).filter(models.CollectionRecord.bin_id == id).all()
    if collections:
        avg_delay = sum(c.delay_minutes for c in collections) / len(collections)
    else:
        avg_delay = 0

    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    missed_count = db.query(models.CollectionRecord).filter(
        models.CollectionRecord.bin_id == id,
        models.CollectionRecord.status == models.CollectionStatus.MISSED,
        models.CollectionRecord.scheduled_date >= seven_days_ago
    ).count()

    complaints_count = db.query(models.Complaint).filter(
        models.Complaint.bin_id == id,
        models.Complaint.reported_at >= seven_days_ago
    ).count()

    freq = db_bin.collection_frequency_days
    fill_growth_per_day = fill_percentage / (freq if freq > 0 else 1)

    features = [
        fill_percentage,
        fill_growth_per_day,
        avg_delay,
        missed_count,
        complaints_count,
        freq
    ]

    try:
        probability, risk_level = predict_overflow_risk(features)
        
        if risk_level in ["HIGH", "CRITICAL"]:
            db_bin.status = models.BinStatus.OVERFLOW_RISK
            db.commit()

        return {
            "bin_id": id,
            "risk_level": risk_level,
            "risk_probability": probability
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
