from model import Department, DepartmentCreate, DepartmentUpdate

departments_db: dict = {}
counter: int = 1


def db_create_department(department: DepartmentCreate) -> Department:
    global counter
    new_department = Department(id=counter, **department.model_dump())
    departments_db[counter] = new_department
    counter += 1
    return new_department


def db_get_all_departments() -> list[Department]:
    return list(departments_db.values())


def db_get_department(department_id: int) -> Department | None:
    return departments_db.get(department_id)


def db_update_department(department_id: int, update: DepartmentUpdate) -> Department | None:
    if department_id not in departments_db:
        return None
    existing = departments_db[department_id]
    updated_data = existing.model_dump()
    for field, value in update.model_dump(exclude_none=True).items():
        updated_data[field] = value
    departments_db[department_id] = Department(**updated_data)
    return departments_db[department_id]


def db_delete_department(department_id: int) -> bool:
    if department_id not in departments_db:
        return False
    del departments_db[department_id]
    return True
