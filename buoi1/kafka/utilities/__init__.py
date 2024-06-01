from contextlib import contextmanager
from datetime import datetime as dt
import logging
import importlib
import subprocess
from pathlib import Path
 
class DatabaseConnectionManager:
    def __init__(self, db_modules):
        self.db_modules = db_modules
 
    @contextmanager
    def get_database_connection(self, db_type=None, *args, **kwargs):
        conn = None
       
        try:
            db_module_name = self.db_modules.get(db_type)
           
            if not db_module_name:
                raise ValueError(f"No module specified for database type: {db_type}")
 
            db_module = importlib.import_module(db_module_name)
 
            conn = db_module.connect(*args, **kwargs)
            yield conn  # Provide the connection to the caller
            conn.commit()  # Commit any pending transactions
 
        except Exception as e:
            logging.error(str(e))
            if conn:
                conn.rollback()
 
        finally:
            if conn:
                conn.close()
 
if __name__ == "__main__":
    # Define your database modules mapping
    DATABASE_MODULES = {
        "mysql": "pymysql",
        "postgres": "psycopg2"
    }
 
    db_params = {
        "host": "bigdata.intelli.vn",
        "database": "upskill",
        "user": "thiennh18",
        "password": "123456123",
        "port": "5432"
    }
 
    # Example usage of the class for MySQL
    db_manager = DatabaseConnectionManager(DATABASE_MODULES)
    with db_manager.get_database_connection("postgres", **db_params) as conn:
        # Execute SQL queries or interact with the database using 'conn'
        print("Success")
        
    print(Path(__file__).parent)