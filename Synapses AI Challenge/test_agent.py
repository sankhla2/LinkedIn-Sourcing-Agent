#!/usr/bin/env python3
"""
Test script for LinkedIn Sourcing Agent
"""

import sys
import time
from models import JobRequest
from sourcing_agent import LinkedInSourcingAgent

def test_basic_functionality():
    """Test basic functionality without API keys"""
    print("🧪 Testing LinkedIn Sourcing Agent...")
    
    # Initialize agent
    agent = LinkedInSourcingAgent()
    
    # Test job request
    test_request = JobRequest(
        job_description="Software Engineer with Python and machine learning experience",
        location="San Francisco",
        company="TechCorp",
        max_candidates=10,
        min_score=5.0
    )
    
    print("✅ Agent initialized successfully")
    print(f"✅ Test job request created: {test_request.job_description[:50]}...")
    
    return agent, test_request

def test_search_functionality(agent, test_request):
    """Test LinkedIn search functionality"""
    print("\n🔍 Testing LinkedIn search...")
    
    try:
        # Test search
        search_results = agent.searcher.search_linkedin_profiles(
            test_request.job_description,
            test_request.location,
            5  # Small number for testing
        )
        
        print(f"✅ Search completed: Found {len(search_results)} search results")
        
        # Test candidate extraction
        candidates = agent.searcher.extract_profile_data(search_results)
        print(f"✅ Candidate extraction: Found {len(candidates)} candidates")
        
        if candidates:
            candidate = candidates[0]
            print(f"   Sample candidate: {candidate.name} - {candidate.headline}")
        
        return candidates
        
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return []

def test_scoring_functionality(agent, candidates, test_request):
    """Test scoring functionality"""
    print("\n📊 Testing scoring functionality...")
    
    if not candidates:
        print("⚠️  No candidates to score")
        return []
    
    try:
        # Test scoring
        scored_candidates = agent.scorer.score_candidates(candidates, test_request.job_description)
        
        print(f"✅ Scoring completed: Scored {len(scored_candidates)} candidates")
        
        if scored_candidates:
            candidate = scored_candidates[0]
            print(f"   Top candidate: {candidate.name} - Score: {candidate.fit_score}/10")
            
            if candidate.score_breakdown:
                print(f"   Score breakdown: {candidate.score_breakdown}")
        
        return scored_candidates
        
    except Exception as e:
        print(f"❌ Scoring test failed: {e}")
        return []

def test_outreach_functionality(agent, candidates, test_request):
    """Test outreach generation functionality"""
    print("\n💬 Testing outreach generation...")
    
    if not candidates:
        print("⚠️  No candidates for outreach")
        return []
    
    try:
        # Test outreach generation (without OpenAI API key, should use fallback)
        outreach_messages = agent.outreach_generator.generate_outreach_messages(
            candidates[:2],  # Test with 2 candidates
            test_request.job_description,
            max_messages=2
        )
        
        print(f"✅ Outreach generation completed: Generated {len(outreach_messages)} messages")
        
        if outreach_messages:
            message = outreach_messages[0]
            print(f"   Sample message for {message.candidate_name}:")
            print(f"   {message.message[:100]}...")
        
        return outreach_messages
        
    except Exception as e:
        print(f"❌ Outreach test failed: {e}")
        return []

def test_full_pipeline(agent, test_request):
    """Test the full sourcing pipeline"""
    print("\n🚀 Testing full sourcing pipeline...")
    
    try:
        start_time = time.time()
        
        # Run full pipeline
        response = agent.source_candidates(test_request)
        
        processing_time = time.time() - start_time
        
        print(f"✅ Full pipeline completed in {processing_time:.2f} seconds")
        print(f"   Status: {response.status.value}")
        print(f"   Candidates found: {response.candidates_found}")
        print(f"   Top candidates: {len(response.top_candidates)}")
        
        if response.top_candidates:
            candidate = response.top_candidates[0]
            print(f"   Top candidate: {candidate.name} - Score: {candidate.fit_score}/10")
        
        return response
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        return None

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        # Import and test API
        from api import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        return True
        
    except ImportError:
        print("⚠️  FastAPI test client not available, skipping API tests")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 LINKEDIN SOURCING AGENT - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic functionality
    agent, test_request = test_basic_functionality()
    
    # Test 2: Search functionality
    candidates = test_search_functionality(agent, test_request)
    
    # Test 3: Scoring functionality
    scored_candidates = test_scoring_functionality(agent, candidates, test_request)
    
    # Test 4: Outreach functionality
    outreach_messages = test_outreach_functionality(agent, scored_candidates, test_request)
    
    # Test 5: Full pipeline
    response = test_full_pipeline(agent, test_request)
    
    # Test 6: API endpoints
    api_working = test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    if agent:
        tests_passed += 1
        print("✅ Basic functionality: PASSED")
    else:
        print("❌ Basic functionality: FAILED")
    
    if candidates:
        tests_passed += 1
        print("✅ Search functionality: PASSED")
    else:
        print("❌ Search functionality: FAILED")
    
    if scored_candidates:
        tests_passed += 1
        print("✅ Scoring functionality: PASSED")
    else:
        print("❌ Scoring functionality: FAILED")
    
    if outreach_messages:
        tests_passed += 1
        print("✅ Outreach functionality: PASSED")
    else:
        print("❌ Outreach functionality: FAILED")
    
    if response and response.status.value == "completed":
        tests_passed += 1
        print("✅ Full pipeline: PASSED")
    else:
        print("❌ Full pipeline: FAILED")
    
    print(f"\n🎯 Overall: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Set up your API keys in .env file")
        print("2. Run: python cli.py --test")
        print("3. Or start the API: python api.py")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 