from pydantic import BaseModel
from typing import Optional


class DepartmentCreate(BaseModel):
    name: str
    head_doctor: str
    location: str
    contact: str
    capacity: int


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    head_doctor: Optional[str] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    capacity: Optional[int] = None


class Department(BaseModel):
    id: int
    name: str
    head_doctor: str
    location: str
    contact: str
    capacity: int
