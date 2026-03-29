from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Appointment Service",
    description="Microservice for managing hospital appointments",
    version="1.0.0",
)

appointments_db: dict = {}
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


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str
    reason: str
    status: str = "Scheduled"


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None


class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str
    time: str
    reason: str
    status: str


@app.get("/", tags=["Health"])
def root():
    return {"service": "Appointment Service", "status": "running"}


@app.post("/appointments", response_model=Appointment, status_code=201, tags=["Appointments"])
def create_appointment(appointment: AppointmentCreate, user: str = Depends(verify_token)):
    global counter
    new_appointment = Appointment(id=counter, **appointment.model_dump())
    appointments_db[counter] = new_appointment
    counter += 1
    return new_appointment


@app.get("/appointments", response_model=list[Appointment], tags=["Appointments"])
def get_all_appointments(user: str = Depends(verify_token)):
    return list(appointments_db.values())


@app.get("/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def get_appointment(appointment_id: int, user: str = Depends(verify_token)):
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointments_db[appointment_id]


@app.put("/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def update_appointment(appointment_id: int, update: AppointmentUpdate, user: str = Depends(verify_token)):
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    existing = appointments_db[appointment_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    appointments_db[appointment_id] = Appointment(**updated_data)
    return appointments_db[appointment_id]


@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def delete_appointment(appointment_id: int, user: str = Depends(verify_token)):
    if appointment_id not in appointments_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    del appointments_db[appointment_id]
    return {"message": f"Appointment {appointment_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
