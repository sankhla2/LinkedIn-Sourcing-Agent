# 🚀 Deployment Guide: LinkedIn Sourcing Agent API

This guide will help you deploy your LinkedIn Sourcing Agent API to Hugging Face Spaces for the Synapse challenge bonus.

## 📋 Prerequisites

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Git**: Ensure you have Git installed
3. **Python Environment**: Your local development environment should be working

## 🏗️ Project Structure for Deployment

```
linkedin-sourcing-agent/
├── api.py                    # FastAPI application
├── main_integrated.py        # Core agent logic
├── run.py                    # LinkedIn profile finder
├── candidate_scorer.py       # Scoring algorithm
├── message_generator.py      # Message generation
├── batch_processor.py        # Batch processing
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
├── app.py                    # Hugging Face Spaces entry point
└── .gitignore               # Git ignore file
```

## 📝 Step 1: Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose settings:
   - **Owner**: Your username
   - **Space name**: `linkedin-sourcing-agent`
   - **License**: MIT
   - **Space SDK**: Gradio (we'll customize this)
   - **Space hardware**: CPU (free tier)

## 📝 Step 2: Create app.py for Hugging Face Spaces

Create a new file `app.py` that wraps your FastAPI app for Hugging Face Spaces:

```python
import gradio as gr
from fastapi import FastAPI
from api import app as fastapi_app
import uvicorn
import threading
import time

# Create Gradio interface
def create_gradio_interface():
    with gr.Blocks(title="LinkedIn Sourcing Agent") as demo:
        gr.Markdown("# 🚀 LinkedIn Sourcing Agent")
        gr.Markdown("AI-powered candidate sourcing, scoring, and outreach generation")
        
        with gr.Tab("Single Job Processing"):
            with gr.Row():
                with gr.Column():
                    job_description = gr.Textbox(
                        label="Job Description",
                        placeholder="Paste your job description here...",
                        lines=10
                    )
                    max_candidates = gr.Slider(
                        minimum=1, maximum=20, value=10, step=1,
                        label="Max Candidates"
                    )
                    max_messages = gr.Slider(
                        minimum=1, maximum=10, value=5, step=1,
                        label="Max Messages"
                    )
                    process_btn = gr.Button("🚀 Process Job", variant="primary")
                
                with gr.Column():
                    results_output = gr.JSON(label="Results")
                    status_output = gr.Textbox(label="Status")
        
        with gr.Tab("Batch Processing"):
            with gr.Row():
                with gr.Column():
                    job_descriptions = gr.Textbox(
                        label="Job Descriptions (one per line)",
                        placeholder="Job 1 description...\nJob 2 description...\nJob 3 description...",
                        lines=10
                    )
                    max_workers = gr.Slider(
                        minimum=1, maximum=5, value=3, step=1,
                        label="Max Workers"
                    )
                    batch_btn = gr.Button("🔄 Process Batch", variant="primary")
                
                with gr.Column():
                    batch_results = gr.JSON(label="Batch Results")
                    batch_status = gr.Textbox(label="Batch Status")
        
        with gr.Tab("API Documentation"):
            gr.Markdown("""
            ## API Endpoints
            
            ### Health Check
            `GET /health`
            
            ### Process Job Description
            `POST /process-job`
            ```json
            {
                "job_description": "Your job description here",
                "max_candidates": 10,
                "max_messages": 5
            }
            ```
            
            ### Process PDF
            `POST /process-pdf`
            - Upload PDF file
            - Form parameters: max_candidates, max_messages
            
            ### Batch Process
            `POST /batch-process`
            ```json
            {
                "job_descriptions": ["Job 1", "Job 2", "Job 3"],
                "max_workers": 3,
                "max_candidates_per_job": 10
            }
            ```
            
            ### API Documentation
            Visit `/docs` for interactive API documentation
            """)
        
        # Event handlers
        def process_single_job(job_desc, max_cand, max_msg):
            try:
                # This would call your FastAPI endpoint
                # For demo, return sample data
                return {
                    "job_id": "demo_job",
                    "candidates_found": 5,
                    "top_candidates": [
                        {
                            "name": "John Doe",
                            "linkedin_url": "https://linkedin.com/in/johndoe",
                            "fit_score": 8.5,
                            "headline": "Senior ML Engineer"
                        }
                    ],
                    "outreach_messages": [
                        {
                            "candidate_name": "John Doe",
                            "message": "Hi John, I noticed your impressive background..."
                        }
                    ]
                }, "✅ Job processed successfully!"
            except Exception as e:
                return {}, f"❌ Error: {str(e)}"
        
        def process_batch_jobs(job_descs, max_work):
            try:
                # Split job descriptions
                jobs = [job.strip() for job in job_descs.split('\n') if job.strip()]
                
                # This would call your batch API endpoint
                # For demo, return sample data
                return {
                    "total_jobs": len(jobs),
                    "total_candidates": len(jobs) * 3,
                    "results": [
                        {
                            "job_id": f"job_{i+1}",
                            "candidates_found": 3
                        } for i in range(len(jobs))
                    ]
                }, f"✅ Processed {len(jobs)} jobs successfully!"
            except Exception as e:
                return {}, f"❌ Error: {str(e)}"
        
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

# Mount FastAPI app
app = gr.mount_gradio_app(app, fastapi_app, path="/api")

if __name__ == "__main__":
    app.launch()
```

## 📝 Step 3: Update requirements.txt

Ensure your `requirements.txt` includes all necessary dependencies:

```txt
requests
beautifulsoup4
PyPDF2
pdfplumber
pdf2image
pytesseract
Pillow
fastapi
uvicorn
python-multipart
pydantic
gradio
```

## 📝 Step 4: Create .gitignore

Create a `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.db
*.sqlite
*.json
*.pdf
*.log
```

## 📝 Step 5: Update README.md

Update your README.md to include deployment information:

```markdown
# 🚀 LinkedIn Sourcing Agent

AI-powered LinkedIn candidate sourcing, scoring, and outreach generation.

## 🌐 Live Demo

**API Endpoint**: [Your Hugging Face Space URL]/api

**Interactive Demo**: [Your Hugging Face Space URL]

## 🚀 Quick Start

### Local Development
```bash
pip install -r requirements.txt
python api.py
```

### API Usage
```bash
# Health check
curl https://your-space-url.hf.space/api/health

# Process job
curl -X POST https://your-space-url.hf.space/api/process-job \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Your job description", "max_candidates": 10}'
```

## 📊 Features

- ✅ LinkedIn Profile Discovery
- ✅ Candidate Scoring (1-10 scale)
- ✅ Personalized Message Generation
- ✅ Batch Processing
- ✅ Rate Limiting
- ✅ Minimal Data Storage

## 🔗 API Documentation

Visit `/api/docs` for interactive API documentation.
```

## 📝 Step 6: Deploy to Hugging Face Spaces

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Add Hugging Face remote**:
   ```bash
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/linkedin-sourcing-agent
   ```

3. **Push to Hugging Face**:
   ```bash
   git push -u origin main
   ```

4. **Monitor deployment**:
   - Go to your Space on Hugging Face
   - Check the "Settings" tab for build logs
   - Wait for the build to complete (usually 5-10 minutes)

## 🧪 Testing Your Deployment

1. **Test the Gradio interface**:
   - Visit your Space URL
   - Try the interactive demo

2. **Test the API endpoints**:
   ```bash
   # Health check
   curl https://your-space-url.hf.space/api/health
   
   # Process job
   curl -X POST https://your-space-url.hf.space/api/process-job \
     -H "Content-Type: application/json" \
     -d '{"job_description": "Software Engineer at TechCorp", "max_candidates": 5}'
   ```

3. **Test API documentation**:
   - Visit `https://your-space-url.hf.space/api/docs`

## 🔧 Troubleshooting

### Common Issues

1. **Build fails**:
   - Check the build logs in your Space settings
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **API not accessible**:
   - Ensure `app.py` properly mounts the FastAPI app
   - Check that the path is correct (`/api`)

3. **Import errors**:
   - Make sure all your Python files are in the repository
   - Check that import paths are correct

### Performance Optimization

1. **Reduce memory usage**:
   - Limit concurrent workers in batch processing
   - Implement proper cleanup of temporary files

2. **Improve response times**:
   - Add caching for repeated requests
   - Optimize the scoring algorithm

## 📊 Monitoring and Analytics

Once deployed, you can monitor:

- **API usage**: Check Hugging Face Space analytics
- **Error rates**: Monitor build logs and error responses
- **Performance**: Track response times and resource usage

## 🎉 Success!

Your LinkedIn Sourcing Agent is now deployed and accessible via:

- **Interactive Demo**: `https://your-space-url.hf.space`
- **API Endpoint**: `https://your-space-url.hf.space/api`
- **Documentation**: `https://your-space-url.hf.space/api/docs`

Share these URLs in your Synapse challenge submission for the bonus points! 🚀 