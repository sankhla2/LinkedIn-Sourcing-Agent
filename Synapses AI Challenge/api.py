"""
FastAPI Application for LinkedIn Sourcing Agent
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any, Optional
import json

from models import JobRequest, JobResponse, APIResponse, Candidate
from sourcing_agent import LinkedInSourcingAgent

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn Sourcing Agent API",
    description="AI-powered LinkedIn candidate sourcing and outreach generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the sourcing agent
agent = LinkedInSourcingAgent()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LinkedIn Sourcing Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /source-candidates": "Submit a job for candidate sourcing",
            "GET /candidates/{job_id}": "Get sourced candidates for a job",
            "GET /jobs": "Get all jobs",
            "GET /health": "Health check",
            "POST /test": "Run test sourcing with sample job"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="Service is healthy",
        data={"status": "healthy", "agent_initialized": True}
    )

@app.post("/source-candidates", response_model=APIResponse)
async def source_candidates(job_request: JobRequest):
    """
    Submit a job for candidate sourcing
    
    This endpoint:
    1. Searches LinkedIn for relevant profiles
    2. Scores candidates based on job fit
    3. Generates personalized outreach messages
    4. Returns top candidates with scores and messages
    """
    try:
        # Run the sourcing process
        response = agent.source_candidates(job_request)
        
        # Get candidate summary
        summary = agent.get_candidate_summary(response.top_candidates)
        
        return APIResponse(
            success=True,
            message=f"Successfully sourced {response.candidates_found} candidates",
            data={
                "job_response": response.dict(),
                "summary": summary
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during sourcing: {str(e)}"
        )

@app.get("/candidates/{job_id}", response_model=APIResponse)
async def get_candidates(job_id: str):
    """
    Get sourced candidates for a specific job
    """
    try:
        job_data = agent.get_job_status(job_id)
        
        if not job_data:
            raise HTTPException(
                status_code=404,
                detail=f"Job {job_id} not found"
            )
        
        return APIResponse(
            success=True,
            message="Job data retrieved successfully",
            data=job_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving job data: {str(e)}"
        )

@app.get("/jobs", response_model=APIResponse)
async def get_all_jobs():
    """
    Get all jobs and their status
    """
    try:
        jobs = agent.get_all_jobs()
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(jobs)} jobs",
            data={"jobs": jobs}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving jobs: {str(e)}"
        )

@app.post("/test", response_model=APIResponse)
async def run_test_sourcing():
    """
    Run test sourcing with the sample job description
    """
    try:
        response = agent.run_test_sourcing()
        
        # Get candidate summary
        summary = agent.get_candidate_summary(response.top_candidates)
        
        return APIResponse(
            success=True,
            message=f"Test sourcing completed. Found {response.candidates_found} candidates",
            data={
                "job_response": response.dict(),
                "summary": summary
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during test sourcing: {str(e)}"
        )

@app.post("/batch-source", response_model=APIResponse)
async def batch_source_candidates(job_requests: List[JobRequest]):
    """
    Process multiple job requests in batch
    """
    try:
        if len(job_requests) > 10:
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 jobs allowed per batch request"
            )
        
        responses = agent.batch_source_candidates(job_requests)
        
        # Calculate batch summary
        total_candidates = sum(r.candidates_found for r in responses)
        successful_jobs = len([r for r in responses if r.status.value == "completed"])
        
        return APIResponse(
            success=True,
            message=f"Batch processing completed. {successful_jobs}/{len(job_requests)} jobs successful. Total candidates: {total_candidates}",
            data={
                "responses": [r.dict() for r in responses],
                "batch_summary": {
                    "total_jobs": len(job_requests),
                    "successful_jobs": successful_jobs,
                    "total_candidates": total_candidates
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during batch sourcing: {str(e)}"
        )

@app.get("/export/{job_id}")
async def export_results(job_id: str, format: str = "json"):
    """
    Export results in different formats (JSON or CSV)
    """
    try:
        job_data = agent.get_job_status(job_id)
        
        if not job_data:
            raise HTTPException(
                status_code=404,
                detail=f"Job {job_id} not found"
            )
        
        if job_data["status"].value != "completed":
            raise HTTPException(
                status_code=400,
                detail="Job not completed yet"
            )
        
        response = job_data["response"]
        exported_data = agent.export_results(response, format)
        
        if format.lower() == "csv":
            return JSONResponse(
                content=exported_data,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=candidates_{job_id}.csv"}
            )
        else:
            return JSONResponse(
                content=json.loads(exported_data),
                media_type="application/json"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting results: {str(e)}"
        )

@app.get("/stats", response_model=APIResponse)
async def get_stats():
    """
    Get overall statistics about the sourcing agent
    """
    try:
        all_jobs = agent.get_all_jobs()
        
        # Calculate statistics
        total_jobs = len(all_jobs)
        completed_jobs = len([j for j in all_jobs if j["status"].value == "completed"])
        failed_jobs = len([j for j in all_jobs if j["status"].value == "failed"])
        
        # Get total candidates from completed jobs
        total_candidates = 0
        for job in all_jobs:
            if job["status"].value == "completed" and "response" in job:
                total_candidates += job["response"].candidates_found
        
        stats = {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "success_rate": round(completed_jobs / total_jobs * 100, 2) if total_jobs > 0 else 0,
            "total_candidates_sourced": total_candidates,
            "average_candidates_per_job": round(total_candidates / completed_jobs, 2) if completed_jobs > 0 else 0
        }
        
        return APIResponse(
            success=True,
            message="Statistics retrieved successfully",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving statistics: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 