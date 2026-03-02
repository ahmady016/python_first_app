#######################################################################
from icecream import ic as print   # pyright: ignore[reportMissingImports]
from uuid6 import uuid7
from sqlite_db import SqliteDb
#######################################################################

class Department:
    def __init__(self,
        name: str,
        description: str,
        id: str = None,
        created_at: str = None,
        updated_at: str = None
    ):
        # Basic validation for required fields
        if not name or len(name.strip()) < 3:
            raise ValueError("Department name is required and must be at least 3 characters long")
        if not description or len(description.strip()) < 10:
            raise ValueError("Department description is required and must be at least 10 characters long")

        self.id = id if id else str(uuid7())
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"""
id: {self.id}
name: {self.name}
description: {self.description}
created_at: {self.created_at}
updated_at: {self.updated_at}
----------------"""
    def __repr__(self):
        return f"Department(id={self.id}, name={self.name}, description={self.description}, created_at={self.created_at}, updated_at={self.updated_at})"

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class DepartmentTable():
    UPDATABLE_FIELDS = ["name", "description"]
    CREATE_TABLE_COMMAND = """
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    CREATE_INDEX_COMMAND = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_departments_name ON departments (name);
    """

    @staticmethod
    def create():
        with SqliteDb.connect() as conn:
            conn.execute(DepartmentTable.CREATE_TABLE_COMMAND)
            conn.execute(DepartmentTable.CREATE_INDEX_COMMAND)
            SqliteDb.create_update_trigger("departments")

    @staticmethod
    def count() -> int:
        count = 0
        with SqliteDb.connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM departments;").fetchone()[0]
        return int(count)

    @staticmethod
    def add_many(departments: list[Department]) -> list[str]:
        if not departments:
            return []

        for dept in departments:
            if not all(field in dept.__dict__() for field in DepartmentTable.UPDATABLE_FIELDS):
                raise ValueError("Each department must have 'name' and 'description'")

        insert_command = """
            INSERT INTO departments (id, name, description)
            VALUES (:id, :name, :description);
        """
        with SqliteDb.connect() as conn:
            conn.executemany(insert_command, [dept.__dict__() for dept in departments])
        print(f"Added {len(departments)} departments")
        return [dept.id for dept in departments]

    @staticmethod
    def add(name: str, description: str) -> str:
        insert_command = """
            INSERT INTO departments (id, name, description) VALUES (:name, :description);
        """
        department = Department(name=name, description=description)
        with SqliteDb.connect() as conn:
            conn.execute(insert_command, department.__dict__())
        return department.id

    @staticmethod
    def update(id: str, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clauses = []
        params = {"id": id}
        for field, value in kwargs.items():
            if field in DepartmentTable.UPDATABLE_FIELDS:
                set_clauses.append(f"{field} = :{field}")
                params[field] = value

        if not set_clauses:
            raise ValueError("No valid fields to update")

        update_command = f"""
            UPDATE departments SET {", ".join(set_clauses)} WHERE id = :id;
        """
        params = {**kwargs, "id": id}
        with SqliteDb.connect() as conn:
            conn.execute(update_command, params)
        return conn.total_changes > 0

    @staticmethod
    def delete(id: str) -> bool:
        delete_command = """
        DELETE FROM departments WHERE id = :id;
        """
        with SqliteDb.connect() as conn:
            conn.execute(delete_command, {"id": id})
        return conn.total_changes > 0

    @staticmethod
    def get_all() -> list[Department] | None:
        query = "SELECT * FROM departments;"
        with SqliteDb.connect() as conn:
            rows = conn.execute(query).fetchall()
            if rows and len(rows) > 0:
                return [Department(**row) for row in rows]
        return None

    @staticmethod
    def get_by_id(id: str) -> Department:
        query = "SELECT * FROM departments WHERE id = :id;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"id": id}).fetchone()
            if row:
                return Department(**row)
        return None

    @staticmethod
    def get_by_name(name: str) -> Department:
        query = "SELECT * FROM departments WHERE name = :name;"
        with SqliteDb.connect() as conn:
            row = conn.execute(query, {"name": name}).fetchone()
            if row:
                return Department(**row)
        return None
