from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Patient Service",
    description="Microservice for managing hospital patients",
    version="1.0.0",
)

patients_db: dict = {}
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


@app.get("/", tags=["Health"])
def root():
    return {"service": "Patient Service", "status": "running"}


@app.post("/patients", response_model=Patient, status_code=201, tags=["Patients"])
def create_patient(patient: PatientCreate, user: str = Depends(verify_token)):
    global counter
    new_patient = Patient(id=counter, **patient.model_dump())
    patients_db[counter] = new_patient
    counter += 1
    return new_patient


@app.get("/patients", response_model=list[Patient], tags=["Patients"])
def get_all_patients(user: str = Depends(verify_token)):
    return list(patients_db.values())


@app.get("/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def get_patient(patient_id: int, user: str = Depends(verify_token)):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients_db[patient_id]


@app.put("/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def update_patient(patient_id: int, update: PatientUpdate, user: str = Depends(verify_token)):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing = patients_db[patient_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    patients_db[patient_id] = Patient(**updated_data)
    return patients_db[patient_id]


@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int, user: str = Depends(verify_token)):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients_db[patient_id]
    return {"message": f"Patient {patient_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
