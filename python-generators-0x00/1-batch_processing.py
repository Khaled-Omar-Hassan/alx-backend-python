import seed

def stream_users_in_batches(batch_size):
  with seed.connect_db() as connection:
    seed.connect_to_prodev(connection)
    seed.create_database(connection)
    seed.create_table(connection)
    seed.insert_data(connection)

    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM user_data;")
      while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
          break
        yield rows

def batch_processing(batch_size):
  for batch in stream_users_in_batches(batch_size):
    for row in batch:
      if int(row[-1]) > 25:
        yield row

  return
