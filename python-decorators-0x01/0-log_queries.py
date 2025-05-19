import sqlite3
import functools
import time
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            logging.info(f"Executing query: {query}")
        else:
            logging.info("No SQL query provided.")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"Query executed in {duration:.4f} seconds")
            return result
        except Exception as e:
            logging.error(f"Error while executing query: {e}")
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

# Fetch users while logging the query and time taken
users = fetch_all_users(query="SELECT * FROM users")
