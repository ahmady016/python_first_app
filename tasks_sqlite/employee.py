###################################################################################
from icecream import ic as print   # pyright: ignore[reportMissingImports]
import re
from uuid6 import uuid7
from datetime import datetime
from sqlite_db import SqliteDb
###################################################################################

class Employee:
    JOB_TYPES = ["full-time", "part-time", "contractor", "internship"]
    GENDERS = ["male", "female"]
    def __init__(self,
        first_name: str,
        last_name: str,
        gender: str,
        birth_date: str,
        mobile: str,
        email: str,
        hire_date: str,
        job_title: str,
        job_type: str,
        salary: float,
        department_id: str,
        id: str = None,
        created_at = None,
        updated_at = None
    ):
        # Basic validation for required fields and formats
        # Validate first name and last name
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")
        # Validate mobile number presence
        if not mobile:
            raise ValueError(f"Mobile number is required")
        # Validate job type
        if job_type not in Employee.JOB_TYPES:
            raise ValueError(f"Invalid job type: {job_type}. Must be one of {Employee.JOB_TYPES}")
        # validate gender
        if gender not in Employee.GENDERS:
            raise ValueError(f"Invalid gender: {gender}. Must be one of {Employee.GENDERS}")
        # Simple email validation with regex
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(f"Invalid email: {email}")
        # Validate birth date and hire date presence
        # and date formats and logical consistency
        if not birth_date or not hire_date:
            raise ValueError("Birth date and hire date are required")
        birth_date_dt = datetime.fromisoformat(birth_date)
        hire_date_dt = datetime.fromisoformat(hire_date)
        if hire_date_dt < birth_date_dt:
            raise ValueError(f"Hire date {hire_date} cannot be before birth date {birth_date}")
        # validate salary presence and range
        if not salary:
            raise ValueError("Salary is required")
        if not isinstance(salary, (int, float)):
            raise ValueError("Salary must be a number")
        if salary < 4000 or salary > 24000:
            raise ValueError("Salary must be between 4000 and 24000")
        # validate department_id presence and type
        if not department_id or not isinstance(department_id, str):
            raise ValueError("department_id is required and must be a string")

        self.id = id if id else str(uuid7())
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.mobile = mobile
        self.hire_date = hire_date
        self.job_title = job_title
        self.job_type = job_type
        self.salary = salary
        self.department_id = department_id
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    @property
    def age(self):
        birth_date_dt = datetime.fromisoformat(self.birth_date)
        today = datetime.today()
        age = today.year - birth_date_dt.year - ((today.month, today.day) < (birth_date_dt.month, birth_date_dt.day))
        return age
    @property
    def years_of_service(self):
        hire_date_dt = datetime.fromisoformat(self.hire_date)
        today = datetime.today()
        years = today.year - hire_date_dt.year - ((today.month, today.day) < (hire_date_dt.month, hire_date_dt.day))
        return years

    def __str__(self):
        return f"""
id: {self.id}
full_name: {self.full_name}
gender: {self.gender}
age: {self.age}
birth_date: {self.birth_date}
email: {self.email}
mobile: {self.mobile}
hire_date: {self.hire_date}
years_of_service: {self.years_of_service}
job_title: {self.job_title}
job_type: {self.job_type}
salary: {self.salary}
department_id: {self.department_id}
created_at: {self.created_at}
updated_at: {self.updated_at}
----------------"""
    def __repr__(self):
        return f"Employee(id={self.id}, full_name={self.full_name}, gender={self.gender}, age={self.age}, birth_date={self.birth_date}, email={self.email}, mobile={self.mobile}, hire_date={self.hire_date}, years_of_service={self.years_of_service}, job_title={self.job_title}, job_type={self.job_type}, salary={self.salary}, department_id={self.department_id}, created_at={self.created_at}, updated_at={self.updated_at})"
    def __dict__(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "email": self.email,
            "mobile": self.mobile,
            "hire_date": self.hire_date,
            "years_of_service": self.years_of_service,
            "job_title": self.job_title,
            "job_type": self.job_type,
            "salary": self.salary,
            "department_id": self.department_id
        }
#################################################################################

