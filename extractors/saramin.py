from requests import get
from bs4 import BeautifulSoup
import numpy as np

def extract_saramin_jobs(keyword):
    results = []
    base_url = "https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print(f"페이지를 로드할 수 없습니다. \n에러코드 : {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html5lib")
        job_list = soup.find("div",class_="content")
        jobs = job_list.find_all("div", class_="item_recruit", recursive=False)
        for job in jobs:
            anchor = job.select("h2 a")
            title = anchor["title"]
            link = anchor["href"]
            date = job.find("div", class_="job_date").find("span", class_="date")
            job_conditions = job.find("div",class_="job_condition")
            for location in job_conditions.find("span").children:
                print(location.string)
            for condition in job_conditions.find("span").next_siblings:
                print(condition.string)
            print(anchor)
            print(title)
            print(link)
            print(date)
extract_saramin_jobs("python")