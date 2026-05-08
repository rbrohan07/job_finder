import feedparser
import requests
import json
from datetime import datetime, timezone, timedelta
import time
import os
from jobspy import scrape_jobs
import pandas as pd
from filter import (
    basic_filter, 
    keyword_filter, 
    role_filter, 
    time_filter, 
    salary_filter, 
    source_filter,
    apply_filters
)
from scorer import (
    score_and_rank_jobs,
    score_job,
    get_top_jobs_by_skill
)
import hashlib


# /////////////////////////////////////////////////////////////////////////////////////////////////////
# remote.io
def fetch_jobs_remoteio():
    results = []

    for pageno in range(1, 4):
        url = f"https://remote.io/api/v2/jobs?page={pageno}&limit=100"

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        data = response.json()

        for job in data["data"]:
            results.append({
                "title": job.get("jobTitle"),
                "company": job.get("companyName"),
                "location": job.get("locationType"),
                "job_url": job.get("applicationUrl"),
                "time":job.get("postedAgo"),
                "salaryMin":job.get("salaryMin"),
                "salaryMax":job.get("salaryMax"),
                "category":job.get("category"),
                "salaryCurrency":job.get("salaryCurrency"),
                "source": "remoteio",
            })

    return results


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# remoteok
def fetch_jobs_remoteok():
    results = []

    for pageno in range(1, 6):
        url = f"https://remoteok.com/api"

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        job = response.json()

        for jobs in job:
            results.append({
                "title": jobs.get("position"),
                "company": jobs.get("companyName"),
                "location": jobs.get("location"),
                "job_url": jobs.get("apply_url"),
                "time":jobs.get("date"),
                "salaryMin":jobs.get("salary_min"),
                "salaryMax":jobs.get("salary_max"),
                "category":jobs.get("category"),
                "salaryCurrency":jobs.get("salaryCurrency"),
                "source": "remoteok",
            })

    return results


# jobspy fetch with user parameters
def fetch_jobs_jobspy(site_name=None, search_term="software engineer", location="INDIA KOLKATA", results_wanted=20, country_indeed='India'):
    """Fetch jobs using JobSpy library
    
    Args:
        site_name: List of site names to scrape from (e.g., ["indeed", "linkedin"])
        search_term: Job search term
        location: Location to search
        results_wanted: Number of results wanted
        country_indeed: Country for Indeed
    """
    if site_name is None:
        site_name = ["indeed", "linkedin"]

    job = scrape_jobs(
        site_name=site_name,
        search_term=search_term,
        google_search_term=f"{search_term} jobs near {location} now",
        location=location,
        results_wanted=results_wanted,
        hours_old=24,
        country_indeed=country_indeed,
    )
    print(f"Found {len(job)} jobs")
    job = job.astype(object).where(pd.notnull(job), None)
    job = job.to_dict(orient="records")
    
    results = []
    for jobs in job:
        results.append({
            "title": jobs.get("title"),
            "company": jobs.get("company"),
            "location": jobs.get("location"),
            "job_url": jobs.get("job_url_direct"),
            "time":jobs.get("date"),
            "salaryMin":jobs.get("min_amount"),
            "salaryMax":jobs.get("max_amount"),
            "category":jobs.get("category"),
            "salaryCurrency":jobs.get("salaryCurrency"),
            "source": jobs.get("site"),
        })
    return results


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Hash function for deduplication
def job_hash(job):
    if job is None:
        return None
    text = " ".join([
        str(job.get("title", "")),
        str(job.get("company", "")),
        str(job.get("location", "")),
        str(job.get("job_url", ""))
    ]).lower().strip()
    
    return hashlib.md5(text.encode()).hexdigest()


def add_ids(jobs):
    for job in jobs:
        job["id"] = job_hash(job)
    return jobs


def remove_duplicate(jobs):
    unique_jobs = []
    unique_id = set()
    for job in jobs:
        if job['id'] not in unique_id:
            unique_id.add(job["id"])
            unique_jobs.append(job)
    return unique_jobs


