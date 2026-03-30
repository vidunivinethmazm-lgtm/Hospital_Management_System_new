from pydantic import BaseModel
from typing import Optional


class BillCreate(BaseModel):
    patient_id: int
    appointment_id: int
    consultation_fee: float
    medicine_fee: float
    lab_fee: float
    status: str = "Pending"


class BillUpdate(BaseModel):
    patient_id: Optional[int] = None
    appointment_id: Optional[int] = None
    consultation_fee: Optional[float] = None
    medicine_fee: Optional[float] = None
    lab_fee: Optional[float] = None
    status: Optional[str] = None


class Bill(BaseModel):
    id: int
    patient_id: int
    appointment_id: int
    consultation_fee: float
    medicine_fee: float
    lab_fee: float
    total_amount: float
    status: str
