from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AIDetectionBase(BaseModel):
    license_plate: str
    confidence: float
    image_path: Optional[str] = None
    processed: bool = False
    vehicle_id: Optional[int] = None

class AIDetectionCreate(AIDetectionBase):
    pass

class AIDetectionUpdate(BaseModel):
    processed: Optional[bool] = None
    vehicle_id: Optional[int] = None

class AIDetectionInDB(AIDetectionBase):
    id: int
    detected_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AIDetection(AIDetectionBase):
    id: int
    detected_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
