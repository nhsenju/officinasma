from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db
from app.schemas.checkin import CheckIn, CheckInCreate, CheckInUpdate
from app.services.checkin_service import CheckInService

router = APIRouter()

@router.get("/", response_model=List[CheckIn])
def get_checkins(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vehicle_id: Optional[int] = Query(None),
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get all check-ins with optional filters"""
    service = CheckInService(db)
    if active_only:
        return service.get_vehicles_in_workshop()
    if vehicle_id:
        return service.get_checkins_by_vehicle(vehicle_id)
    return service.get_checkins(skip=skip, limit=limit)

@router.post("/", response_model=CheckIn)
def create_checkin(
    checkin: CheckInCreate,
    db: Session = Depends(get_db)
):
    """Create a new check-in"""
    service = CheckInService(db)
    return service.create_checkin(checkin)

@router.get("/{checkin_id}", response_model=CheckIn)
def get_checkin(
    checkin_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific check-in by ID"""
    service = CheckInService(db)
    checkin = service.get_checkin(checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return checkin

@router.put("/{checkin_id}", response_model=CheckIn)
def update_checkin(
    checkin_id: int,
    checkin: CheckInUpdate,
    db: Session = Depends(get_db)
):
    """Update a check-in"""
    service = CheckInService(db)
    updated_checkin = service.update_checkin(checkin_id, checkin)
    if not updated_checkin:
        raise HTTPException(status_code=404, detail="Check-in not found")
    return updated_checkin

@router.post("/checkout/{vehicle_id}", response_model=CheckIn)
def checkout_vehicle(
    vehicle_id: int,
    checkout_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Check-out a vehicle"""
    service = CheckInService(db)
    checkout = service.checkout_vehicle(vehicle_id, checkout_time)
    if not checkout:
        raise HTTPException(status_code=404, detail="No active check-in found for this vehicle")
    return checkout

@router.get("/active/", response_model=List[CheckIn])
def get_active_checkins(db: Session = Depends(get_db)):
    """Get all active check-ins (vehicles currently in workshop)"""
    service = CheckInService(db)
    return service.get_vehicles_in_workshop()

@router.get("/statistics/")
def get_checkin_statistics(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get check-in statistics for a date range"""
    service = CheckInService(db)
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    return service.get_checkin_statistics(start_datetime, end_datetime)
