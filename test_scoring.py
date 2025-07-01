#!/usr/bin/env python3
"""
Test script for candidate scoring functionality
Demonstrates the fit score algorithm with sample data
"""

from candidate_scorer import CandidateScorer
from run import LinkedInProfileFinder
import json

def test_scoring_with_sample_data():
    """Test scoring with sample candidate data"""
    
    # Sample job description (AI/ML focused)
    job_description = """
    Software Engineer, ML Research at Windsurf (Codeium)
    
    We're looking for a talented ML engineer to train LLMs for code generation.
    Requirements:
    - Strong Python programming skills
    - Experience with PyTorch, TensorFlow, or similar ML frameworks
    - Knowledge of NLP and transformer architectures
    - Experience with large language models (GPT, LLaMA, etc.)
    - Located in Mountain View, CA or remote
    - 3+ years of experience in ML/AI
    """
    
    # Sample candidates (simulated data for testing)
    sample_candidates = [
        {
            "name": "Dr. Sarah Chen",
            "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
            "headline": "Senior ML Engineer at Google | PhD Stanford | PyTorch, Transformers, LLMs",
            "profile_data": {
                "education": ["Stanford University", "MIT"],
                "experience": ["Google", "OpenAI", "Microsoft"],
                "skills": ["python", "pytorch", "transformers", "llm", "nlp", "gpt"],
                "location": "Mountain View, CA"
            }
        },
        {
            "name": "Alex Rodriguez",
            "linkedin_url": "https://linkedin.com/in/alex-rodriguez-ai",
            "headline": "AI Engineer | Machine Learning | Python, TensorFlow, Computer Vision",
            "profile_data": {
                "education": ["UC Berkeley", "University of Washington"],
                "experience": ["Meta", "Uber", "StartupXYZ"],
                "skills": ["python", "tensorflow", "computer vision", "machine learning"],
                "location": "San Francisco, CA"
            }
        },
        {
            "name": "Priya Patel",
            "linkedin_url": "https://linkedin.com/in/priya-patel-data",
            "headline": "Data Scientist | Python, Scikit-learn, AWS | 5+ years experience",
            "profile_data": {
                "education": ["University of Michigan"],
                "experience": ["Amazon", "Netflix", "DataCorp"],
                "skills": ["python", "scikit-learn", "aws", "pandas", "numpy"],
                "location": "Seattle, WA"
            }
        },
        {
            "name": "Michael Johnson",
            "linkedin_url": "https://linkedin.com/in/michael-johnson-dev",
            "headline": "Software Engineer | Full Stack | JavaScript, React, Node.js",
            "profile_data": {
                "education": ["State University"],
                "experience": ["TechStartup", "WebCorp", "DevCompany"],
                "skills": ["javascript", "react", "node.js", "html", "css"],
                "location": "Austin, TX"
            }
        }
    ]
    
    # Initialize scorer
    scorer = CandidateScorer()
    
    print("🎯 Testing Candidate Scoring System")
    print("=" * 50)
    print(f"Job: Software Engineer, ML Research at Windsurf")
    print(f"Candidates to score: {len(sample_candidates)}")
    print()
    
    # Score candidates
    scored_candidates = scorer.score_candidates(sample_candidates, job_description)
    
    # Display results
    print("\n📊 SCORING RESULTS")
    print("=" * 50)
    
    for i, candidate in enumerate(scored_candidates, 1):
        print(f"\n🏆 #{i} - {candidate['name']}")
        print(f"   Headline: {candidate['headline']}")
        print(f"   Overall Fit Score: {candidate['fit_score']}/10")
        print(f"   LinkedIn: {candidate['linkedin_url']}")
        
        # Show breakdown
        breakdown = candidate['score_breakdown']
        print(f"   📈 Score Breakdown:")
        print(f"      Education (20%): {breakdown['education']}/10")
        print(f"      Career Trajectory (20%): {breakdown['trajectory']}/10")
        print(f"      Company Relevance (15%): {breakdown['company']}/10")
        print(f"      Skills Match (25%): {breakdown['skills']}/10")
        print(f"      Location Match (10%): {breakdown['location']}/10")
        print(f"      Tenure (10%): {breakdown['tenure']}/10")
        
        # Show profile data
        profile_data = candidate['profile_data']
        if profile_data.get('education'):
            print(f"   🎓 Education: {', '.join(profile_data['education'])}")
        if profile_data.get('experience'):
            print(f"   💼 Experience: {', '.join(profile_data['experience'])}")
        if profile_data.get('skills'):
            print(f"   🛠️  Skills: {', '.join(profile_data['skills'])}")
        if profile_data.get('location'):
            print(f"   📍 Location: {profile_data['location']}")
        
        print("-" * 50)

def test_integration_with_linkedin_search():
    """Test integration with actual LinkedIn search"""
    
    print("\n🔍 Testing Integration with LinkedIn Search")
    print("=" * 50)
    
    # Initialize both components
    finder = LinkedInProfileFinder()
    scorer = CandidateScorer()
    
    # Use the PDF job description
    pdf_path = "Data & AI-JD-Gen AI Solution architect.pdf"
    
    try:
        # Step 1: Find candidates
        print("Step 1: Finding LinkedIn profiles...")
        candidates = finder.find_profiles_from_pdf(pdf_path, max_results=5)
        
        if not candidates:
            print("No candidates found. Using sample data for demonstration.")
            return
        
        print(f"Found {len(candidates)} candidates")
        
        # Step 2: Score candidates
        print("\nStep 2: Scoring candidates...")
        job_description = finder.extract_text_from_pdf(pdf_path)
        scored_candidates = scorer.score_candidates(candidates, job_description)
        
        # Step 3: Display top results
        print(f"\n🏆 TOP {min(3, len(scored_candidates))} CANDIDATES")
        print("=" * 50)
        
        for i, candidate in enumerate(scored_candidates[:3], 1):
            print(f"\n#{i} - {candidate['name']}")
            print(f"   Score: {candidate['fit_score']}/10")
            print(f"   Headline: {candidate['headline']}")
            print(f"   URL: {candidate['linkedin_url']}")
            
            # Show key scores
            breakdown = candidate['score_breakdown']
            print(f"   Key Strengths:")
            if breakdown['skills'] >= 8:
                print(f"     ✅ Strong skills match ({breakdown['skills']}/10)")
            if breakdown['company'] >= 8:
                print(f"     ✅ Relevant company experience ({breakdown['company']}/10)")
            if breakdown['education'] >= 8:
                print(f"     ✅ Strong education background ({breakdown['education']}/10)")
        
    except Exception as e:
        print(f"Error during integration test: {e}")

if __name__ == "__main__":
    # Test with sample data first
    test_scoring_with_sample_data()
    
    # Test integration with LinkedIn search
    test_integration_with_linkedin_search()
    
    print("\n✅ Scoring system test completed!")
    print("\nNext steps:")
    print("1. Run 'python run.py' to test full pipeline")
    print("2. Implement message generation (Step 3)")
    print("3. Add FastAPI endpoint for deployment") 