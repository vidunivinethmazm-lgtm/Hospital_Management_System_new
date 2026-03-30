from fastapi import FastAPI, Depends
from model import Medicine, MedicineCreate, MedicineUpdate
import service

app = FastAPI(
    title="Medicine Service",
    description="Microservice for managing hospital medicines/pharmacy",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"service": "Medicine Service", "status": "running"}


@app.post("/medicines", response_model=Medicine, status_code=201, tags=["Medicines"])
def create_medicine(medicine: MedicineCreate, user: str = Depends(service.verify_token)):
    return service.create_medicine(medicine)


@app.get("/medicines", response_model=list[Medicine], tags=["Medicines"])
def get_all_medicines(user: str = Depends(service.verify_token)):
    return service.get_all_medicines()


@app.get("/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def get_medicine(medicine_id: int, user: str = Depends(service.verify_token)):
    return service.get_medicine(medicine_id)


@app.put("/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def update_medicine(medicine_id: int, update: MedicineUpdate, user: str = Depends(service.verify_token)):
    return service.update_medicine(medicine_id, update)


@app.delete("/medicines/{medicine_id}", tags=["Medicines"])
def delete_medicine(medicine_id: int, user: str = Depends(service.verify_token)):
    return service.delete_medicine(medicine_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
