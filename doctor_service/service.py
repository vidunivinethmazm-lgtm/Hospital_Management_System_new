from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Doctor, DoctorCreate, DoctorUpdate
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


def create_doctor(doctor: DoctorCreate) -> Doctor:
    return data_service.db_create_doctor(doctor)


def get_all_doctors() -> list[Doctor]:
    return data_service.db_get_all_doctors()


def get_doctor(doctor_id: int) -> Doctor:
    doctor = data_service.db_get_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def update_doctor(doctor_id: int, update: DoctorUpdate) -> Doctor:
    doctor = data_service.db_update_doctor(doctor_id, update)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def delete_doctor(doctor_id: int) -> dict:
    deleted = data_service.db_delete_doctor(doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": f"Doctor {doctor_id} deleted successfully"}
