# 🚀 LinkedIn Sourcing Agent

An autonomous AI agent that sources LinkedIn profiles at scale, scores candidates using a fit score algorithm, and generates personalized outreach messages.

## 🌟 Features

- **LinkedIn Profile Discovery**: Searches for relevant LinkedIn profiles based on job descriptions
- **Intelligent Fit Scoring**: Rates candidates 1-10 using a comprehensive scoring rubric
- **Personalized Outreach**: Generates AI-powered personalized messages
- **Scalable Architecture**: Handles multiple jobs simultaneously
- **RESTful API**: FastAPI endpoints for easy integration

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python
- **AI/LLM**: OpenAI GPT-4
- **Data Storage**: SQLite
- **Web Scraping**: Selenium + BeautifulSoup
- **Search**: Google Search API

## 📦 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd linkedin-sourcing-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
python main.py
```

## 🚀 Quick Start

### Using the API

```python
import requests

# Submit a job for sourcing
job_data = {
    "job_description": "Senior Backend Engineer at fintech startup...",
    "location": "San Francisco",
    "company": "Windsurf"
}

response = requests.post("http://localhost:8000/source-candidates", json=job_data)
candidates = response.json()
```

### Using the CLI

```bash
python cli.py --job-description "Senior Backend Engineer" --location "San Francisco"
```

## 📊 Fit Score Rubric

The agent scores candidates on:
- **Education (20%)**: School prestige and progression
- **Career Trajectory (20%)**: Growth and advancement
- **Company Relevance (15%)**: Industry and company quality
- **Experience Match (25%)**: Skills alignment
- **Location Match (10%)**: Geographic fit
- **Tenure (10%)**: Job stability and progression

## 🔧 Configuration

Edit `config.py` to customize:
- Scoring weights
- Search parameters
- Rate limiting settings
- LLM prompts

## 📈 API Endpoints

- `POST /source-candidates`: Submit job for sourcing
- `GET /candidates/{job_id}`: Get sourced candidates
- `POST /score-candidates`: Score existing candidates
- `GET /health`: Health check

## 🎯 Example Output

```json
{
  "job_id": "backend-fintech-sf",
  "candidates_found": 25,
  "top_candidates": [
    {
      "name": "Jane Smith",
      "linkedin_url": "linkedin.com/in/janesmith",
      "fit_score": 8.5,
      "score_breakdown": {
        "education": 9.0,
        "trajectory": 8.0,
        "company": 8.5,
        "skills": 9.0,
        "location": 10.0,
        "tenure": 7.0
      },
      "outreach_message": "Hi Jane, I noticed your 6 years..."
    }
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 