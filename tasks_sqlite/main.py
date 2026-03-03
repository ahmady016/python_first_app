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
def list_departments(page=1, limit=5):
    print("Departments:")
    print("----------------------------")
    for department in TasksDb.DEPARTMENTS.get_page(page, limit):
        print(str(department))
    print("----------------------------")
#######################################################################
def list_employees(page=1, limit=5):
    print("Employees:")
    print("----------------------------")
    for employee in TasksDb.EMPLOYEES.get_page(page, limit):
        print(str(employee))
    print("----------------------------")
#######################################################################
def list_tasks(page=1, limit=5):
    print("Tasks:")
    print("----------------------------")
    for task in TasksDb.TASKS.get_page(page, limit):
        print(str(task))
    print("----------------------------")
#######################################################################
print("############################")
print("SQLite Task Management App Started")
print("############################")
#######################################################################
# create a TaskDb instance and seed the database with random data
TasksDb.create("tasks.db")
#######################################################################
APP_ACTIONS = {
    "1": list_departments,
    "2": list_employees,
    "3": list_tasks
}
#######################################################################
APP_MENU = """
Please select an option:
-----------------------
1. List Departments
2. List Employees
3. List Tasks
4. Exit
Type the number of your selection:
"""
while (selection := input(APP_MENU)) != "4":
    if selection in APP_ACTIONS:
        try:
            page = int(input("Enter page number: "))
            limit = int(input("Enter page size: "))
            APP_ACTIONS[selection](page, limit)
        except ValueError as error:
            print("not a number. Please try again.")
            print(error)
    else:
        print("Not an option. Please try again.")
#######################################################################
print("############################")
print("SQLite Task Management App Finished")
print("############################")
#######################################################################
