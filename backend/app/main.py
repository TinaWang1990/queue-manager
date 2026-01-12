from contextlib import asynccontextmanager
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine, text, inspect
import app.models
from app.database import Base
from fastapi import FastAPI
from app.routers import api_router
from app.database import SessionLocal
from app.services.seed_root_admin import seed_root_admin
import asyncio

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):  
    # Startup code
    print("Starting up...")
    db = SessionLocal()
    try:
        seed_root_admin(db)
    finally:
        db.close()
    yield
    # Shutdown code (optional)
    print("Shutting down...")

# Create app with lifespan
app = FastAPI(
    title="Queue System",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Queue System API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "queue-system"}