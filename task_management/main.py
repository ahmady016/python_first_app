# build a task management app using classes and json files as a database:
# create a department class that has a id, name and description
# create an employee class that has a id, first name, last name, email,
# phone number, role and department_id
# create a task class that has a id, title, description, created date,
# due date, completed date, status and priority
# the task class has employee_id that is a foreign key to the employee class
# generate all objects ids using uuid
# create a JSON_database class that allow Folder-Based JSON Database Management
###########################################################################
# test the app using faker and icecream
###########################################################################
from datetime import timedelta
from icecream import ic     # pyright: ignore[reportMissingImports]
from faker import Faker     # pyright: ignore[reportMissingImports]
from department import Department
from employee import Employee
from task import Task
from json_database import JsonDatabase
from ic_config import icecream_config
############################################################################
ic("################################")
ic("Task Management App Started")
ic("################################")
############################################################################
# run the configuration for icecream
icecream_config()
# create a faker instance
fake = Faker()
############################################################################
# create random departments using faker
def random_departments(
    min_count: int = 10,
    max_count: int = 15
) -> list[Department]:
    return [
        Department(fake.company(), fake.catch_phrase())
        for _ in range(fake.random_int(min_count, max_count))
    ]
############################################################################
# create random employees using faker and assign them to random departments
def random_employees(
    departments: list[Department],
    min_count: int = 100,
    max_count: int = 200
) -> list[Employee]:
    return  [
        Employee(
            fake.first_name(),
            fake.last_name(),
            fake.random_element(Employee.EMPLOYEE_GENDERS),
            fake.email(),
            fake.phone_number(),
            fake.date_of_birth(minimum_age=20, maximum_age=60).strftime("%Y-%m-%d"),
            fake.date_between(start_date="-14y", end_date="today").strftime("%Y-%m-%d"),
            fake.job(),
            fake.random_element(Employee.EMPLOYEE_STATES),
            fake.random_element(departments).id
        )
        for _ in range(fake.random_int(min_count, max_count))
    ]
#############################################################################
# create random tasks using faker and assign them to random employees
def random_tasks(
    employees: list[Employee],
    min_count: int = 360,
    max_count: int = 640
) -> list[Task]:
    tasks = []
    for _ in range(fake.random_int(min_count, max_count)):
        # generate created_at datetime
        created_at = fake.date_time_between(start_date="-360d", end_date="now")
        # generate due_date datetime that is after created_at
        due_date = created_at + timedelta(days=fake.random_int(1, 30))
        # generate completed_at datetime that is after due_date
        completed_at_start_date = fake.random_element([created_at, due_date])
        completed_at = completed_at_start_date + timedelta(days=fake.random_int(1, 30))
        # create a task object and append it to the tasks list
        task = Task(
            fake.sentence(nb_words=fake.random_int(3, 7)),
            fake.sentence(nb_words=fake.random_int(20, 50)),
            created_at.strftime("%Y-%m-%d %H:%M:%S"),
            due_date.strftime("%Y-%m-%d %H:%M:%S"),
            completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            fake.random_element(Task.TASK_PRIORITIES),
            fake.random_element(Task.TASK_STATES),
            fake.random_element(employees).id
        )
        tasks.append(task)
    return tasks
############################################################################
# create a JSON database instance and save the departments, employees and tasks
def save_to_json_database(
    departments: list[Department],
    employees: list[Employee],
    tasks: list[Task]
) -> JsonDatabase:
    db = JsonDatabase(".db")
    for department in departments:
        db.save_record("departments", department.id, department)
    for employee in employees:
        db.save_record("employees", employee.id, employee)
    for task in tasks:
        db.save_record("tasks", task.id, task)
    return db
############################################################################
departments = random_departments()
# print the departments
ic(f"({len(departments)}) Departments Created:")
ic("-------------------------")
# ic("\n".join(str(department) for department in departments))
############################################################################
employees = random_employees(departments=departments)
# print the employees
ic(f"({len(employees)}) Employees Created:")
ic("-------------------------")
# ic("\n".join(str(employee) for employee in employees))
############################################################################
tasks = random_tasks(employees=employees)
# print the tasks
ic(f"({len(tasks)}) Tasks Created:")
ic("-------------------------")
# ic("\n".join(str(task) for task in tasks))
############################################################################
db = save_to_json_database(departments, employees, tasks)
ic("Data Saved To JSON Database:")
ic("-------------------------")
ic(db)
############################################################################
ic("################################")
ic("Task Management App Finished")
ic("################################")
############################################################################
