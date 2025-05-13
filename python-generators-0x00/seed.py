import mysql.connector


def connect_db():
  db = mysql.connector.connect(
    host="localhost",
    user='root',
    password=''
  )

  return db

def create_database(db):
  cursor = db.cursor()
  cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
   

def connect_to_prodev(db):
  cursor = db.cursor()
  cursor.execute("USE ALX_prodev")


def create_table(db):
  cursor = db.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS user_data (user_id Primary Key UUID Indexed, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, age DECIMAL NOT NULL);")


def insert_data(db):
  cursor = db.cursor()
  csv_gen = (row for row in open("user_data.csv"))
  for row in csv_gen:
    cursor.execute("INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)", row)

