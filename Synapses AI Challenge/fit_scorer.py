"""
Fit Scoring Algorithm for Candidate Evaluation
"""

import re
from typing import List, Dict, Optional, Any
from config import Config
from models import Candidate, ScoreBreakdown

class FitScorer:
    """Implements the fit scoring algorithm for candidate evaluation"""
    
    def __init__(self):
        self.config = Config()
        self.weights = self.config.SCORING_WEIGHTS
    
    def score_candidates(self, candidates: List[Candidate], job_description: str) -> List[Candidate]:
        """
        Score all candidates based on job description
        """
        for candidate in candidates:
            score_breakdown = self._calculate_score_breakdown(candidate, job_description)
            candidate.fit_score = score_breakdown.total_score
            candidate.score_breakdown = score_breakdown.to_dict()
            candidate.confidence_score = self._calculate_confidence_score(candidate)
        
        # Sort candidates by fit score (highest first)
        candidates.sort(key=lambda x: x.fit_score or 0, reverse=True)
        
        return candidates
    
    def _calculate_score_breakdown(self, candidate: Candidate, job_description: str) -> ScoreBreakdown:
        """
        Calculate detailed score breakdown for a candidate
        """
        education_score = self._score_education(candidate)
        trajectory_score = self._score_career_trajectory(candidate)
        company_score = self._score_company_relevance(candidate)
        skills_score = self._score_skills_match(candidate, job_description)
        location_score = self._score_location_match(candidate, job_description)
        tenure_score = self._score_tenure(candidate)
        
        # Calculate weighted total
        total_score = (
            education_score * self.weights["education"] +
            trajectory_score * self.weights["trajectory"] +
            company_score * self.weights["company"] +
            skills_score * self.weights["skills"] +
            location_score * self.weights["location"] +
            tenure_score * self.weights["tenure"]
        )
        
        return ScoreBreakdown(
            education=education_score,
            trajectory=trajectory_score,
            company=company_score,
            skills=skills_score,
            location=location_score,
            tenure=tenure_score,
            total_score=round(total_score, 2)
        )
    
    def _score_education(self, candidate: Candidate) -> float:
        """
        Score education (20% weight)
        - Elite schools: 9-10
        - Strong schools: 7-8
        - Standard universities: 5-6
        - Clear progression: 8-10
        """
        if not candidate.education:
            return 5.0  # Default score for unknown education
        
        education_lower = candidate.education.lower()
        
        # Check for elite schools
        for school in self.config.ELITE_SCHOOLS:
            if school in education_lower:
                return 9.5
        
        # Check for strong schools (top 50 universities)
        strong_schools = {
            "university of michigan", "georgia tech", "university of illinois", 
            "university of texas", "university of wisconsin", "purdue university",
            "university of maryland", "university of pennsylvania", "carnegie mellon",
            "university of washington", "university of california", "university of virginia"
        }
        
        for school in strong_schools:
            if school in education_lower:
                return 7.5
        
        # Check for clear progression (BS -> MS -> PhD)
        if any(degree in education_lower for degree in ["phd", "doctorate", "ph.d"]):
            return 9.0
        elif any(degree in education_lower for degree in ["master", "ms", "m.s"]):
            return 8.0
        elif any(degree in education_lower for degree in ["bachelor", "bs", "b.s"]):
            return 6.0
        
        return 5.0
    
    def _score_career_trajectory(self, candidate: Candidate) -> float:
        """
        Score career trajectory (20% weight)
        - Steady growth: 6-8
        - Limited progression: 3-5
        """
        if not candidate.experience:
            return 5.0  # Default score
        
        # Analyze experience progression
        experience_count = len(candidate.experience)
        
        if experience_count >= 3:
            # Check for title progression
            titles = [exp.get("title", "").lower() for exp in candidate.experience]
            
            # Look for progression indicators
            progression_indicators = [
                "senior", "lead", "principal", "staff", "director", "manager",
                "architect", "head of", "vp", "cto"
            ]
            
            progression_count = sum(1 for title in titles 
                                  for indicator in progression_indicators 
                                  if indicator in title)
            
            if progression_count >= 2:
                return 7.5  # Steady growth
            elif progression_count >= 1:
                return 6.0  # Some growth
            else:
                return 4.0  # Limited progression
        
        return 5.0
    
    def _score_company_relevance(self, candidate: Candidate) -> float:
        """
        Score company relevance (15% weight)
        - Top tech companies: 9-10
        - Relevant industry: 7-8
        - Any experience: 5-6
        """
        if not candidate.company:
            return 5.0
        
        company_lower = candidate.company.lower()
        
        # Check for top tech companies
        for company in self.config.TOP_TECH_COMPANIES:
            if company in company_lower:
                return 9.5
        
        # Check for relevant industry keywords
        relevant_industries = [
            "tech", "software", "ai", "machine learning", "fintech", "startup",
            "saas", "cloud", "data", "analytics", "cybersecurity"
        ]
        
        for industry in relevant_industries:
            if industry in company_lower:
                return 7.5
        
        return 5.0
    
    def _score_skills_match(self, candidate: Candidate, job_description: str) -> float:
        """
        Score skills match (25% weight)
        - Perfect skill match: 9-10
        - Strong overlap: 7-8
        - Some relevant skills: 5-6
        """
        if not candidate.skills:
            return 5.0
        
        # Extract skills from job description
        job_skills = self._extract_skills_from_job(job_description)
        
        if not job_skills:
            return 5.0
        
        # Calculate skill overlap
        candidate_skills_lower = [skill.lower() for skill in candidate.skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Find matching skills
        matching_skills = []
        for job_skill in job_skills_lower:
            for candidate_skill in candidate_skills_lower:
                if job_skill in candidate_skill or candidate_skill in job_skill:
                    matching_skills.append(job_skill)
                    break
        
        # Calculate match percentage
        match_percentage = len(matching_skills) / len(job_skills_lower)
        
        if match_percentage >= 0.7:
            return 9.5  # Perfect match
        elif match_percentage >= 0.4:
            return 7.5  # Strong overlap
        elif match_percentage >= 0.2:
            return 6.0  # Some relevant skills
        else:
            return 4.0  # Poor match
    
    def _score_location_match(self, candidate: Candidate, job_description: str) -> float:
        """
        Score location match (10% weight)
        - Exact city: 10
        - Same metro: 8
        - Remote-friendly: 6
        """
        if not candidate.location:
            return 6.0  # Assume remote-friendly
        
        # Extract location from job description
        job_location = self._extract_location_from_job(job_description)
        
        if not job_location:
            return 6.0  # Assume remote-friendly
        
        candidate_location_lower = candidate.location.lower()
        job_location_lower = job_location.lower()
        
        # Check for exact city match
        if candidate_location_lower == job_location_lower:
            return 10.0
        
        # Check for same metro area
        metro_areas = {
            "san francisco": ["san francisco", "sf", "bay area", "silicon valley", "mountain view", "palo alto"],
            "new york": ["new york", "nyc", "manhattan", "brooklyn", "queens"],
            "seattle": ["seattle", "bellevue", "redmond", "kirkland"],
            "austin": ["austin", "round rock", "cedar park"],
            "boston": ["boston", "cambridge", "somerville", "waltham"]
        }
        
        for metro, cities in metro_areas.items():
            if (candidate_location_lower in cities and job_location_lower in cities) or \
               (candidate_location_lower == metro and job_location_lower in cities) or \
               (job_location_lower == metro and candidate_location_lower in cities):
                return 8.0
        
        return 6.0  # Remote-friendly
    
    def _score_tenure(self, candidate: Candidate) -> float:
        """
        Score tenure (10% weight)
        - 2-3 years average: 9-10
        - 1-2 years: 6-8
        - Job hopping: 3-5
        """
        if not candidate.experience:
            return 5.0
        
        # Calculate average tenure
        total_years = 0
        job_count = len(candidate.experience)
        
        for exp in candidate.experience:
            duration = exp.get("duration", "1 year")
            # Extract years from duration string
            years_match = re.search(r'(\d+)', duration)
            if years_match:
                total_years += int(years_match.group(1))
            else:
                total_years += 1  # Default to 1 year
        
        if job_count > 0:
            avg_tenure = total_years / job_count
        else:
            avg_tenure = 1.0
        
        if avg_tenure >= 2.5:
            return 9.5  # Long tenure
        elif avg_tenure >= 1.5:
            return 7.0  # Moderate tenure
        elif avg_tenure >= 1.0:
            return 5.5  # Short tenure
        else:
            return 3.0  # Job hopping
    
    def _extract_skills_from_job(self, job_description: str) -> List[str]:
        """Extract required skills from job description"""
        skills = []
        
        # Common tech skills to look for
        tech_skills = [
            "python", "javascript", "java", "react", "node.js", "aws", "docker", 
            "kubernetes", "machine learning", "deep learning", "tensorflow", 
            "pytorch", "sql", "mongodb", "redis", "kafka", "microservices",
            "api", "rest", "graphql", "git", "linux", "agile", "scrum"
        ]
        
        description_lower = job_description.lower()
        
        for skill in tech_skills:
            if skill in description_lower:
                skills.append(skill)
        
        return skills
    
    def _extract_location_from_job(self, job_description: str) -> Optional[str]:
        """Extract location from job description"""
        # Common location patterns
        location_patterns = [
            r'location[:\s]+([A-Z][a-zA-Z\s,]+)',
            r'in ([A-Z][a-zA-Z\s,]+), [A-Z]{2}',
            r'based in ([A-Z][a-zA-Z\s,]+)',
            r'([A-Z][a-zA-Z\s,]+), [A-Z]{2}'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _calculate_confidence_score(self, candidate: Candidate) -> float:
        """
        Calculate confidence score based on data completeness
        """
        confidence_factors = []
        
        # Check data completeness
        if candidate.name and candidate.name != "Unknown":
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.3)
        
        if candidate.headline:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)
        
        if candidate.location:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)
        
        if candidate.company:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)
        
        if candidate.skills and len(candidate.skills) > 0:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.3)
        
        if candidate.education:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)
        
        # Calculate average confidence
        avg_confidence = sum(confidence_factors) / len(confidence_factors)
        return round(avg_confidence, 2) 