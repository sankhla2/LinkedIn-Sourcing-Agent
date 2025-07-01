import re
import json
from typing import Dict, List, Optional
import random

class MessageGenerator:
    def __init__(self):
        # Professional tone templates
        self.templates = {
            "high_score": [
                "Hi {name}, I came across your impressive background in {key_skill} and {company_experience}. Your experience at {top_company} and expertise in {technical_skills} caught my attention.",
                "Hello {name}, I was impressed by your {education_background} and your work at {top_company}. Your {years_experience} years of experience in {key_skill} align perfectly with what we're looking for.",
                "Hi {name}, your profile stood out to me - particularly your {education_background} and your role at {top_company}. Your expertise in {technical_skills} is exactly what we need."
            ],
            "medium_score": [
                "Hi {name}, I noticed your background in {key_skill} and your experience at {company_experience}. Your skills in {technical_skills} could be a great fit for our team.",
                "Hello {name}, I came across your profile and was interested in your {education_background} and experience with {key_skill}. Your work at {company_experience} shows relevant expertise.",
                "Hi {name}, your experience in {key_skill} and background at {company_experience} caught my attention. Your {technical_skills} skills could be valuable for our position."
            ],
            "low_score": [
                "Hi {name}, I noticed your background in {key_skill} and thought you might be interested in learning about an opportunity that could leverage your {technical_skills} experience.",
                "Hello {name}, I came across your profile and was curious about your experience with {key_skill}. Your background at {company_experience} shows some relevant skills.",
                "Hi {name}, I saw your profile and was interested in your {education_background}. Your experience with {technical_skills} might align with an opportunity we have."
            ]
        }
        
        # Call-to-action templates
        self.cta_templates = [
            "Would you be open to a brief conversation about this opportunity?",
            "I'd love to discuss this role with you if you're interested.",
            "Would you be available for a quick call to learn more?",
            "I'd appreciate the chance to tell you more about this position.",
            "Are you open to exploring this opportunity further?"
        ]
        
        # Job-specific details
        self.job_context = {
            "company": "Windsurf (Codeium)",
            "role": "Software Engineer, ML Research",
            "location": "Mountain View, CA (or remote)",
            "salary_range": "$140-300k + equity",
            "focus": "training LLMs for code generation"
        }

    def extract_candidate_highlights(self, candidate: Dict, job_description: str) -> Dict:
        """
        Extract key highlights from candidate profile for personalization
        """
        profile_data = candidate.get('profile_data', {})
        score_breakdown = candidate.get('score_breakdown', {})
        
        highlights = {
            'name': candidate.get('name', 'there'),
            'key_skill': '',
            'company_experience': '',
            'top_company': '',
            'education_background': '',
            'technical_skills': '',
            'years_experience': '',
            'location_match': '',
            'strengths': []
        }
        
        # Extract name (handle empty names)
        if not highlights['name'] or highlights['name'] == 'Unknown':
            highlights['name'] = 'there'
        
        # Extract key skills
        skills = profile_data.get('skills', [])
        if skills:
            highlights['key_skill'] = skills[0].title()
            highlights['technical_skills'] = ', '.join(skills[:3]).title()
        
        # Extract company experience
        experience = profile_data.get('experience', [])
        if experience:
            highlights['company_experience'] = experience[0]
            # Find top company
            top_companies = ['google', 'microsoft', 'apple', 'amazon', 'meta', 'openai', 'anthropic']
            for company in experience:
                if any(top in company.lower() for top in top_companies):
                    highlights['top_company'] = company
                    break
            if not highlights['top_company']:
                highlights['top_company'] = experience[0]
        
        # Extract education
        education = profile_data.get('education', [])
        if education:
            highlights['education_background'] = education[0]
        
        # Estimate years of experience
        if experience:
            highlights['years_experience'] = str(len(experience) * 2)  # Rough estimate
        
        # Extract location
        location = profile_data.get('location', '')
        if location:
            highlights['location_match'] = location
        
        # Identify strengths based on scores
        if score_breakdown.get('skills', 0) >= 8:
            highlights['strengths'].append('strong technical skills')
        if score_breakdown.get('company', 0) >= 8:
            highlights['strengths'].append('relevant company experience')
        if score_breakdown.get('education', 0) >= 8:
            highlights['strengths'].append('strong education background')
        if score_breakdown.get('location', 0) >= 8:
            highlights['strengths'].append('location match')
        
        return highlights

    def generate_job_context(self, job_description: str) -> str:
        """
        Generate job context paragraph
        """
        return f"""
I'm reaching out because we're hiring for a {self.job_context['role']} position at {self.job_context['company']}, a Forbes AI 50 company building AI-powered developer tools. 

The role focuses on {self.job_context['focus']} and offers {self.job_context['salary_range']} in {self.job_context['location']}.
"""

    def generate_personalized_message(self, candidate: Dict, job_description: str) -> str:
        """
        Generate a personalized LinkedIn message for a candidate
        """
        highlights = self.extract_candidate_highlights(candidate, job_description)
        score = candidate.get('fit_score', 5.0)
        
        # Choose template based on score
        if score >= 8.0:
            template_category = "high_score"
        elif score >= 6.0:
            template_category = "medium_score"
        else:
            template_category = "low_score"
        
        # Select random template
        template = random.choice(self.templates[template_category])
        
        # Fill template with candidate details
        try:
            personalized_opening = template.format(**highlights)
        except KeyError:
            # Fallback if template formatting fails
            personalized_opening = f"Hi {highlights['name']}, I came across your profile and was impressed by your background."
        
        # Add job context
        job_context = self.generate_job_context(job_description)
        
        # Add call-to-action
        cta = random.choice(self.cta_templates)
        
        # Combine into full message
        message = f"{personalized_opening}\n\n{job_context}\n\n{cta}"
        
        # Clean up formatting
        message = re.sub(r'\n\s*\n\s*\n', '\n\n', message)  # Remove extra line breaks
        message = message.strip()
        
        return message

    def generate_messages_for_candidates(self, scored_candidates: List[Dict], job_description: str, max_messages: int = 5) -> List[Dict]:
        """
        Generate personalized messages for top candidates
        """
        messages = []
        
        # Generate messages for top candidates
        for candidate in scored_candidates[:max_messages]:
            message = self.generate_personalized_message(candidate, job_description)
            
            message_data = {
                'candidate_name': candidate.get('name', 'Unknown'),
                'linkedin_url': candidate.get('linkedin_url', ''),
                'fit_score': candidate.get('fit_score', 0),
                'message': message,
                'score_breakdown': candidate.get('score_breakdown', {}),
                'key_highlights': self.extract_candidate_highlights(candidate, job_description)
            }
            
            messages.append(message_data)
        
        return messages

    def generate_message_variations(self, candidate: Dict, job_description: str, num_variations: int = 3) -> List[str]:
        """
        Generate multiple message variations for A/B testing
        """
        variations = []
        
        for _ in range(num_variations):
            message = self.generate_personalized_message(candidate, job_description)
            variations.append(message)
        
        return variations

    def analyze_message_effectiveness(self, message: str) -> Dict:
        """
        Analyze message for effectiveness indicators
        """
        analysis = {
            'length': len(message),
            'personalization_score': 0,
            'professional_tone': True,
            'has_call_to_action': False,
            'mentions_company': False,
            'mentions_role': False,
            'mentions_skills': False
        }
        
        # Check personalization (mentions specific details)
        personalization_indicators = [
            'your experience', 'your background', 'your work', 'your expertise',
            'your skills', 'your role', 'your profile'
        ]
        analysis['personalization_score'] = sum(1 for indicator in personalization_indicators if indicator in message.lower())
        
        # Check for call-to-action
        cta_indicators = ['would you', 'are you', 'i\'d love', 'i\'d appreciate', 'open to']
        analysis['has_call_to_action'] = any(cta in message.lower() for cta in cta_indicators)
        
        # Check for company mention
        analysis['mentions_company'] = 'windsurf' in message.lower() or 'codeium' in message.lower()
        
        # Check for role mention
        analysis['mentions_role'] = 'ml research' in message.lower() or 'software engineer' in message.lower()
        
        # Check for skills mention
        analysis['mentions_skills'] = any(skill in message.lower() for skill in ['python', 'ml', 'ai', 'llm', 'pytorch', 'tensorflow'])
        
        return analysis

    def format_message_for_linkedin(self, message: str) -> str:
        """
        Format message for LinkedIn's character limits and formatting
        """
        # LinkedIn message character limit is ~2000 characters
        max_length = 1800  # Leave some buffer
        
        if len(message) > max_length:
            # Truncate and add ellipsis
            message = message[:max_length-3] + "..."
        
        # Ensure proper line breaks
        message = message.replace('\n\n\n', '\n\n')
        
        return message.strip()

    def create_message_summary(self, messages: List[Dict]) -> Dict:
        """
        Create a summary of generated messages
        """
        summary = {
            'total_messages': len(messages),
            'average_score': 0,
            'score_distribution': {'high': 0, 'medium': 0, 'low': 0},
            'message_analysis': []
        }
        
        if messages:
            scores = [msg['fit_score'] for msg in messages]
            summary['average_score'] = sum(scores) / len(scores)
            
            # Score distribution
            for msg in messages:
                score = msg['fit_score']
                if score >= 8.0:
                    summary['score_distribution']['high'] += 1
                elif score >= 6.0:
                    summary['score_distribution']['medium'] += 1
                else:
                    summary['score_distribution']['low'] += 1
            
            # Analyze each message
            for msg in messages:
                analysis = self.analyze_message_effectiveness(msg['message'])
                summary['message_analysis'].append({
                    'candidate': msg['candidate_name'],
                    'score': msg['fit_score'],
                    'analysis': analysis
                })
        
        return summary 