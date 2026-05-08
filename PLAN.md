# Job Search Scoring Methodology Plan

## Objective
Replace the current filtering approach with a scoring methodology that ranks jobs based on multiple relevance factors, providing better results to the user.

## Current Problem
- The current system uses hard filters that exclude jobs
- Jobs are not ranked by relevance
- Good jobs might be filtered out due to strict criteria

## Proposed Scoring Methodology

### Score Components (Total: 100 points)

#### 1. Keyword Match Score (30 points)
- Exact title match: 20 points
- Partial title match: 10 points
- Skills/keywords in description: 10 points

#### 2. Salary Score (25 points)
- Salary matches expected (within ±20%): 25 points
- Salary above expected: 20 points
- Salary not disclosed: 5 points
- Salary below expected (but >50%): 10 points

#### 3. Recency Score (20 points)
- Posted today: 20 points
- Posted within 3 days: 15 points
- Posted within 7 days: 10 points
- Posted within 14 days: 5 points
- Posted >14 days ago: 0 points

#### 4. Source Reputation Score (10 points)
- LinkedIn: 10 points
- Indeed: 8 points
- Remote.io: 7 points
- RemoteOK: 7 points
- Glassdoor: 6 points
- ZipRecruiter: 6 points
- Google: 5 points
- Naukri: 4 points
- Bayt: 3 points
- BDJobs: 3 points

#### 5. Role Fit Score (10 points)
- Not senior/manager/director: 10 points
- Junior/Mid-level: 10 points
- Senior (if OK): 5 points
- Manager/Director: 0 points

#### 6. Location Score (5 points)
- Exact location match: 5 points
- Remote/Work from home: 5 points
- Same country: 3 points
- Different country: 0 points

## Implementation Plan

### Phase 1: Create Scoring Module
1. Create `scorer.py` module with scoring functions
2. Implement individual score calculators
3. Create main `score_job()` function

### Phase 2: Modify API Flow
1. Replace/explement `apply_filters()` with `score_and_rank_jobs()`
2. Sort jobs by score (descending)
3. Return top N jobs (or all with scores)

### Phase 3: Display Improvements
1. Show score in result.json
2. Add score breakdown to each job
3. Optionally filter by minimum score threshold

## Files to Modify/Create
- `scorer.py` (new) - Score calculation module
- `api.py` - Update to use scoring instead of filtering

## Expected Output
- Jobs ranked by total score (0-100)
- Each job has a `score` and `score_breakdown` field
- Results sorted by score (highest first)
