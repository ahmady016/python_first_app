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
from icecream import ic     # pyright: ignore[reportMissingImports]
from faker import Faker     # pyright: ignore[reportMissingImports]
from datetime import timedelta
from department import Department
from employee import Employee
from task import Task
from json_database import JsonDatabase
############################################################################
ic("################################")
ic("Task Management App Started")
ic("################################")
############################################################################
# create a faker instance
fake = Faker()
############################################################################
# create random departments using faker
departments = [
    Department(fake.company(), fake.catch_phrase())
    for _ in range(fake.random_int(7, 12))
]
# print the departments
_ = f"({len(departments)}) Departments Created:"
ic(_)
ic("-------------------------")
_ = "\n".join(str(department) for department in departments)
ic(_)
############################################################################
# create random employees using faker and assign them to random departments
employees = [
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
    for _ in range(fake.random_int(70, 120))
]
# print the employees
_ = f"({len(employees)}) Employees Created:"
ic(_)
ic("-------------------------")
_ = "\n".join(str(employee) for employee in employees)
ic(_)
#############################################################################
# create random tasks using faker and assign them to random employees
tasks = []
for _ in range(fake.random_int(180, 360)):
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
# print the tasks
_ = f"({len(tasks)}) Tasks Created:"
ic(_)
ic("-------------------------")
_ = "\n".join(str(task) for task in tasks)
ic(_)
############################################################################
# create a JSON database instance and save the departments, employees and tasks
db = JsonDatabase(".db")
for department in departments:
    db.save_record("departments", department.id, department)
for employee in employees:
    db.save_record("employees", employee.id, employee)
for task in tasks:
    db.save_record("tasks", task.id, task)
############################################################################
ic("✅ Data Saved To JSON Database:")
ic("-------------------------")
ic(db)
############################################################################
ic("################################")
ic("Task Management App Finished")
ic("################################")
############################################################################
