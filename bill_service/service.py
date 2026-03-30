from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from model import Bill, BillCreate, BillUpdate
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


def create_bill(bill: BillCreate) -> Bill:
    return data_service.db_create_bill(bill)


def get_all_bills() -> list[Bill]:
    return data_service.db_get_all_bills()


def get_bill(bill_id: int) -> Bill:
    bill = data_service.db_get_bill(bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def update_bill(bill_id: int, update: BillUpdate) -> Bill:
    bill = data_service.db_update_bill(bill_id, update)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


def delete_bill(bill_id: int) -> dict:
    deleted = data_service.db_delete_bill(bill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {"message": f"Bill {bill_id} deleted successfully"}
