from model import Medicine, MedicineCreate, MedicineUpdate

medicines_db: dict = {}
counter: int = 1


def db_create_medicine(medicine: MedicineCreate) -> Medicine:
    global counter
    new_medicine = Medicine(id=counter, **medicine.model_dump())
    medicines_db[counter] = new_medicine
    counter += 1
    return new_medicine


def db_get_all_medicines() -> list[Medicine]:
    return list(medicines_db.values())


def db_get_medicine(medicine_id: int) -> Medicine | None:
    return medicines_db.get(medicine_id)


def db_update_medicine(medicine_id: int, update: MedicineUpdate) -> Medicine | None:
    if medicine_id not in medicines_db:
        return None
    existing = medicines_db[medicine_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    medicines_db[medicine_id] = Medicine(**updated_data)
    return medicines_db[medicine_id]


def db_delete_medicine(medicine_id: int) -> bool:
    if medicine_id not in medicines_db:
        return False
    del medicines_db[medicine_id]
    return True
