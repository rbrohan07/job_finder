"""
Job Scoring Module
Scores jobs based on multiple relevance factors to provide better results.
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


# Configuration
SOURCE_WEIGHTS = {
    "linkedin": 10,
    "indeed": 8,
    "remoteio": 7,
    "remoteok": 7,
    "glassdoor": 6,
    "ziprecruiter": 6,
    "google": 5,
    "naukri": 4,
    "bayt": 3,
    "bdjobs": 3,
}

# Senior role keywords to downweight
SENIOR_KEYWORDS = ["senior", "sr.", "sr ", "lead", "manager", "director", "chief", "head of", "principal"]
JUNIOR_KEYWORDS = ["junior", "jr.", "jr ", "intern", "trainee", "entry"]


def parse_time_to_days(time_str: str) -> Optional[int]:
    """Parse time string to number of days ago"""
    if not time_str:
        return None
    
    time_str = str(time_str).lower().strip()
    
    # Handle ISO dates
    try:
        if re.search(r'\d{4}-\d{2}-\d{2}', time_str):
            date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', time_str)
            if date_match:
                job_date = datetime(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
                return (datetime.now() - job_date).days
    except:
        pass
    
    # Handle relative time (e.g., "5d", "2 days ago", "1w")
    days_match = re.search(r'(\d+)\s*d(ay)?', time_str)
    if days_match:
        return int(days_match.group(1))
    
    hours_match = re.search(r'(\d+)\s*h(our)?', time_str)
    if hours_match:
        return 0  # Less than 1 day
    
    weeks_match = re.search(r'(\d+)\s*w(eek)?', time_str)
    if weeks_match:
        return int(weeks_match.group(1)) * 7
    
    months_match = re.search(r'(\d+)\s*m(onth)?', time_str)
    if months_match:
        return int(months_match.group(1)) * 30
    
    return None


def score_keyword_match(job: Dict, query: str) -> int:
    """Score keyword/role match (30 points max)"""
    score = 0
    title = str(job.get("title", "")).lower()
    query_lower = query.lower() if query else ""
    
    if query_lower:
        query_words = query_lower.split()
        
        # Exact title match (all query words in title)
        if all(word in title for word in query_words if len(word) > 2):
            score += 20
        # Partial title match
        elif any(word in title for word in query_words if len(word) > 2):
            score += 10
        
        # Check for keywords anywhere in job
        job_text = f"{title} {job.get('company', '')} {job.get('category', '')}".lower()
        matching_words = sum(1 for word in query_words if word in job_text and len(word) > 2)
        score += min(matching_words * 5, 10)  # Up to 10 points for additional matches
    
    return min(score, 30)


def score_salary(job: Dict, expected_salary: Optional[float]) -> int:
    """Score salary match (25 points max)"""
    if expected_salary is None:
        return 5  # Default for no salary preference
    
    job_min = job.get("salaryMin")
    job_max = job.get("salaryMax")
    
    # Handle empty/null values
    if not job_min and not job_max:
        return 5  # Salary not disclosed
    
    try:
        job_min = float(job_min) if job_min else 0
        job_max = float(job_max) if job_max else job_min
    except (ValueError, TypeError):
        return 5
    
    # No expected salary to compare
    if expected_salary <= 0:
        return 5
    
    # Calculate match
    if job_min >= expected_salary * 0.8 and job_max <= expected_salary * 1.2:
        return 25  # Within range
    elif job_max >= expected_salary:
        return 20  # Above expected
    elif job_max >= expected_salary * 0.5:
        return 10  # Acceptable (at least 50%)
    else:
        return 5  # Too low


def score_recency(job: Dict) -> int:
    """Score job recency (20 points max)"""
    time_str = job.get("time")
    days_ago = parse_time_to_days(time_str)
    
    if days_ago is None:
        return 5  # Unknown
    
    if days_ago == 0:
        return 20
    elif days_ago <= 3:
        return 15
    elif days_ago <= 7:
        return 10
    elif days_ago <= 14:
        return 5
    else:
        return 0


def score_source(job: Dict) -> int:
    """Score source reputation (10 points max)"""
    source = str(job.get("source", "")).lower()
    return SOURCE_WEIGHTS.get(source, 5)


def score_role(job: Dict) -> int:
    """Score role fit (10 points max)"""
    title = str(job.get("title", "")).lower()
    
    # Check for senior/manager/director
    for keyword in SENIOR_KEYWORDS:
        if keyword in title:
            return 5  # Senior role - lower score
    
    # Check for junior
    for keyword in JUNIOR_KEYWORDS:
        if keyword in title:
            return 10  # Junior is OK
    
    return 10  # Mid-level is good


def score_location(job: Dict, preferred_location: Optional[str] = None) -> int:
    """Score location match (5 points max)"""
    location = str(job.get("location", "")).lower()
    
    if not location or location == "null":
        return 2  # Unknown
    
    if preferred_location:
        pref = preferred_location.lower()
        
        if pref in location or location in pref:
            return 5  # Exact match
        elif "remote" in location or "home" in location:
            return 5  # Remote work
        elif location == pref:
            return 5
        else:
            return 2  # Different
    
    # No preference - prefer remote
    if "remote" in location or "home" in location:
        return 5
    
    return 3


def score_job(
    job: Dict,
    query: str = "",
    expected_salary: Optional[float] = None,
    preferred_location: Optional[str] = None
) -> Dict:
    """
    Calculate total score for a job.
    
    Returns a dict with:
    - total_score: int (0-100)
    - score_breakdown: dict with individual scores
    """
    # Calculate individual scores
    breakdown = {
        "keyword": score_keyword_match(job, query),
        "salary": score_salary(job, expected_salary),
        "recency": score_recency(job),
        "source": score_source(job),
        "role": score_role(job),
        "location": score_location(job, preferred_location),
    }
    
    # Calculate total
    total = sum(breakdown.values())
    
    return {
        "total_score": total,
        "score_breakdown": breakdown,
        **job  # Keep original job data
    }


def score_and_rank_jobs(
    jobs: List[Dict],
    query: str = "",
    expected_salary: Optional[float] = None,
    preferred_location: Optional[str] = None,
    min_score: int = 0,
    limit: int = None
) -> List[Dict]:
    """
    Score and rank all jobs.
    
    Args:
        jobs: List of job dictionaries
        query: Search query for keyword matching
        expected_salary: Expected salary for salary scoring
        preferred_location: Preferred location
        min_score: Minimum score to include (0-100)
        limit: Maximum number of jobs to return
    
    Returns:
        List of jobs with scores, sorted by score (highest first)
    """
    if not jobs:
        return []
    
    # Score each job
    scored_jobs = []
    for job in jobs:
        scored = score_job(job, query, expected_salary, preferred_location)
        scored_jobs.append(scored)
    
    # Sort by score (descending)
    scored_jobs.sort(key=lambda x: x["total_score"], reverse=True)
    
    # Filter by minimum score
    if min_score > 0:
        scored_jobs = [j for j in scored_jobs if j["total_score"] >= min_score]
    
    # Apply limit
    if limit and limit > 0:
        scored_jobs = scored_jobs[:limit]
    
    return scored_jobs


def get_top_jobs_by_skill(
    jobs: List[Dict],
    skill: str,
    top_n: int = 10
) -> List[Dict]:
    """
    Get top jobs for a specific skill.
    
    Args:
        jobs: List of job dictionaries
        skill: Skill to filter by (e.g., "react", "python")
        top_n: Number of top jobs to return
    
    Returns:
        List of top jobs for the skill
    """
    skill_lower = skill.lower()
    
    # Score based on skill match
    for job in jobs:
        title = str(job.get("title", "")).lower()
        category = str(job.get("category", "")).lower()
        
        # Boost score if skill in title
        if skill_lower in title:
            job["skill_match_boost"] = 20
        elif skill_lower in category:
            job["skill_match_boost"] = 10
        else:
            job["skill_match_boost"] = 0
    
    # Sort by boost
    jobs.sort(key=lambda x: x.get("skill_match_boost", 0), reverse=True)
    
    return jobs[:top_n]
