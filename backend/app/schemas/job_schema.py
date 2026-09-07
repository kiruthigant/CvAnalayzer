from pydantic import BaseModel
from typing import List, Optional

class JobMatch(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    match_score: int
    match_reasons: List[str]
    missing_skills: List[str]
    salary_range: Optional[str] = None
    url: str

class RoleMatch(BaseModel):
    title: str
    match_score: int
    description: str
    key_skills: List[str]

class MatchResponse(BaseModel):
    roles: List[RoleMatch]
    jobs: List[JobMatch]
