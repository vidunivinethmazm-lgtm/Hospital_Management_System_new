from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Doctor Service",
    description="Microservice for managing hospital doctors",
    version="1.0.0",
)

doctors_db: dict = {}
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


@app.get("/", tags=["Health"])
def root():
    return {"service": "Doctor Service", "status": "running"}


@app.post("/doctors", response_model=Doctor, status_code=201, tags=["Doctors"])
def create_doctor(doctor: DoctorCreate, user: str = Depends(verify_token)):
    global counter
    new_doctor = Doctor(id=counter, **doctor.model_dump())
    doctors_db[counter] = new_doctor
    counter += 1
    return new_doctor


@app.get("/doctors", response_model=list[Doctor], tags=["Doctors"])
def get_all_doctors(user: str = Depends(verify_token)):
    return list(doctors_db.values())


@app.get("/doctors/{doctor_id}", response_model=Doctor, tags=["Doctors"])
def get_doctor(doctor_id: int, user: str = Depends(verify_token)):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctors_db[doctor_id]


@app.put("/doctors/{doctor_id}", response_model=Doctor, tags=["Doctors"])
def update_doctor(doctor_id: int, update: DoctorUpdate, user: str = Depends(verify_token)):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    existing = doctors_db[doctor_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    doctors_db[doctor_id] = Doctor(**updated_data)
    return doctors_db[doctor_id]


@app.delete("/doctors/{doctor_id}", tags=["Doctors"])
def delete_doctor(doctor_id: int, user: str = Depends(verify_token)):
    if doctor_id not in doctors_db:
        raise HTTPException(status_code=404, detail="Doctor not found")
    del doctors_db[doctor_id]
    return {"message": f"Doctor {doctor_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
