from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.cv import router as cv_router
from app.api.jobs import router as jobs_router

app = FastAPI(title="AI Career Analyzer API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cv_router, prefix="/api/v1/cv", tags=["CV Analysis"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["Jobs & Roles"])

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "message": "API is healthy"}
