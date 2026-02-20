###############################################################################
from uuid import uuid4
from datetime import datetime
###############################################################################


class Task:
    TASK_PRIORITIES = ["low", "normal", "high", "urgent"]
    TASK_STATES = ["pending", "in-progress", "paused", "completed", "cancelled"]

    def __init__(
        self,
        title: str,
        description: str,
        created_at: str,
        due_date: str,
        completed_at: str,
        priority: str,
        state: str,
        employee_id: str,
    ):
        # Validate date constraints
        # convert created_at, due_date and completed_at to datetime objects
        created_at_dt = datetime.fromisoformat(created_at)
        due_date_dt = datetime.fromisoformat(due_date)
        completed_at_dt = datetime.fromisoformat(completed_at)
        # due_date must be after created_at
        if due_date_dt <= created_at_dt:
            raise ValueError(
                f"due_date ({due_date}) must be after created_at ({created_at})"
            )
        # completed_at must be after created_at
        if completed_at_dt <= created_at_dt:
            raise ValueError(
                f"completed_at ({completed_at}) must be after created_at ({created_at})"
            )

        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.created_at = created_at
        self.due_date = due_date
        self.completed_at = completed_at
        self.priority = priority if priority in self.TASK_PRIORITIES else "normal"
        self.state = state if state in self.TASK_STATES else "pending"
        self.employee_id = employee_id

    def __str__(self):
        return f"""----------------
id: {self.id}
title: {self.title}
description: {self.description}
created_at: {self.created_at}
due_date: {self.due_date}
completed_at: {self.completed_at}
priority: {self.priority}
state: {self.state}
employee_id: {self.employee_id}
----------------"""

    def __repr__(self):
        return (
            f"Task({self.id}, {self.title}, {self.description}, "
            f"{self.created_at}, {self.due_date}, {self.completed_at}, "
            f"{self.priority}, {self.state}, {self.employee_id})"
        )

    def __eq__(self, other):
        return self.id == other.id and self.title == other.title

    def __hash__(self):
        return hash((self.id, self.title))
