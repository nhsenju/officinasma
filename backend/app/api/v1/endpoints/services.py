from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.service import Service, ServiceCreate, ServiceUpdate
from app.services.service_service import ServiceService

router = APIRouter()

@router.get("/", response_model=List[Service])
def get_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all services with optional filters"""
    service = ServiceService(db)
    if category:
        return service.get_services_by_category(category)
    if search:
        return service.search_services(search)
    return service.get_services(skip=skip, limit=limit)

@router.post("/", response_model=Service)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    """Create a new service"""
    service_obj = ServiceService(db)
    return service_obj.create_service(service)

@router.get("/{service_id}", response_model=Service)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific service by ID"""
    service = ServiceService(db)
    service_obj = service.get_service(service_id)
    if not service_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_obj

@router.put("/{service_id}", response_model=Service)
def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db)
):
    """Update a service"""
    service_obj = ServiceService(db)
    updated_service = service_obj.update_service(service_id, service)
    if not updated_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return updated_service

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """Delete a service"""
    service = ServiceService(db)
    success = service.delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

@router.get("/categories/", response_model=List[str])
def get_service_categories(db: Session = Depends(get_db)):
    """Get all service categories"""
    service = ServiceService(db)
    services = service.get_services()
    categories = list(set(s.category for s in services))
    return sorted(categories)
