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
from task_db import TaskDb
from ic_config import icecream_config
############################################################################
# run the configuration for icecream
icecream_config()
############################################################################
ic("################################")
ic("Task Management App Started")
ic("################################")
############################################################################
# create a TaskDb instance and seed the database with random data
task_db = TaskDb()
task_db.seed()
# test get update a task
TASK_ID = "ffe3f9cc-631c-40af-923f-fca5839688be"
existed_task = task_db.get_task(TASK_ID)
if existed_task:
    ic(f"Task with id ({TASK_ID}) Found")
    ic("-------------------------------")
    # existed_task.title += " (The Title Updated Again)"
    # existed_task.description += " (The Description Updated Again)"
    # existed_task.priority = "low"
    # existed_task.state = "cancelled"
    # task_db.update_task(existed_task)
    task_db.delete_task(TASK_ID)
else:
    ic(f"Task with id ({TASK_ID}) Not Found")
    ic("-------------------------------")
############################################################################
ic("################################")
ic("Task Management App Finished")
ic("################################")
############################################################################
