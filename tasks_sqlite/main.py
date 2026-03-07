# build a simple tasks management app using sqlite as the database
# ----------------------------------------------------------------
# the TasksDb class will be a simple wrapper around the sqlite3 module
# to provide a connection to the database and setup base configuration
# like enabling foreign keys and setting row factory to return dicts
# and for each entity like Department, Task, etc. we have a corresponding table class
# that use TasksDb to create the table and provide methods for CRUD operations
# and we have a concrete class for each entity that represent the data
# and provide a method to convert to dict for easy database manipulation
# finally test the app using faker and icecream print
#######################################################################
from ice_config import icecream_config
from icecream import ic as print   # pyright: ignore[reportMissingImports]
from tasks_db import TasksDb
#######################################################################
# run the icecream configuration to set up logging
# with rich console and timestamp prefix
icecream_config()
#######################################################################
def prompt_for_page() -> tuple[int, int]:
    try:
        page = int(input("Enter page number: "))
        limit = int(input("Enter page size: "))
        return page, limit
    except ValueError as error:
        print("not a number. Please try again.")
        print(error)
        return prompt_for_page()
#######################################################################
def prompt_for_limit() -> int:
    try:
        limit = int(input("Enter limit: "))
        return limit
    except ValueError as error:
        print("not a number. Please try again.")
        print(error)
        return prompt_for_limit()
#######################################################################
def list_departments():
    page, limit = prompt_for_page()
    departments = TasksDb.DEPARTMENTS.get_page(page, limit)
    print("Departments:")
    print("----------------------------")
    for department in departments:
        print(str(department))
    print("----------------------------")
