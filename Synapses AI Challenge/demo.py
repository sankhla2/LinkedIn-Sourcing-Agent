#!/usr/bin/env python3
"""
Demo script for LinkedIn Sourcing Agent
"""

import json
import time
from models import JobRequest
from sourcing_agent import LinkedInSourcingAgent

def run_demo():
    """Run a complete demo of the LinkedIn sourcing agent"""
    
    print("🚀 LINKEDIN SOURCING AGENT DEMO")
    print("=" * 60)
    
    # Initialize the agent
    agent = LinkedInSourcingAgent()
    
    # Use the provided job description from the challenge
    job_description = """
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
    
    # Create job request
    job_request = JobRequest(
        job_description=job_description,
        location="Mountain View, CA",
        company="Windsurf",
        max_candidates=25,
        min_score=6.0
    )
    
    print("📋 Job Description:")
    print(f"   Company: {job_request.company}")
    print(f"   Location: {job_request.location}")
    print(f"   Max candidates: {job_request.max_candidates}")
    print(f"   Min score: {job_request.min_score}")
    print()
    
    print("🔍 Starting LinkedIn profile search...")
    start_time = time.time()
    
    # Run the sourcing process
    response = agent.source_candidates(job_request)
    
    processing_time = time.time() - start_time
    
    print(f"✅ Sourcing completed in {processing_time:.2f} seconds")
    print()
    
    # Display results
    display_results(response)
    
    # Generate summary
    summary = agent.get_candidate_summary(response.top_candidates)
    display_summary(summary)
    
    # Export results
    export_demo_results(response)
    
    return response

def display_results(response):
    """Display the sourcing results"""
    print("🎯 SOURCING RESULTS")
    print("-" * 60)
    print(f"Job ID: {response.job_id}")
    print(f"Status: {response.status.value}")
    print(f"Total candidates found: {response.candidates_found}")
    print(f"Top candidates returned: {len(response.top_candidates)}")
    print()
    
    if response.top_candidates:
        print("📊 TOP CANDIDATES:")
        print("-" * 60)
        
        for i, candidate in enumerate(response.top_candidates[:5], 1):  # Show top 5
            print(f"\n{i}. {candidate.name}")
            print(f"   LinkedIn: {candidate.linkedin_url}")
            print(f"   Fit Score: {candidate.fit_score}/10")
            
            if candidate.headline:
                print(f"   Current Role: {candidate.headline}")
            
            if candidate.company:
                print(f"   Company: {candidate.company}")
            
            if candidate.location:
                print(f"   Location: {candidate.location}")
            
            if candidate.skills:
                print(f"   Skills: {', '.join(candidate.skills[:3])}")
            
            if candidate.score_breakdown:
                print(f"   Score Breakdown:")
                breakdown = candidate.score_breakdown
                print(f"     Education: {breakdown.get('education', 'N/A')}")
                print(f"     Skills: {breakdown.get('skills', 'N/A')}")
                print(f"     Company: {breakdown.get('company', 'N/A')}")
                print(f"     Location: {breakdown.get('location', 'N/A')}")
            
            if candidate.outreach_message:
                print(f"   Outreach Message:")
                print(f"     {candidate.outreach_message[:150]}...")
            
            print("-" * 40)

def display_summary(summary):
    """Display candidate summary statistics"""
    print("\n📈 CANDIDATE SUMMARY")
    print("-" * 60)
    print(f"Total candidates: {summary['total_candidates']}")
    print(f"Average fit score: {summary['average_score']}/10")
    print()
    
    print("Score Distribution:")
    for range_key, count in summary['score_distribution'].items():
        if count > 0:
            print(f"  {range_key}: {count} candidates")
    print()
    
    if summary['top_skills']:
        print("Top Skills:")
        for skill, count in summary['top_skills'][:5]:
            print(f"  {skill}: {count} mentions")
        print()
    
    if summary['top_companies']:
        print("Top Companies:")
        for company, count in summary['top_companies'][:5]:
            print(f"  {company}: {count} candidates")
        print()

def export_demo_results(response):
    """Export demo results to files"""
    print("💾 EXPORTING RESULTS")
    print("-" * 60)
    
    try:
        # Export to JSON
        json_filename = "demo_results.json"
        with open(json_filename, 'w') as f:
            json.dump(response.dict(), f, indent=2, default=str)
        print(f"✅ JSON results exported to: {json_filename}")
        
        # Export to CSV
        csv_filename = "demo_results.csv"
        agent = LinkedInSourcingAgent()
        csv_data = agent.export_results(response, "csv")
        with open(csv_filename, 'w') as f:
            f.write(csv_data)
        print(f"✅ CSV results exported to: {csv_filename}")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")

def show_api_usage():
    """Show how to use the API"""
    print("\n🌐 API USAGE")
    print("-" * 60)
    print("To use the API, start the server:")
    print("  python api.py")
    print()
    print("Then make requests:")
    print("  curl -X POST http://localhost:8000/source-candidates \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"job_description\": \"Software Engineer\", \"location\": \"San Francisco\"}'")
    print()
    print("Or use the test endpoint:")
    print("  curl -X POST http://localhost:8000/test")

def main():
    """Main demo function"""
    try:
        # Run the demo
        response = run_demo()
        
        # Show API usage
        show_api_usage()
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Review the exported files (demo_results.json, demo_results.csv)")
        print("2. Start the API server: python api.py")
        print("3. Use the CLI: python cli.py --test")
        print("4. Customize the job description and run again")
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 