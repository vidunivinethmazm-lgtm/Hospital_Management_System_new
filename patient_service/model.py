from pydantic import BaseModel
from typing import Optional


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    contact: str
    address: str


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None


class Patient(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    contact: str
    address: str
