from fastapi import FastAPI, Depends
from model import Patient, PatientCreate, PatientUpdate
import service

app = FastAPI(
    title="Patient Service",
    description="Microservice for managing hospital patients",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"service": "Patient Service", "status": "running"}


@app.post("/patients", response_model=Patient, status_code=201, tags=["Patients"])
def create_patient(patient: PatientCreate, user: str = Depends(service.verify_token)):
    return service.create_patient(patient)


@app.get("/patients", response_model=list[Patient], tags=["Patients"])
def get_all_patients(user: str = Depends(service.verify_token)):
    return service.get_all_patients()


@app.get("/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def get_patient(patient_id: int, user: str = Depends(service.verify_token)):
    return service.get_patient(patient_id)


@app.put("/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def update_patient(patient_id: int, update: PatientUpdate, user: str = Depends(service.verify_token)):
    return service.update_patient(patient_id, update)


@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int, user: str = Depends(service.verify_token)):
    return service.delete_patient(patient_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
