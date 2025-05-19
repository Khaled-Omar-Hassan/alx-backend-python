import time
import sqlite3 
import functools

#### paste your with_db_decorator here

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      db = sqlite3.connect("ALX_prodev.db")
      result = func(db, *args, **kwargs)
      db.close()
      return result
    return wrapper

def retry_on_failure(func, retries, delay):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    for i in range(retries):
      try:
        func(*args, **kwargs)
        break
      except:
        time.sleep(delay)
    raise 
  return wrapper


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
