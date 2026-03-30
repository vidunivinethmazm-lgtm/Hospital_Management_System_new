from fastapi import FastAPI, Depends
from model import Department, DepartmentCreate, DepartmentUpdate
import service

app = FastAPI(
    title="Department Service",
    description="Microservice for managing hospital departments",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"service": "Department Service", "status": "running"}


@app.post("/departments", response_model=Department, status_code=201, tags=["Departments"])
def create_department(department: DepartmentCreate, user: str = Depends(service.verify_token)):
    return service.create_department(department)


@app.get("/departments", response_model=list[Department], tags=["Departments"])
def get_all_departments(user: str = Depends(service.verify_token)):
    return service.get_all_departments()


@app.get("/departments/{department_id}", response_model=Department, tags=["Departments"])
def get_department(department_id: int, user: str = Depends(service.verify_token)):
    return service.get_department(department_id)


@app.put("/departments/{department_id}", response_model=Department, tags=["Departments"])
def update_department(department_id: int, update: DepartmentUpdate, user: str = Depends(service.verify_token)):
    return service.update_department(department_id, update)


@app.delete("/departments/{department_id}", tags=["Departments"])
def delete_department(department_id: int, user: str = Depends(service.verify_token)):
    return service.delete_department(department_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
