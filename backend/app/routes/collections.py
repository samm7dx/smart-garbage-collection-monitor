from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import datetime
from ..status_utils import refresh_collection_record, get_bin_status_from_latest_collection, utcnow_naive

router = APIRouter()

@router.get("/collections", response_model=list[schemas.Collection])
def get_collections(db: Session = Depends(get_db)):
    records = db.query(models.CollectionRecord).all()
    changed = any(refresh_collection_record(record) for record in records)
    if changed:
        db.commit()
    return records

@router.get("/collections/{id}", response_model=schemas.Collection)
def get_collection(id: int, db: Session = Depends(get_db)):
    record = db.query(models.CollectionRecord).filter(models.CollectionRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Collection not found")
    return record

@router.post("/collections", response_model=schemas.Collection)
def create_collection(collection: schemas.CollectionCreate, db: Session = Depends(get_db)):
    db_record = models.CollectionRecord(**collection.model_dump())
    refresh_collection_record(db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.put("/collections/{id}", response_model=schemas.Collection)
def update_collection(id: int, data: schemas.CollectionUpdate, db: Session = Depends(get_db)):
    record = db.query(models.CollectionRecord).filter(models.CollectionRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Collection not found")

    if data.actual_collection_date and data.actual_collection_time:
        record.actual_collection_date = data.actual_collection_date
        record.actual_collection_time = data.actual_collection_time

    refresh_collection_record(record)

    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == record.bin_id).first()
    if db_bin and data.actual_collection_date and data.actual_collection_time:
        db_bin.current_fill_percentage = 0.0
        db_bin.status = get_bin_status_from_latest_collection(db_bin, record)

    db.commit()
    db.refresh(record)
    return record


@router.post("/collections/record/{bin_id}", response_model=schemas.Collection)
def record_collection(bin_id: int, db: Session = Depends(get_db)):
    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == bin_id).first()
    if not db_bin:
        raise HTTPException(status_code=404, detail="Bin not found")

    record = (
        db.query(models.CollectionRecord)
        .filter(
            models.CollectionRecord.bin_id == bin_id,
            models.CollectionRecord.actual_collection_date.is_(None),
        )
        .order_by(models.CollectionRecord.scheduled_date.desc())
        .first()
    )

    if record is None:
        now = utcnow_naive()
        record = models.CollectionRecord(
            bin_id=bin_id,
            scheduled_date=now,
            scheduled_time=db_bin.scheduled_collection_time,
        )
        db.add(record)

    now = utcnow_naive()
    record.actual_collection_date = now
    record.actual_collection_time = now.strftime("%H:%M")
    refresh_collection_record(record, now=now)

    db_bin.current_fill_percentage = 0.0
    db_bin.status = get_bin_status_from_latest_collection(db_bin, record)

    db.commit()
    db.refresh(record)
    return record
