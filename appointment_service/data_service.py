from model import Appointment, AppointmentCreate, AppointmentUpdate

appointments_db: dict = {}
counter: int = 1


def db_create_appointment(appointment: AppointmentCreate) -> Appointment:
    global counter
    new_appointment = Appointment(id=counter, **appointment.model_dump())
    appointments_db[counter] = new_appointment
    counter += 1
    return new_appointment


def db_get_all_appointments() -> list[Appointment]:
    return list(appointments_db.values())


def db_get_appointment(appointment_id: int) -> Appointment | None:
    return appointments_db.get(appointment_id)


def db_update_appointment(appointment_id: int, update: AppointmentUpdate) -> Appointment | None:
    if appointment_id not in appointments_db:
        return None
    existing = appointments_db[appointment_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    appointments_db[appointment_id] = Appointment(**updated_data)
    return appointments_db[appointment_id]


def db_delete_appointment(appointment_id: int) -> bool:
    if appointment_id not in appointments_db:
        return False
    del appointments_db[appointment_id]
    return True
