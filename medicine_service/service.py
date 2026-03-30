from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Medicine, MedicineCreate, MedicineUpdate
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


def create_medicine(medicine: MedicineCreate) -> Medicine:
    return data_service.db_create_medicine(medicine)


def get_all_medicines() -> list[Medicine]:
    return data_service.db_get_all_medicines()


def get_medicine(medicine_id: int) -> Medicine:
    medicine = data_service.db_get_medicine(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


def update_medicine(medicine_id: int, update: MedicineUpdate) -> Medicine:
    medicine = data_service.db_update_medicine(medicine_id, update)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


def delete_medicine(medicine_id: int) -> dict:
    deleted = data_service.db_delete_medicine(medicine_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"message": f"Medicine {medicine_id} deleted successfully"}
