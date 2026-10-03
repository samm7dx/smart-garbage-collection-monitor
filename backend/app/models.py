from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum
import datetime
from .database import Base

class BinStatus(str, enum.Enum):
    NORMAL = "NORMAL"
    DELAYED = "DELAYED"
    MISSED = "MISSED"
    OVERFLOW_RISK = "OVERFLOW_RISK"

class CollectionStatus(str, enum.Enum):
    ON_TIME = "ON_TIME"
    DELAYED = "DELAYED"
    MISSED = "MISSED"

class ComplaintStatus(str, enum.Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"

class GarbageBin(Base):
    __tablename__ = "garbage_bins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    area = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Float)
    current_fill_percentage = Column(Float, default=0.0)
    collection_frequency_days = Column(Integer, default=1)
    scheduled_collection_time = Column(String) 
    status = Column(String, default=BinStatus.NORMAL)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    collections = relationship("CollectionRecord", back_populates="bin")
    complaints = relationship("Complaint", back_populates="bin")


class CollectionRecord(Base):
    __tablename__ = "collection_records"

    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, ForeignKey("garbage_bins.id"))
    scheduled_date = Column(DateTime)
    scheduled_time = Column(String)
    actual_collection_date = Column(DateTime, nullable=True)
    actual_collection_time = Column(String, nullable=True)
    delay_minutes = Column(Integer, default=0)
    status = Column(String, default=CollectionStatus.ON_TIME)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    bin = relationship("GarbageBin", back_populates="collections")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    bin_id = Column(Integer, ForeignKey("garbage_bins.id"))
    area = Column(String)
    description = Column(String)
    reported_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default=ComplaintStatus.OPEN)
    
    bin = relationship("GarbageBin", back_populates="complaints")
