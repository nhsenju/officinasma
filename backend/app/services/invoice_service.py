from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Invoice, InvoiceStatus
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from datetime import datetime
import uuid

class InvoiceService:
    def __init__(self, db: Session):
        self.db = db

    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()

    def get_invoices(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).offset(skip).limit(limit).all()

    def get_invoices_by_customer(self, customer_id: int) -> List[Invoice]:
        return self.db.query(Invoice).filter(Invoice.customer_id == customer_id).all()

    def get_invoices_by_status(self, status: InvoiceStatus) -> List[Invoice]:
        return self.db.query(Invoice).filter(Invoice.status == status).all()

    def create_invoice(self, invoice: InvoiceCreate) -> Invoice:
        # Generate unique invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}"
        
        db_invoice = Invoice(
            invoice_number=invoice_number,
            customer_id=invoice.customer_id,
            appointment_id=invoice.appointment_id,
            total_amount=invoice.total_amount,
            tax_amount=invoice.tax_amount,
            status=invoice.status,
            due_date=invoice.due_date,
            notes=invoice.notes
        )
        self.db.add(db_invoice)
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def update_invoice(self, invoice_id: int, invoice: InvoiceUpdate) -> Optional[Invoice]:
        db_invoice = self.get_invoice(invoice_id)
        if not db_invoice:
            return None
        
        update_data = invoice.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_invoice, field, value)
        
        db_invoice.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def delete_invoice(self, invoice_id: int) -> bool:
        db_invoice = self.get_invoice(invoice_id)
        if not db_invoice:
            return False
        
        self.db.delete(db_invoice)
        self.db.commit()
        return True

    def update_invoice_status(self, invoice_id: int, status: InvoiceStatus) -> Optional[Invoice]:
        db_invoice = self.get_invoice(invoice_id)
        if not db_invoice:
            return None
        
        db_invoice.status = status
        db_invoice.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def get_overdue_invoices(self) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.due_date < datetime.utcnow(),
            Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.DRAFT])
        ).all()

    def get_invoice_statistics(self, start_date: datetime, end_date: datetime) -> dict:
        invoices = self.db.query(Invoice).filter(
            Invoice.created_at >= start_date,
            Invoice.created_at <= end_date
        ).all()
        
        total_amount = sum(inv.total_amount for inv in invoices)
        paid_amount = sum(inv.total_amount for inv in invoices if inv.status == InvoiceStatus.PAID)
        overdue_amount = sum(inv.total_amount for inv in invoices if inv.status == InvoiceStatus.OVERDUE)
        
        return {
            "total_invoices": len(invoices),
            "total_amount": total_amount,
            "paid_amount": paid_amount,
            "overdue_amount": overdue_amount,
            "payment_rate": (paid_amount / total_amount * 100) if total_amount > 0 else 0
        }
