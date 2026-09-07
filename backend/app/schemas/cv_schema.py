from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateInfo(BaseModel):
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    location: Optional[str] = Field(None, description="Candidate's location or city")

class ExperienceItem(BaseModel):
    job_title: Optional[str] = Field(None)
    company: Optional[str] = Field(None)
    duration: Optional[str] = Field(None)
    description: Optional[List[str]] = Field(default_factory=list, description="Bullet points of achievements/responsibilities")

class EducationItem(BaseModel):
    degree: Optional[str] = Field(None)
    institution: Optional[str] = Field(None)
    year: Optional[str] = Field(None)

class ATSScoreBreakdown(BaseModel):
    keyword_optimization: int = Field(..., ge=0, le=100)
    experience_relevance: int = Field(..., ge=0, le=100)
    technical_skills: int = Field(..., ge=0, le=100)
    resume_structure: int = Field(..., ge=0, le=100)
    achievements: int = Field(..., ge=0, le=100)
    readability: int = Field(..., ge=0, le=100)

class ATSAnalysis(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    breakdown: ATSScoreBreakdown
    feedback: List[str] = Field(default_factory=list, description="Constructive feedback on ATS readability and keyword usage")

class Strength(BaseModel):
    title: str = Field(..., description="E.g., Backend Development")
    description: str = Field(..., description="Explanation based on CV evidence")

class ImprovementArea(BaseModel):
    skill: str = Field(..., description="E.g., PyTorch")
    status: str = Field(..., description="'Missing / Not demonstrated' or 'Weakly demonstrated'")
    recommendation: str = Field(..., description="Actionable recommendation for improvement")
    priority: str = Field(..., description="'HIGH PRIORITY', 'MEDIUM PRIORITY', or 'LOW PRIORITY'")

class CVAnalysisResponse(BaseModel):
    candidate: CandidateInfo
    summary: Optional[str] = Field(None, description="Professional summary extracted or inferred")
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    
    ats_analysis: ATSAnalysis
    strengths: List[Strength] = Field(default_factory=list)
    improvement_areas: List[ImprovementArea] = Field(default_factory=list)
