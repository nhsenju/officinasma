from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, time
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentBase(BaseModel):
    customer_id: int
    vehicle_id: int
    service_id: int
    appointment_date: datetime
    start_time: time
    end_time: time
    estimated_duration: int
    notes: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    customer_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    service_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    estimated_duration: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[AppointmentStatus] = None

class AppointmentInDB(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Appointment(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
