#!/usr/bin/env python3
"""
Test script for message generation functionality
Demonstrates personalized LinkedIn outreach message creation
"""

from message_generator import MessageGenerator
from candidate_scorer import CandidateScorer
import json

def test_message_generation():
    """Test message generation with sample candidate data"""
    
    # Sample job description
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
    
    # Sample scored candidates
    sample_candidates = [
        {
            "name": "Dr. Sarah Chen",
            "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
            "headline": "Senior ML Engineer at Google | PhD Stanford | PyTorch, Transformers, LLMs",
            "fit_score": 8.7,
            "score_breakdown": {
                "education": 9.5,
                "trajectory": 8.0,
                "company": 9.0,
                "skills": 9.5,
                "location": 8.0,
                "tenure": 7.0
            },
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
            "fit_score": 7.2,
            "score_breakdown": {
                "education": 7.5,
                "trajectory": 7.0,
                "company": 8.0,
                "skills": 8.0,
                "location": 8.0,
                "tenure": 6.0
            },
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
            "fit_score": 6.8,
            "score_breakdown": {
                "education": 7.0,
                "trajectory": 6.5,
                "company": 7.0,
                "skills": 7.0,
                "location": 6.0,
                "tenure": 7.0
            },
            "profile_data": {
                "education": ["University of Michigan"],
                "experience": ["Amazon", "Netflix", "DataCorp"],
                "skills": ["python", "scikit-learn", "aws", "pandas", "numpy"],
                "location": "Seattle, WA"
            }
        }
    ]
    
    # Initialize message generator
    message_gen = MessageGenerator()
    
    print("💬 Testing Message Generation System")
    print("=" * 60)
    print(f"Job: Software Engineer, ML Research at Windsurf")
    print(f"Candidates to generate messages for: {len(sample_candidates)}")
    print()
    
    # Generate messages for each candidate
    for i, candidate in enumerate(sample_candidates, 1):
        print(f"\n📧 CANDIDATE #{i}: {candidate['name']}")
        print(f"   Score: {candidate['fit_score']}/10")
        print(f"   Headline: {candidate['headline']}")
        print(f"   LinkedIn: {candidate['linkedin_url']}")
        
        # Generate personalized message
        message = message_gen.generate_personalized_message(candidate, job_description)
        
        print(f"\n📝 GENERATED MESSAGE:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        # Analyze message effectiveness
        analysis = message_gen.analyze_message_effectiveness(message)
        print(f"\n📊 MESSAGE ANALYSIS:")
        print(f"   Length: {analysis['length']} characters")
        print(f"   Personalization Score: {analysis['personalization_score']}/6")
        print(f"   Professional Tone: {'✅' if analysis['professional_tone'] else '❌'}")
        print(f"   Has Call-to-Action: {'✅' if analysis['has_call_to_action'] else '❌'}")
        print(f"   Mentions Company: {'✅' if analysis['mentions_company'] else '❌'}")
        print(f"   Mentions Role: {'✅' if analysis['mentions_role'] else '❌'}")
        print(f"   Mentions Skills: {'✅' if analysis['mentions_skills'] else '❌'}")
        
        # Generate message variations
        print(f"\n🔄 MESSAGE VARIATIONS:")
        variations = message_gen.generate_message_variations(candidate, job_description, 2)
        for j, variation in enumerate(variations, 1):
            print(f"\n   Variation {j}:")
            print(f"   {variation[:100]}...")
        
        print("\n" + "=" * 60)

def test_batch_message_generation():
    """Test batch message generation for multiple candidates"""
    
    print("\n🔄 Testing Batch Message Generation")
    print("=" * 60)
    
    # Sample job description
    job_description = """
    Software Engineer, ML Research at Windsurf (Codeium)
    Focus on training LLMs for code generation. $140-300k + equity in Mountain View, CA.
    """
    
    # Sample candidates with different scores
    candidates = [
        {
            "name": "Dr. Sarah Chen",
            "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
            "headline": "Senior ML Engineer at Google | PhD Stanford",
            "fit_score": 8.7,
            "profile_data": {
                "education": ["Stanford University"],
                "experience": ["Google", "OpenAI"],
                "skills": ["python", "pytorch", "llm"],
                "location": "Mountain View, CA"
            }
        },
        {
            "name": "Alex Rodriguez",
            "linkedin_url": "https://linkedin.com/in/alex-rodriguez-ai",
            "headline": "AI Engineer | Machine Learning",
            "fit_score": 7.2,
            "profile_data": {
                "education": ["UC Berkeley"],
                "experience": ["Meta", "Uber"],
                "skills": ["python", "tensorflow"],
                "location": "San Francisco, CA"
            }
        },
        {
            "name": "Michael Johnson",
            "linkedin_url": "https://linkedin.com/in/michael-johnson-dev",
            "headline": "Software Engineer | Full Stack",
            "fit_score": 4.5,
            "profile_data": {
                "education": ["State University"],
                "experience": ["TechStartup"],
                "skills": ["javascript", "react"],
                "location": "Austin, TX"
            }
        }
    ]
    
    # Initialize message generator
    message_gen = MessageGenerator()
    
    # Generate messages for all candidates
    messages = message_gen.generate_messages_for_candidates(candidates, job_description, max_messages=3)
    
    print(f"Generated {len(messages)} messages for {len(candidates)} candidates")
    
    # Display all messages
    for i, message_data in enumerate(messages, 1):
        print(f"\n📧 MESSAGE #{i}")
        print(f"Candidate: {message_data['candidate_name']} (Score: {message_data['fit_score']}/10)")
        print(f"LinkedIn: {message_data['linkedin_url']}")
        print(f"Message:")
        print("-" * 40)
        print(message_data['message'])
        print("-" * 40)
    
    # Create and display summary
    summary = message_gen.create_message_summary(messages)
    print(f"\n📈 BATCH GENERATION SUMMARY")
    print(f"Total Messages: {summary['total_messages']}")
    print(f"Average Score: {summary['average_score']:.2f}/10")
    print(f"Score Distribution:")
    print(f"   High (8+): {summary['score_distribution']['high']}")
    print(f"   Medium (6-8): {summary['score_distribution']['medium']}")
    print(f"   Low (<6): {summary['score_distribution']['low']}")

def test_message_formatting():
    """Test message formatting for LinkedIn"""
    
    print("\n📝 Testing Message Formatting")
    print("=" * 60)
    
    # Long message test
    long_message = """
    Hi there, I came across your impressive background in Python and your work at Google. Your experience at Google and expertise in PyTorch, Transformers, LLMs caught my attention.

    I'm reaching out because we're hiring for a Software Engineer, ML Research position at Windsurf (Codeium), a Forbes AI 50 company building AI-powered developer tools. 

    The role focuses on training LLMs for code generation and offers $140-300k + equity in Mountain View, CA.

    Would you be open to a brief conversation about this opportunity?
    """ * 10  # Make it very long
    
    message_gen = MessageGenerator()
    formatted_message = message_gen.format_message_for_linkedin(long_message)
    
    print(f"Original length: {len(long_message)} characters")
    print(f"Formatted length: {len(formatted_message)} characters")
    print(f"Formatted message preview: {formatted_message[:200]}...")

if __name__ == "__main__":
    # Test individual message generation
    test_message_generation()
    
    # Test batch message generation
    test_batch_message_generation()
    
    # Test message formatting
    test_message_formatting()
    
    print("\n✅ Message generation tests completed!")
    print("\nNext steps:")
    print("1. Run 'python main_integrated.py' to test complete pipeline")
    print("2. Add FastAPI endpoint for deployment")
    print("3. Deploy to Hugging Face Spaces") 