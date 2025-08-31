from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Service
from app.schemas.service import ServiceCreate, ServiceUpdate
from datetime import datetime

class ServiceService:
    def __init__(self, db: Session):
        self.db = db

    def get_service(self, service_id: int) -> Optional[Service]:
        return self.db.query(Service).filter(Service.id == service_id).first()

    def get_services(self, skip: int = 0, limit: int = 100) -> List[Service]:
        return self.db.query(Service).offset(skip).limit(limit).all()

    def get_services_by_category(self, category: str) -> List[Service]:
        return self.db.query(Service).filter(Service.category == category).all()

    def create_service(self, service: ServiceCreate) -> Service:
        db_service = Service(
            name=service.name,
            description=service.description,
            price=service.price,
            duration_minutes=service.duration_minutes,
            category=service.category
        )
        self.db.add(db_service)
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def update_service(self, service_id: int, service: ServiceUpdate) -> Optional[Service]:
        db_service = self.get_service(service_id)
        if not db_service:
            return None
        
        update_data = service.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_service, field, value)
        
        db_service.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def delete_service(self, service_id: int) -> bool:
        db_service = self.get_service(service_id)
        if not db_service:
            return False
        
        self.db.delete(db_service)
        self.db.commit()
        return True

    def search_services(self, query: str) -> List[Service]:
        return self.db.query(Service).filter(
            Service.name.ilike(f"%{query}%") |
            Service.description.ilike(f"%{query}%") |
            Service.category.ilike(f"%{query}%")
        ).all()
