import os
from openai import AsyncOpenAI
import json
from ...schemas.cv_schema import CVAnalysisResponse
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client with Groq's base URL
client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are an expert AI Career Analyzer and ATS system. 
Your goal is to parse the provided CV, extract all relevant information, and critically evaluate the candidate's strengths, weaknesses, and ATS compatibility.
DO NOT hallucinate. Only use information explicitly present or highly probable based on the CV.
If information is missing, use null or empty lists as defined in the schema.
For ATS scoring, simulate a strict but fair ATS system.
Provide actionable improvement recommendations.

IMPORTANT: You MUST respond with ONLY a valid JSON object. Do not include markdown formatting or extra text.
The JSON must strictly match this schema structure:
{
  "candidate": {"name": "", "email": "", "phone": "", "location": ""},
  "summary": "",
  "technical_skills": [],
  "soft_skills": [],
  "experience": [{"job_title": "", "company": "", "duration": "", "description": []}],
  "education": [{"degree": "", "institution": "", "year": ""}],
  "projects": [],
  "certifications": [],
  "languages": [],
  "ats_analysis": {
    "overall_score": 0,
    "breakdown": {"keyword_optimization": 0, "experience_relevance": 0, "technical_skills": 0, "resume_structure": 0, "achievements": 0, "readability": 0},
    "feedback": []
  },
  "strengths": [{"title": "", "description": ""}],
  "improvement_areas": [{"skill": "", "status": "", "recommendation": "", "priority": ""}]
}
"""

async def analyze_cv_with_openai(cv_content: Dict[str, Any]) -> CVAnalysisResponse:
    """
    Sends the CV to Groq and returns a structured response.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    is_vision = cv_content.get("is_scanned") and cv_content.get("images")
    
    if is_vision:
        # Vision-based extraction
        content_array = [{"type": "text", "text": "Please analyze this scanned CV. The pages are provided as images below."}]
        for img_url in cv_content["images"]:
            content_array.append({
                "type": "image_url",
                "image_url": {"url": img_url}
            })
        messages.append({"role": "user", "content": content_array})
    else:
        # Text-based extraction
        messages.append({
            "role": "user", 
            "content": f"Please analyze this CV text:\n\n{cv_content.get('text', '')}"
        })
        
    completion = await client.chat.completions.create(
        model=VISION_MODEL if is_vision else TEXT_MODEL,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    raw_json = completion.choices[0].message.content
    try:
        parsed_data = json.loads(raw_json)
        return CVAnalysisResponse(**parsed_data)
    except json.JSONDecodeError:
        print("Failed to decode JSON from Groq:", raw_json)
        raise
