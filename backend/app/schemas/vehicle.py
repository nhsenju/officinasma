from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VehicleBase(BaseModel):
    license_plate: str
    brand: str
    model: str
    year: int
    color: str
    vin: Optional[str] = None
    engine_size: Optional[str] = None
    fuel_type: Optional[str] = None
    customer_id: int

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    vin: Optional[str] = None
    engine_size: Optional[str] = None
    fuel_type: Optional[str] = None

class VehicleInDB(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Vehicle(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
