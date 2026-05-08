import requests
from bs4 import BeautifulSoup

url = "https://remoteok.com/remote-engineering+senior-jobs?location=region_AS,Worldwide"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text[:1000])
with open("response.html", "w", encoding="utf-8") as f:
    f.write(response.text)
soup = BeautifulSoup(response.text, "lxml")

jobs = soup.find_all("tr", class_="job")

for job in jobs:
    title = job.find("h2")
    company = job.find("h3")
    
    if title and company:
        print("Title:", title.text.strip())
        print("Company:", company.text.strip())
        print("-----------")