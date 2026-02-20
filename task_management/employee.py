#########################################################################################
from uuid import uuid4
from datetime import datetime
#########################################################################################
class Employee:
    EMPLOYEE_GENDERS = ["male", "female"]
    EMPLOYEE_STATES = ["full-time", "part-time", "internship", "retired", "unemployed"]

    def __init__(self, first_name: str, last_name: str, gender: str, email: str, phone_number: str, birth_date: str, hire_date: str, job_title: str, state: str, department_id: str):
        self.id = str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender if gender in self.EMPLOYEE_GENDERS else "male"
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.hire_date = hire_date
        self.job_title = job_title
        self.state = state if state in self.EMPLOYEE_STATES else "unemployed"
        self.department_id = department_id

    ### convert date to date object and get the current date then calculate years passed from the date
    def __get_years_from(self, date: str):
        from_date = datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.today().date()
        years = int(today.year - from_date.year)
        day_not_passed = (today.month, today.day) < (from_date.month, from_date.day)
        return (years - 1) if day_not_passed else years

    @property
    def age(self) -> int:
        return self.__get_years_from(self.birth_date)
    @property
    def work_experience(self):
        return self.__get_years_from(self.hire_date)

    def __str__(self):
        return f"""----------------
id: {self.id}
first_name: {self.first_name}
last_name: {self.last_name}
gender: {self.gender}
email: {self.email}
phone_number: {self.phone_number}
birth_date: {self.birth_date}
hire_date: {self.hire_date}
job_title: {self.job_title}
age: {self.age}
work_experience: {self.work_experience}
state: {self.state}
department_id: {self.department_id}
----------------"""
    def __repr__(self):
        return f"Employee({self.id}, {self.first_name}, {self.last_name}, {self.gender}, {self.email}, {self.phone_number}, {self.birth_date}, {self.hire_date}, {self.job_title}, {self.state}, {self.department_id})"
