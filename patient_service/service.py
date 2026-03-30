from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Patient, PatientCreate, PatientUpdate
import data_service

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def create_patient(patient: PatientCreate) -> Patient:
    return data_service.db_create_patient(patient)


def get_all_patients() -> list[Patient]:
    return data_service.db_get_all_patients()


def get_patient(patient_id: int) -> Patient:
    patient = data_service.db_get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def update_patient(patient_id: int, update: PatientUpdate) -> Patient:
    patient = data_service.db_update_patient(patient_id, update)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def delete_patient(patient_id: int) -> dict:
    deleted = data_service.db_delete_patient(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": f"Patient {patient_id} deleted successfully"}
