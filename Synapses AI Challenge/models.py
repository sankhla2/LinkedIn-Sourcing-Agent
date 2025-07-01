"""
Data models for the LinkedIn Sourcing Agent
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Candidate(BaseModel):
    """Model for a LinkedIn candidate profile"""
    name: str
    linkedin_url: str
    headline: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    summary: Optional[str] = None
    
    # Scoring fields
    fit_score: Optional[float] = None
    score_breakdown: Optional[Dict[str, float]] = None
    confidence_score: Optional[float] = None
    
    # Outreach
    outreach_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class JobRequest(BaseModel):
    """Model for job sourcing requests"""
    job_description: str
    location: Optional[str] = None
    company: Optional[str] = None
    max_candidates: Optional[int] = 25
    min_score: Optional[float] = 6.0
    
class JobResponse(BaseModel):
    """Model for job sourcing responses"""
    job_id: str
    status: JobStatus
    candidates_found: int
    top_candidates: List[Candidate]
    processing_time: Optional[float] = None
    created_at: datetime = datetime.now()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ScoreBreakdown(BaseModel):
    """Detailed scoring breakdown"""
    education: float
    trajectory: float
    company: float
    skills: float
    location: float
    tenure: float
    total_score: float
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "education": self.education,
            "trajectory": self.trajectory,
            "company": self.company,
            "skills": self.skills,
            "location": self.location,
            "tenure": self.tenure,
            "total_score": self.total_score
        }

class SearchResult(BaseModel):
    """Model for LinkedIn search results"""
    title: str
    url: str
    snippet: str
    position: int
    
class OutreachMessage(BaseModel):
    """Model for generated outreach messages"""
    candidate_name: str
    message: str
    personalization_score: Optional[float] = None
    key_highlights: Optional[List[str]] = None

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None 