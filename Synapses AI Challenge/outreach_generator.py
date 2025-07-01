"""
AI-Powered Outreach Message Generator
"""

import openai
from typing import List, Dict, Optional
from config import Config
from models import Candidate, OutreachMessage

class OutreachGenerator:
    """Generates personalized outreach messages using AI"""
    
    def __init__(self):
        self.config = Config()
        openai.api_key = self.config.OPENAI_API_KEY
    
    def generate_outreach_messages(self, candidates: List[Candidate], job_description: str, max_messages: int = 10) -> List[OutreachMessage]:
        """
        Generate personalized outreach messages for top candidates
        """
        messages = []
        top_candidates = candidates[:max_messages]
        
        for candidate in top_candidates:
            try:
                message = self._generate_single_message(candidate, job_description)
                messages.append(message)
            except Exception as e:
                print(f"Error generating message for {candidate.name}: {e}")
                # Create a fallback message
                fallback_message = self._create_fallback_message(candidate, job_description)
                messages.append(fallback_message)
        
        return messages
    
    def _generate_single_message(self, candidate: Candidate, job_description: str) -> OutreachMessage:
        """
        Generate a personalized message for a single candidate
        """
        # Prepare candidate information for the prompt
        candidate_info = self._format_candidate_info(candidate)
        
        # Create the prompt
        prompt = self._create_outreach_prompt(candidate_info, job_description)
        
        try:
            # Generate message using OpenAI
            response = openai.ChatCompletion.create(
                model=self.config.LLM_CONFIG["model"],
                messages=[
                    {"role": "system", "content": "You are a professional recruiter writing personalized LinkedIn outreach messages. Be concise, professional, and highlight specific candidate strengths."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.LLM_CONFIG["temperature"],
                max_tokens=self.config.LLM_CONFIG["max_tokens"]
            )
            
            generated_message = response.choices[0].message.content.strip()
            
            # Extract key highlights
            key_highlights = self._extract_key_highlights(candidate)
            
            # Calculate personalization score
            personalization_score = self._calculate_personalization_score(candidate, generated_message)
            
            return OutreachMessage(
                candidate_name=candidate.name,
                message=generated_message,
                personalization_score=personalization_score,
                key_highlights=key_highlights
            )
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._create_fallback_message(candidate, job_description)
    
    def _format_candidate_info(self, candidate: Candidate) -> str:
        """Format candidate information for the prompt"""
        info_parts = []
        
        if candidate.name:
            info_parts.append(f"Name: {candidate.name}")
        
        if candidate.headline:
            info_parts.append(f"Current Role: {candidate.headline}")
        
        if candidate.company:
            info_parts.append(f"Company: {candidate.company}")
        
        if candidate.location:
            info_parts.append(f"Location: {candidate.location}")
        
        if candidate.skills:
            info_parts.append(f"Skills: {', '.join(candidate.skills)}")
        
        if candidate.education:
            info_parts.append(f"Education: {candidate.education}")
        
        if candidate.fit_score:
            info_parts.append(f"Fit Score: {candidate.fit_score}/10")
        
        if candidate.score_breakdown:
            breakdown = candidate.score_breakdown
            info_parts.append(f"Score Breakdown: Education({breakdown.get('education', 'N/A')}), Skills({breakdown.get('skills', 'N/A')}), Experience({breakdown.get('company', 'N/A')})")
        
        return "\n".join(info_parts)
    
    def _create_outreach_prompt(self, candidate_info: str, job_description: str) -> str:
        """Create the prompt for message generation"""
        return f"""
Please write a personalized LinkedIn outreach message for this candidate. The message should be:

1. Professional and concise (150-200 words max)
2. Personalized to their background and experience
3. Highlight specific strengths that match the job
4. Include a clear call-to-action
5. Reference their current role/company if relevant

Candidate Information:
{candidate_info}

Job Description:
{job_description}

Write a compelling outreach message that would make this candidate interested in the opportunity. Start with "Hi [Name]," and end with a professional closing.
"""
    
    def _extract_key_highlights(self, candidate: Candidate) -> List[str]:
        """Extract key highlights from candidate profile"""
        highlights = []
        
        if candidate.fit_score and candidate.fit_score >= 8.0:
            highlights.append(f"High fit score: {candidate.fit_score}/10")
        
        if candidate.skills and len(candidate.skills) >= 3:
            highlights.append(f"Strong technical skills: {', '.join(candidate.skills[:3])}")
        
        if candidate.company:
            highlights.append(f"Experience at {candidate.company}")
        
        if candidate.education:
            highlights.append(f"Education: {candidate.education}")
        
        if candidate.score_breakdown:
            breakdown = candidate.score_breakdown
            if breakdown.get('skills', 0) >= 8.0:
                highlights.append("Excellent skills match")
            if breakdown.get('education', 0) >= 8.0:
                highlights.append("Strong educational background")
        
        return highlights[:5]  # Limit to 5 highlights
    
    def _calculate_personalization_score(self, candidate: Candidate, message: str) -> float:
        """Calculate how personalized the message is"""
        score = 0.0
        total_factors = 0
        
        # Check if candidate name is mentioned
        if candidate.name and candidate.name.lower() in message.lower():
            score += 1.0
        total_factors += 1
        
        # Check if current company is mentioned
        if candidate.company and candidate.company.lower() in message.lower():
            score += 1.0
        total_factors += 1
        
        # Check if skills are mentioned
        if candidate.skills:
            skills_mentioned = sum(1 for skill in candidate.skills if skill.lower() in message.lower())
            if skills_mentioned > 0:
                score += min(1.0, skills_mentioned / len(candidate.skills))
        total_factors += 1
        
        # Check if location is mentioned
        if candidate.location and candidate.location.lower() in message.lower():
            score += 1.0
        total_factors += 1
        
        # Check if education is mentioned
        if candidate.education and any(word in message.lower() for word in candidate.education.lower().split()):
            score += 1.0
        total_factors += 1
        
        return round(score / total_factors, 2) if total_factors > 0 else 0.0
    
    def _create_fallback_message(self, candidate: Candidate, job_description: str) -> OutreachMessage:
        """Create a fallback message when AI generation fails"""
        name = candidate.name or "there"
        
        # Extract job title from description
        job_title = self._extract_job_title(job_description)
        
        # Create a simple but professional message
        message = f"""Hi {name},

I came across your profile and was impressed by your background in software engineering. I'm reaching out because I think you'd be a great fit for a {job_title} role we're hiring for.

Your experience with {', '.join(candidate.skills[:3]) if candidate.skills else 'software development'} aligns perfectly with what we're looking for. 

Would you be interested in learning more about this opportunity? I'd love to schedule a quick call to discuss the role and see if it might be a good fit for your career goals.

Best regards,
[Your Name]"""
        
        return OutreachMessage(
            candidate_name=candidate.name,
            message=message,
            personalization_score=0.6,
            key_highlights=self._extract_key_highlights(candidate)
        )
    
    def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from job description"""
        # Common job titles to look for
        job_titles = [
            "software engineer", "backend engineer", "frontend engineer", "full stack engineer",
            "machine learning engineer", "data scientist", "devops engineer", "product manager",
            "senior engineer", "lead engineer", "principal engineer", "staff engineer"
        ]
        
        description_lower = job_description.lower()
        
        for title in job_titles:
            if title in description_lower:
                return title.title()
        
        return "Software Engineer"  # Default
    
    def generate_batch_messages(self, candidates: List[Candidate], job_description: str) -> List[OutreachMessage]:
        """
        Generate messages for multiple candidates efficiently
        """
        # For batch processing, we can optimize by creating a single prompt with multiple candidates
        # This reduces API calls and costs
        
        batch_messages = []
        
        # Process in smaller batches to avoid rate limits
        batch_size = 5
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i + batch_size]
            
            for candidate in batch:
                message = self._generate_single_message(candidate, job_description)
                batch_messages.append(message)
        
        return batch_messages 