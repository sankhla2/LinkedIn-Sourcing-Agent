import os
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from main_integrated import LinkedInSourcingAgent

class BatchJobProcessor:
    def __init__(self, max_workers: int = 3, min_delay: float = 2.0, max_delay: float = 5.0):
        self.agent = LinkedInSourcingAgent()
        self.max_workers = max_workers
        self.min_delay = min_delay
        self.max_delay = max_delay

    def process_single_job(self, pdf_path: str, job_id: Optional[str] = None) -> Dict:
        """
        Process a single job description PDF and return minimal candidate data
        """
        print(f"\n[Batch] Processing job: {pdf_path}")
        results = self.agent.process_job_description(pdf_path, max_candidates=10, max_messages=5)
        minimal_candidates = []
        for c in results.get('scored_candidates', []):
            minimal_candidates.append({
                'name': c.get('name', ''),
                'linkedin_url': c.get('linkedin_url', ''),
                'fit_score': c.get('fit_score', 0),
                'score_breakdown': c.get('score_breakdown', {}),
                'headline': c.get('headline', '')
            })
        return {
            'job_id': job_id or os.path.basename(pdf_path),
            'candidates_found': len(minimal_candidates),
            'candidates': minimal_candidates
        }

    def process_jobs_in_batch(self, pdf_paths: List[str], output_file: str = "batch_results.json") -> List[Dict]:
        """
        Process multiple job descriptions in parallel, with rate limiting
        """
        print(f"\n[Batch] Starting batch processing for {len(pdf_paths)} jobs...")
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_job = {}
            for i, pdf_path in enumerate(pdf_paths):
                # Add random delay to avoid rate limiting
                delay = random.uniform(self.min_delay, self.max_delay)
                print(f"[Batch] Scheduling job {i+1}/{len(pdf_paths)}: {pdf_path} (delay: {delay:.2f}s)")
                time.sleep(delay)
                future = executor.submit(self.process_single_job, pdf_path, f"job_{i+1}")
                future_to_job[future] = pdf_path
            for future in as_completed(future_to_job):
                job_result = future.result()
                results.append(job_result)
                print(f"[Batch] Completed: {job_result['job_id']} (candidates: {job_result['candidates_found']})")
        # Save minimal results
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n[Batch] Batch processing complete. Results saved to {output_file}")
        return results

if __name__ == "__main__":
    # Example usage: process all PDFs in the current directory
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    processor = BatchJobProcessor(max_workers=3)
    processor.process_jobs_in_batch(pdf_files) 