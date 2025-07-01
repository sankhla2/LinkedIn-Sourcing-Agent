"""
Main LinkedIn Sourcing Agent
"""

import time
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from config import Config
from models import Candidate, JobRequest, JobResponse, JobStatus
from linkedin_searcher import LinkedInSearcher
from scorer import FitScorer
from outreach_generator import OutreachGenerator

class LinkedInSourcingAgent:
    """Main agent that orchestrates the entire sourcing process"""
    
    def __init__(self):
        self.config = Config()
        self.searcher = LinkedInSearcher()
        self.scorer = FitScorer()
        self.outreach_generator = OutreachGenerator()
        self.jobs = {}  # Simple in-memory storage for jobs
    
    def source_candidates(self, job_request: JobRequest) -> JobResponse:
        """
        Complete sourcing pipeline: search → score → generate outreach
        """
        start_time = time.time()
        job_id = str(uuid.uuid4())
        
        try:
            # Update job status
            self.jobs[job_id] = {
                "status": JobStatus.PROCESSING,
                "request": job_request,
                "start_time": start_time
            }
            
            print(f"Starting sourcing for job {job_id}")
            
            # Step 1: Search for LinkedIn profiles
            print("Step 1: Searching LinkedIn profiles...")
            search_results = self.searcher.search_linkedin_profiles(
                job_request.job_description,
                job_request.location,
                job_request.max_candidates
            )
            
            # Step 2: Extract candidate data
            print("Step 2: Extracting candidate data...")
            candidates = self.searcher.extract_profile_data(search_results)
            
            if not candidates:
                raise Exception("No candidates found")
            
            print(f"Found {len(candidates)} candidates")
            
            # Step 3: Score candidates
            print("Step 3: Scoring candidates...")
            scored_candidates = self.scorer.score_candidates(candidates, job_request.job_description)
            
            # Step 4: Filter by minimum score
            filtered_candidates = [
                c for c in scored_candidates 
                if c.fit_score and c.fit_score >= job_request.min_score
            ]
            
            print(f"Filtered to {len(filtered_candidates)} candidates with score >= {job_request.min_score}")
            
            # Step 5: Generate outreach messages for top candidates
            print("Step 5: Generating outreach messages...")
            top_candidates = filtered_candidates[:10]  # Top 10 candidates
            
            for candidate in top_candidates:
                outreach_message = self.outreach_generator.generate_outreach_messages(
                    [candidate], 
                    job_request.job_description,
                    max_messages=1
                )
                if outreach_message:
                    candidate.outreach_message = outreach_message[0].message
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create response
            response = JobResponse(
                job_id=job_id,
                status=JobStatus.COMPLETED,
                candidates_found=len(candidates),
                top_candidates=top_candidates,
                processing_time=round(processing_time, 2)
            )
            
            # Update job status
            self.jobs[job_id]["status"] = JobStatus.COMPLETED
            self.jobs[job_id]["response"] = response
            
            print(f"Sourcing completed in {processing_time:.2f} seconds")
            return response
            
        except Exception as e:
            print(f"Error during sourcing: {e}")
            
            # Update job status
            self.jobs[job_id]["status"] = JobStatus.FAILED
            self.jobs[job_id]["error"] = str(e)
            
            # Return error response
            return JobResponse(
                job_id=job_id,
                status=JobStatus.FAILED,
                candidates_found=0,
                top_candidates=[],
                processing_time=time.time() - start_time
            )
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific job"""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Get all jobs"""
        return [
            {
                "job_id": job_id,
                "status": job_data["status"],
                "request": job_data["request"],
                "start_time": job_data.get("start_time"),
                "error": job_data.get("error")
            }
            for job_id, job_data in self.jobs.items()
        ]
    
    def run_test_sourcing(self) -> JobResponse:
        """
        Run sourcing with the test job description
        """
        test_request = JobRequest(
            job_description=self.config.TEST_JOB_DESCRIPTION,
            location="Mountain View, CA",
            company="Windsurf",
            max_candidates=25,
            min_score=6.0
        )
        
        return self.source_candidates(test_request)
    
    def batch_source_candidates(self, job_requests: List[JobRequest]) -> List[JobResponse]:
        """
        Process multiple job requests in batch
        """
        responses = []
        
        for request in job_requests:
            try:
                response = self.source_candidates(request)
                responses.append(response)
                
                # Add delay between jobs to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing batch job: {e}")
                # Create error response
                error_response = JobResponse(
                    job_id=str(uuid.uuid4()),
                    status=JobStatus.FAILED,
                    candidates_found=0,
                    top_candidates=[],
                    processing_time=0
                )
                responses.append(error_response)
        
        return responses
    
    def get_candidate_summary(self, candidates: List[Candidate]) -> Dict[str, Any]:
        """
        Generate a summary of candidates
        """
        if not candidates:
            return {
                "total_candidates": 0,
                "average_score": 0,
                "score_distribution": {},
                "top_skills": [],
                "top_companies": [],
                "location_distribution": {}
            }
        
        # Calculate statistics
        scores = [c.fit_score for c in candidates if c.fit_score]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Score distribution
        score_distribution = {
            "9-10": len([c for c in candidates if c.fit_score and c.fit_score >= 9]),
            "8-9": len([c for c in candidates if c.fit_score and 8 <= c.fit_score < 9]),
            "7-8": len([c for c in candidates if c.fit_score and 7 <= c.fit_score < 8]),
            "6-7": len([c for c in candidates if c.fit_score and 6 <= c.fit_score < 7]),
            "5-6": len([c for c in candidates if c.fit_score and 5 <= c.fit_score < 6]),
            "<5": len([c for c in candidates if c.fit_score and c.fit_score < 5])
        }
        
        # Top skills
        all_skills = []
        for candidate in candidates:
            if candidate.skills:
                all_skills.extend(candidate.skills)
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top companies
        company_counts = {}
        for candidate in candidates:
            if candidate.company:
                company_counts[candidate.company] = company_counts.get(candidate.company, 0) + 1
        
        top_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Location distribution
        location_counts = {}
        for candidate in candidates:
            if candidate.location:
                location_counts[candidate.location] = location_counts.get(candidate.location, 0) + 1
        
        return {
            "total_candidates": len(candidates),
            "average_score": round(average_score, 2),
            "score_distribution": score_distribution,
            "top_skills": top_skills,
            "top_companies": top_companies,
            "location_distribution": location_counts
        }
    
    def export_results(self, job_response: JobResponse, format: str = "json") -> str:
        """
        Export results in different formats
        """
        if format.lower() == "json":
            return job_response.json(indent=2)
        elif format.lower() == "csv":
            # Create CSV format
            csv_lines = ["Name,LinkedIn URL,Fit Score,Company,Location,Skills,Outreach Message"]
            
            for candidate in job_response.top_candidates:
                skills_str = ";".join(candidate.skills) if candidate.skills else ""
                outreach_str = candidate.outreach_message.replace('"', '""') if candidate.outreach_message else ""
                
                csv_line = f'"{candidate.name}","{candidate.linkedin_url}",{candidate.fit_score},"{candidate.company}","{candidate.location}","{skills_str}","{outreach_str}"'
                csv_lines.append(csv_line)
            
            return "\n".join(csv_lines)
        else:
            raise ValueError(f"Unsupported format: {format}") 