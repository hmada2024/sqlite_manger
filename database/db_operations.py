import sqlite3
from threading import Lock
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self._connection = None
        self._lock = Lock()
        self.database_path = None
    
    def connect(self, db_path):
        try:
            with self._lock:
                self._connection = sqlite3.connect(db_path)
                self.database_path = db_path
                logger.info(f"Connected to database: {db_path}")
                return True
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def execute_query(self, query, params=None):
        try:
            with self._lock:
                cursor = self._connection.cursor()
                cursor.execute(query, params or [])
                self._connection.commit()
                return cursor
        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def get_tables(self):
        cursor = self.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cursor.fetchall()]

    def get_table_columns(self, table_name):
        cursor = self.execute_query(f"PRAGMA table_info({table_name})")
        return [col[1] for col in cursor.fetchall()]

    def get_table_data(self, table_name):
        cursor = self.execute_query(f"SELECT * FROM {table_name}")
        return cursor.fetchall()

    def create_table(self, table_name, columns):
        columns_sql = ", ".join([f"{name} {type_}" for name, type_ in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        self.execute_query(query)

    def insert_data(self, table_name, data):
        placeholders = ",".join(["?" for _ in data[0]])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        for row in data:
            self.execute_query(query, row)

    def close(self):
        if self._connection:
            self._connection.close()