from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/bins", response_model=list[schemas.Bin])
def get_bins(db: Session = Depends(get_db)):
    return db.query(models.GarbageBin).all()

@router.get("/bins/{id}", response_model=schemas.Bin)
def get_bin(id: int, db: Session = Depends(get_db)):
    db_bin = db.query(models.GarbageBin).filter(models.GarbageBin.id == id).first()
    if not db_bin:
        raise HTTPException(status_code=404, detail="Bin not found")
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
