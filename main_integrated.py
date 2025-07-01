#!/usr/bin/env python3
"""
Integrated LinkedIn Sourcing Agent
Combines profile discovery, candidate scoring, and message generation
"""

# from run import LinkedInProfileFinder
from linkedin_agent import LinkedInProfileFinder
from candidate_scorer import CandidateScorer
from message_generator import MessageGenerator
import json
import os
from typing import Dict, List

class LinkedInSourcingAgent:
    def __init__(self):
        self.finder = LinkedInProfileFinder()
        self.scorer = CandidateScorer()
        self.message_gen = MessageGenerator()
    
    def process_job_description(self, pdf_path: str, max_candidates: int = 10, max_messages: int = 5) -> Dict:
        """
        Complete pipeline: Extract job description → Find candidates → Score them → Generate messages
        Returns comprehensive results
        """
        print("🚀 LinkedIn Sourcing Agent - Complete Pipeline")
        print("=" * 60)
        
        # Step 1: Extract job description
        print(f"\n📄 Step 1: Extracting job description from {pdf_path}")
        job_description = self.finder.extract_text_from_pdf(pdf_path)
        
        if not job_description:
            return {"error": "Failed to extract job description from PDF"}
        
        print(f"✅ Extracted {len(job_description)} characters")
        print(f"📝 Sample: {job_description[:200]}...")
        
        # Step 2: Find LinkedIn profiles
        print(f"\n🔍 Step 2: Finding LinkedIn profiles (max: {max_candidates})")
        candidates = self.finder.find_profiles_from_pdf(pdf_path, max_results=max_candidates)
        
        if not candidates:
            return {
                "job_description": job_description[:500],
                "candidates_found": 0,
                "scored_candidates": [],
                "messages": [],
                "message": "No LinkedIn profiles found for this job description"
            }
        
        print(f"✅ Found {len(candidates)} candidates")
        
        # Step 3: Score candidates
        print(f"\n📊 Step 3: Scoring candidates using fit score algorithm")
        scored_candidates = self.scorer.score_candidates(candidates, job_description)
        
        print(f"✅ Scored {len(scored_candidates)} candidates")
        
        # Step 4: Generate personalized messages
        print(f"\n💬 Step 4: Generating personalized outreach messages (max: {max_messages})")
        messages = self.message_gen.generate_messages_for_candidates(scored_candidates, job_description, max_messages)
        
        print(f"✅ Generated {len(messages)} personalized messages")
        
        # Step 5: Create message summary
        message_summary = self.message_gen.create_message_summary(messages)
        
        # Step 6: Prepare results
        results = {
            "job_description": job_description[:500] + "...",
            "candidates_found": len(candidates),
            "scored_candidates": scored_candidates,
            "top_candidates": scored_candidates[:5],  # Top 5 for quick reference
            "messages": messages,
            "message_summary": message_summary
        }
        
        return results
    
    def display_results(self, results: Dict):
        """Display formatted results including messages"""
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        print(f"📄 Job Description: {results['job_description'][:100]}...")
        print(f"👥 Candidates Found: {results['candidates_found']}")
        
        if results['scored_candidates']:
            print(f"\n🏆 TOP CANDIDATES (Ranked by Fit Score)")
            print("-" * 60)
            
            for i, candidate in enumerate(results['top_candidates'], 1):
                print(f"\n#{i} - {candidate['name']}")
                print(f"   🎯 Fit Score: {candidate['fit_score']}/10")
                print(f"   💼 Headline: {candidate['headline']}")
                print(f"   🔗 LinkedIn: {candidate['linkedin_url']}")
                
                # Show score breakdown
                breakdown = candidate['score_breakdown']
                print(f"   📈 Score Breakdown:")
                print(f"      🎓 Education (20%): {breakdown['education']}/10")
                print(f"      📈 Career Trajectory (20%): {breakdown['trajectory']}/10")
                print(f"      🏢 Company Relevance (15%): {breakdown['company']}/10")
                print(f"      🛠️  Skills Match (25%): {breakdown['skills']}/10")
                print(f"      📍 Location Match (10%): {breakdown['location']}/10")
                print(f"      ⏱️  Tenure (10%): {breakdown['tenure']}/10")
                
                # Show key strengths
                strengths = []
                if breakdown['skills'] >= 8:
                    strengths.append("Strong technical skills")
                if breakdown['company'] >= 8:
                    strengths.append("Relevant company experience")
                if breakdown['education'] >= 8:
                    strengths.append("Strong education background")
                if breakdown['location'] >= 8:
                    strengths.append("Location match")
                
                if strengths:
                    print(f"   ✅ Key Strengths: {', '.join(strengths)}")
                
                print("-" * 40)
        
        # Display generated messages
        if results['messages']:
            print(f"\n💬 PERSONALIZED OUTREACH MESSAGES")
            print("-" * 60)
            
            for i, message_data in enumerate(results['messages'], 1):
                print(f"\n📧 Message #{i} - {message_data['candidate_name']} (Score: {message_data['fit_score']}/10)")
                print(f"🔗 LinkedIn: {message_data['linkedin_url']}")
                print(f"📝 Message:")
                print("-" * 40)
                print(message_data['message'])
                print("-" * 40)
                
                # Show message analysis
                analysis = message_data.get('analysis', {})
                if analysis:
                    print(f"📊 Message Analysis:")
                    print(f"   Length: {analysis.get('length', 0)} characters")
                    print(f"   Personalization Score: {analysis.get('personalization_score', 0)}/6")
                    print(f"   Has Call-to-Action: {'✅' if analysis.get('has_call_to_action') else '❌'}")
                    print(f"   Mentions Company: {'✅' if analysis.get('mentions_company') else '❌'}")
                    print(f"   Mentions Role: {'✅' if analysis.get('mentions_role') else '❌'}")
                    print(f"   Mentions Skills: {'✅' if analysis.get('mentions_skills') else '❌'}")
        
        # Display message summary
        if 'message_summary' in results:
            summary = results['message_summary']
            print(f"\n📈 MESSAGE GENERATION SUMMARY")
            print("-" * 60)
            print(f"Total Messages Generated: {summary['total_messages']}")
            print(f"Average Candidate Score: {summary['average_score']:.2f}/10")
            print(f"Score Distribution:")
            print(f"   High Score (8+): {summary['score_distribution']['high']}")
            print(f"   Medium Score (6-8): {summary['score_distribution']['medium']}")
            print(f"   Low Score (<6): {summary['score_distribution']['low']}")
        else:
            print("\n❌ No candidates found or scored")
    
    def save_results(self, results: Dict, output_file: str = "sourcing_results.json"):
        """Save results to JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n💾 Results saved to {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def get_api_response_format(self, results: Dict) -> Dict:
        """Format results for API response including messages"""
        if 'error' in results:
            return {"error": results['error']}
        
        api_response = {
            "job_id": "ai-ml-research-windsurf",
            "candidates_found": results['candidates_found'],
            "top_candidates": [],
            "outreach_messages": []
        }
        
        # Add top candidates
        for candidate in results['top_candidates']:
            api_candidate = {
                "name": candidate['name'],
                "linkedin_url": candidate['linkedin_url'],
                "fit_score": candidate['fit_score'],
                "score_breakdown": candidate['score_breakdown'],
                "headline": candidate['headline']
            }
            api_response['top_candidates'].append(api_candidate)
        
        # Add outreach messages
        for message_data in results.get('messages', []):
            api_message = {
                "candidate_name": message_data['candidate_name'],
                "linkedin_url": message_data['linkedin_url'],
                "fit_score": message_data['fit_score'],
                "message": message_data['message'],
                "key_highlights": message_data.get('key_highlights', {})
            }
            api_response['outreach_messages'].append(api_message)
        
        return api_response

def main():
    """Main execution function"""
    agent = LinkedInSourcingAgent()
    
    # Use the provided PDF
    pdf_path = "Data & AI-JD-Gen AI Solution architect.pdf"
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        print("Please ensure the PDF file is in the current directory")
        return
    
    # Process the job description
    results = agent.process_job_description(pdf_path, max_candidates=10, max_messages=5)
    
    # Display results
    agent.display_results(results)
    
    # Save results
    agent.save_results(results)
    
    # Show API format
    api_response = agent.get_api_response_format(results)
    print(f"\n🔗 API Response Format:")
    print(json.dumps(api_response, indent=2))
    
    print("\n✅ Complete pipeline finished successfully!")
    print("\n🎉 All 3 steps completed:")
    print("1. ✅ LinkedIn Profile Discovery")
    print("2. ✅ Candidate Scoring")
    print("3. ✅ Personalized Message Generation")
    print("\nNext steps:")
    print("1. Add FastAPI endpoint for deployment")
    print("2. Test with different job descriptions")
    print("3. Deploy to Hugging Face Spaces")

if __name__ == "__main__":
    main() 