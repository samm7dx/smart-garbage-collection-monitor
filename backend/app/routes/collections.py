from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import datetime

router = APIRouter()

@router.get("/collections", response_model=list[schemas.Collection])
def get_collections(db: Session = Depends(get_db)):
    return db.query(models.CollectionRecord).all()

@router.get("/collections/{id}", response_model=schemas.Collection)
def get_collection(id: int, db: Session = Depends(get_db)):
    record = db.query(models.CollectionRecord).filter(models.CollectionRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Collection not found")
    return record

@router.post("/collections", response_model=schemas.Collection)
def create_collection(collection: schemas.CollectionCreate, db: Session = Depends(get_db)):
    db_record = models.CollectionRecord(**collection.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.put("/collections/{id}")
def update_collection(id: int, data: schemas.CollectionUpdate, db: Session = Depends(get_db)):
    record = db.query(models.CollectionRecord).filter(models.CollectionRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Collection not found")

    if data.actual_collection_date and data.actual_collection_time:
        record.actual_collection_date = data.actual_collection_date
        record.actual_collection_time = data.actual_collection_time
        
        try:
            sch_datetime = datetime.datetime.combine(record.scheduled_date.date(), datetime.datetime.strptime(record.scheduled_time, "%H:%M").time())
            act_datetime = datetime.datetime.combine(record.actual_collection_date.date(), datetime.datetime.strptime(record.actual_collection_time, "%H:%M").time())
            
            delay_minutes = int((act_datetime - sch_datetime).total_seconds() / 60)
            record.delay_minutes = delay_minutes

            bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == record.bin_id).first()
            if delay_minutes <= 30:
                record.status = models.CollectionStatus.ON_TIME
                if bin:
                    bin.status = models.BinStatus.NORMAL
                    bin.current_fill_percentage = 0.0
            else:
                record.status = models.CollectionStatus.DELAYED
                if bin:
                    bin.status = models.BinStatus.DELAYED
                    bin.current_fill_percentage = 0.0
        except Exception as e:
            pass

    db.commit()
    db.refresh(record)
    return record
