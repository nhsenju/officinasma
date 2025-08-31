from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db, AppointmentStatus
from app.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate
from app.services.appointment_service import AppointmentService

router = APIRouter()

@router.get("/", response_model=List[Appointment])
def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[int] = Query(None),
    status: Optional[AppointmentStatus] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all appointments with optional filters"""
    service = AppointmentService(db)
    appointments = service.get_appointments(skip=skip, limit=limit)
    
    # Apply filters
    if customer_id:
        appointments = [a for a in appointments if a.customer_id == customer_id]
    if status:
        appointments = [a for a in appointments if a.status == status]
    if date_from:
        appointments = [a for a in appointments if a.appointment_date.date() >= date_from]
    if date_to:
        appointments = [a for a in appointments if a.appointment_date.date() <= date_to]
    
    return appointments

@router.post("/", response_model=Appointment)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new appointment"""
    service = AppointmentService(db)
    
    # Check availability
    if not service.check_availability(appointment.appointment_date, appointment.estimated_duration):
        raise HTTPException(status_code=400, detail="Time slot not available")
    
    return service.create_appointment(appointment)

@router.get("/{appointment_id}", response_model=Appointment)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific appointment by ID"""
    service = AppointmentService(db)
    appointment = service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=Appointment)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Update an appointment"""
    service = AppointmentService(db)
    updated_appointment = service.update_appointment(appointment_id, appointment)
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated_appointment

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """Delete an appointment"""
    service = AppointmentService(db)
    success = service.delete_appointment(appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

@router.put("/{appointment_id}/status", response_model=Appointment)
def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    db: Session = Depends(get_db)
):
    """Update appointment status"""
    service = AppointmentService(db)
    updated_appointment = service.update_appointment_status(appointment_id, status)
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated_appointment

@router.get("/upcoming/", response_model=List[Appointment])
def get_upcoming_appointments(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get upcoming appointments"""
    service = AppointmentService(db)
    return service.get_upcoming_appointments(days)

@router.get("/date/{appointment_date}", response_model=List[Appointment])
def get_appointments_by_date(
    appointment_date: date,
    db: Session = Depends(get_db)
):
    """Get appointments for a specific date"""
    service = AppointmentService(db)
    datetime_obj = datetime.combine(appointment_date, datetime.min.time())
    return service.get_appointments_by_date(datetime_obj)

@router.get("/customer/{customer_id}", response_model=List[Appointment])
def get_appointments_by_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Get appointments for a specific customer"""
    service = AppointmentService(db)
    return service.get_appointments_by_customer(customer_id)
