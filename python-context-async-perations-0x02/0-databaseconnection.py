import sqlite3

class DatabaseConnection():
  def __init__(self, db_name):
    self.db_name = db_name
    self.conn = sqlite3.connect(db_name)

  def __enter__(self):
    return self.conn
  
  def __exit__(self, type, value, traceback):
    self.conn.close()


with DatabaseConnection("ALX_prodev") as conn:
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  result = cursor.fetchall()
  print(result)


