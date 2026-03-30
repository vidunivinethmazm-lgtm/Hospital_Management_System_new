from fastapi import FastAPI, Depends
from model import Bill, BillCreate, BillUpdate
import service

app = FastAPI(
    title="Bill Service",
    description="Microservice for managing hospital billing",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"service": "Bill Service", "status": "running"}


@app.post("/bills", response_model=Bill, status_code=201, tags=["Bills"])
def create_bill(bill: BillCreate, user: str = Depends(service.verify_token)):
    return service.create_bill(bill)


@app.get("/bills", response_model=list[Bill], tags=["Bills"])
def get_all_bills(user: str = Depends(service.verify_token)):
    return service.get_all_bills()


@app.get("/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def get_bill(bill_id: int, user: str = Depends(service.verify_token)):
    return service.get_bill(bill_id)


@app.put("/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def update_bill(bill_id: int, update: BillUpdate, user: str = Depends(service.verify_token)):
    return service.update_bill(bill_id, update)


@app.delete("/bills/{bill_id}", tags=["Bills"])
def delete_bill(bill_id: int, user: str = Depends(service.verify_token)):
    return service.delete_bill(bill_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=True)
