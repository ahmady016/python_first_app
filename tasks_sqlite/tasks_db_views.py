#####################################################################################
from sqlite_db import SqliteDb
from dataclasses import dataclass
#####################################################################################
# data classes for views results
#####################################################################################
@dataclass
class DepartmentMember:
    id: str
    name: str
    description: str
    employees: int
#####################################################################################
@dataclass
class DepartmentMemberByType:
    id: str
    name: str
    full_time: int
    part_time: int
    contractor: int
    internship: int
    total_employees: int
#####################################################################################
@dataclass
class DepartmentMemberByGender:
    id: str
    name: str
    male: int
    female: int
    total_employees: int
#####################################################################################
@dataclass
class EmployeeTask:
    id: str
    full_name: str
    birth_date: str
    gender: str
    email: str
    hire_date: str
    job_title: str
    job_type: str
    salary: float
    tasks: int
#####################################################################################
@dataclass
class EmployeeTaskByState:
    id: str
    full_name: str
    gender: str
    job_title: str
    job_type: str
    salary: float
    pending: int
    in_progress: int
    paused: int
    completed: int
    cancelled: int
    total_tasks: int
#####################################################################################
@dataclass
class EmployeeTaskByPriority:
    id: str
    full_name: str
    gender: str
    job_title: str
    job_type: str
    salary: float
    high: int
    medium: int
    low: int
    total_tasks: int
#####################################################################################
@dataclass
class EmployeeExperienceAndAgeByYear:
    id: str
    full_name: str
    gender: str
    job_title: str
    job_type: str
    salary: float
    age: float
    experience: float
#####################################################################################
@dataclass
class EmployeeExperienceAndAgeByYearAndMonth:
    id: str
    full_name: str
    gender: str
    job_title: str
    job_type: str
    salary: float
    age: str
    experience: str
#####################################################################################
@dataclass
class TopEarnerEmployee:
    id: str
    full_name: str
    birth_date: str
    gender: str
    email: str
    hire_date: str
    job_title: str
    job_type: str
    salary: float
#####################################################################################
@dataclass
class TopBusyEmployee:
    id: str
    full_name: str
    birth_date: str
    gender: str
    email: str
    hire_date: str
    job_title: str
    job_type: str
    salary: float
    tasks: int
#####################################################################################
@dataclass
class TopAchieverEmployee:
    id: str
    full_name: str
    birth_date: str
    gender: str
    email: str
    hire_date: str
    job_title: str
    job_type: str
    salary: float
    tasks: int
