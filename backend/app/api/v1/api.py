from fastapi import APIRouter
from app.api.v1.endpoints import auth, customers, vehicles, services, appointments, checkins, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(checkins.router, prefix="/checkins", tags=["check-ins"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai-detection"])
