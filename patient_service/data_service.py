from model import Patient, PatientCreate, PatientUpdate

patients_db: dict = {}
counter: int = 1


def db_create_patient(patient: PatientCreate) -> Patient:
    global counter
    new_patient = Patient(id=counter, **patient.model_dump())
    patients_db[counter] = new_patient
    counter += 1
    return new_patient


def db_get_all_patients() -> list[Patient]:
    return list(patients_db.values())


def db_get_patient(patient_id: int) -> Patient | None:
    return patients_db.get(patient_id)


def db_update_patient(patient_id: int, update: PatientUpdate) -> Patient | None:
    if patient_id not in patients_db:
        return None
    existing = patients_db[patient_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    patients_db[patient_id] = Patient(**updated_data)
    return patients_db[patient_id]


def db_delete_patient(patient_id: int) -> bool:
    if patient_id not in patients_db:
        return False
    del patients_db[patient_id]
    return True
