from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/complaints", response_model=list[schemas.Complaint])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(models.Complaint).all()

@router.post("/complaints", response_model=schemas.Complaint)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    db_complaint = models.Complaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.put("/complaints/{id}", response_model=schemas.Complaint)
def update_complaint(id: int, complaint: schemas.ComplaintUpdate, db: Session = Depends(get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.id == id).first()
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    db_complaint.status = complaint.status
    db.commit()
    db.refresh(db_complaint)
    return db_complaint