class EmployeeTable():
    REQUIRED_FIELDS = ["id", "first_name", "last_name", "gender", "birth_date", "email", "mobile", "hire_date", "job_title", "job_type", "salary", "department_id"]
    UPDATABLE_FIELDS = REQUIRED_FIELDS[1:]
    CREATE_TABLE_COMMAND = """
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                job_title TEXT NOT NULL,
                job_type TEXT NOT NULL,
                salary FLOAT NOT NULL,
                department_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """
    CREATE_INDEX_COMMAND = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
    """

    @staticmethod
    def create():
        with SqliteDb.connect() as conn:
            conn.execute(EmployeeTable.CREATE_TABLE_COMMAND)
            conn.execute(EmployeeTable.CREATE_INDEX_COMMAND)
            SqliteDb.create_update_trigger("employees")

    @staticmethod
    def count() -> int:
        with SqliteDb.connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM employees;").fetchone()[0]
        return int(count)

    @staticmethod
    def add_many(employees: list[Employee]) -> list[str]:
        if not employees:
            return []

        for emp in employees:
            for field in EmployeeTable.REQUIRED_FIELDS:
                if field not in emp.__dict__():
                    raise ValueError(f"Missing required field: {field}")

        fields_placeholder = ", ".join(EmployeeTable.REQUIRED_FIELDS)
        values_placeholder = ", ".join(":" + field for field in EmployeeTable.REQUIRED_FIELDS)
        insert_command = f"INSERT INTO employees ({fields_placeholder}) VALUES ({values_placeholder});"
        with SqliteDb.connect() as conn:
            conn.executemany(insert_command, [emp.__dict__() for emp in employees])

        print(f"Added {len(employees)} employees")
        return [emp.id for emp in employees]

    @staticmethod
    def add(**kwargs) -> str:
        if not kwargs:
            raise ValueError("No employee data provided")

        for field in EmployeeTable.REQUIRED_FIELDS:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        fields_placeholder = ", ".join(EmployeeTable.REQUIRED_FIELDS)
        values_placeholder = ", ".join(":" + field for field in EmployeeTable.REQUIRED_FIELDS)
        insert_command = f"INSERT INTO employees ({fields_placeholder}) VALUES ({values_placeholder});"
        employee = Employee(**kwargs)
        with SqliteDb.connect() as conn:
            conn.execute(insert_command, employee.__dict__())

        print(f"employee with id: ({employee.id}) was added successfully")
        return employee.id

    @staticmethod
    def update(id: str, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clauses = []
        params = {"id": id}
        for field, value in kwargs.items():
            if field in EmployeeTable.UPDATABLE_FIELDS:
                set_clauses.append(f"{field} = :{field}")
                params[field] = value

        if not set_clauses:
            raise ValueError("No valid fields to update")

        update_query = f"UPDATE employees SET {', '.join(set_clauses)} WHERE id = :id;"
        with SqliteDb.connect() as conn:
            conn.execute(update_query, params)

        print(f"employee with id: ({id}) was updated successfully")
        return conn.total_changes > 0

    @staticmethod
    def delete(id: str) -> bool:
        delete_query = """
            DELETE FROM employees WHERE id = :id;
        """
        with SqliteDb.connect() as conn:
            conn.execute(delete_query, {"id": id})

        print(f"employee with id: ({id}) was deleted successfully")
        return conn.total_changes > 0

    @staticmethod
    def get_all() -> list[Employee] | None:
        query = "SELECT * FROM employees;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query).fetchall()
            if rows and len(rows) > 0:
                return [Employee(**row) for row in rows]
        return None

    @staticmethod
    def get_page(page: int, size: int) -> list[Employee] | None:
        query = f"SELECT * FROM employees LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, params).fetchall()
            if rows and len(rows) > 0:
                return [Employee(**row) for row in rows]
        return None

    @staticmethod
    def get_by_id(id: str) -> Employee | None:
        query = "SELECT * FROM employees WHERE id = :id;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"id": id}).fetchone()
            if row:
                return Employee(**row)
        return None

    @staticmethod
    def get_by_email(email: str) -> Employee | None:
        query = "SELECT * FROM employees WHERE email = :email;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"email": email}).fetchone()
            if row:
                return Employee(**row)
        return None

    @staticmethod
    def get_by_department_id(department_id: str) -> list[Employee] | None:
        query = "SELECT * FROM employees WHERE department_id = :department_id;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"department_id": department_id}).fetchall()
            if rows and len(rows) > 0:
                return [Employee(**row) for row in rows]
        return None
