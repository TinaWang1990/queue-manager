from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

# ============ STATUS UPDATE SCHEMAS ============

class PatientStatus(str, Enum):
    """Valid patient status values"""
    WAITING = "waiting"
    PROCESSING = "processing"
    DONE = "done"
    CANCELLED = "cancelled"

class StatusUpdateRequest(BaseModel):
    """Request schema for updating patient status"""
    status: PatientStatus
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "processing"
        }
    })

class StatusUpdateResponse(BaseModel):
    """Response schema for status update"""
    ok: bool = True
    entry_id: UUID
    new_status: str
    updated_by: str
    updated_at: Optional[datetime] = None
    processing_at: Optional[datetime] = None
    done_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# ============ NOTE MANAGEMENT SCHEMAS ============

class NoteCreate(BaseModel):
    """Schema for creating a note"""
    message: str = Field(..., min_length=1, max_length=1000, description="Note content")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "message": "Doctor will be 10 minutes late"
        }
    })

class NoteOut(BaseModel):
    """Response schema for note"""
    id: UUID
    queue_id: UUID
    message: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class NoteCreateResponse(BaseModel):
    """Response schema for note creation"""
    ok: bool = True
    note: NoteOut

# ============ QUEUE OVERVIEW SCHEMAS ============

class QueueStats(BaseModel):
    """Statistics for a queue"""
    total_waiting: int = 0
    total_processing: int = 0
    total_done_today: int = 0
    average_wait_time_minutes: float = 0.0

class AdminQueueOut(BaseModel):
    """Queue info for admin view"""
    id: UUID
    name: str
    type: str
    active: bool
    created_at: datetime
    stats: QueueStats
    
    model_config = ConfigDict(from_attributes=True)

# ============ PATIENT INFO SCHEMAS ============

class AdminPatientInfo(BaseModel):
    """Detailed patient info for admin view"""
    entry_id: UUID
    user_id: UUID
    username: str
    phone: Optional[str]
    phone_verified: bool
    status: str
    position: int  # Position in queue
    wait_time_minutes: int  # Minutes since registration
    registered_at: datetime
    processing_at: Optional[datetime]
    done_at: Optional[datetime]
    updated_by: str

# ============ BULK OPERATION SCHEMAS ============

class BulkStatusUpdate(BaseModel):
    """Schema for updating multiple patients at once"""
    entry_ids: list[UUID]
    status: PatientStatus
    reason: Optional[str] = None
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "entry_ids": ["123e4567-e89b-12d3-a456-426614174000"],
            "status": "done",
            "reason": "Completed appointment"
        }
    })

class BulkStatusResponse(BaseModel):
    """Response for bulk updates"""
    updated_count: int
    failed_entries: list[UUID] = []
    ok: bool = True

# ============ ADMIN AUTH SCHEMAS ============

class AdminLogin(BaseModel):
    """Admin login request"""
    username: str
    password: str

class AdminToken(BaseModel):
    """Token response for admin auth"""
    access_token: str
    token_type: str = "bearer"
    admin_id: UUID
    username: str
    queue_id: UUID

class AdminProfile(BaseModel):
    """Admin profile info"""
    id: UUID
    username: str
    queue_id: UUID
    queue_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)