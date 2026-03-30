from model import Bill, BillCreate, BillUpdate

bills_db: dict = {}
counter: int = 1


def db_create_bill(bill: BillCreate) -> Bill:
    global counter
    total = bill.consultation_fee + bill.medicine_fee + bill.lab_fee
    new_bill = Bill(id=counter, total_amount=total, **bill.model_dump())
    bills_db[counter] = new_bill
    counter += 1
    return new_bill


def db_get_all_bills() -> list[Bill]:
    return list(bills_db.values())


def db_get_bill(bill_id: int) -> Bill | None:
    return bills_db.get(bill_id)


def db_update_bill(bill_id: int, update: BillUpdate) -> Bill | None:
    if bill_id not in bills_db:
        return None
    existing = bills_db[bill_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    updated_data["total_amount"] = (
        updated_data["consultation_fee"]
        + updated_data["medicine_fee"]
        + updated_data["lab_fee"]
    )
    bills_db[bill_id] = Bill(**updated_data)
    return bills_db[bill_id]


def db_delete_bill(bill_id: int) -> bool:
    if bill_id not in bills_db:
        return False
    del bills_db[bill_id]
    return True
