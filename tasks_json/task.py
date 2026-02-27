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
        create_date: str,
        due_date: str,
        complete_date: str,
        priority: str,
        state: str,
        employee_id: str,
        id: str = "",
        created_at: str = "",
        updated_at: str = ""
    ):
        # Validate date constraints
        # convert created_at, due_date and completed_at to datetime objects
        create_date_dt = datetime.fromisoformat(create_date)
        due_date_dt = datetime.fromisoformat(due_date)
        complete_date_dt = datetime.fromisoformat(complete_date)
        # due_date must be after created_at
        if due_date_dt <= create_date_dt:
            raise ValueError(
                f"due_date ({due_date}) must be after create_date ({create_date})"
            )
        # completed_at must be after created_at
        if complete_date_dt <= create_date_dt:
            raise ValueError(
                f"complete_date ({complete_date}) must be after create_date ({create_date})"
            )

        self.id = id if id else str(uuid4())
        self.title = title
        self.description = description
        self.create_date = create_date
        self.due_date = due_date
        self.complete_date = complete_date
        self.priority = priority if priority in self.TASK_PRIORITIES else "normal"
        self.state = state if state in self.TASK_STATES else "pending"
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
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )

    def __eq__(self, other):
        return self.id == other.id and self.title == other.title

    def __hash__(self):
        return hash((self.id, self.title))
