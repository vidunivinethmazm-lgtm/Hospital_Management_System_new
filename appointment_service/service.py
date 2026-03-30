from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Appointment, AppointmentCreate, AppointmentUpdate
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


def create_appointment(appointment: AppointmentCreate) -> Appointment:
    return data_service.db_create_appointment(appointment)


def get_all_appointments() -> list[Appointment]:
    return data_service.db_get_all_appointments()


def get_appointment(appointment_id: int) -> Appointment:
    appointment = data_service.db_get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


def update_appointment(appointment_id: int, update: AppointmentUpdate) -> Appointment:
    appointment = data_service.db_update_appointment(appointment_id, update)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


def delete_appointment(appointment_id: int) -> dict:
    deleted = data_service.db_delete_appointment(appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": f"Appointment {appointment_id} deleted successfully"}
