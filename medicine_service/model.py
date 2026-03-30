from pydantic import BaseModel
from typing import Optional


class MedicineCreate(BaseModel):
    name: str
    category: str
    dosage: str
    price: float
    stock: int
    manufacturer: str


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    dosage: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    manufacturer: Optional[str] = None


class Medicine(BaseModel):
    id: int
    name: str
    category: str
    dosage: str
    price: float
    stock: int
    manufacturer: str
