from linkedin_agent import LinkedInProfileFinder
from candidate_scorer import CandidateScorer
import os

if __name__ == "__main__":
    # Initialize both components
    profile_finder = LinkedInProfileFinder()
    candidate_scorer = CandidateScorer()
    
    # Path to your PDF file
    pdf_path = "/Users/renusankhla/Downloads/AI challenge/Data & AI-JD-Gen AI Solution architect.pdf"
    # pdf_path = "/Users/renusankhla/Downloads/AI challenge/Job_Description.pdf"    
    
    if not os.path.exists(pdf_path):
        print(f"\nError: File not found at {pdf_path}")
    else:
        print(f"\nFinding and scoring candidates for: {pdf_path}")
        
        # Step 1: Find profiles
        profiles = profile_finder.find_profiles_from_pdf(pdf_path)
        
        if profiles:
            # Step 2: Extract text from PDF for scoring
            with open(pdf_path, 'rb') as f:
                job_description = profile_finder.extract_text_from_pdf(f)
            
            # Step 3: Score candidates
            scored_candidates = candidate_scorer.score_candidates(profiles, job_description)
            
            # Display top candidates
            print(f"\nTop {min(5, len(scored_candidates))} Candidates:")
            for i, candidate in enumerate(scored_candidates[:5], 1):
                print(f"\nCandidate #{i}:")
                print(f"Name: {candidate['name']}")
                print(f"URL: {candidate['linkedin_url']}")
                print(f"Fit Score: {candidate['fit_score']}/10")
                print("Score Breakdown:")
                for category, score in candidate['score_breakdown'].items():
                    print(f"  {category.capitalize()}: {score}/10")
        else:
            print("\nNo profiles found to score")






# from linkedin_agent import LinkedInProfileFinder
# import os

# if __name__ == "__main__":
#     finder = LinkedInProfileFinder()
    
#     # Use absolute path to your PDF file
#     pdf_path = "/Users/renusankhla/Downloads/AI challenge/Data & AI-JD-Gen AI Solution architect.pdf"
    
#     # Verify file exists before proceeding
#     if not os.path.exists(pdf_path):
#         print(f"\nError: File not found at {pdf_path}")
#         print("Please verify the path to your PDF file")
#     else:
#         print(f"\nFinding LinkedIn profiles for job description: {pdf_path}")
#         profiles = finder.find_profiles_from_pdf(pdf_path)
        
#         if profiles:
#             print(f"\nFound {len(profiles)} profiles:")
#             for i, profile in enumerate(profiles[:10], 1):  # Show first 10 results
#                 print(f"\nProfile {i}:")
#                 print(f"Name: {profile['name']}")
#                 print(f"URL: {profile['linkedin_url']}")
#                 print(f"Headline: {profile['headline']}")
#         else:
#             print("\nNo profiles found. Suggestions:")
#             print("1. Try searching LinkedIn directly with these terms:")
#             print(f"   site:linkedin.com/in Gen AI Solution Architect Python India")
#             print("2. Consider using LinkedIn's official API with proper authentication")
#             print("3. The role may be too specific - try broader terms first")
