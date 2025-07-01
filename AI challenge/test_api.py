#!/usr/bin/env python3
"""
Test script for the FastAPI endpoints
Demonstrates how to use the LinkedIn Sourcing Agent API
"""

import requests
import json
import time

# API base URL (change this to your deployed URL)
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_process_job():
    """Test processing a job description"""
    print("\n📝 Testing Job Description Processing...")
    
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
    
    payload = {
        "job_description": job_description,
        "max_candidates": 5,
        "max_messages": 3
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/process-job", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Job ID: {result['job_id']}")
            print(f"Candidates Found: {result['candidates_found']}")
            print(f"Top Candidates: {len(result['top_candidates'])}")
            print(f"Outreach Messages: {len(result['outreach_messages'])}")
            
            # Show first candidate
            if result['top_candidates']:
                candidate = result['top_candidates'][0]
                print(f"\nTop Candidate:")
                print(f"  Name: {candidate['name']}")
                print(f"  Score: {candidate['fit_score']}/10")
                print(f"  LinkedIn: {candidate['linkedin_url']}")
            
            # Show first message
            if result['outreach_messages']:
                message = result['outreach_messages'][0]
                print(f"\nSample Message:")
                print(f"  To: {message['candidate_name']}")
                print(f"  Message: {message['message'][:100]}...")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_batch_process():
    """Test batch processing of multiple job descriptions"""
    print("\n🔄 Testing Batch Processing...")
    
    job_descriptions = [
        """
        Senior Backend Engineer at TechCorp
        Requirements: Python, Django, PostgreSQL, AWS
        Location: San Francisco, CA
        """,
        """
        Data Scientist at DataCorp
        Requirements: Python, Machine Learning, SQL, Statistics
        Location: New York, NY
        """,
        """
        Frontend Developer at WebCorp
        Requirements: JavaScript, React, TypeScript, CSS
        Location: Remote
        """
    ]
    
    payload = {
        "job_descriptions": job_descriptions,
        "max_workers": 2,
        "max_candidates_per_job": 3
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/batch-process", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Total Jobs: {result['total_jobs']}")
            print(f"Total Candidates: {result['total_candidates']}")
            
            for i, job_result in enumerate(result['results']):
                print(f"\nJob {i+1}: {job_result['job_id']}")
                print(f"  Candidates: {job_result['candidates_found']}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_documentation():
    """Test accessing API documentation"""
    print("\n📚 Testing API Documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API documentation is accessible")
            print(f"📖 Visit: {API_BASE_URL}/docs")
            return True
        else:
            print("❌ API documentation not accessible")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 LinkedIn Sourcing Agent API Tests")
    print("=" * 50)
    
    # Check if API is running
    print("Checking if API is running...")
    if not test_health_check():
        print("❌ API is not running. Please start it with:")
        print("   python api.py")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Job Processing", test_process_job),
        ("Batch Processing", test_batch_process),
        ("API Documentation", test_api_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"{'✅ PASS' if success else '❌ FAIL'}: {test_name}")
        except Exception as e:
            print(f"❌ ERROR: {test_name} - {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print(f"\n📖 API Documentation: {API_BASE_URL}/docs")
    print(f"🔗 API Base URL: {API_BASE_URL}")

if __name__ == "__main__":
    main() 