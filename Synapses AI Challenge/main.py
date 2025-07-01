#!/usr/bin/env python3
"""
Main entry point for LinkedIn Sourcing Agent
"""

import sys
import argparse
from sourcing_agent import LinkedInSourcingAgent

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="LinkedIn Sourcing Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the demo
  python main.py --demo

  # Run tests
  python main.py --test

  # Start API server
  python main.py --api

  # Run CLI
  python main.py --cli --job-description "Software Engineer"
        """
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the demo with sample job description"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test suite"
    )
    
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the FastAPI server"
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the CLI interface"
    )
    
    parser.add_argument(
        "--job-description",
        type=str,
        help="Job description for sourcing (used with --cli)"
    )
    
    parser.add_argument(
        "--location",
        type=str,
        help="Job location (used with --cli)"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        print("🚀 Starting LinkedIn Sourcing Agent Demo...")
        from demo import run_demo
        run_demo()
        
    elif args.test:
        print("🧪 Running LinkedIn Sourcing Agent Tests...")
        from test_agent import main as run_tests
        success = run_tests()
        sys.exit(0 if success else 1)
        
    elif args.api:
        print("🌐 Starting FastAPI Server...")
        import uvicorn
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    elif args.cli:
        print("💻 Starting CLI Interface...")
        if args.job_description:
            # Create a simple job request and run sourcing
            from models import JobRequest
            job_request = JobRequest(
                job_description=args.job_description,
                location=args.location,
                max_candidates=25,
                min_score=6.0
            )
            
            agent = LinkedInSourcingAgent()
            response = agent.source_candidates(job_request)
            
            print(f"\n✅ Sourcing completed!")
            print(f"Found {response.candidates_found} candidates")
            print(f"Top {len(response.top_candidates)} candidates returned")
            
            if response.top_candidates:
                print("\nTop candidates:")
                for i, candidate in enumerate(response.top_candidates[:3], 1):
                    print(f"{i}. {candidate.name} - Score: {candidate.fit_score}/10")
        else:
            print("Please provide a job description with --job-description")
            sys.exit(1)
            
    else:
        print("🎯 LinkedIn Sourcing Agent")
        print("=" * 40)
        print("Choose an option:")
        print("  --demo     Run the demo")
        print("  --test     Run tests")
        print("  --api      Start API server")
        print("  --cli      Use CLI interface")
        print()
        print("For more options, run: python main.py --help")

if __name__ == "__main__":
    main() 