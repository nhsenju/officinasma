from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from datetime import datetime

class VehicleService:
    def __init__(self, db: Session):
        self.db = db

    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_vehicles(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        return self.db.query(Vehicle).offset(skip).limit(limit).all()

    def get_vehicle_by_license_plate(self, license_plate: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()

    def get_vehicles_by_customer(self, customer_id: int) -> List[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.customer_id == customer_id).all()

    def create_vehicle(self, vehicle: VehicleCreate) -> Vehicle:
        db_vehicle = Vehicle(
            license_plate=vehicle.license_plate,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            color=vehicle.color,
            vin=vehicle.vin,
            engine_size=vehicle.engine_size,
            fuel_type=vehicle.fuel_type,
            customer_id=vehicle.customer_id
        )
        self.db.add(db_vehicle)
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdate) -> Optional[Vehicle]:
        db_vehicle = self.get_vehicle(vehicle_id)
        if not db_vehicle:
            return None
        
        update_data = vehicle.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)
        
        db_vehicle.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_vehicle)
        return db_vehicle

    def delete_vehicle(self, vehicle_id: int) -> bool:
        db_vehicle = self.get_vehicle(vehicle_id)
        if not db_vehicle:
            return False
        
        self.db.delete(db_vehicle)
        self.db.commit()
        return True

    def search_vehicles(self, query: str) -> List[Vehicle]:
        return self.db.query(Vehicle).filter(
            Vehicle.license_plate.ilike(f"%{query}%") |
            Vehicle.brand.ilike(f"%{query}%") |
            Vehicle.model.ilike(f"%{query}%") |
            Vehicle.vin.ilike(f"%{query}%")
        ).all()
