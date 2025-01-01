import sqlite3
from threading import Lock
import logging
from typing import List, Tuple, Any, Optional

class DatabaseManager:
    def __init__(self):
        self._connection = None
        self._lock = Lock()
        self.database_path = None
        self._setup_logging()
    
    def _setup_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def connect(self, db_path: str) -> bool:
        """Connect to a SQLite database"""
        try:
            with self._lock:
                self._connection = sqlite3.connect(db_path)
                self.database_path = db_path
                self.logger.info(f"Connected to database: {db_path}")
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> sqlite3.Cursor:
        """Execute a SQL query with optional parameters"""
        try:
            with self._lock:
                cursor = self._connection.cursor()
                cursor.execute(query, params or [])
                self._connection.commit()
                return cursor
        except sqlite3.Error as e:
            self.logger.error(f"Query execution failed: {e}")
            raise
    
    def get_tables(self) -> List[str]:
        """Get list of all tables in the database"""
        cursor = self.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cursor.fetchall()]
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get list of columns for a specific table"""
        cursor = self.execute_query(f"PRAGMA table_info({table_name})")
        return [col[1] for col in cursor.fetchall()]
    
    def get_table_data(self, table_name: str) -> List[Tuple]:
        """Get all data from a specific table"""
        cursor = self.execute_query(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    
    def create_table(self, table_name: str, columns: List[Tuple[str, str]]):
        """Create a new table with specified columns"""
        columns_sql = ", ".join([f"{name} {type_}" for name, type_ in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        self.execute_query(query)
    
    def insert_data(self, table_name: str, data: List[Tuple]):
        """Insert data into a table"""
        placeholders = ",".join(["?" for _ in data[0]])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        for row in data:
            self.execute_query(query, row)
    
    def update_data(self, table_name: str, column: str, value: Any, condition: str):
        """Update data in a table"""
        query = f"UPDATE {table_name} SET {column} = ? WHERE {condition}"
        self.execute_query(query, [value])
    
    def delete_data(self, table_name: str, condition: str):
        """Delete data from a table"""
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute_query(query)
    
    def close(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            self.logger.info("Database connection closed")