from requests import get
from bs4 import BeautifulSoup

def extract_saramin_jobs(keyword):
    results = []
    base_url = "https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print(f"페이지를 로드할 수 없습니다. \n에러코드 : {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("div", class_="item_recruit")
        for job in jobs:
            area_job = job.find("div", class_="area_job")
            
            anchor = area_job.select_one("h2 a")#구인공고 타이틀
            title = anchor["title"]
            job_link = "https://www.saramin.co.kr" + anchor["href"]#구인공고 링크
            job_date = area_job.find("div", class_="job_date")
            date = job_date.find("span", class_="date").string#구인공고 데드라인
            
            job_condition = area_job.find("div", class_="job_condition")
            job_condition_spans = job_condition.find_all("span")
            
            def listToString(str_list):
                result = ""
                for item in str_list:
                    result += item + " "
                return result.strip()
            
            job_location = job_condition_spans[0]
            locations = job_location.find_all("a")
            region = []
            for location in locations:
                region.append(location.string)
                locate = listToString(region)
            #print(locate)
            """if len(region) == 2:
                region = [region[0] + " " +region[1]]
            region = region[0]"""
            
            
            working_jobs = []
            job_options = job_condition_spans[1:]
            for job_option in job_options:
                working_jobs.append(job_option.string)
                option = listToString(working_jobs)
                #print(option.replace(" ", ","))
                
            area_corp = job.find("div", class_="area_corp")
            area_corp_names = area_corp.select_one("strong a")#회사 이름
            
            
            job_data = {
                "company" : area_corp_names.string.replace(",", " ").strip(),
                "location" : locate.replace(" ", ","),
                "option" : option.replace(" ", ","),
                "position" : title.replace(" ", ","),
                "date" : date.replace(" ", ","),
                "link" : job_link
            }
            results.append(job_data)
    return results        
extract_saramin_jobs("파이썬")