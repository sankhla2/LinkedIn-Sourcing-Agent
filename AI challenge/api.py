from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import json
import tempfile
import os
from main_integrated import LinkedInSourcingAgent
from batch_processor import BatchJobProcessor

app = FastAPI(
    title="LinkedIn Sourcing Agent API",
    description="AI-powered LinkedIn candidate sourcing, scoring, and outreach generation",
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

# Initialize the agent
agent = LinkedInSourcingAgent()

# Pydantic models for request/response
class JobDescriptionRequest(BaseModel):
    job_description: str
    max_candidates: Optional[int] = 10
    max_messages: Optional[int] = 5

class JobDescriptionResponse(BaseModel):
    job_id: str
    candidates_found: int
    top_candidates: List[Dict]
    outreach_messages: List[Dict]
    message_summary: Dict

class BatchJobRequest(BaseModel):
    job_descriptions: List[str]
    max_workers: Optional[int] = 3
    max_candidates_per_job: Optional[int] = 10

class BatchJobResponse(BaseModel):
    total_jobs: int
    total_candidates: int
    results: List[Dict]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "LinkedIn Sourcing Agent API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/process-job": "Process a single job description",
            "/process-pdf": "Process a job description PDF",
            "/batch-process": "Process multiple job descriptions",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "linkedin-sourcing-agent"}

@app.post("/process-job", response_model=JobDescriptionResponse)
async def process_job_description(request: JobDescriptionRequest):
    """
    Process a job description text and return candidates with scores and messages
    """
    try:
        # Create a temporary file with the job description
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(request.job_description)
            temp_file = f.name
        
        # Process the job description
        results = agent.process_job_description(
            temp_file, 
            max_candidates=request.max_candidates,
            max_messages=request.max_messages
        )
        
        # Clean up temporary file
        os.unlink(temp_file)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        # Format response
        response = {
            "job_id": "job_" + str(hash(request.job_description))[:8],
            "candidates_found": results["candidates_found"],
            "top_candidates": results["top_candidates"],
            "outreach_messages": results.get("messages", []),
            "message_summary": results.get("message_summary", {})
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job: {str(e)}")

@app.post("/process-pdf", response_model=JobDescriptionResponse)
async def process_pdf_job(
    file: UploadFile = File(...),
    max_candidates: int = Form(10),
    max_messages: int = Form(5)
):
    """
    Process a job description PDF and return candidates with scores and messages
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f:
            content = await file.read()
            f.write(content)
            temp_file = f.name
        
        # Process the PDF
        results = agent.process_job_description(
            temp_file,
            max_candidates=max_candidates,
            max_messages=max_messages
        )
        
        # Clean up temporary file
        os.unlink(temp_file)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        # Format response
        response = {
            "job_id": "pdf_" + file.filename.replace('.pdf', ''),
            "candidates_found": results["candidates_found"],
            "top_candidates": results["top_candidates"],
            "outreach_messages": results.get("messages", []),
            "message_summary": results.get("message_summary", {})
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/batch-process", response_model=BatchJobResponse)
async def batch_process_jobs(request: BatchJobRequest):
    """
    Process multiple job descriptions in parallel
    """
    try:
        # Create temporary files for each job description
        temp_files = []
        for i, job_desc in enumerate(request.job_descriptions):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(job_desc)
                temp_files.append(f.name)
        
        # Initialize batch processor
        processor = BatchJobProcessor(
            max_workers=request.max_workers,
            min_delay=2.0,
            max_delay=5.0
        )
        
        # Process jobs in batch
        batch_results = processor.process_jobs_in_batch(temp_files)
        
        # Clean up temporary files
        for temp_file in temp_files:
            os.unlink(temp_file)
        
        # Calculate totals
        total_candidates = sum(result["candidates_found"] for result in batch_results)
        
        response = {
            "total_jobs": len(batch_results),
            "total_candidates": total_candidates,
            "results": batch_results
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch processing: {str(e)}")

@app.get("/candidates/{job_id}")
async def get_candidates(job_id: str):
    """
    Get candidates for a specific job (if cached)
    """
    try:
        # This would typically query a database
        # For now, return a placeholder
        return {
            "job_id": job_id,
            "message": "Candidates not found in cache. Process the job first using /process-job endpoint."
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

@app.get("/stats")
async def get_stats():
    """
    Get API usage statistics
    """
    return {
        "total_requests": 0,  # Would be tracked in production
        "successful_requests": 0,
        "average_response_time": 0,
        "uptime": "100%"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 