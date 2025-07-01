#!/usr/bin/env python3
"""
Test script to verify API keys work
"""

import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

def test_serpapi():
    """Test SerpAPI functionality"""
    serpapi_key = os.getenv("SERPAPI_KEY")
    
    if not serpapi_key:
        print("❌ No SerpAPI key found in environment variables")
        return False
    
    print(f"✅ SerpAPI key found: {serpapi_key[:10]}...")
    
    try:
        # Test a simple search
        search = GoogleSearch({
            "q": "site:linkedin.com/in software engineer",
            "api_key": serpapi_key,
            "num": 3
        })
        
        results = search.get_dict()
        
        if "organic_results" in results:
            print(f"✅ SerpAPI test successful! Found {len(results['organic_results'])} results")
            return True
        else:
            print("❌ No organic results found in SerpAPI response")
            return False
            
    except Exception as e:
        print(f"❌ SerpAPI test failed: {e}")
        return False

def test_openai():
    """Test OpenAI functionality"""
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        print("⚠️  No OpenAI key found - will use fallback message generation")
        return False
    
    print(f"✅ OpenAI key found: {openai_key[:10]}...")
    
    try:
        import openai
        openai.api_key = openai_key
        
        # Test a simple completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        
        print("✅ OpenAI test successful!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

def main():
    """Run API tests"""
    print("🧪 API KEY TESTING")
    print("=" * 40)
    
    serpapi_working = test_serpapi()
    openai_working = test_openai()
    
    print("\n📋 SUMMARY:")
    print(f"SerpAPI: {'✅ Working' if serpapi_working else '❌ Not working'}")
    print(f"OpenAI: {'✅ Working' if openai_working else '⚠️  Using fallback'}")
    
    if serpapi_working:
        print("\n🎉 Ready to run the LinkedIn Sourcing Agent!")
        print("Run: python demo.py")
    else:
        print("\n⚠️  Please check your API keys")

if __name__ == "__main__":
    main() 