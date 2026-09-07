from typing import List, Dict, Any
import time
from .scraper import scrape_sri_lankan_jobs

# Simple in-memory cache for scraped jobs to prevent getting IP blocked
_cached_jobs = []
_last_scrape_time = 0
CACHE_TTL = 3600  # 1 hour in seconds

# Mock Roles Taxonomy (We keep this since roles are static)
MOCK_ROLES = [
    {
        "title": "Frontend Developer",
        "description": "Builds user interfaces and web applications.",
        "skills": ["react", "javascript", "typescript", "html", "css", "vue", "angular", "tailwind"]
    },
    {
        "title": "Backend Developer",
        "description": "Builds and maintains server-side logic and APIs.",
        "skills": ["python", "node", "java", "c#", "sql", "django", "fastapi", "express", "go", "aws"]
    },
    {
        "title": "Full Stack Developer",
        "description": "Works on both frontend and backend development.",
        "skills": ["javascript", "react", "python", "node", "sql", "typescript", "aws", "docker"]
    },
    {
        "title": "Data Scientist",
        "description": "Analyzes complex data to help guide decision-making.",
        "skills": ["python", "machine learning", "data analysis", "sql", "r", "pandas", "tensorflow"]
    },
    {
        "title": "DevOps Engineer",
        "description": "Manages infrastructure, deployments, and CI/CD.",
        "skills": ["aws", "docker", "kubernetes", "linux", "ci/cd", "terraform", "bash", "jenkins"]
    }
]

def calculate_match(candidate_skills: List[str], required_skills: List[str]) -> tuple[int, List[str], List[str]]:
    """Calculates compatibility score and identifies matching/missing skills."""
    if not required_skills:
        return 0, [], []
        
    candidate_skills_lower = [s.lower().strip() for s in candidate_skills]
    matched = []
    missing = []
    
    for req in required_skills:
        req_lower = req.lower().strip()
        # Basic substring or exact match
        if any(req_lower in cs or cs in req_lower for cs in candidate_skills_lower):
            matched.append(req)
        else:
            missing.append(req)
            
    score = int((len(matched) / len(required_skills)) * 100)
    return score, matched, missing

async def get_job_matches(candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Matches the CV profile against roles and newly scraped real jobs."""
    global _cached_jobs, _last_scrape_time
    
    candidate_skills = candidate_profile.get("technical_skills", [])
    
    # 1. Match Roles
    matched_roles = []
    for role in MOCK_ROLES:
        score, matched, _ = calculate_match(candidate_skills, role["skills"])
        if score > 0:
            matched_roles.append({
                "title": role["title"],
                "description": role["description"],
                "key_skills": role["skills"],
                "match_score": score
            })
            
    # Sort roles by score descending
    matched_roles.sort(key=lambda x: x["match_score"], reverse=True)
    
    # 2. Get Live Sri Lankan Jobs (using Cache)
    current_time = time.time()
    if not _cached_jobs or (current_time - _last_scrape_time) > CACHE_TTL:
        print("Scraping fresh jobs...")
        _cached_jobs = await scrape_sri_lankan_jobs()
        _last_scrape_time = current_time
    else:
        print("Using cached scraped jobs.")

    # 3. Match Jobs
    matched_jobs = []
    for job in _cached_jobs:
        score, matched, missing = calculate_match(candidate_skills, job["required_skills"])
        if score > 20: # Only return jobs with > 20% match
            matched_jobs.append({
                "id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "description": job["description"],
                "required_skills": job["required_skills"],
                "salary_range": job["salary_range"],
                "url": job["url"],
                "match_score": score,
                "match_reasons": matched,
                "missing_skills": missing
            })
            
    # Sort jobs by score descending
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "roles": matched_roles[:3], # Top 3 roles
        "jobs": matched_jobs
    }
