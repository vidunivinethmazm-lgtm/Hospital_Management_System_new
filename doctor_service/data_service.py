from model import Doctor, DoctorCreate, DoctorUpdate

# In-memory database
doctors_db: dict = {}
counter: int = 1


def db_create_doctor(doctor: DoctorCreate) -> Doctor:
    global counter
    new_doctor = Doctor(id=counter, **doctor.model_dump())
    doctors_db[counter] = new_doctor
    counter += 1
    return new_doctor


def db_get_all_doctors() -> list[Doctor]:
    return list(doctors_db.values())


def db_get_doctor(doctor_id: int) -> Doctor | None:
    return doctors_db.get(doctor_id)


def db_update_doctor(doctor_id: int, update: DoctorUpdate) -> Doctor | None:
    if doctor_id not in doctors_db:
        return None
    existing = doctors_db[doctor_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    doctors_db[doctor_id] = Doctor(**updated_data)
    return doctors_db[doctor_id]


def db_delete_doctor(doctor_id: int) -> bool:
    if doctor_id not in doctors_db:
        return False
    del doctors_db[doctor_id]
    return True
