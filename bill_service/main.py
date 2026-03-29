from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Bill Service",
    description="Microservice for managing hospital billing",
    version="1.0.0",
)

bills_db: dict = {}
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


@app.get("/", tags=["Health"])
def root():
    return {"service": "Bill Service", "status": "running"}


@app.post("/bills", response_model=Bill, status_code=201, tags=["Bills"])
def create_bill(bill: BillCreate, user: str = Depends(verify_token)):
    global counter
    total = bill.consultation_fee + bill.medicine_fee + bill.lab_fee
    new_bill = Bill(id=counter, total_amount=total, **bill.model_dump())
    bills_db[counter] = new_bill
    counter += 1
    return new_bill


@app.get("/bills", response_model=list[Bill], tags=["Bills"])
def get_all_bills(user: str = Depends(verify_token)):
    return list(bills_db.values())


@app.get("/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def get_bill(bill_id: int, user: str = Depends(verify_token)):
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bills_db[bill_id]


@app.put("/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def update_bill(bill_id: int, update: BillUpdate, user: str = Depends(verify_token)):
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    existing = bills_db[bill_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    updated_data["total_amount"] = (
        updated_data["consultation_fee"]
        + updated_data["medicine_fee"]
        + updated_data["lab_fee"]
    )
    bills_db[bill_id] = Bill(**updated_data)
    return bills_db[bill_id]


@app.delete("/bills/{bill_id}", tags=["Bills"])
def delete_bill(bill_id: int, user: str = Depends(verify_token)):
    if bill_id not in bills_db:
        raise HTTPException(status_code=404, detail="Bill not found")
    del bills_db[bill_id]
    return {"message": f"Bill {bill_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
