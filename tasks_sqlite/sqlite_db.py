#####################################################################
import sqlite3
#####################################################################

class SqliteDb:
    DB_PATH = None

    @staticmethod
    def create(db_path: str):
        # set database path
        SqliteDb.DB_PATH = db_path
        # create database
        sqlite3.connect(SqliteDb.DB_PATH)

    @staticmethod
    def connect():
        conn = sqlite3.connect(SqliteDb.DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @staticmethod
    def create_update_trigger(table_name):
        trigger = f"""
            CREATE TRIGGER IF NOT EXISTS update_{table_name}_timestamp AFTER UPDATE ON {table_name}
            FOR EACH ROW BEGIN UPDATE {table_name} SET updated_at = CURRENT_TIMESTAMP WHERE id = old.id; END;
        """
        with SqliteDb.connect() as conn:
            conn.execute(trigger)
