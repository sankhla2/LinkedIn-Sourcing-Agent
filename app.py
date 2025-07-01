import gradio as gr
from fastapi import FastAPI
import requests
import json
import os

# Import your FastAPI app
try:
    from api import app as fastapi_app
except ImportError:
    # Fallback if api.py is not available
    fastapi_app = FastAPI()

# Create Gradio interface
def create_gradio_interface():
    with gr.Blocks(title="LinkedIn Sourcing Agent", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🚀 LinkedIn Sourcing Agent")
        gr.Markdown("AI-powered candidate sourcing, scoring, and outreach generation for the Synapse Challenge")
        
        with gr.Tab("Single Job Processing"):
            with gr.Row():
                with gr.Column(scale=1):
                    job_description = gr.Textbox(
                        label="Job Description",
                        placeholder="Paste your job description here...\n\nExample:\nSoftware Engineer, ML Research at Windsurf (Codeium)\n\nWe're looking for a talented ML engineer to train LLMs for code generation.\nRequirements:\n- Strong Python programming skills\n- Experience with PyTorch, TensorFlow\n- Located in Mountain View, CA or remote",
                        lines=12
                    )
                    with gr.Row():
                        max_candidates = gr.Slider(
                            minimum=1, maximum=20, value=10, step=1,
                            label="Max Candidates"
                        )
                        max_messages = gr.Slider(
                            minimum=1, maximum=10, value=5, step=1,
                            label="Max Messages"
                        )
                    process_btn = gr.Button("🚀 Process Job", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    results_output = gr.JSON(label="Results", height=400)
                    status_output = gr.Textbox(label="Status", interactive=False)
        
        with gr.Tab("Batch Processing"):
            with gr.Row():
                with gr.Column(scale=1):
                    job_descriptions = gr.Textbox(
                        label="Job Descriptions (one per line)",
                        placeholder="Job 1: Senior Backend Engineer at TechCorp\nRequirements: Python, Django, PostgreSQL\nLocation: San Francisco, CA\n\nJob 2: Data Scientist at DataCorp\nRequirements: Python, ML, SQL\nLocation: New York, NY",
                        lines=12
                    )
                    max_workers = gr.Slider(
                        minimum=1, maximum=5, value=3, step=1,
                        label="Max Workers"
                    )
                    batch_btn = gr.Button("🔄 Process Batch", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    batch_results = gr.JSON(label="Batch Results", height=400)
                    batch_status = gr.Textbox(label="Batch Status", interactive=False)
        
        with gr.Tab("API Documentation"):
            gr.Markdown("""
            ## 🔗 API Endpoints
            
            ### Health Check
            `GET /api/health`
            
            ### Process Job Description
            `POST /api/process-job`
            ```json
            {
                "job_description": "Your job description here",
                "max_candidates": 10,
                "max_messages": 5
            }
            ```
            
            ### Process PDF
            `POST /api/process-pdf`
            - Upload PDF file
            - Form parameters: max_candidates, max_messages
            
            ### Batch Process
            `POST /api/batch-process`
            ```json
            {
                "job_descriptions": ["Job 1", "Job 2", "Job 3"],
                "max_workers": 3,
                "max_candidates_per_job": 10
            }
            ```
            
            ### Interactive API Documentation
            Visit `/api/docs` for Swagger UI documentation
            
            ## 📊 Sample Response
            
            ```json
            {
                "job_id": "ml_research_windsurf",
                "candidates_found": 8,
                "top_candidates": [
                    {
                        "name": "Dr. Sarah Chen",
                        "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
                        "fit_score": 8.7,
                        "score_breakdown": {
                            "education": 9.5,
                            "trajectory": 8.0,
                            "company": 9.0,
                            "skills": 9.5,
                            "location": 8.0,
                            "tenure": 7.0
                        },
                        "headline": "Senior ML Engineer at Google | PhD Stanford"
                    }
                ],
                "outreach_messages": [
                    {
                        "candidate_name": "Dr. Sarah Chen",
                        "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
                        "fit_score": 8.7,
                        "message": "Hi Sarah, I came across your impressive background...",
                        "key_highlights": {
                            "education": "Stanford University",
                            "top_company": "Google",
                            "key_skill": "Python"
                        }
                    }
                ]
            }
            ```
            """)
        
        with gr.Tab("About"):
            gr.Markdown("""
            ## 🎯 About This Project
            
            This LinkedIn Sourcing Agent was built for the **Synapse AI Hackathon Challenge**.
            
            ### 🏆 Features Implemented
            
            ✅ **LinkedIn Profile Discovery**
            - Extracts job descriptions from PDFs using OCR
            - Searches Google for relevant LinkedIn profiles
            - Robust parsing with fallback strategies
            
            ✅ **Candidate Scoring (1-10 scale)**
            - Education (20%): Elite schools, technical degrees
            - Career Trajectory (20%): Progression, seniority levels
            - Company Relevance (15%): Top tech companies, industry match
            - Skills Match (25%): Technical skills alignment
            - Location Match (10%): Geographic compatibility
            - Tenure (10%): Job stability and progression
            
            ✅ **Personalized Message Generation**
            - AI-generated outreach messages
            - References specific candidate details
            - Professional tone with call-to-action
            
            ✅ **Scale & Performance**
            - Batch processing for multiple jobs
            - Intelligent rate limiting
            - Minimal data storage (URLs + scores)
            - SQLite caching system
            
            ### 🛠️ Technical Stack
            
            - **Backend**: FastAPI, Python
            - **Frontend**: Gradio
            - **Data Processing**: BeautifulSoup, PyPDF2, OCR
            - **Deployment**: Hugging Face Spaces
            
            ### 🚀 Built with Cursor AI
            
            This entire project was developed using Cursor IDE, demonstrating the power of AI-assisted development.
            
            ### 📞 Contact
            
            For questions about this implementation, check the code comments and documentation.
            """)
        
        # Event handlers
        def process_single_job(job_desc, max_cand, max_msg):
            try:
                if not job_desc.strip():
                    return {}, "❌ Please provide a job description"
                
                # Try to call the FastAPI endpoint if available
                try:
                    # This would work if the FastAPI app is running
                    response = requests.post(
                        "http://localhost:8000/process-job",
                        json={
                            "job_description": job_desc,
                            "max_candidates": max_cand,
                            "max_messages": max_msg
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result, "✅ Job processed successfully via API!"
                    else:
                        raise Exception(f"API returned status {response.status_code}")
                        
                except Exception as api_error:
                    # Fallback to demo data if API is not available
                    print(f"API call failed: {api_error}")
                    
                    # Generate demo data based on input
                    demo_result = {
                        "job_id": f"demo_{hash(job_desc) % 10000}",
                        "candidates_found": min(max_cand, 5),
                        "top_candidates": [
                            {
                                "name": "Dr. Sarah Chen",
                                "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
                                "fit_score": 8.7,
                                "score_breakdown": {
                                    "education": 9.5,
                                    "trajectory": 8.0,
                                    "company": 9.0,
                                    "skills": 9.5,
                                    "location": 8.0,
                                    "tenure": 7.0
                                },
                                "headline": "Senior ML Engineer at Google | PhD Stanford"
                            },
                            {
                                "name": "Alex Rodriguez",
                                "linkedin_url": "https://linkedin.com/in/alex-rodriguez-ai",
                                "fit_score": 7.2,
                                "score_breakdown": {
                                    "education": 7.5,
                                    "trajectory": 7.0,
                                    "company": 8.0,
                                    "skills": 8.0,
                                    "location": 8.0,
                                    "tenure": 6.0
                                },
                                "headline": "AI Engineer | Machine Learning | Python, TensorFlow"
                            }
                        ],
                        "outreach_messages": [
                            {
                                "candidate_name": "Dr. Sarah Chen",
                                "linkedin_url": "https://linkedin.com/in/sarah-chen-ml",
                                "fit_score": 8.7,
                                "message": f"Hi Sarah, I came across your impressive background in Python and your work at Google. Your experience at Google and expertise in PyTorch, Transformers, LLMs caught my attention.\n\nI'm reaching out because we're hiring for a Software Engineer, ML Research position at Windsurf (Codeium), a Forbes AI 50 company building AI-powered developer tools.\n\nThe role focuses on training LLMs for code generation and offers $140-300k + equity in Mountain View, CA.\n\nWould you be open to a brief conversation about this opportunity?",
                                "key_highlights": {
                                    "education": "Stanford University",
                                    "top_company": "Google",
                                    "key_skill": "Python"
                                }
                            }
                        ],
                        "message_summary": {
                            "total_messages": 1,
                            "average_score": 8.7,
                            "score_distribution": {"high": 1, "medium": 0, "low": 0}
                        }
                    }
                    
                    return demo_result, "✅ Demo mode: Job processed successfully! (API not available)"
                
            except Exception as e:
                return {}, f"❌ Error: {str(e)}"
        
        def process_batch_jobs(job_descs, max_work):
            try:
                if not job_descs.strip():
                    return {}, "❌ Please provide job descriptions"
                
                # Split job descriptions
                jobs = [job.strip() for job in job_descs.split('\n\n') if job.strip()]
                
                if len(jobs) == 0:
                    return {}, "❌ No valid job descriptions found"
                
                # Try to call the batch API endpoint
                try:
                    response = requests.post(
                        "http://localhost:8000/batch-process",
                        json={
                            "job_descriptions": jobs,
                            "max_workers": max_work,
                            "max_candidates_per_job": 5
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result, f"✅ Batch processed successfully via API!"
                    else:
                        raise Exception(f"API returned status {response.status_code}")
                        
                except Exception as api_error:
                    # Fallback to demo data
                    print(f"Batch API call failed: {api_error}")
                    
                    demo_result = {
                        "total_jobs": len(jobs),
                        "total_candidates": len(jobs) * 3,
                        "results": [
                            {
                                "job_id": f"batch_job_{i+1}",
                                "candidates_found": 3,
                                "candidates": [
                                    {
                                        "name": f"Candidate {i+1}-{j+1}",
                                        "linkedin_url": f"https://linkedin.com/in/candidate-{i+1}-{j+1}",
                                        "fit_score": 7.5 - j * 0.5,
                                        "headline": f"Software Engineer at Company {j+1}"
                                    } for j in range(3)
                                ]
                            } for i in range(len(jobs))
                        ]
                    }
                    
                    return demo_result, f"✅ Demo mode: Processed {len(jobs)} jobs successfully! (API not available)"
                
            except Exception as e:
                return {}, f"❌ Error: {str(e)}"
        
        # Connect event handlers
        process_btn.click(
            process_single_job,
            inputs=[job_description, max_candidates, max_messages],
            outputs=[results_output, status_output]
        )
        
        batch_btn.click(
            process_batch_jobs,
            inputs=[job_descriptions, max_workers],
            outputs=[batch_results, batch_status]
        )
    
    return demo

# Create the Gradio app
app = create_gradio_interface()

# Mount FastAPI app if available
try:
    app = gr.mount_gradio_app(app, fastapi_app, path="/api")
except Exception as e:
    print(f"Could not mount FastAPI app: {e}")
    print("Running in Gradio-only mode")

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 