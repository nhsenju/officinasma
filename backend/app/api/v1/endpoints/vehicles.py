from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from app.services.vehicle_service import VehicleService

router = APIRouter()

@router.get("/", response_model=List[Vehicle])
def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    customer_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all vehicles with optional filters"""
    service = VehicleService(db)
    if customer_id:
        return service.get_vehicles_by_customer(customer_id)
    if search:
        return service.search_vehicles(search)
    return service.get_vehicles(skip=skip, limit=limit)

@router.post("/", response_model=Vehicle)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    """Create a new vehicle"""
    service = VehicleService(db)
    return service.create_vehicle(vehicle)

@router.get("/{vehicle_id}", response_model=Vehicle)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific vehicle by ID"""
    service = VehicleService(db)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=Vehicle)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """Update a vehicle"""
    service = VehicleService(db)
    updated_vehicle = service.update_vehicle(vehicle_id, vehicle)
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Delete a vehicle"""
    service = VehicleService(db)
    success = service.delete_vehicle(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted successfully"}

@router.get("/license-plate/{license_plate}", response_model=Vehicle)
def get_vehicle_by_license_plate(
    license_plate: str,
    db: Session = Depends(get_db)
):
    """Get a vehicle by license plate"""
    service = VehicleService(db)
    vehicle = service.get_vehicle_by_license_plate(license_plate)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