#####################################################################################
# all views class to create, drop and get results
#####################################################################################
class TasksDbViews:

    DEPARTMENTS_MEMBERS_VIEW = """
        CREATE VIEW IF NOT EXISTS departments_members_view AS
        SELECT
            dept.id,
            dept.name,
            dept.description,
            COUNT(emp.id) as employees
        FROM departments dept JOIN employees emp ON dept.id = emp.department_id
        GROUP BY dept.id
        ORDER BY employees DESC
    """

    DEPARTMENTS_MEMBERS_BY_TYPE_VIEW = """
        CREATE VIEW IF NOT EXISTS departments_members_by_type_view AS
        SELECT
            d.id,
            d.name,
            COUNT(CASE WHEN e.job_type = 'full-time' THEN 1 END) AS full_time,
            COUNT(CASE WHEN e.job_type = 'part-time' THEN 1 END) AS part_time,
            COUNT(CASE WHEN e.job_type = 'contractor' THEN 1 END) AS contractor,
            COUNT(CASE WHEN e.job_type = 'internship' THEN 1 END) AS internship,
            COUNT(e.id) AS total_employees
        FROM departments d LEFT JOIN employees e ON d.id = e.department_id
        GROUP BY d.id
        ORDER BY total_employees DESC
    """

    DEPARTMENTS_MEMBERS_BY_GENDER_VIEW = """
        CREATE VIEW IF NOT EXISTS departments_members_by_gender_view AS
        SELECT
            d.id,
            d.name,
            COUNT(CASE WHEN e.gender = 'male' THEN 1 END) AS male,
            COUNT(CASE WHEN e.gender = 'female' THEN 1 END) AS female,
            COUNT(e.id) AS total_employees
        FROM departments d LEFT JOIN employees e ON d.id = e.department_id
        GROUP BY d.id
        ORDER BY total_employees DESC
    """

    EMPLOYEES_TASKS_VIEW = """
        CREATE VIEW IF NOT EXISTS employees_tasks_view AS
        SELECT
            e.id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.birth_date,
            e.gender,
            e.email,
            e.hire_date,
            e.job_title,
            e.job_type,
            e.salary,
            COUNT(t.id) AS tasks
        FROM employees e LEFT JOIN tasks t ON e.id = t.employee_id
        GROUP BY e.id
        ORDER BY tasks DESC
    """

    EMPLOYEES_TASKS_BY_STATE_VIEW = """
        CREATE VIEW IF NOT EXISTS employees_tasks_by_state_view AS
        SELECT
            e.id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.gender,
            e.job_title,
            e.job_type,
            e.salary,
            COUNT(CASE WHEN t.state = 'pending' THEN 1 END) AS pending,
            COUNT(CASE WHEN t.state = 'in_progress' THEN 1 END) AS in_progress,
            COUNT(CASE WHEN t.state = 'paused' THEN 1 END) AS paused,
            COUNT(CASE WHEN t.state = 'completed' THEN 1 END) AS completed,
            COUNT(CASE WHEN t.state = 'cancelled' THEN 1 END) AS cancelled,
            COUNT(t.id) AS total_tasks
        FROM employees e LEFT JOIN tasks t ON e.id = t.employee_id
        GROUP BY e.id
        ORDER BY total_tasks DESC
    """

    EMPLOYEES_TASKS_BY_PRIORITY_VIEW = """
        CREATE VIEW IF NOT EXISTS employees_tasks_by_priority_view AS
        SELECT
            e.id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.gender,
            e.job_title,
            e.job_type,
            e.salary,
            COUNT(CASE WHEN t.priority = 'low' THEN 1 END) AS low,
            COUNT(CASE WHEN t.priority = 'medium' THEN 1 END) AS medium,
            COUNT(CASE WHEN t.priority = 'high' THEN 1 END) AS high,
            COUNT(t.id) AS total_tasks
        FROM employees e LEFT JOIN tasks t ON e.id = t.employee_id
        GROUP BY e.id
        ORDER BY total_tasks DESC
    """

    EMPLOYEES_EXPERIENCE_AND_AGE_BY_YEAR_VIEW = """
        CREATE VIEW IF NOT EXISTS employees_experience_and_age_by_year_view AS
        SELECT
            id,
            first_name || ' ' || last_name AS full_name,
            gender,
            job_title,
            job_type,
            salary,
            ROUND(CAST(CAST((julianday('now') - julianday(birth_date)) / 30.4375 AS FLOAT) / 12 AS FLOAT), 2) AS age,
            ROUND(CAST(CAST((julianday('now') - julianday(hire_date)) / 30.4375 AS FLOAT) / 12 AS FLOAT), 2) AS experience
        FROM employees
        ORDER BY experience DESC, age DESC
    """

    EMPLOYEES_EXPERIENCE_AND_AGE_BY_YEAR_AND_MONTH_VIEW = """
        CREATE VIEW IF NOT EXISTS employees_experience_and_age_by_year_and_month_view AS
        WITH total_months AS (
            SELECT
                id,
                first_name || ' ' || last_name AS full_name,
                gender,
                job_title,
                job_type,
                salary,
                CAST((julianday('now') - julianday(birth_date)) / 30.4375 AS INT) AS age_months,
                CAST((julianday('now') - julianday(hire_date)) / 30.4375 AS INT) AS experience_months
            FROM employees
        )
        SELECT
            id,
            full_name,
            gender,
            job_title,
            job_type,
            salary,
            (age_months / 12) || ' Years, ' || (age_months % 12) || ' Months' AS age,
            (experience_months / 12) || ' Years, ' || (experience_months % 12) || ' Months' AS experience
        FROM total_months
        ORDER BY experience_months DESC, age_months DESC
    """

    TOP_EARNERS_EMPLOYEES_VIEW = """
        CREATE VIEW IF NOT EXISTS top_earners_employees_view AS
        SELECT
            id,
            first_name || ' ' || last_name AS full_name,
            birth_date,
            gender,
            email,
            hire_date,
            job_title,
            job_type,
            salary
        FROM employees
        ORDER BY salary DESC
    """

    TOP_BUSIEST_EMPLOYEES_VIEW = """
        CREATE VIEW IF NOT EXISTS top_busiest_employees_view AS
        SELECT
            e.id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.birth_date,
            e.gender,
            e.email,
            e.hire_date,
            e.job_title,
            e.job_type,
            e.salary,
            COUNT(t.id) AS tasks
        FROM employees e JOIN tasks t ON e.id = t.employee_id
        WHERE t.state IN ('pending', 'in_progress', 'paused')
        GROUP BY e.id
        ORDER BY tasks DESC
    """

    TOP_ACHIEVERS_EMPLOYEES_VIEW = """
        CREATE VIEW IF NOT EXISTS top_achievers_employees_view AS
        SELECT
            e.id,
            e.first_name || ' ' || e.last_name AS full_name,
            e.birth_date,
            e.gender,
            e.email,
            e.hire_date,
            e.job_title,
            e.job_type,
            e.salary,
            COUNT(t.id) AS tasks
        FROM employees e JOIN tasks t ON e.id = t.employee_id
        WHERE t.state = 'completed'
        GROUP BY e.id
        ORDER BY tasks DESC
    """

    def create():
        with SqliteDb.connect() as conn:
            conn.execute(TasksDbViews.DEPARTMENTS_MEMBERS_VIEW)
            conn.execute(TasksDbViews.DEPARTMENTS_MEMBERS_BY_TYPE_VIEW)
            conn.execute(TasksDbViews.DEPARTMENTS_MEMBERS_BY_GENDER_VIEW)

            conn.execute(TasksDbViews.EMPLOYEES_TASKS_VIEW)
            conn.execute(TasksDbViews.EMPLOYEES_TASKS_BY_STATE_VIEW)
            conn.execute(TasksDbViews.EMPLOYEES_TASKS_BY_PRIORITY_VIEW)

            conn.execute(TasksDbViews.EMPLOYEES_EXPERIENCE_AND_AGE_BY_YEAR_VIEW)
            conn.execute(TasksDbViews.EMPLOYEES_EXPERIENCE_AND_AGE_BY_YEAR_AND_MONTH_VIEW)

            conn.execute(TasksDbViews.TOP_EARNERS_EMPLOYEES_VIEW)
            conn.execute(TasksDbViews.TOP_BUSIEST_EMPLOYEES_VIEW)
            conn.execute(TasksDbViews.TOP_ACHIEVERS_EMPLOYEES_VIEW)

    def drop():
        with SqliteDb.connect() as conn:
            conn.execute("DROP VIEW IF EXISTS departments_members_view;")
            conn.execute("DROP VIEW IF EXISTS departments_members_by_type_view;")
            conn.execute("DROP VIEW IF EXISTS departments_members_by_gender_view;")

            conn.execute("DROP VIEW IF EXISTS employees_tasks_view;")
            conn.execute("DROP VIEW IF EXISTS employees_tasks_by_state_view;")
            conn.execute("DROP VIEW IF EXISTS employees_tasks_by_priority_view;")

            conn.execute("DROP VIEW IF EXISTS employees_experience_and_age_by_year_view;")
            conn.execute("DROP VIEW IF EXISTS employees_experience_and_age_by_year_and_month_view;")

            conn.execute("DROP VIEW IF EXISTS top_earners_employees_view;")
            conn.execute("DROP VIEW IF EXISTS top_busiest_employees_view;")
            conn.execute("DROP VIEW IF EXISTS top_achievers_employees_view;")

    def departments_members(page: int = 1, size: int = 10) -> list[DepartmentMember]:
        query = "SELECT * FROM departments_members_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [DepartmentMember(**row) for row in result]

    def departments_members_by_type(page: int = 1, size: int = 10) -> list[DepartmentMemberByType]:
        query = "SELECT * FROM departments_members_by_type_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [DepartmentMemberByType(**row) for row in result]

    def departments_members_by_gender(page: int = 1, size: int = 10) -> list[DepartmentMemberByGender]:
        query = "SELECT * FROM departments_members_by_gender_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [DepartmentMemberByGender(**row) for row in result]

    def employees_tasks(page: int = 1, size: int = 10) -> list[EmployeeTask]:
        query = "SELECT * FROM employees_tasks_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [EmployeeTask(**row) for row in result]

    def employees_tasks_by_state(page : int = 1, size: int = 10) -> list[EmployeeTaskByState]:
        query = "SELECT * FROM employees_tasks_by_state_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [EmployeeTaskByState(**row) for row in result]

    def employees_tasks_by_priority(page: int = 1, size: int = 10) -> list[EmployeeTaskByPriority]:
        query = "SELECT * FROM employees_tasks_by_priority_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [EmployeeTaskByPriority(**row) for row in result]

    def employees_experience_and_age_by_year(
        page : int = 1,
        size: int = 10
    ) -> list[EmployeeExperienceAndAgeByYear]:
        query = "SELECT * FROM employees_experience_and_age_by_year_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [EmployeeExperienceAndAgeByYear(**row) for row in result]

    def employees_experience_and_age_by_year_and_month(
        page : int = 1,
        size: int = 10
    ) -> list[EmployeeExperienceAndAgeByYearAndMonth]:
        query = "SELECT * FROM employees_experience_and_age_by_year_and_month_view LIMIT :limit OFFSET :offset;"
        params = {"limit": size, "offset": (page - 1) * size}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [EmployeeExperienceAndAgeByYearAndMonth(**row) for row in result]

    def top_earners_employees(limit: int = 5) -> list[TopEarnerEmployee]:
        query = "SELECT * FROM top_earners_employees_view LIMIT :limit;"
        params = {"limit": limit}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [TopEarnerEmployee(**row) for row in result]

    def top_busiest_employees(limit: int = 5) -> list[TopBusyEmployee]:
        query = "SELECT * FROM top_busiest_employees_view LIMIT :limit;"
        params = {"limit": limit}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [TopBusyEmployee(**row) for row in result]

    def top_achievers_employees(limit: int = 5) -> list[TopAchieverEmployee]:
        query = "SELECT * FROM top_achievers_employees_view LIMIT :limit;"
        params = {"limit": limit}
        with SqliteDb.connect() as conn:
            result = conn.execute(query, params).fetchall()
        return [TopAchieverEmployee(**row) for row in result]
