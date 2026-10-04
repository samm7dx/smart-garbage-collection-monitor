from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..status_utils import compute_collection_status, get_bin_status_from_latest_collection

router = APIRouter()

@router.get("/bins", response_model=list[schemas.Bin])
def get_bins(db: Session = Depends(get_db)):
    bins = db.query(models.GarbageBin).all()
    collections = db.query(models.CollectionRecord).all()
    latest_by_bin: dict[int, models.CollectionRecord] = {}

    for record in collections:
        status, delay_minutes = compute_collection_status(record)
        record.status = status
        record.delay_minutes = delay_minutes
        current = latest_by_bin.get(record.bin_id)
        if current is None or record.scheduled_date > current.scheduled_date:
            latest_by_bin[record.bin_id] = record

    for db_bin in bins:
        status = get_bin_status_from_latest_collection(db_bin, latest_by_bin.get(db_bin.id))
        db_bin.status = status
    return bins

@router.get("/bins/{id}", response_model=schemas.Bin)
def get_bin(id: int, db: Session = Depends(get_db)):
    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == id).first()
    if not db_bin:
        raise HTTPException(status_code=404, detail="Bin not found")
    collections = (
        db.query(models.CollectionRecord)
        .filter(models.CollectionRecord.bin_id == id)
        .order_by(models.CollectionRecord.scheduled_date.desc())
        .all()
    )
    for record in collections:
        status, delay_minutes = compute_collection_status(record)
        record.status = status
        record.delay_minutes = delay_minutes
    latest = collections[0] if collections else None
    status = get_bin_status_from_latest_collection(db_bin, latest)
    db_bin.status = status
    return db_bin

@router.post("/bins", response_model=schemas.Bin)
def create_bin(bin: schemas.BinCreate, db: Session = Depends(get_db)):
    db_bin = models.GarbageBin(**bin.model_dump())
    db.add(db_bin)
    db.commit()
    db.refresh(db_bin)
    return db_bin

@router.put("/bins/{id}", response_model=schemas.Bin)
def update_bin(id: int, bin: schemas.BinUpdate, db: Session = Depends(get_db)):
    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == id).first()
    if not db_bin:
        raise HTTPException(status_code=404, detail="Bin not found")
    update_data = bin.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bin, key, value)
    db.commit()
    db.refresh(db_bin)
    return db_bin
