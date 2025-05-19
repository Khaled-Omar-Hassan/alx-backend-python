import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      db = sqlite3.connect("ALX_prodev.db")
      result = func(db, *args, **kwargs)
      db.close()
      return result
    return wrapper

def cache_query(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
     if args[1] in query_cache:
        return query_cache[args[1]]
     query_cache[args[1]] = func(*args, **kwargs)
     return query_cache[args[1]]
  return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
