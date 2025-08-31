from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from datetime import datetime

class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email).first()

    def create_customer(self, customer: CustomerCreate) -> Customer:
        db_customer = Customer(
            full_name=customer.full_name,
            email=customer.email,
            phone=customer.phone,
            address=customer.address,
            notes=customer.notes
        )
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def update_customer(self, customer_id: int, customer: CustomerUpdate) -> Optional[Customer]:
        db_customer = self.get_customer(customer_id)
        if not db_customer:
            return None
        
        update_data = customer.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        db_customer.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def delete_customer(self, customer_id: int) -> bool:
        db_customer = self.get_customer(customer_id)
        if not db_customer:
            return False
        
        self.db.delete(db_customer)
        self.db.commit()
        return True

    def search_customers(self, query: str) -> List[Customer]:
        return self.db.query(Customer).filter(
            Customer.full_name.ilike(f"%{query}%") |
            Customer.email.ilike(f"%{query}%") |
            Customer.phone.ilike(f"%{query}%")
        ).all()