#######################################################################
def list_employees():
    page, limit = prompt_for_page()
    employees = TasksDb.EMPLOYEES.get_page(page, limit)
    print("Employees:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#######################################################################
def list_tasks():
    page, limit = prompt_for_page()
    tasks = TasksDb.TASKS.get_page(page, limit)
    print("Tasks:")
    print("----------------------------")
    for task in tasks:
        print(str(task))
    print("----------------------------")
#######################################################################
def add_department():
    name = input("Enter department name: ")
    description = input("Enter department description: ")
    TasksDb.DEPARTMENTS.add(name, description)
#######################################################################
def update_department():
    dept_id = input("Enter department id: ")
    name = input("Enter department name: ")
    description = input("Enter department description: ")
    TasksDb.DEPARTMENTS.update(dept_id, name=name, description=description)
#######################################################################
def delete_department():
    dept_id = input("Enter department id: ")
    TasksDb.DEPARTMENTS.delete(dept_id)
#######################################################################
def add_employee():
    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    gender = input("Enter employee gender: ")
    birth_date = input("Enter employee birth date: ")
    mobile = input("Enter employee mobile number: ")
    email = input("Enter employee email: ")
    hire_date = input("Enter employee hire date: ")
    job_title = input("Enter employee job title: ")
    job_type = input("Enter employee job type: ")
    salary = float(input("Enter employee salary: "))
    department_id = input("Enter employee department id: ")
    TasksDb.EMPLOYEES.add(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birth_date=birth_date,
        mobile=mobile,
        email=email,
        hire_date=hire_date,
        job_title=job_title,
        job_type=job_type,
        salary=salary,
        department_id=department_id
    )
#######################################################################
def update_employee():
    emp_id = input("Enter employee id: ")
    first_name = input("Enter employee first name: ")
    last_name = input("Enter employee last name: ")
    gender = input("Enter employee gender: ")
    mobile = input("Enter employee mobile number: ")
    email = input("Enter employee email: ")
    TasksDb.EMPLOYEES.update(emp_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        mobile=mobile,
        email=email
    )
#######################################################################
def delete_employee():
    emp_id = input("Enter employee id: ")
    TasksDb.EMPLOYEES.delete(emp_id)
#######################################################################
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    create_date = input("Enter task create date: ")
    due_date = input("Enter task due date: ")
    employee_id = input("Enter task employee id: ")
    TasksDb.TASKS.add(
        title=title,
        description=description,
        create_date=create_date,
        due_date=due_date,
        employee_id=employee_id
    )
#######################################################################
def update_task():
    task_id = input("Enter task id: ")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    TasksDb.TASKS.update(task_id,
        title=title,
        description=description
    )
#######################################################################
def delete_task():
    task_id = input("Enter task id: ")
    TasksDb.TASKS.delete(task_id)
#######################################################################
def departments_members():
    page, limit = prompt_for_page()
    departments = TasksDb.VIEWS.departments_members(page, limit)
    print("Departments Members:")
    print("----------------------------")
    for department in departments:
        print(str(department))
    print("----------------------------")
#######################################################################
def departments_members_by_type():
    page, limit = prompt_for_page()
    departments = TasksDb.VIEWS.departments_members_by_type(page, limit)
    print("Departments Members By Type:")
    print("----------------------------")
    for department in departments:
        print(str(department))
    print("----------------------------")
#######################################################################
def departments_members_by_gender():
    page, limit = prompt_for_page()
    departments = TasksDb.VIEWS.departments_members_by_gender(page, limit)
    print("Departments Members By Gender:")
    print("----------------------------")
    for department in departments:
        print(str(department))
    print("----------------------------")
#######################################################################
def employees_tasks():
    page, limit = prompt_for_page()
    employees = TasksDb.VIEWS.employees_tasks(page, limit)
    print("Employees Tasks:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#######################################################################
def employees_tasks_by_state():
    page, limit = prompt_for_page()
    employees = TasksDb.VIEWS.employees_tasks_by_state(page, limit)
    print("Employees Tasks By State:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#######################################################################
def employees_tasks_by_priority():
    page, limit = prompt_for_page()
    employees = TasksDb.VIEWS.employees_tasks_by_priority(page, limit)
    print("Employees Tasks By Priority:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#######################################################################
def employees_experience_and_age_by_year():
    page, limit = prompt_for_page()
    employees = TasksDb.VIEWS.employees_experience_and_age_by_year(page, limit)
    print("Employees Experience And Age By Year:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#######################################################################
def employees_experience_and_age_by_year_and_month():
    page, limit = prompt_for_page()
    employees = TasksDb.VIEWS.employees_experience_and_age_by_year_and_month(page, limit)
    print("Employees Experience And Age By Year And Month:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#########################################################################
def top_earners_employees():
    limit = prompt_for_limit()
    employees = TasksDb.VIEWS.top_earners_employees(limit)
    print("Top Earners Employees:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#########################################################################
def top_busiest_employees():
    limit = prompt_for_limit()
    employees = TasksDb.VIEWS.top_busiest_employees(limit)
    print("Top Busiest Employees:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#########################################################################
def top_achievers_employees():
    limit = prompt_for_limit()
    employees = TasksDb.VIEWS.top_achievers_employees(limit)
    print("Top Achievers Employees:")
    print("----------------------------")
    for employee in employees:
        print(str(employee))
    print("----------------------------")
#########################################################################
print("############################")
print("SQLite Task Management App Started")
print("############################")
#########################################################################
# create a TaskDb instance and seed the database with random data
TasksDb.create("tasks.db")
#########################################################################
APP_ACTIONS = {
    "1": list_departments,
    "2": add_department,
    "3": update_department,
    "4": delete_department,
    "5": list_employees,
    "6": add_employee,
    "7": update_employee,
    "8": delete_employee,
    "9": list_tasks,
    "10": add_task,
    "11": update_task,
    "12": delete_task,
    "13": departments_members,
    "14": departments_members_by_type,
    "15": departments_members_by_gender,
    "16": employees_tasks,
    "17": employees_tasks_by_state,
    "18": employees_tasks_by_priority,
    "19": employees_experience_and_age_by_year,
    "20": employees_experience_and_age_by_year_and_month,
    "21": top_earners_employees,
    "22": top_busiest_employees,
    "23": top_achievers_employees
}
#########################################################################
APP_MENU = """
Please select an option:
-----------------------
0. Exit
1. List Departments
2. Add Department
3. Update Department
4. Delete Department
5. List Employees
6. Add Employee
7. Update Employee
8. Delete Employee
9. List Tasks
10. Add Task
11. Update Task
12. Delete Task
13. Departments Members
14. Departments Members By Type
15. Departments Members By Gender
16. Employees Tasks
17. Employees Tasks By State
18. Employees Tasks By Priority
19. Employees Experience And Age By Year
20. Employees Experience And Age By Year And Month
21. Top Earners Employees
22. Top Busiest Employees
23. Top Achievers Employees
Type the number of your selection:
"""
while (selection := input(APP_MENU)) != "0":
    APP_ACTIONS[selection]() if selection in APP_ACTIONS else print("Not an option. Please try again.")
#########################################################################
print("############################")
print("SQLite Task Management App Finished")
print("############################")
#########################################################################
