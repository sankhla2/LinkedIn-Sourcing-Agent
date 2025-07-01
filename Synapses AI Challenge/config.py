"""
Configuration settings for the LinkedIn Sourcing Agent
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sourcing_agent.db")
    
    # Scoring Weights
    SCORING_WEIGHTS = {
        "education": 0.20,
        "trajectory": 0.20,
        "company": 0.15,
        "skills": 0.25,
        "location": 0.10,
        "tenure": 0.10
    }
    
    # Elite Schools (for education scoring)
    ELITE_SCHOOLS = {
        "mit", "stanford", "harvard", "berkeley", "caltech", "princeton", 
        "yale", "columbia", "cornell", "upenn", "brown", "dartmouth",
        "northwestern", "duke", "vanderbilt", "rice", "washington university",
        "georgetown", "notre dame", "tufts", "emory", "usc", "ucla", "ucsd"
    }
    
    # Top Tech Companies (for company scoring)
    TOP_TECH_COMPANIES = {
        "google", "microsoft", "apple", "amazon", "meta", "netflix", "tesla",
        "uber", "lyft", "airbnb", "stripe", "square", "palantir", "databricks",
        "snowflake", "mongodb", "elastic", "confluent", "hashicorp", "gitlab",
        "atlassian", "salesforce", "adobe", "intel", "nvidia", "amd", "oracle",
        "ibm", "cisco", "vmware", "splunk", "servicenow", "workday", "zoom"
    }
    
    # Search Configuration
    SEARCH_CONFIG = {
        "max_results": 50,
        "search_delay": 2,  # seconds between searches
        "max_retries": 3,
        "timeout": 30
    }
    
    # LLM Configuration
    LLM_CONFIG = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    # Rate Limiting
    RATE_LIMITS = {
        "requests_per_minute": 30,
        "requests_per_hour": 1000
    }
    
    # Job Description for Testing
    TEST_JOB_DESCRIPTION = """
    Software Engineer, ML Research at Windsurf
    
    Windsurf (the company behind Codeium) is a Forbes AI 50 company building AI-powered developer tools. 
    We're looking for someone to train LLMs for code generation.
    
    Requirements:
    - Strong background in machine learning and deep learning
    - Experience with large language models and transformer architectures
    - Proficiency in Python, PyTorch, and related ML frameworks
    - Experience with code generation or program synthesis
    - Strong software engineering fundamentals
    - PhD or equivalent experience preferred
    
    Location: Mountain View, CA
    Salary: $140-300k + equity
    """
    
    # Scoring Rubrics
    EDUCATION_SCORES = {
        "elite_school": (9, 10),
        "strong_school": (7, 8),
        "standard_university": (5, 6),
        "clear_progression": (8, 10)
    }
    
    TRAJECTORY_SCORES = {
        "steady_growth": (6, 8),
        "limited_progression": (3, 5)
    }
    
    COMPANY_SCORES = {
        "top_tech": (9, 10),
        "relevant_industry": (7, 8),
        "any_experience": (5, 6)
    }
    
    SKILLS_SCORES = {
        "perfect_match": (9, 10),
        "strong_overlap": (7, 8),
        "some_relevant": (5, 6)
    }
    
    LOCATION_SCORES = {
        "exact_city": 10,
        "same_metro": 8,
        "remote_friendly": 6
    }
    
    TENURE_SCORES = {
        "2_3_years": (9, 10),
        "1_2_years": (6, 8),
        "job_hopping": (3, 5)
    } 