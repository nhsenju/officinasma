from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from datetime import datetime, timedelta

class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_appointments(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        return self.db.query(Appointment).offset(skip).limit(limit).all()

    def get_appointments_by_customer(self, customer_id: int) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.customer_id == customer_id).all()

    def get_appointments_by_vehicle(self, vehicle_id: int) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.vehicle_id == vehicle_id).all()

    def get_appointments_by_date(self, date: datetime) -> List[Appointment]:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return self.db.query(Appointment).filter(
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date < end_date
        ).all()

    def get_upcoming_appointments(self, days: int = 7) -> List[Appointment]:
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=days)
        return self.db.query(Appointment).filter(
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date <= end_date,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED])
        ).order_by(Appointment.appointment_date).all()

    def create_appointment(self, appointment: AppointmentCreate) -> Appointment:
        db_appointment = Appointment(
            customer_id=appointment.customer_id,
            vehicle_id=appointment.vehicle_id,
            service_id=appointment.service_id,
            appointment_date=appointment.appointment_date,
            estimated_duration=appointment.estimated_duration,
            notes=appointment.notes,
            status=appointment.status
        )
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def update_appointment(self, appointment_id: int, appointment: AppointmentUpdate) -> Optional[Appointment]:
        db_appointment = self.get_appointment(appointment_id)
        if not db_appointment:
            return None
        
        update_data = appointment.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_appointment, field, value)
        
        db_appointment.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def delete_appointment(self, appointment_id: int) -> bool:
        db_appointment = self.get_appointment(appointment_id)
        if not db_appointment:
            return False
        
        self.db.delete(db_appointment)
        self.db.commit()
        return True

    def update_appointment_status(self, appointment_id: int, status: AppointmentStatus) -> Optional[Appointment]:
        db_appointment = self.get_appointment(appointment_id)
        if not db_appointment:
            return None
        
        db_appointment.status = status
        db_appointment.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def check_availability(self, appointment_date: datetime, duration: int) -> bool:
        end_time = appointment_date + timedelta(minutes=duration)
        
        conflicting_appointments = self.db.query(Appointment).filter(
            Appointment.appointment_date < end_time,
            Appointment.appointment_date + timedelta(minutes=Appointment.estimated_duration) > appointment_date,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS])
        ).count()
        
        return conflicting_appointments == 0
