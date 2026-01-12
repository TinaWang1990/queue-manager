from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

# Base schema - shared fields
class QueueBase(BaseModel):
    name: str
    type: str
    active: Optional[bool] = True

# Schema for creating a queue (POST /queues)
class QueueCreate(QueueBase):
    name: str
    type: str # hospital | restaurant
    address: str
    image_name: str


# Schema for updating a queue (PATCH /queues/{id})
class QueueUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None

# Main response schema (GET /queues)
class QueueOut(QueueBase):
    id: UUID
    created_at: datetime
    
    # Use model_config instead of inner Config class in Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# Response with statistics
class QueueWithStatsOut(QueueOut):
    waiting_count: int = 0
    processing_count: int = 0
    total_today: int = 0
    
    model_config = ConfigDict(from_attributes=True)

# Schema for queue list with pagination
class QueueList(BaseModel):
    queues: List[QueueOut]
    total: int
    page: int
    size: int
    pages: int

# Schema for admin/management view
class QueueAdminOut(QueueOut):
    notes: Optional[List[str]] = []
    admin_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)