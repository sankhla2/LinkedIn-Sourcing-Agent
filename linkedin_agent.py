
import re
import requests
import PyPDF2
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import List, Dict, Optional
import sqlite3
from datetime import datetime
import json
import os
import time
import random

class LinkedInProfileFinder:
    def __init__(self):
        self.cache_db = "linkedin_cache.db"
        self._init_db()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def _init_db(self):
        """Initialize SQLite database for caching"""
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    query TEXT PRIMARY KEY,
                    results TEXT,
                    timestamp DATETIME
                )
            """)
    
    def _get_from_cache(self, query: str) -> Optional[List[Dict]]:
        """Retrieve cached search results"""
        with sqlite3.connect(self.cache_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT results FROM cache WHERE query = ? AND timestamp > datetime('now', '-1 day')",
                (query,)
            )
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
    
    def _save_to_cache(self, query: str, results: List[Dict]):
        """Save search results to cache"""
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (query, results, timestamp) VALUES (?, ?, ?)",
                (query, json.dumps(results), datetime.now())
            )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file with improved error handling"""
        text = ""
        try:
            # Verify file exists
            if not os.path.exists(pdf_path):
                print(f"Error: File not found at {pdf_path}")
                return text
            
            # Verify it's a PDF file
            if not pdf_path.lower().endswith('.pdf'):
                print("Error: File is not a PDF")
                return text
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if reader.is_encrypted:
                    try:
                        reader.decrypt('')  # Try empty password
                    except:
                        print("Error: PDF is encrypted and cannot be read")
                        return text
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
        return text.strip()
    
    def extract_search_terms(self, job_description: str) -> str:
        """
        Improved search term extraction specifically for Gen AI Solution Architect roles
        """
        # First try to extract the exact job title from common patterns
        title_patterns = [
            r'Role:\s*(.*?)\n',
            r'Proposed Role:\s*(.*?)\n', 
            r'Title:\s*(.*?)\n',
            r'Position:\s*(.*?)\n',
            r'Job Title:\s*(.*?)\n',
            r'AI Engineer\s*-\s*(.*?)\n'
        ]
        
        title = None
        for pattern in title_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
                
        # If no explicit title found, look for Gen AI Solution Architect patterns
        if not title:
            title_matches = re.findall(
                r'(Gen(?:erative)?\s*AI\s*Solution\s*Architect|'
                r'AI\s*(?:Solution\s*)?Architect|'
                r'Artificial\s*Intelligence\s*Solution\s*Architect)',
                job_description,
                re.IGNORECASE
            )
            if title_matches:
                title = title_matches[0]
            else:
                title = "Gen AI Solution Architect"  # Default fallback

        # Extract skills - expanded list focused on AI/ML
        skills = re.findall(
            r'(Python|Java|TensorFlow|PyTorch|LLM|GPT|NLP|Natural\s*Language\s*Processing|'
            r'Machine\s*Learning|Deep\s*Learning|Computer\s*Vision|Generative\s*AI|'
            r'AWS|Azure|GCP|Docker|Kubernetes|Spark|Hadoop|LangChain|Hugging\s*Face|'
            r'LLaMA|GPT-4|Transformers|Neural\s*Networks)',
            job_description,
            re.IGNORECASE
        )
        skills = list(set([s.capitalize() for s in skills]))  # Dedupe and standardize
        
        # Extract locations - expanded list
        locations = re.findall(
            r'(San\s*Francisco|SF|New\s*York|NYC|Mountain\s*View|Remote|'
            r'Austin|Seattle|Boston|Chicago|Pan\s*India|India|Bangalore|'
            r'Hyderabad|Pune|Chennai|Delhi|NCR|Gurgaon)',
            job_description,
            re.IGNORECASE
        )
        
        # Format search terms - be less specific to find more results
        terms = []
        
        # Add title (but make it less specific)
        if title:
            # Simplify the title for better search results
            if "Gen AI" in title or "Generative AI" in title:
                terms.append("AI Solution Architect")
            else:
                terms.append(title)
        
        # Add key skills (limit to most common ones)
        if skills:
            # Focus on broader, more common skills
            common_skills = [s for s in skills if s.lower() in ['python', 'machine learning', 'ai', 'ml', 'tensorflow', 'pytorch']]
            terms.extend(common_skills[:3])
        
        # Add location if found
        if locations:
            terms.append(locations[0])
            
        # Clean up terms and remove empty/none values
        terms = [t for t in terms if t and str(t).strip()]
        
        # If still too specific, add some broader terms
        if len(terms) < 3:
            terms.extend(['AI', 'Machine Learning'])
            
        return " ".join(terms)
    
    def search_linkedin_via_google(self, search_terms: str, max_results: int = 10) -> List[Dict]:
        """
        Robust LinkedIn profile search via Google with:
        - Realistic delays to avoid blocking
        - Multiple selector patterns
        - Better error handling
        """
        # Check cache first
        cached_results = self._get_from_cache(search_terms)
        if cached_results:
            return cached_results
        
        # Format Google search query
        query = f'site:linkedin.com/in {search_terms}'
        encoded_query = quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&num={max_results}"
        
        try:
            # Add realistic delay to mimic human behavior
            time.sleep(random.uniform(2, 5))
            
            response = requests.get(search_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # Debug: Print response status and content preview
            print(f"Response status: {response.status_code}")
            print(f"Response content preview: {response.text[:500]}...")
            
            # Parse results with more comprehensive selectors
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Method 1: Find all links containing linkedin.com/in
            all_links = soup.find_all('a', href=True)
            linkedin_links = [link for link in all_links if 'linkedin.com/in/' in link['href']]
            
            print(f"Found {len(linkedin_links)} LinkedIn links in HTML")
            
            for link in linkedin_links[:max_results]:
                url = link['href']
                
                # Clean URL - remove Google redirect parameters
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                elif '&ved=' in url:
                    url = url.split('&ved=')[0]
                
                # Get title from link text or parent elements
                title = link.get_text().strip()
                if not title:
                    # Try to find title in parent elements
                    parent = link.parent
                    if parent:
                        title_elem = parent.find('h3') or parent.find('div', class_='title')
                        if title_elem:
                            title = title_elem.get_text().strip()
                
                # Extract name and headline
                if '|' in title:
                    name, headline = title.split('|', 1)
                elif ' - ' in title:
                    name, headline = title.split(' - ', 1)
                else:
                    name = title
                    headline = ""
                
                name = name.strip()
                headline = headline.strip()
                
                # Skip if no meaningful name
                if len(name) < 2:
                    continue
                
                results.append({
                    "name": name,
                    "linkedin_url": url,
                    "headline": headline
                })
            
            # Cache results
            if results:
                self._save_to_cache(search_terms, results)
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Network error searching LinkedIn: {e}")
            return []
        except Exception as e:
            print(f"Error parsing search results: {e}")
            return []
    
    def find_profiles_from_pdf(self, pdf_path: str, max_results: int = 10) -> List[Dict]:
        """Main function to find LinkedIn profiles from a job description PDF"""
        print(f"\nAttempting to read PDF from: {pdf_path}")
        
        # Step 1: Extract text from PDF
        job_description = self.extract_text_from_pdf(pdf_path)
        if not job_description:
            print("\nFailed to extract text from PDF. Possible reasons:")
            print("- File is not a valid PDF")
            print("- PDF is password protected")
            print("- File path is incorrect")
            print("- PDF contains scanned images (non-text content)")
            return []
        
        print("\nSuccessfully extracted text from PDF")
        print("\nSample of extracted text (first 300 chars):")
        print(job_description[:300] + "...")
        
        # Step 2: Extract search terms
        search_terms = self.extract_search_terms(job_description)
        if not search_terms:
            print("\nNo search terms extracted from job description")
            return []
        
        print(f"\nSearching LinkedIn for: {search_terms}")
        
        # Step 3: Search LinkedIn via Google
        profiles = self.search_linkedin_via_google(search_terms, max_results)
        
        if not profiles:
            print("\nNo profiles found with primary search terms. Trying fallback terms...")
            # Try multiple fallback strategies
            fallback_terms_list = [
                "AI Solution Architect Python",
                "Machine Learning Engineer Python",
                "AI Engineer Python",
                "Data Scientist Python",
                "Software Engineer AI"
            ]
            
            for fallback_terms in fallback_terms_list:
                print(f"Trying: {fallback_terms}")
                profiles = self.search_linkedin_via_google(fallback_terms, max_results)
                if profiles:
                    print(f"Found {len(profiles)} profiles with fallback terms")
                    break
        
        return profiles





















# import requests
# from bs4 import BeautifulSoup
# import PyPDF2
# import re
# import pdfplumber
# import pdf2image
# import pytesseract
# from PIL import Image
# import os


# def extract_job_description_from_pdf(pdf_path):
#     # Try text extraction first
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         text = ''
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + '\n'
#     if text.strip():
#         return text.strip()

#     # Fallback: OCR for scanned/image-based PDFs
#     print("No text found with PyPDF2, using OCR...")
#     images = pdf2image.convert_from_path(pdf_path)
#     ocr_text = ''
#     for i, image in enumerate(images):
#         page_text = pytesseract.image_to_string(image)
#         print(f"OCR Page {i+1}: {repr(page_text)[:200]}")
#         ocr_text += page_text + '\n'
#     return ocr_text.strip()


# def google_linkedin_search(query, num_results=10):
#     search_url = f"https://www.google.com/search?q=site:linkedin.com/in+{requests.utils.quote(query)}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     response = requests.get(search_url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     results = []
#     for g in soup.find_all('div', class_='g'):
#         link = g.find('a', href=True)
#         if link and 'linkedin.com/in/' in link['href']:
#             title = g.find('h3')
#             snippet = g.find('span', {'class': 'aCOpRe'})
#             results.append({
#                 'linkedin_url': link['href'],
#                 'name': title.text if title else '',
#                 'headline': snippet.text if snippet else ''
#             })
#         if len(results) >= num_results:
#             break
#     return results


# def search_linkedin_candidates(job_description, num_results=10):
#     # Use keywords from job description for search
#     keywords = ' '.join(job_description.split()[:10])  # crude, improve later
#     candidates = google_linkedin_search(keywords, num_results=num_results)
#     return candidates 