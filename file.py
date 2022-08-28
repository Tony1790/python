def save_to_file(file_name, jobs):
  file = open(f"{file_name}.csv", "w", encoding='utf8')
  file.write("Position, Company ,location, date, option, URL\n")
  
  for job in jobs:
    file.write(f"{job['position']}, {job['company']}, {job['date']}, {job['link']}, {job['location']}, {job['option']}\n")
  
  file.close()