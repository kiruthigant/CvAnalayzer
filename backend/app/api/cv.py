from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
from ..services.parser import extract_cv_content
from ..services.ai.openai_service import analyze_cv_with_openai

router = APIRouter()

@router.post("/analyze")
async def analyze_cv(file: UploadFile = File(...)):
    """
    Analyzes an uploaded CV file.
    Critically ensures the file is temporarily saved for processing
    and ALWAYS deleted before returning the response.
    """
    # 1. Validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    temp_file_path = ""
    try:
        # 2. Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # 3. Extract text / images
        cv_content = extract_cv_content(temp_file_path, file.filename)
        
        if not cv_content.get("text") and not cv_content.get("images"):
            raise HTTPException(status_code=422, detail="Could not extract text or images from the provided document.")
            
        # 4. Phase 3 - Pass cv_content to AI Analysis Engine
        analysis_result = await analyze_cv_with_openai(cv_content)
        
        return {
            "status": "success",
            "message": "CV analyzed successfully",
            "data": analysis_result.model_dump()
        }
        
    except Exception as e:
        # Avoid exposing stack traces
        print(f"Error analyzing CV: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during CV processing.")
        
    finally:
        # 5. Mandatory Cleanup - ALWAYS EXECUTED
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
