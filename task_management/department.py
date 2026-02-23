######################################################################################
from uuid import uuid4
######################################################################################
class Department:
    def __init__(self,
        name: str,
        description: str,
        id: str = "",
        employees_count: int = 0,
        created_at: str = "",
        updated_at: str = ""
    ):
        self.id = id if id else str(uuid4())
        self.name = name
        self.description = description
        self.employees_count = employees_count
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"""
id: {self.id}
name: {self.name}
description: {self.description}
employees: ({self.employees_count})
created_at: {self.created_at}
updated_at: {self.updated_at}
----------------"""
    def __repr__(self):
        return f"Department(id={self.id}, name={self.name}, description={self.description}, employees={self.employees_count}, created_at={self.created_at}, updated_at={self.updated_at})"
