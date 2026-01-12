from pydantic import BaseModel
from uuid import UUID

class JoinQueue(BaseModel):
    username: str
    phone: str | None = None

class PatientStatusOut(BaseModel):
    position: int
    status: str
    updated_by: str
    estimated_wait_minutes: int
    verified: bool
