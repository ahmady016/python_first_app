############################################################################
from faker import Faker     # pyright: ignore[reportMissingImports]
from icecream import ic     # pyright: ignore[reportMissingImports]
from datetime import timedelta
from json_database import JsonDatabase
from department import Department
from employee import Employee
from task import Task
############################################################################

class TaskDb:
    # create a Faker instance as a class variable to be used in all methods
    FAKE = Faker()

    # create a JsonDatabase instance with folder path
    def __init__(self, db_path: str = ".db"):
        self.db = JsonDatabase(db_path)

    # generate random range of departments
    @staticmethod
    def __random_departments(min_count: int = 10, max_count: int = 15) -> list[Department]:
        return [
            Department(TaskDb.FAKE.company(), TaskDb.FAKE.catch_phrase())
            for _ in range(TaskDb.FAKE.random_int(min_count, max_count))
        ]

    # generate random range of employees and assign them to random departments
    @staticmethod
    def __random_employees(
        departments: list[Department],
        min_count: int = 100,
        max_count: int = 200
    ) -> list[Employee]:
        return  [
            Employee(
                TaskDb.FAKE.first_name(),
                TaskDb.FAKE.last_name(),
                TaskDb.FAKE.random_element(Employee.EMPLOYEE_GENDERS),
                TaskDb.FAKE.email(),
                TaskDb.FAKE.phone_number(),
                TaskDb.FAKE.date_of_birth(minimum_age=20, maximum_age=60).strftime("%Y-%m-%d"),
                TaskDb.FAKE.date_between(start_date="-14y", end_date="today").strftime("%Y-%m-%d"),
                TaskDb.FAKE.job(),
                TaskDb.FAKE.random_element(Employee.EMPLOYEE_STATES),
                TaskDb.FAKE.random_element(departments).id
            )
            for _ in range(TaskDb.FAKE.random_int(min_count, max_count))
        ]

    # generate random range of tasks and assign them to random employees
    @staticmethod
    def __random_tasks(
        employees: list[Employee],
        min_count: int = 360,
        max_count: int = 640
    ) -> list[Task]:
        tasks = []
        for _ in range(TaskDb.FAKE.random_int(min_count, max_count)):
            # generate created_at datetime
            created_at = TaskDb.FAKE.date_time_between(start_date="-360d", end_date="now")
            # generate due_date datetime that is after created_at
            due_date = created_at + timedelta(days=TaskDb.FAKE.random_int(1, 30))
            # generate completed_at datetime that is after due_date
            completed_at_start_date = TaskDb.FAKE.random_element([created_at, due_date])
            completed_at = completed_at_start_date + timedelta(days=TaskDb.FAKE.random_int(1, 30))
            # create a task object and append it to the tasks list
            task = Task(
                TaskDb.FAKE.sentence(nb_words=TaskDb.FAKE.random_int(3, 7)),
                TaskDb.FAKE.sentence(nb_words=TaskDb.FAKE.random_int(20, 50)),
                created_at.strftime("%Y-%m-%d %H:%M:%S"),
                due_date.strftime("%Y-%m-%d %H:%M:%S"),
                completed_at.strftime("%Y-%m-%d %H:%M:%S"),
                TaskDb.FAKE.random_element(Task.TASK_PRIORITIES),
                TaskDb.FAKE.random_element(Task.TASK_STATES),
                TaskDb.FAKE.random_element(employees).id
            )
            tasks.append(task)
        return tasks

    # save departments list to the JSON database
    def save_departments(self, departments: list[Department]):
        for department in departments:
            self.db.save_record("departments", department.id, department)

    # save employees list to the JSON database
    def save_employees(self, employees: list[Employee]):
        for employee in employees:
            self.db.save_record("employees", employee.id, employee)

    # save tasks list to the JSON database
    def save_tasks(self, tasks: list[Task]):
        for task in tasks:
            self.db.save_record("tasks", task.id, task)

    # save all departments, employees and tasks to the JSON database
    def save_all(self, departments: list[Department], employees: list[Employee], tasks: list[Task]):
        self.save_departments(departments)
        self.save_employees(employees)
        self.save_tasks(tasks)

    # check if the database is seeded with data
    def __data_seeded(self) -> bool:
        if self.db.entities_dict and any(count > 0 for count in self.db.entities_dict.values()):
            return True
        return False

    # seed the database with random range of departments, employees and tasks
    # and save all of them to the JSON database
    def seed(self):
        if not self.__data_seeded():
            departments = self.__random_departments()
            ic(f"({len(departments)}) Departments Created:")
            ic("-------------------------")

            employees = self.__random_employees(departments)
            ic(f"({len(employees)}) Employees Created:")
            ic("-------------------------")

            tasks = self.__random_tasks(employees)
            ic(f"({len(tasks)}) Tasks Created:")
            ic("-------------------------")

            self.save_all(departments, employees, tasks)
            ic("Data Saved To JSON Database:")
            ic("-------------------------")
        else:
            ic("Data Already Seeded in JSON Database:")
            ic("-------------------------")

        ic("Task Management Database State:")
        ic("-------------------------")
        ic(self.db.entities_dict)
        ic("-------------------------")
