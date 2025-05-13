import seed

def stream_user_ages():
  connection = seed.connect_to_prodev()
  cursor = connection.cursor()
  yield from cursor.execute("SELECT age FROM user_data")

def calculate_average():
  avg = 0
  count = 0
  for age in stream_user_ages():
    avg += age
    count +=1
  print(f"Average age of users: {avg/count}")
  
  
