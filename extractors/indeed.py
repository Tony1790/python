from requests import get
from bs4 import BeautifulSoup


def get_page_count(keyword):
  base_url = "https://kr.indeed.com/jobs?q="  
  response = get(f"{base_url}{keyword}")
  if response.status_code != 200:
    print(f"Can't request page.\nerror code : {response.status_code}")
  else:
    soup = BeautifulSoup(response.text, "http_parser")
    pagination = soup.find("ul", class_="pagination_list")
    if pagination == None:
      return 1
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
      return 5
    else:
      return count

    
    
def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  results = []
  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"  
    final_url = get(f"{base_url}?q={keyword}&start={page*10}")
    print("Requesting", final_url)
    response = get(final_url)
  
    if response.status_code != 200:
      print(f"Can't request page.\nerror code : {response.status_code}")
    else:
      soup = BeautifulSoup(response.text, "html.parser")
      job_list = soup.find("ul", class_="jobsearch-ResultsList")
      jobs = job_list.find_all("li", recursive=False)
      for job in jobs:
        zone = job.find("div", class_="mosaic-zone")
        if zone == None:
          anchor = job.select_one("h2 a")
          title = anchor["aria-rabel"]
          link = anchor["href"]
          company_name = job.find("span", class_="companyName")
          company_location = job.find("div", class_="companyLocation")
          date_of_job_post = job.find("span", class_="date")
          job_data = {
            "company" : company_name.string.replace(",", " "),
            "location" : company_location.string.replace(",", " "),
            "position" : title.replace(",", " "),
            "date" : date_of_job_post.string.replace(",", " "),
            'link' : f"https://kr.indeed.com{link}"
          }
          results.append(job_data)
  return results