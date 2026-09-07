from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.jobs.aggregator import get_job_matches
from app.schemas.job_schema import MatchResponse

router = APIRouter()

@router.post("/match", response_model=MatchResponse)
async def match_jobs(candidate_profile: Dict[str, Any]):
    """
    Accepts the AI-extracted candidate profile (specifically technical skills)
    and returns matching roles and mock Sri Lankan job postings.
    """
    try:
        matches = await get_job_matches(candidate_profile)
        return matches
    except Exception as e:
        print(f"Error matching jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to match jobs and roles.")
