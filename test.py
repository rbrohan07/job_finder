# import csv
# from jobspy import scrape_jobs

# jobs = scrape_jobs(
#     # site_name=["indeed", "linkedin", "zip_recruiter", "google"], # "glassdoor", "bayt", "naukri", "bdjobs"
#     site_name=["indeed", "linkedin"],
#     search_term="software engineer",
#     google_search_term="software engineer jobs near INDIA kolkata now",
#     location="INDIA KOLKATA",
#     results_wanted=20,
#     hours_old=24,
#     country_indeed='India',
    
#     # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
#     # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
# )
# print(f"Found {len(jobs)} jobs")
# print(jobs.head())
# jobs.to_json("jobs.json") # to_excel

import hashlib


job=[
 {
  
  "title": "Frontend Engineer",
  "company": "Stripe",
  "location": "Remote",
  "source": "linkedin"
 },
  {

  "title": "Frontend Engineer",
  "company": "Stripe",
  "location": "Remote",
  "source": "linkedin"
 },
 {
 
  "title": "Backend Engineer",
  "company": "Airbnb",
  "location": "Remote",
  "source": "remoteio"
 },{'title': 'Remote C++ Developer', 'company': 'Turing', 'location': 'Kolkata, West Bengal, India', 'job_url': None, 'time': None, 'salaryMin': None, 'salaryMax': None, 'category': None, 'salaryCurrency': None, 'source': 'linkedin'}
]

def job_hash(job):
    text = job['title'] + job["company"] + job["location"]
    return hashlib.md5(text.encode()).hexdigest()
def add_ids(jobs):

    for i, job in enumerate(jobs, start=1):
        job["id"] = job_hash(job)

    return jobs


print(add_ids(job))