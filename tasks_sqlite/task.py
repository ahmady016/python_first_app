###################################################################################
from icecream import ic as print   # pyright: ignore[reportMissingImports]
import re
from uuid6 import uuid7
from datetime import datetime
from sqlite_db import SqliteDb
###################################################################################

class Task:
    TASK_PRIORITIES = ["low", "medium", "high"]
    TASK_STATES = ["pending", "in_progress", "completed", "cancelled", "paused"]

    def __init__(self,
        title: str,
        description: str,
        create_date: str,
        due_date: str,
        complete_date: str,
        priority: str,
        state: str,
        employee_id: str,
        id: str = None,
        created_at: str = None,
        updated_at: str = None
    ):
        # Basic validation for required fields and formats
        if not title or len(title.strip()) < 3:
            raise ValueError("Task title is required and must be at least 3 characters long")
        if not description or len(description.strip()) < 10:
            raise ValueError("Task description is required and must be at least 10 characters long")

        if not create_date or not isinstance(create_date, str):
            raise ValueError("Task create_date is required and must be a string in ISO format")
        if not due_date or not isinstance(due_date, str):
            raise ValueError("Task due_date is required and must be a string in ISO format")

        if not priority or priority not in Task.TASK_PRIORITIES:
            raise ValueError(f"Task priority is required and must be one of {Task.TASK_PRIORITIES}")
        if not state or state not in Task.TASK_STATES:
            raise ValueError(f"Task state is required and must be one of {Task.TASK_STATES}")

        if not employee_id or not isinstance(employee_id, str):
            raise ValueError("Task employee_id is required and must be a string")

        # convert create_date, due_date and complete_date to datetime objects
        create_date_dt = datetime.fromisoformat(create_date)
        due_date_dt = datetime.fromisoformat(due_date)
        complete_date_dt = datetime.fromisoformat(complete_date)
        # Validate date constraints
        # due_date must be after create_date
        if due_date_dt <= create_date_dt:
            raise ValueError(f"due_date ({due_date}) must be after create_date ({create_date})")
        # complete_date must be after create_date
        if complete_date_dt <= create_date_dt:
            raise ValueError(f"complete_date ({complete_date}) must be after create_date ({create_date})")

        self.id = id if id else str(uuid7())
        self.title = title
        self.description = description
        self.create_date = create_date
        self.due_date = due_date
        self.complete_date = complete_date
        self.priority = priority
        self.state = state
        self.employee_id = employee_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"""
id: {self.id}
title: {self.title}
description: {self.description}
create_date: {self.create_date}
due_date: {self.due_date}
complete_date: {self.complete_date}
priority: {self.priority}
state: {self.state}
employee_id: {self.employee_id}
created_at: {self.created_at}
updated_at: {self.updated_at}
--------------"""
    def __repr__(self):
        return (
            f"Task(id={self.id}, title={self.title}, description={self.description}, "
            f"create_date={self.create_date}, due_date={self.due_date}, "
            f"complete_date={self.complete_date}, priority={self.priority}, "
            f"state={self.state}, employee_id={self.employee_id}), "
            f"created_at={self.created_at}, updated_at={self.updated_at}"
        )

    def __dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "create_date": self.create_date,
            "due_date": self.due_date,
            "complete_date": self.complete_date,
            "priority": self.priority,
            "state": self.state,
            "employee_id": self.employee_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
###################################################################################

