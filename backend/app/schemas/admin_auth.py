# schemas/admin_auth.py
from pydantic import BaseModel, ConfigDict

class AdminChangePassword(BaseModel):
    current_password: str
    new_password: str

class AdminResetQueue(BaseModel):
    """Schema for resetting queue (clear all waiting)"""
    confirm: bool = Field(..., description="Must be True to confirm reset")
    reason: Optional[str] = None

class AdminExportData(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_patient_info: bool = False
    format: str = "json"  # json, csv