# Define available sources
AVAILABLE_SOURCES = {
    "remoteio": ("Remote.io", lambda: fetch_jobs_remoteio()),
    "remoteok": ("RemoteOK", lambda: fetch_jobs_remoteok()),
    "indeed": ("Indeed (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["indeed"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "linkedin": ("LinkedIn (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["linkedin"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "zip_recruiter": ("ZipRecruiter (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["zip_recruiter"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "glassdoor": ("Glassdoor (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["glassdoor"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "google": ("Google (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["google"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "naukri": ("Naukri (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["naukri"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "bayt": ("Bayt (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["bayt"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
    "bdjobs": ("BDJobs (JobSpy)", lambda st, loc, rw, c: fetch_jobs_jobspy(site_name=["bdjobs"], search_term=st, location=loc, results_wanted=rw, country_indeed=c)),
}


def display_available_sources():
    """Display available sources to user"""
    print("\n" + "="*50)
    print("Available Job Sources")
    print("="*50)
    print("0. All sources")
    for i, (key, (name, _)) in enumerate(AVAILABLE_SOURCES.items(), 1):
        print(f"{i}. {name}")
    print("="*50 + "\n")


# Get all user input at once
def get_user_input():
    """Get all filter criteria from user first"""
    print("\n" + "="*50)
    print("Job Search Configuration")
    print("="*50)
    
    # 1. Job search query
    query = input("Enter job search query (e.g., 'python developer fullstack'): ").strip()
    if not query:
        query = "software engineer"
        print(f"Using default query: {query}")
    
    # 2. Expected salary
    salary_input = input("Enter expected salary (or press Enter to skip): ").strip()
    expected_salary = float(salary_input) if salary_input else None
    if expected_salary:
        print(f"Expected salary: ${expected_salary:,.0f}")
    
    # 3. Preferred location
    location = input("Enter preferred location (or press Enter for default): ").strip()
    if not location:
        location = "INDIA KOLKATA"
        print(f"Using default location: {location}")
    
    # 4. Number of results wanted
    results_wanted_input = input("Enter number of results wanted (default 20): ").strip()
    results_wanted = int(results_wanted_input) if results_wanted_input else 20
    
    # 5. Country for Indeed
    country = input("Enter country for Indeed (default 'India'): ").strip()
    if not country:
        country = "India"
    
    # 6. Source selection
    print("\n--- Select Job Sources ---")
    display_available_sources()
    selected_sources_input = input("Enter source number(s) separated by comma (or press Enter for all): ").strip()
    
    if not selected_sources_input:
        selected_sources = list(AVAILABLE_SOURCES.keys())
        print("Fetching from ALL sources...")
    else:
        try:
            indices = [int(x.strip()) for x in selected_sources_input.split(",")]
        except ValueError:
            selected_sources = list(AVAILABLE_SOURCES.keys())
            print("Invalid input. Fetching from ALL sources...")
        
        selected_sources = []
        for idx in indices:
            if idx == 0:
                selected_sources = list(AVAILABLE_SOURCES.keys())
                print("Fetching from ALL sources...")
                break
            elif 1 <= idx <= len(AVAILABLE_SOURCES):
                selected_sources.append(list(AVAILABLE_SOURCES.keys())[idx - 1])
            else:
                print(f"Invalid option: {idx}. Ignoring...")
        
        if not selected_sources:
            selected_sources = list(AVAILABLE_SOURCES.keys())
            print("No valid sources selected. Fetching from ALL sources...")
    
    print(f"Selected sources: {[AVAILABLE_SOURCES.get(s, (s,))[0] for s in selected_sources]}")
    print("="*50 + "\n")
    
    return query, expected_salary, location, results_wanted, country, selected_sources


# Main execution
print("\n" + "="*50)
print("Job Search Application")
print("="*50)

# Get all user input first
query, expected_salary, location, results_wanted, country, selected_sources = get_user_input()

# Fetch jobs from selected sources
print("Fetching Jobs...")
print("="*50 + "\n")

result = []
for source in selected_sources:
    name, fetch_func = AVAILABLE_SOURCES[source]
    print(f"Fetching from {name}...")
    try:
        # Check if fetch_func needs parameters (for JobSpy sources)
        if source in ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "naukri", "bayt", "bdjobs"]:
            jobs = fetch_func(query, location, results_wanted, country)
        else:
            jobs = fetch_func()
        
        result.extend(jobs)
        print(f"  -> Got {len(jobs)} jobs from {name}")
    except Exception as e:
        print(f"  -> Error fetching from {name}: {e}")
        print(f"  -> Exception: {str(e)}")

print(f"\nTotal jobs fetched: {len(result)}")

# Remove duplicates
result = add_ids(result)
result = remove_duplicate(result)
print(f"Jobs after removing duplicates: {len(result)}")

# Apply filters (basic filtering)
print("Applying filters...")
result = apply_filters(result, query=query, expected_salary=expected_salary, allowed_sources=None)

# Apply scoring and ranking
print("Scoring and ranking jobs...")
result = score_and_rank_jobs(
    result, 
    query=query, 
    expected_salary=expected_salary,
    min_score=30,  # Minimum score threshold
    limit=50  # Top 50 jobs
)

# Save results
with open("result.json", "w") as json_file:
    json.dump(result, json_file, indent=4)

print(f"\nSaved {len(result)} scored and ranked jobs to result.json")
print("Done!")
