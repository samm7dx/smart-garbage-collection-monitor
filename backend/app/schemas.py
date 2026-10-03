from pydantic import BaseModel
from typing import Optional, List
import datetime

# Bin schemas
class BinBase(BaseModel):
    name: str
    area: str
    latitude: float
    longitude: float
    capacity: float
    current_fill_percentage: float
    collection_frequency_days: int
    scheduled_collection_time: str
    status: str = "NORMAL"

class BinCreate(BinBase):
    pass

class BinUpdate(BaseModel):
    current_fill_percentage: Optional[float] = None
    status: Optional[str] = None

class Bin(BinBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Collection schemas
class CollectionBase(BaseModel):
    bin_id: int
    scheduled_date: datetime.datetime
    scheduled_time: str
    
class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    actual_collection_date: Optional[datetime.datetime] = None
    actual_collection_time: Optional[str] = None

class Collection(CollectionBase):
    id: int
    actual_collection_date: Optional[datetime.datetime] = None
    actual_collection_time: Optional[str] = None
    delay_minutes: int
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Complaint schemas
class ComplaintBase(BaseModel):
    bin_id: int
    area: str
    description: str

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: str

class Complaint(ComplaintBase):
    id: int
    reported_at: datetime.datetime
    status: str

    class Config:
        from_attributes = True
