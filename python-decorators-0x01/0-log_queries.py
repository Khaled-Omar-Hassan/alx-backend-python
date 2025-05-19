import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries and execution time using print and datetime
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        start_time = datetime.now()
        
        if query:
            print(f"[{start_time}] Executing query: {query}")
        else:
            print(f"[{start_time}] No SQL query provided.")

        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"[{end_time}] Query executed in {duration:.4f} seconds")
            return result
        except Exception as e:
            error_time = datetime.now()
            print(f"[{error_time}] Error executing query: {e}")
            raise
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query and execution time
users = fetch_all_users(query="SELECT * FROM users")
