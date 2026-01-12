# app/routers/__init__.py
from fastapi import APIRouter

# Create main router
api_router = APIRouter()

# Import and include all sub-routers
from .admin import router as admin_router
from .root import router as root_router
from .queues import router as queues_router
from .patient import router as patient_router

api_router.include_router(admin_router, prefix="/api/admin", tags=["admin"])
api_router.include_router(root_router, prefix="/api/root", tags=["root"])
api_router.include_router(queues_router, prefix="/api/queues", tags=["queues"])
api_router.include_router(patient_router, prefix="/api/patient", tags=["patient"])