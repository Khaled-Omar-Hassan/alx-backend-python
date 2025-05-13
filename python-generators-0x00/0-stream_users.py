import seed



def stream_users():
  db = seed.connect_db()
  seed.connect_to_prodev(db)
  seed.create_database(db)
  seed.create_table(db)
  seed.insert_data(db)

  for row in db.cursor().execute("SELECT * FROM user_data;"):
    yield(row)

  
