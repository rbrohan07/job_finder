
# Import ROLE_MAP from roles.py
from roles import ROLE_MAP
def expand_keywords(query):
    base = query.lower().split()
    
    expanded = set(base)
    
    for word in base:
        if word in ROLE_MAP:
            expanded.update(ROLE_MAP[word])
    
    return list(expanded)

def keyword_filter(job, keywords):
    if not keywords:
        return True
    
    text = job["title"].lower()
    
    matches = sum(1 for k in keywords if k in text)
    
    return matches >= 1
    
    return any(k in text for k in KEYWORDS)
def role_filter(job):
    title = str(job.get("title", "")).lower()
    
    # ❌ remove unwanted roles
    if "senior" in title:
        return False
    if "manager" in title:
        return False
    if "director" in title:
        return False
    
    return True
def time_filter(job):
    time_str = str(job.get("time", "")).lower()
    
    # remove old jobs
    if "30" in time_str or "month" in time_str:
        return False
    
    return True
def salary_filter(job, expected_salary):
    
    job_min = job.get("salaryMin")
    job_max = job.get("salaryMax")
    
    # ✅ Case 1: No salary → still show
    if not job_min and not job_max:
        job["salary_remark"] = "Salary not disclosed"
        return True
    
    # convert to number safely
    try:
        job_min = float(job_min) if job_min else 0
        job_max = float(job_max) if job_max else job_min
    except:
        job["salary_remark"] = "Invalid salary data"
        return True
    
    lower_bound = expected_salary * 0.8
    upper_bound = expected_salary * 1.2
    
    # ✅ within range
    if job_min >= lower_bound and job_max <= upper_bound:
        job["salary_remark"] = "Within expected range"
        return True
    
    # 🟡 close enough
    if job_max >= lower_bound:
        job["salary_remark"] = "Slightly below expectation"
        return True
    
    # 🔴 too low
    job["salary_remark"] = "Below expected range"
    return False


def source_filter(job, allowed_sources):
    """Filter jobs by source/platform"""
    if not allowed_sources:
        return True
    job_source = job.get("source", "").lower()
    return job_source in [s.lower() for s in allowed_sources]


def basic_filter(job):
    """Basic filter - removes jobs with missing essential data"""
    # Remove jobs without title
    if not job.get("title"):
        return False
    # Remove jobs without company (optional - comment out if you want to keep)
    # if not job.get("company"):
    #     return False
    return True


def apply_filters(jobs, query="", expected_salary=None, allowed_sources=None):
    """
    Apply all filters to the jobs list.
    
    Args:
        jobs: List of job dictionaries
        query: User search query (for keyword filtering)
        expected_salary: Expected salary (for salary filtering)
        allowed_sources: List of allowed sources (e.g., ["remoteio", "linkedin"])
    
    Returns:
        Filtered list of jobs
    """
    if not jobs:
        return []
    
    # Expand keywords from query
    keywords = expand_keywords(query) if query else []
    
    filtered_jobs = []
    for job in jobs:
        # 1. Basic filter
        if not basic_filter(job):
            continue
        
        # 2. Role filter (exclude senior/manager/director)
        if not role_filter(job):
            continue
        
        # 3. Time filter (exclude old jobs)
        if not time_filter(job):
            continue
        
        # 4. Keyword filter (if query provided)
        if query and not keyword_filter(job, keywords):
            continue
        
        # 5. Salary filter (if expected_salary provided)
        if expected_salary is not None and not salary_filter(job, expected_salary):
            continue
        
        # 6. Source filter (if allowed_sources provided)
        if allowed_sources and not source_filter(job, allowed_sources):
            continue
        
        filtered_jobs.append(job)
    
    print(f"Filtered {len(filtered_jobs)} jobs from {len(jobs)} total")
    return filtered_jobs