class TasksTable():
    REQUIRED_FIELDS = ["title", "description", "create_date", "due_date", "employee_id"]
    UPDATABLE_FIELDS = ["title", "description", "create_date", "due_date", "complete_date", "priority", "state", "employee_id"]
    CREATE_TABLE_COMMAND = """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            create_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            complete_date TEXT NULL,
            priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'low',
            state TEXT NOT NULL CHECK (state IN ('pending', 'in_progress', 'completed', 'cancelled', 'paused')) DEFAULT 'pending',
            employee_id TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE ON UPDATE CASCADE
        );
    """
    CREATE_INDEX_COMMAND = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_title ON tasks (title);
    """

    @staticmethod
    def create():
        with SqliteDb.connect() as conn:
            conn.execute(TasksTable.CREATE_TABLE_COMMAND)
            conn.execute(TasksTable.CREATE_INDEX_COMMAND)
            SqliteDb.create_update_trigger("tasks")

    @staticmethod
    def count():
        count = 0
        with SqliteDb.connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        return int(count)

    @staticmethod
    def add_many(tasks: list[Task], mode: str = "all") -> list[str]:
        if not tasks:
            return []

        for task in tasks:
            if not all(field in task.__dict__() for field in TasksTable.REQUIRED_FIELDS):
                raise ValueError("Each task must have 'title', 'description', 'create_date', 'due_date' and 'employee_id'")

        fields_placeholder, values_placeholder = "", ""
        if mode == "required":
            fields_placeholder = ", ".join(TasksTable.REQUIRED_FIELDS)
            values_placeholder = ", ".join(":" + field for field in TasksTable.REQUIRED_FIELDS)
        else:
            fields_placeholder = ", ".join(TasksTable.UPDATABLE_FIELDS)
            values_placeholder = ", ".join(":" + field for field in TasksTable.UPDATABLE_FIELDS)

        insert_command = f"INSERT INTO tasks ({fields_placeholder}) VALUES ({values_placeholder});"
        with SqliteDb.connect() as conn:
            conn.executemany(insert_command, [task.__dict__() for task in tasks])
        print(f"Added {len(tasks)} tasks")
        return [task.id for task in tasks]

    @staticmethod
    def add(mode: str = "all", **kwargs) -> str:
        if not kwargs:
            raise ValueError("No task data provided")

        for field in TasksTable.REQUIRED_FIELDS:
            if field not in kwargs:
                raise ValueError(f"Missing required field: {field}")

        fields_placeholder, values_placeholder = "", ""
        if mode == "required":
            fields_placeholder = ", ".join(TasksTable.REQUIRED_FIELDS)
            values_placeholder = ", ".join(":" + field for field in TasksTable.REQUIRED_FIELDS)
        else:
            fields_placeholder = ", ".join(TasksTable.UPDATABLE_FIELDS)
            values_placeholder = ", ".join(":" + field for field in TasksTable.UPDATABLE_FIELDS)

        insert_command = f"INSERT INTO tasks ({fields_placeholder}) VALUES ({values_placeholder});"
        task = Task(**kwargs)
        with SqliteDb.connect() as conn:
            conn.execute(insert_command, task.__dict__())
        return task.id

    @staticmethod
    def update(id: str, **kwargs) -> bool:
        if not kwargs:
            raise ValueError("No task data provided")

        set_clauses = []
        params = {"id": id}
        for field, value in kwargs.items():
            if field in TasksTable.UPDATABLE_FIELDS:
                set_clauses.append(f"{field} = :{field}")
                params[field] = value

        if not set_clauses:
            raise ValueError("No valid fields to update")

        update_command = f"UPDATE tasks SET {", ".join(set_clauses)} WHERE id = :id;"
        with SqliteDb.connect() as conn:
            conn.execute(update_command, params)
        return conn.total_changes > 0

    @staticmethod
    def delete(id: str) -> bool:
        delete_command = "DELETE FROM tasks WHERE id = :id;"
        with SqliteDb.connect() as conn:
            conn.execute(delete_command, {"id": id})
        return conn.total_changes > 0

    @staticmethod
    def get_all() -> list[Task] | None:
        query = "SELECT * FROM tasks;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def get_by_id(id: str) -> Task | None:
        query = "SELECT * FROM tasks WHERE id = :id;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"id": id}).fetchone()
            if row:
                return Task(**row)
        return None

    @staticmethod
    def get_by_title(title: str) -> Task | None:
        query = "SELECT * FROM tasks WHERE title = :title;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"title": title}).fetchone()
            if row:
                return Task(**row)
        return None

    @staticmethod
    def get_by_state(state: str) -> list[Task] | None:
        query = "SELECT * FROM tasks WHERE state = :state;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"state": state}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def get_by_priority(priority: str) -> list[Task] | None:
        query = "SELECT * FROM tasks WHERE priority = :priority;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"priority": priority}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def get_by_employee_id(employee_id: str) -> list[Task] | None:
        query = "SELECT * FROM tasks WHERE employee_id = :employee_id;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"employee_id": employee_id}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def validate_date(date_str: str, field_name: str = "date") -> bool:
        if not date_str:
            raise ValueError(f"{field_name} is required")
        if not isinstance(date_str, str):
            raise TypeError(f"{field_name} must be a string")
        if not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
            raise ValueError(f"{field_name} must be in the format YYYY-MM-DD")

    @staticmethod
    def get_by_create_date(created_date: str) -> list[Task] | None:
        TasksTable.validate_date(created_date, "created_date")
        query = "SELECT * FROM tasks WHERE created_date = :created_date;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"created_date": created_date}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def get_by_due_date(due_date: str) -> list[Task] | None:
        TasksTable.validate_date(due_date, "due_date")
        query = "SELECT * FROM tasks WHERE due_date = :due_date;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"due_date": due_date}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None

    @staticmethod
    def get_by_complete_date(complete_date: str) -> list[Task] | None:
        TasksTable.validate_date(complete_date, "complete_date")
        query = "SELECT * FROM tasks WHERE complete_date = :complete_date;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query, {"complete_date": complete_date}).fetchall()
            if rows and len(rows) > 0:
                return [Task(**row) for row in rows]
        return None
##################################################################################
