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
print("############################")
print("SQLite Task Management App Started")
print("############################")
#######################################################################
# create a TaskDb instance and seed the database with random data
TasksDb.create("tasks.db")
print("Departments:")
print("----------------------------")
for department in TasksDb.DEPARTMENTS.get_all():
    print(str(department))
print("----------------------------")
#######################################################################
print("############################")
print("SQLite Task Management App Finished")
print("############################")
#######################################################################
