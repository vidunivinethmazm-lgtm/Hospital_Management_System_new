from fastapi import FastAPI, Depends
from model import Appointment, AppointmentCreate, AppointmentUpdate
import service

app = FastAPI(
    title="Appointment Service",
    description="Microservice for managing hospital appointments",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"service": "Appointment Service", "status": "running"}


@app.post("/appointments", response_model=Appointment, status_code=201, tags=["Appointments"])
def create_appointment(appointment: AppointmentCreate, user: str = Depends(service.verify_token)):
    return service.create_appointment(appointment)


@app.get("/appointments", response_model=list[Appointment], tags=["Appointments"])
def get_all_appointments(user: str = Depends(service.verify_token)):
    return service.get_all_appointments()


@app.get("/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def get_appointment(appointment_id: int, user: str = Depends(service.verify_token)):
    return service.get_appointment(appointment_id)


@app.put("/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def update_appointment(appointment_id: int, update: AppointmentUpdate, user: str = Depends(service.verify_token)):
    return service.update_appointment(appointment_id, update)


@app.delete("/appointments/{appointment_id}", tags=["Appointments"])
def delete_appointment(appointment_id: int, user: str = Depends(service.verify_token)):
    return service.delete_appointment(appointment_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
