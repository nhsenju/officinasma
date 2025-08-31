from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import CheckIn
from app.schemas.checkin import CheckInCreate, CheckInUpdate
from datetime import datetime

class CheckInService:
    def __init__(self, db: Session):
        self.db = db

    def get_checkin(self, checkin_id: int) -> Optional[CheckIn]:
        return self.db.query(CheckIn).filter(CheckIn.id == checkin_id).first()

    def get_checkins(self, skip: int = 0, limit: int = 100) -> List[CheckIn]:
        return self.db.query(CheckIn).offset(skip).limit(limit).all()

    def get_checkins_by_vehicle(self, vehicle_id: int) -> List[CheckIn]:
        return self.db.query(CheckIn).filter(CheckIn.vehicle_id == vehicle_id).all()

    def get_active_checkin(self, vehicle_id: int) -> Optional[CheckIn]:
        return self.db.query(CheckIn).filter(
            CheckIn.vehicle_id == vehicle_id,
            CheckIn.checkout_time.is_(None)
        ).first()

    def create_checkin(self, checkin: CheckInCreate) -> CheckIn:
        db_checkin = CheckIn(
            vehicle_id=checkin.vehicle_id,
            checkin_time=checkin.checkin_time,
            checkout_time=checkin.checkout_time,
            notes=checkin.notes,
            is_automatic=checkin.is_automatic
        )
        self.db.add(db_checkin)
        self.db.commit()
        self.db.refresh(db_checkin)
        return db_checkin

    def update_checkin(self, checkin_id: int, checkin: CheckInUpdate) -> Optional[CheckIn]:
        db_checkin = self.get_checkin(checkin_id)
        if not db_checkin:
            return None
        
        update_data = checkin.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_checkin, field, value)
        
        db_checkin.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_checkin)
        return db_checkin

    def checkout_vehicle(self, vehicle_id: int, checkout_time: datetime = None) -> Optional[CheckIn]:
        active_checkin = self.get_active_checkin(vehicle_id)
        if not active_checkin:
            return None
        
        active_checkin.checkout_time = checkout_time or datetime.utcnow()
        active_checkin.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(active_checkin)
        return active_checkin

    def get_vehicles_in_workshop(self) -> List[CheckIn]:
        return self.db.query(CheckIn).filter(CheckIn.checkout_time.is_(None)).all()

    def get_checkin_statistics(self, start_date: datetime, end_date: datetime) -> dict:
        checkins = self.db.query(CheckIn).filter(
            CheckIn.checkin_time >= start_date,
            CheckIn.checkin_time <= end_date
        ).all()
        
        total_checkins = len(checkins)
        total_duration = sum([
            (c.checkout_time - c.checkin_time).total_seconds() / 3600 
            for c in checkins if c.checkout_time
        ])
        
        return {
            "total_checkins": total_checkins,
            "total_hours": round(total_duration, 2),
            "average_duration": round(total_duration / total_checkins, 2) if total_checkins > 0 else 0
        }
