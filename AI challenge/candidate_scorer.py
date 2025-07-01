import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time
import random

class CandidateScorer:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Elite schools for education scoring
        self.elite_schools = {
            'mit', 'stanford', 'harvard', 'berkeley', 'caltech', 'cmu', 'princeton', 
            'yale', 'columbia', 'upenn', 'cornell', 'brown', 'dartmouth', 'duke',
            'northwestern', 'uchicago', 'nyu', 'usc', 'ucla', 'ucsd', 'gatech',
            'uiuc', 'umich', 'uw', 'utaustin', 'georgia tech', 'georgia institute of technology'
        }
        
        # Top tech companies for company relevance
        self.top_tech_companies = {
            'google', 'microsoft', 'apple', 'amazon', 'meta', 'facebook', 'netflix',
            'uber', 'lyft', 'airbnb', 'stripe', 'square', 'palantir', 'databricks',
            'snowflake', 'mongodb', 'elastic', 'confluent', 'hashicorp', 'gitlab',
            'atlassian', 'salesforce', 'adobe', 'intel', 'nvidia', 'amd', 'qualcomm',
            'oracle', 'ibm', 'cisco', 'vmware', 'splunk', 'workday', 'servicenow',
            'zoom', 'slack', 'notion', 'figma', 'canva', 'robinhood', 'coinbase',
            'openai', 'anthropic', 'deepmind', 'waymo', 'tesla', 'spacex'
        }
        
        # Job-specific skills for experience matching
        self.ai_ml_skills = {
            'python', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'numpy', 'pandas',
            'matplotlib', 'seaborn', 'jupyter', 'spark', 'hadoop', 'kafka', 'airflow',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'mlflow', 'wandb',
            'transformers', 'hugging face', 'langchain', 'openai', 'gpt', 'llm',
            'nlp', 'natural language processing', 'computer vision', 'deep learning',
            'machine learning', 'neural networks', 'reinforcement learning', 'gans',
            'bert', 'gpt-3', 'gpt-4', 'llama', 'claude', 'stable diffusion',
            'autocad', 'solidworks', 'matlab', 'r', 'julia', 'c++', 'cuda', 'gpu'
        }

    def extract_profile_data(self, linkedin_url: str) -> Dict:
        """
        Extract detailed profile data from LinkedIn URL
        Returns profile information for scoring
        """
        try:
            # Add delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(linkedin_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return {}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic profile information
            profile_data = {
                'name': '',
                'headline': '',
                'location': '',
                'education': [],
                'experience': [],
                'skills': [],
                'summary': ''
            }
            
            # Extract name (from title or meta tags)
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.get_text()
                if '|' in title_text:
                    profile_data['name'] = title_text.split('|')[0].strip()
            
            # Extract headline
            headline_elem = soup.find('div', {'class': 'text-body-medium'}) or \
                          soup.find('h2', {'class': 'pv-text-details__left-panel'})
            if headline_elem:
                profile_data['headline'] = headline_elem.get_text().strip()
            
            # Extract location
            location_elem = soup.find('span', {'class': 'text-body-small'}) or \
                          soup.find('div', {'class': 'pv-text-details__left-panel'})
            if location_elem:
                profile_data['location'] = location_elem.get_text().strip()
            
            # Extract education (simplified - look for education section)
            education_section = soup.find('section', {'id': 'education'}) or \
                              soup.find('section', string=re.compile('education', re.I))
            if education_section:
                schools = education_section.find_all('h3') or education_section.find_all('div', {'class': 'pv-entity__school-name'})
                for school in schools:
                    profile_data['education'].append(school.get_text().strip())
            
            # Extract experience (simplified)
            experience_section = soup.find('section', {'id': 'experience'}) or \
                               soup.find('section', string=re.compile('experience', re.I))
            if experience_section:
                companies = experience_section.find_all('h3') or experience_section.find_all('div', {'class': 'pv-entity__company-name'})
                for company in companies:
                    profile_data['experience'].append(company.get_text().strip())
            
            # Extract skills from headline and summary
            all_text = soup.get_text().lower()
            found_skills = []
            for skill in self.ai_ml_skills:
                if skill in all_text:
                    found_skills.append(skill)
            profile_data['skills'] = found_skills
            
            return profile_data
            
        except Exception as e:
            print(f"Error extracting profile data from {linkedin_url}: {e}")
            return {}

    def score_education(self, education: List[str], job_description: str) -> float:
        """
        Score education based on school prestige and relevance
        Returns score 1-10
        """
        if not education:
            return 5.0  # Default score for unknown education
        
        max_score = 0
        for school in education:
            school_lower = school.lower()
            
            # Check for elite schools
            if any(elite in school_lower for elite in self.elite_schools):
                score = 9.5
            # Check for strong technical schools
            elif any(tech in school_lower for tech in ['university', 'college', 'institute']):
                score = 7.5
            else:
                score = 6.0
            
            # Bonus for relevant degrees
            if any(degree in school_lower for degree in ['computer science', 'engineering', 'ai', 'ml', 'data science']):
                score += 1.0
            
            max_score = max(max_score, score)
        
        return min(max_score, 10.0)

    def score_career_trajectory(self, experience: List[str], headline: str) -> float:
        """
        Score career trajectory based on progression and growth
        Returns score 1-10
        """
        if not experience:
            return 5.0
        
        # Analyze progression in titles
        progression_keywords = ['senior', 'lead', 'principal', 'director', 'manager', 'head']
        current_level = 0
        
        for exp in experience + [headline]:
            exp_lower = exp.lower()
            for i, keyword in enumerate(progression_keywords):
                if keyword in exp_lower:
                    current_level = max(current_level, i + 1)
        
        # Score based on level
        if current_level >= 4:  # Director/Principal level
            return 9.0
        elif current_level >= 3:  # Lead/Senior level
            return 7.5
        elif current_level >= 2:  # Mid-level
            return 6.5
        else:
            return 5.0

    def score_company_relevance(self, experience: List[str], job_description: str) -> float:
        """
        Score company relevance based on tech companies and industry match
        Returns score 1-10
        """
        if not experience:
            return 5.0
        
        max_score = 0
        for company in experience:
            company_lower = company.lower()
            
            # Check for top tech companies
            if any(top_company in company_lower for top_company in self.top_tech_companies):
                score = 9.0
            # Check for AI/ML companies
            elif any(ai_company in company_lower for ai_company in ['ai', 'ml', 'data', 'analytics', 'intelligence']):
                score = 8.0
            # Check for startup/tech indicators
            elif any(startup in company_lower for startup in ['inc', 'corp', 'ltd', 'startup', 'tech']):
                score = 7.0
            else:
                score = 6.0
            
            max_score = max(max_score, score)
        
        return min(max_score, 10.0)

    def score_experience_match(self, skills: List[str], headline: str, job_description: str) -> float:
        """
        Score experience match based on skills and job requirements
        Returns score 1-10
        """
        job_lower = job_description.lower()
        headline_lower = headline.lower()
        
        # Count matching skills
        matching_skills = 0
        for skill in skills:
            if skill in job_lower:
                matching_skills += 1
        
        # Score based on skill matches
        if matching_skills >= 5:
            return 9.5
        elif matching_skills >= 3:
            return 8.0
        elif matching_skills >= 1:
            return 6.5
        else:
            return 5.0

    def score_location_match(self, location: str, job_description: str) -> float:
        """
        Score location match based on job requirements
        Returns score 1-10
        """
        if not location:
            return 6.0  # Remote-friendly default
        
        location_lower = location.lower()
        job_lower = job_description.lower()
        
        # Extract location from job description
        job_locations = []
        location_keywords = ['san francisco', 'sf', 'new york', 'nyc', 'mountain view', 
                           'remote', 'austin', 'seattle', 'boston', 'chicago', 'india']
        
        for loc in location_keywords:
            if loc in job_lower:
                job_locations.append(loc)
        
        # Check for exact match
        for job_loc in job_locations:
            if job_loc in location_lower:
                return 10.0
        
        # Check for metro area match
        if any(metro in location_lower for metro in ['california', 'bay area', 'silicon valley']):
            return 8.0
        
        # Check for remote-friendly
        if 'remote' in job_lower or 'anywhere' in job_lower:
            return 6.0
        
        return 5.0

    def score_tenure(self, experience: List[str]) -> float:
        """
        Score tenure based on job stability and progression
        Returns score 1-10
        """
        if not experience:
            return 5.0
        
        # Simple heuristic: more companies = potentially more job hopping
        num_companies = len(experience)
        
        if num_companies <= 2:
            return 9.0  # Stable
        elif num_companies <= 4:
            return 7.0  # Reasonable progression
        elif num_companies <= 6:
            return 5.0  # Some job hopping
        else:
            return 3.0  # Frequent job changes

    def calculate_fit_score(self, candidate: Dict, job_description: str) -> Dict:
        """
        Calculate comprehensive fit score for a candidate
        Returns score breakdown and total score
        """
        # Extract profile data if not already available
        if 'profile_data' not in candidate:
            candidate['profile_data'] = self.extract_profile_data(candidate['linkedin_url'])
        
        profile_data = candidate['profile_data']
        
        # Calculate individual scores
        education_score = self.score_education(profile_data.get('education', []), job_description)
        trajectory_score = self.score_career_trajectory(profile_data.get('experience', []), profile_data.get('headline', ''))
        company_score = self.score_company_relevance(profile_data.get('experience', []), job_description)
        experience_score = self.score_experience_match(profile_data.get('skills', []), profile_data.get('headline', ''), job_description)
        location_score = self.score_location_match(profile_data.get('location', ''), job_description)
        tenure_score = self.score_tenure(profile_data.get('experience', []))
        
        # Calculate weighted total score
        total_score = (
            education_score * 0.20 +      # 20%
            trajectory_score * 0.20 +     # 20%
            company_score * 0.15 +        # 15%
            experience_score * 0.25 +     # 25%
            location_score * 0.10 +       # 10%
            tenure_score * 0.10           # 10%
        )
        
        return {
            'total_score': round(total_score, 2),
            'breakdown': {
                'education': round(education_score, 2),
                'trajectory': round(trajectory_score, 2),
                'company': round(company_score, 2),
                'skills': round(experience_score, 2),
                'location': round(location_score, 2),
                'tenure': round(tenure_score, 2)
            },
            'profile_data': profile_data
        }

    def score_candidates(self, candidates: List[Dict], job_description: str) -> List[Dict]:
        """
        Score all candidates and return sorted results
        """
        scored_candidates = []
        
        for candidate in candidates:
            print(f"Scoring candidate: {candidate.get('name', 'Unknown')}")
            
            score_result = self.calculate_fit_score(candidate, job_description)
            
            scored_candidate = {
                'name': candidate.get('name', 'Unknown'),
                'linkedin_url': candidate.get('linkedin_url', ''),
                'headline': candidate.get('headline', ''),
                'fit_score': score_result['total_score'],
                'score_breakdown': score_result['breakdown'],
                'profile_data': score_result['profile_data']
            }
            
            scored_candidates.append(scored_candidate)
        
        # Sort by fit score (highest first)
        scored_candidates.sort(key=lambda x: x['fit_score'], reverse=True)
        
        return scored_candidates 