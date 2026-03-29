from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
security = HTTPBearer()

app = FastAPI(
    title="Department Service",
    description="Microservice for managing hospital departments",
    version="1.0.0",
)

departments_db: dict = {}
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


class DepartmentCreate(BaseModel):
    name: str
    head_doctor: str
    location: str
    contact: str
    capacity: int


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    head_doctor: Optional[str] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    capacity: Optional[int] = None


class Department(BaseModel):
    id: int
    name: str
    head_doctor: str
    location: str
    contact: str
    capacity: int


@app.get("/", tags=["Health"])
def root():
    return {"service": "Department Service", "status": "running"}


@app.post("/departments", response_model=Department, status_code=201, tags=["Departments"])
def create_department(department: DepartmentCreate, user: str = Depends(verify_token)):
    global counter
    new_department = Department(id=counter, **department.model_dump())
    departments_db[counter] = new_department
    counter += 1
    return new_department


@app.get("/departments", response_model=list[Department], tags=["Departments"])
def get_all_departments(user: str = Depends(verify_token)):
    return list(departments_db.values())


@app.get("/departments/{department_id}", response_model=Department, tags=["Departments"])
def get_department(department_id: int, user: str = Depends(verify_token)):
    if department_id not in departments_db:
        raise HTTPException(status_code=404, detail="Department not found")
    return departments_db[department_id]


@app.put("/departments/{department_id}", response_model=Department, tags=["Departments"])
def update_department(department_id: int, update: DepartmentUpdate, user: str = Depends(verify_token)):
    if department_id not in departments_db:
        raise HTTPException(status_code=404, detail="Department not found")
    existing = departments_db[department_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    departments_db[department_id] = Department(**updated_data)
    return departments_db[department_id]


@app.delete("/departments/{department_id}", tags=["Departments"])
def delete_department(department_id: int, user: str = Depends(verify_token)):
    if department_id not in departments_db:
        raise HTTPException(status_code=404, detail="Department not found")
    del departments_db[department_id]
    return {"message": f"Department {department_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
