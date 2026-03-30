from pydantic import BaseModel
from typing import Optional


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    contact: str
    department: str
    available: bool = True


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    contact: Optional[str] = None
    department: Optional[str] = None
    available: Optional[bool] = None


class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    contact: str
    department: str
    available: bool
