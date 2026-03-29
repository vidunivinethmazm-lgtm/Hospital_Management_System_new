from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Medicine Service",
    description="Microservice for managing hospital medicines/pharmacy",
    version="1.0.0",
)

medicines_db: dict = {}
counter: int = 1


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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


@app.get("/", tags=["Health"])
def root():
    return {"service": "Medicine Service", "status": "running"}


@app.post("/medicines", response_model=Medicine, status_code=201, tags=["Medicines"])
def create_medicine(medicine: MedicineCreate, user: str = Depends(verify_token)):
    global counter
    new_medicine = Medicine(id=counter, **medicine.model_dump())
    medicines_db[counter] = new_medicine
    counter += 1
    return new_medicine


@app.get("/medicines", response_model=list[Medicine], tags=["Medicines"])
def get_all_medicines(user: str = Depends(verify_token)):
    return list(medicines_db.values())


@app.get("/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def get_medicine(medicine_id: int, user: str = Depends(verify_token)):
    if medicine_id not in medicines_db:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicines_db[medicine_id]


@app.put("/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def update_medicine(medicine_id: int, update: MedicineUpdate, user: str = Depends(verify_token)):
    if medicine_id not in medicines_db:
        raise HTTPException(status_code=404, detail="Medicine not found")
    existing = medicines_db[medicine_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    medicines_db[medicine_id] = Medicine(**updated_data)
    return medicines_db[medicine_id]


@app.delete("/medicines/{medicine_id}", tags=["Medicines"])
def delete_medicine(medicine_id: int, user: str = Depends(verify_token)):
    if medicine_id not in medicines_db:
        raise HTTPException(status_code=404, detail="Medicine not found")
    del medicines_db[medicine_id]
    return {"message": f"Medicine {medicine_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
