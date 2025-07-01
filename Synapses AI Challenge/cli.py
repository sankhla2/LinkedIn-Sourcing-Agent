#!/usr/bin/env python3
"""
Command Line Interface for LinkedIn Sourcing Agent
"""

import argparse
import json
import sys
from typing import Optional
from models import JobRequest
from sourcing_agent import LinkedInSourcingAgent

def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Sourcing Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run test sourcing with sample job
  python cli.py --test

  # Source candidates for a specific job
  python cli.py --job-description "Senior Backend Engineer" --location "San Francisco"

  # Source with custom parameters
  python cli.py --job-description "ML Engineer" --location "Mountain View" --max-candidates 50 --min-score 7.0

  # Export results to CSV
  python cli.py --test --export-format csv
        """
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test sourcing with sample job description"
    )
    
    parser.add_argument(
        "--job-description",
        type=str,
        help="Job description for sourcing"
    )
    
    parser.add_argument(
        "--location",
        type=str,
        help="Job location"
    )
    
    parser.add_argument(
        "--company",
        type=str,
        help="Company name"
    )
    
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=25,
        help="Maximum number of candidates to source (default: 25)"
    )
    
    parser.add_argument(
        "--min-score",
        type=float,
        default=6.0,
        help="Minimum fit score for candidates (default: 6.0)"
    )
    
    parser.add_argument(
        "--export-format",
        choices=["json", "csv"],
        default="json",
        help="Export format for results (default: json)"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path (if not specified, prints to stdout)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize the sourcing agent
    agent = LinkedInSourcingAgent()
    
    try:
        if args.test:
            print("Running test sourcing with sample job description...")
            response = agent.run_test_sourcing()
        elif args.job_description:
            # Create job request
            job_request = JobRequest(
                job_description=args.job_description,
                location=args.location,
                company=args.company,
                max_candidates=args.max_candidates,
                min_score=args.min_score
            )
            
            print(f"Starting sourcing for: {args.job_description}")
            if args.location:
                print(f"Location: {args.location}")
            if args.company:
                print(f"Company: {args.company}")
            
            response = agent.source_candidates(job_request)
        else:
            print("Error: Either --test or --job-description must be specified")
            parser.print_help()
            sys.exit(1)
        
        # Check if sourcing was successful
        if response.status.value == "failed":
            print(f"❌ Sourcing failed: {response}")
            sys.exit(1)
        
        # Print results
        print_results(response, args.verbose)
        
        # Export results if requested
        if args.output_file:
            export_results(response, args.export_format, args.output_file)
            print(f"\n✅ Results exported to: {args.output_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Sourcing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def print_results(response, verbose: bool = False):
    """Print sourcing results in a formatted way"""
    print("\n" + "="*60)
    print("🎯 SOURCING RESULTS")
    print("="*60)
    
    print(f"Job ID: {response.job_id}")
    print(f"Status: {response.status.value}")
    print(f"Total candidates found: {response.candidates_found}")
    print(f"Processing time: {response.processing_time} seconds")
    
    if response.top_candidates:
        print(f"\n📊 TOP {len(response.top_candidates)} CANDIDATES:")
        print("-" * 60)
        
        for i, candidate in enumerate(response.top_candidates, 1):
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
                print(f"   Skills: {', '.join(candidate.skills[:5])}")
            
            if verbose and candidate.score_breakdown:
                print(f"   Score Breakdown:")
                for category, score in candidate.score_breakdown.items():
                    if category != "total_score":
                        print(f"     {category.title()}: {score}")
            
            if candidate.outreach_message:
                print(f"   Outreach Message:")
                print(f"     {candidate.outreach_message[:200]}...")
            
            print("-" * 40)
    
    # Print summary statistics
    if response.top_candidates:
        scores = [c.fit_score for c in response.top_candidates if c.fit_score]
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"\n📈 SUMMARY:")
            print(f"Average fit score: {avg_score:.2f}/10")
            print(f"Highest score: {max(scores):.1f}/10")
            print(f"Lowest score: {min(scores):.1f}/10")
    
    print("\n✅ Sourcing completed successfully!")

def export_results(response, format: str, output_file: str):
    """Export results to file"""
    try:
        # Get the sourcing agent to export
        from sourcing_agent import LinkedInSourcingAgent
        agent = LinkedInSourcingAgent()
        
        exported_data = agent.export_results(response, format)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(exported_data)
            
    except Exception as e:
        print(f"Error exporting results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 