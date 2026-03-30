from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Department, DepartmentCreate, DepartmentUpdate
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


def create_department(department: DepartmentCreate) -> Department:
    return data_service.db_create_department(department)


def get_all_departments() -> list[Department]:
    return data_service.db_get_all_departments()


def get_department(department_id: int) -> Department:
    department = data_service.db_get_department(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


def update_department(department_id: int, update: DepartmentUpdate) -> Department:
    department = data_service.db_update_department(department_id, update)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


def delete_department(department_id: int) -> dict:
    deleted = data_service.db_delete_department(department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": f"Department {department_id} deleted successfully"}
