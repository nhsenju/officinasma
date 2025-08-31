from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class InvoiceBase(BaseModel):
    customer_id: int
    appointment_id: int
    total_amount: float
    tax_amount: float
    status: InvoiceStatus = InvoiceStatus.DRAFT
    due_date: datetime
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    status: Optional[InvoiceStatus] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None

class InvoiceInDB(InvoiceBase):
    id: int
    invoice_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Invoice(InvoiceBase):
    id: int
    invoice_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
