# Pydantic schemas for API models
from .user import User, UserCreate, UserUpdate, UserInDB
from .appointment import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentInDB
from .customer import Customer, CustomerCreate, CustomerUpdate, CustomerInDB
from .vehicle import Vehicle, VehicleCreate, VehicleUpdate, VehicleInDB
from .service import Service, ServiceCreate, ServiceUpdate, ServiceInDB
from .invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceInDB
from .checkin import CheckIn, CheckInCreate, CheckInUpdate, CheckInInDB
from .ai_detection import AIDetection, AIDetectionCreate, AIDetectionUpdate, AIDetectionInDB

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserInDB",
    "Appointment", "AppointmentCreate", "AppointmentUpdate", "AppointmentInDB",
    "Customer", "CustomerCreate", "CustomerUpdate", "CustomerInDB",
    "Vehicle", "VehicleCreate", "VehicleUpdate", "VehicleInDB",
    "Service", "ServiceCreate", "ServiceUpdate", "ServiceInDB",
    "Invoice", "InvoiceCreate", "InvoiceUpdate", "InvoiceInDB",
    "CheckIn", "CheckInCreate", "CheckInUpdate", "CheckInInDB",
    "AIDetection", "AIDetectionCreate", "AIDetectionUpdate", "AIDetectionInDB"
]
