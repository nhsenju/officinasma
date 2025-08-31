from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CheckInBase(BaseModel):
    vehicle_id: int
    checkin_time: datetime
    checkout_time: Optional[datetime] = None
    notes: Optional[str] = None
    is_automatic: bool = False

class CheckInCreate(CheckInBase):
    pass

class CheckInUpdate(BaseModel):
    checkout_time: Optional[datetime] = None
    notes: Optional[str] = None

class CheckInInDB(CheckInBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CheckIn(CheckInBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
