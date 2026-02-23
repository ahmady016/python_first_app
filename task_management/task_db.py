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
    # create a dictionary to store all entities in memory for easy access and manipulation
    ENTITIES = {}

    # create a JsonDatabase instance with folder path
    def __init__(self, db_path: str = ".db"):
        # create a JsonDatabase instance with base path
        self.__db = JsonDatabase(db_path)
        # if the database has data then load all entities from database files
        # and convert them to their respective classes
        # and store them in the ENTITIES dictionary class variable
        # for easy access and manipulation
        if self.__has_data():
            TaskDb.ENTITIES = {
                "departments": {dept["id"]: Department(**dept) for dept in self.__db.get_all_records("departments")},
                "employees": {emp["id"]: Employee(**emp) for emp in self.__db.get_all_records("employees")},
                "tasks": {task["id"]: Task(**task) for task in self.__db.get_all_records("tasks")}
            }
            # print entities stats
            self.print_entities_stats()
            # print departments info
            self.print_departments_info()
            # print employees info
            self.print_employees_info()
            # print tasks info
            self.print_tasks_info()

    def print_entities_stats(self):
        ic("Task Management Database State:")
        ic("-------------------------")
        ic(self.entities_stats)
        ic("-------------------------")

    def print_departments_info(self):
        ic("Departments info:")
        ic("-------------------------")
        for department in TaskDb.ENTITIES.get("departments", {}).values():
            department_info = self.get_department_info(department.id)
            ic(department_info)
        ic("-------------------------")

    def print_employees_info(self):
        ic("Employees info:")
        ic("-------------------------")
        for employee in TaskDb.ENTITIES.get("employees", {}).values():
            employee_info = self.get_employee_info(employee.id)
            ic(employee_info)
        ic("-------------------------")

    def print_tasks_info(self):
        ic("Tasks info:")
        ic("-------------------------")
        for task in TaskDb.ENTITIES.get("tasks", {}).values():
            ic(task)
        ic("-------------------------")

    def get_department_info(self, department_id: str) -> Department | None:
        if department_id in TaskDb.ENTITIES.get("departments"):
            department = TaskDb.ENTITIES["departments"][department_id]
            department.employees_count = sum(
                1 for employee in TaskDb.ENTITIES.get("employees", {}).values()
                if employee.department_id == department_id
            )
            return department
        return None

    def get_employee_info(self, employee_id: str) -> Employee | None:
        if employee_id in TaskDb.ENTITIES.get("employees"):
            employee = TaskDb.ENTITIES["employees"][employee_id]
            employee.tasks_count = sum(
                1 for task in TaskDb.ENTITIES.get("tasks", {}).values()
                if task.employee_id == employee_id
            )
            return employee
        return None

    @property
    def entities_stats(self) -> dict[str, int]:
        return self.__db.entities_dict
    @property
    def departments_count(self) -> int:
        return self.__db.get_records_count("departments")
    @property
    def employees_count(self) -> int:
        return self.__db.get_records_count("employees")
    @property
    def tasks_count(self) -> int:
        return self.__db.get_records_count("tasks")

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
            self.__db.save_record("departments", department.id, department)

    # save employees list to the JSON database
    def save_employees(self, employees: list[Employee]):
        for employee in employees:
            self.__db.save_record("employees", employee.id, employee)

    # save tasks list to the JSON database
    def save_tasks(self, tasks: list[Task]):
        for task in tasks:
            self.__db.save_record("tasks", task.id, task)

    # save all departments, employees and tasks to the JSON database
    def save_all(
        self,
        departments: list[Department],
        employees: list[Employee],
        tasks: list[Task]
    ) -> None:
        self.save_departments(departments)
        self.save_employees(employees)
        self.save_tasks(tasks)

    # check if the database is seeded with data
    def __has_data(self) -> bool:
        if self.__db.entities_dict and any(count > 0 for count in self.__db.entities_dict.values()):
            return True
        return False

    # seed the database with random range of departments, employees and tasks
    # and save all of them to the JSON database
    def seed(self):
        if not self.__has_data():
            departments = self.__random_departments()
            ic(f"({len(departments)}) Departments Generated")
            ic("-------------------------")

            employees = self.__random_employees(departments)
            ic(f"({len(employees)}) Employees Generated")
            ic("-------------------------")

            tasks = self.__random_tasks(employees)
            ic(f"({len(tasks)}) Tasks Generated")
            ic("-------------------------")

            TaskDb.ENTITIES = {
                "departments": {department.id: department for department in departments},
                "employees": {employee.id: employee for employee in employees},
                "tasks": {task.id: task for task in tasks}
            }

            self.save_all(departments, employees, tasks)
            ic("Data Saved To JSON Database:")
            ic("-------------------------")
        else:
            ic("Data Already Seeded in JSON Database:")
            ic("-------------------------")

        # print entities stats
        self.print_entities_stats()
        # print departments info
        self.print_departments_info()
        # print employees info
        self.print_employees_info()
        # print tasks info
        self.print_tasks_info()
