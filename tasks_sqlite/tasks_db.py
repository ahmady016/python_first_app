#####################################################################################
from icecream import ic as print   # pyright: ignore[reportMissingImports]
from faker import Faker     # pyright: ignore[reportMissingImports]
from datetime import timedelta

from sqlite_db import SqliteDb
from department import DepartmentTable, Department
from employee import EmployeeTable, Employee
from task import TasksTable, Task
#####################################################################################
class TasksDb:
    FAKER = Faker()
    ENTITIES_STATES = {
        "departments": 0,
        "employees": 0,
        "tasks": 0
    }
    DEPARTMENTS = DepartmentTable
    EMPLOYEES = EmployeeTable
    TASKS = TasksTable

    @staticmethod
    def create(db_path: str = None):
        # check if database path is provided
        if not db_path:
            raise ValueError("Database path is required")

        # create database and tables
        SqliteDb.create(db_path)
        DepartmentTable.create()
        EmployeeTable.create()
        TasksTable.create()
        print("Database created successfully")

        if not TasksDb.has_data():
            # seed the database
            TasksDb.seed()
            print("Database seeded successfully")
        else:
            print("Database is already populated with data")
            # set the entities stats
            TasksDb.set_entities_stats()
            # print entities stats
            TasksDb.print_entities_stats()

    @staticmethod
    def set_entities_stats():
        TasksDb.ENTITIES_STATES = {
            "departments": DepartmentTable.count(),
            "employees": EmployeeTable.count(),
            "tasks": TasksTable.count()
        }

    @staticmethod
    def print_entities_stats():
        print(f"Entities Stats: {TasksDb.ENTITIES_STATES}")
        print("-------------------------")

    # generate random range of departments
    @staticmethod
    def random_departments(
        min_count: int = 10,
        max_count: int = 15
    ) -> list[Department]:
        return [
            Department(TasksDb.FAKER.company(), TasksDb.FAKER.catch_phrase())
            for _ in range(TasksDb.FAKER.random_int(min_count, max_count))
        ]

    # generate random range of employees
    @staticmethod
    def random_employees(
        departments: list[Department],
        min_count: int = 100,
        max_count: int = 200
    ) -> list[Employee]:
        random_gender = TasksDb.FAKER.random_element(Employee.GENDERS)
        return  [
            Employee(
                TasksDb.FAKER.first_name(),
                TasksDb.FAKER.last_name(),
                random_gender,
                TasksDb.FAKER.date_of_birth(minimum_age=20, maximum_age=60).strftime("%Y-%m-%d"),
                TasksDb.FAKER.phone_number(),
                TasksDb.FAKER.email(),
                TasksDb.FAKER.date_between(start_date="-14y", end_date="today").strftime("%Y-%m-%d"),
                TasksDb.FAKER.job(),
                TasksDb.FAKER.random_element(Employee.JOB_TYPES),
                TasksDb.FAKER.random_element(departments).id
            )
            for _ in range(TasksDb.FAKER.random_int(min_count, max_count))
        ]

    # generate random range of tasks
    @staticmethod
    def random_tasks(
        employees: list[Employee],
        min_count: int = 360,
        max_count: int = 640
    ) -> list[Task]:
        tasks = []
        for _ in range(TasksDb.FAKER.random_int(min_count, max_count)):
            # generate created_at datetime
            created_date = TasksDb.FAKER.date_time_between(start_date="-360d", end_date="now")
            # generate due_date datetime that is after created_at
            due_date = created_date + timedelta(days=TasksDb.FAKER.random_int(1, 30))
            # generate completed_at datetime that is after due_date
            completed_at_start_date = TasksDb.FAKER.random_element([created_date, due_date])
            complete_date = completed_at_start_date + timedelta(days=TasksDb.FAKER.random_int(1, 30))
            # create a task object and append it to the tasks list
            task = Task(
                TasksDb.FAKER.sentence(nb_words=TasksDb.FAKER.random_int(3, 7)),
                TasksDb.FAKER.sentence(nb_words=TasksDb.FAKER.random_int(20, 50)),
                created_date.strftime("%Y-%m-%d %H:%M:%S"),
                due_date.strftime("%Y-%m-%d %H:%M:%S"),
                complete_date.strftime("%Y-%m-%d %H:%M:%S"),
                TasksDb.FAKER.random_element(Task.TASK_PRIORITIES),
                TasksDb.FAKER.random_element(Task.TASK_STATES),
                TasksDb.FAKER.random_element(employees).id
            )
            tasks.append(task)
        return tasks

    @staticmethod
    def save_all(
        departments: list[Department],
        employees: list[Employee],
        tasks: list[Task]
    ):
        DepartmentTable.add_many(departments)
        EmployeeTable.add_many(employees)
        TasksTable.add_many(tasks)

    @staticmethod
    def has_data():
        return (
            DepartmentTable.count() > 0 and
            EmployeeTable.count() > 0 and
            TasksTable.count() > 0
        )

    @staticmethod
    def seed():
        departments = TasksDb.random_departments()
        employees = TasksDb.random_employees(departments)
        tasks = TasksDb.random_tasks(employees)
        # save random data to the database
        TasksDb.save_all(departments, employees, tasks)
        # set the entities stats
        TasksDb.set_entities_stats()
        # print entities stats
        TasksDb.print_entities_stats()
