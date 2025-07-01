# 🚀 LinkedIn Sourcing Agent with Candidate Scoring

A comprehensive AI agent that sources LinkedIn profiles, scores candidates using a sophisticated fit score algorithm, and generates personalized outreach messages.

## 🎯 Features

### ✅ Step 1: LinkedIn Profile Discovery
- **PDF Job Description Processing**: Extracts text from PDF job descriptions using OCR
- **Intelligent Search**: Uses Google search to find relevant LinkedIn profiles
- **Robust Parsing**: Handles various LinkedIn URL formats and profile structures
- **Caching System**: Implements SQLite caching to avoid re-fetching data

### ✅ Step 2: Candidate Scoring Algorithm
- **Comprehensive Fit Score**: 1-10 rating based on 6 key criteria
- **Weighted Scoring System**: 
  - Education (20%): Elite schools, technical degrees
  - Career Trajectory (20%): Progression, seniority levels
  - Company Relevance (15%): Top tech companies, industry match
  - Skills Match (25%): Technical skills alignment
  - Location Match (10%): Geographic compatibility
  - Tenure (10%): Job stability and progression

### ✅ Step 3: Message Generation
- **Personalized Outreach**: AI-generated messages referencing candidate details
- **Professional Tone**: Maintains recruiter-friendly communication style
- **Customization**: Tailored to specific job requirements and candidate strengths
- **Message Analysis**: Effectiveness scoring and optimization
- **Multiple Variations**: A/B testing capabilities

## 🏗️ Architecture

```
Job Description PDF → Text Extraction → LinkedIn Search → Profile Scoring → Message Generation → Results
       ↓                    ↓                ↓              ↓              ↓              ↓
   OCR/PDF2Image    Google Search API   BeautifulSoup   Fit Algorithm   AI Templates   JSON Output
```

## 📊 Scoring Rubric

### Education (20%)
- **Elite Schools** (MIT, Stanford, Harvard, etc.): 9-10
- **Strong Technical Schools**: 7-8
- **Standard Universities**: 5-6
- **Relevant Degrees** (CS, Engineering, AI/ML): +1 bonus

### Career Trajectory (20%)
- **Director/Principal Level**: 9.0
- **Lead/Senior Level**: 7.5
- **Mid-Level**: 6.5
- **Entry Level**: 5.0

### Company Relevance (15%)
- **Top Tech Companies** (Google, Microsoft, etc.): 9.0
- **AI/ML Companies**: 8.0
- **Tech Startups**: 7.0
- **Other Companies**: 6.0

### Skills Match (25%)
- **5+ Matching Skills**: 9.5
- **3-4 Matching Skills**: 8.0
- **1-2 Matching Skills**: 6.5
- **No Matches**: 5.0

### Location Match (10%)
- **Exact City Match**: 10.0
- **Metro Area Match**: 8.0
- **Remote-Friendly**: 6.0
- **No Match**: 5.0

### Tenure (10%)
- **1-2 Companies** (Stable): 9.0
- **3-4 Companies** (Reasonable): 7.0
- **5-6 Companies** (Some hopping): 5.0
- **7+ Companies** (Frequent changes): 3.0

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Complete Pipeline
```bash
python main_integrated.py
```

### 3. Test Message Generation
```bash
python test_messages.py
```

### 4. Test Complete Pipeline
```bash
python main_integrated.py
```

### 5. Run Individual Components
```bash
# LinkedIn search only
python run.py

# Scoring with sample data
python test_scoring.py

# Message generation only
python test_messages.py
```

## 📁 Project Structure

```
AI_challenge/
├── main_integrated.py          # Complete pipeline
├── run.py                      # LinkedIn profile finder
├── candidate_scorer.py         # Scoring algorithm
├── message_generator.py        # Message generation
├── test_scoring.py            # Test script with sample data
├── test_messages.py           # Test script for messages
├── linkedin_agent.py          # Basic LinkedIn search
├── main.py                    # Simple entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── sourcing_results.json      # Output results
├── linkedin_cache.db          # SQLite cache
└── *.pdf                      # Job description PDFs
```

## 🔧 Configuration

### Elite Schools List
The system recognizes top-tier institutions for education scoring:
- MIT, Stanford, Harvard, Berkeley, Caltech, CMU, Princeton
- Yale, Columbia, UPenn, Cornell, Brown, Dartmouth, Duke
- Northwestern, UChicago, NYU, USC, UCLA, UCSD, Georgia Tech
- UIUC, UMich, UW, UT Austin, and more

### Top Tech Companies
Recognized companies for company relevance scoring:
- Google, Microsoft, Apple, Amazon, Meta, Netflix
- Uber, Lyft, Airbnb, Stripe, Palantir, Databricks
- OpenAI, Anthropic, DeepMind, Waymo, Tesla, SpaceX
- And 30+ other top tech companies

### AI/ML Skills
Comprehensive skill matching for technical roles:
- Programming: Python, C++, Java, Julia, R, MATLAB
- ML Frameworks: TensorFlow, PyTorch, Scikit-learn, Keras
- AI/ML: NLP, Computer Vision, Deep Learning, LLMs
- Tools: AWS, Azure, GCP, Docker, Kubernetes, Spark
- And 40+ other relevant skills

## 📊 Sample Output

```json
{
  "job_id": "ai-ml-research-windsurf",
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
      "message": "Hi Sarah, I came across your impressive background in Python and your work at Google...",
      "key_highlights": {
        "education": "Stanford University",
        "top_company": "Google",
        "key_skill": "Python"
      }
    }
  ]
}
```

## 🛠️ API Integration

The system provides API-ready response formats:

```python
from main_integrated import LinkedInSourcingAgent

agent = LinkedInSourcingAgent()
results = agent.process_job_description("job_description.pdf")
api_response = agent.get_api_response_format(results)
```

## 🌐 API Deployment

### Local Development
```bash
# Start the FastAPI server
python api.py

# Test the API
python test_api.py
```

### Hugging Face Spaces Deployment
1. **Create Space**: Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. **Upload Code**: Push your code to the Space repository
3. **Access API**: Your API will be available at `https://your-space-url.hf.space/api`

### API Endpoints
- **Health Check**: `GET /api/health`
- **Process Job**: `POST /api/process-job`
- **Process PDF**: `POST /api/process-pdf`
- **Batch Process**: `POST /api/batch-process`
- **Documentation**: `GET /api/docs`

### Interactive Demo
Visit your Hugging Face Space URL for an interactive Gradio interface.

For detailed deployment instructions, see `deployment_guide.md`.

## 🔄 Caching System

- **SQLite Database**: Stores search results for 24 hours
- **Automatic Cache Management**: Prevents duplicate requests
- **Configurable TTL**: Adjustable cache expiration

## 🚨 Rate Limiting

- **Intelligent Delays**: Random delays between requests (1-5 seconds)
- **User-Agent Rotation**: Realistic browser headers
- **Error Handling**: Graceful handling of blocked requests

## 🔮 Future Enhancements

### Planned Features
- [x] **Message Generation**: AI-powered personalized outreach
- [x] **FastAPI Endpoint**: Deployable API service
- [x] **Batch Processing**: Handle multiple jobs simultaneously
- [ ] **Multi-Source Integration**: GitHub, Twitter, personal websites
- [ ] **Confidence Scoring**: Uncertainty quantification
- [ ] **Advanced Analytics**: Detailed candidate insights

### Technical Improvements
- [ ] **LinkedIn API Integration**: Official API access
- [ ] **Enhanced OCR**: Better PDF text extraction
- [ ] **Machine Learning**: Learn from scoring patterns
- [ ] **Distributed Processing**: Scale to 100s of jobs

## 🤝 Contributing

This project is part of the **Synapse AI Hackathon Challenge**. 

### Development Guidelines
1. **Use Cursor**: All development should be done in Cursor IDE
2. **Python Focus**: Primary language is Python
3. **Documentation**: Comment code and explain decisions
4. **Testing**: Include test cases for new features
5. **Performance**: Consider scalability and rate limiting

## 📝 License

This project is created for educational purposes as part of the Synapse AI Hackathon Challenge.

## 🆘 Troubleshooting

### Common Issues

**PDF Text Extraction Fails**
- Ensure PDF is not password protected
- Try different PDF files
- Check if PDF contains scanned images

**No LinkedIn Profiles Found**
- Try broader search terms
- Check internet connection
- Verify Google search is accessible

**Scoring Errors**
- Ensure all dependencies are installed
- Check candidate data format
- Verify job description content

### Debug Mode
Enable debug output by modifying the search functions to print detailed information about the search process.

## 📞 Support

For questions about this implementation:
- Check the code comments for detailed explanations
- Review the test scripts for usage examples
- Examine the scoring algorithm for customization options

---

**Built with ❤️ for the Synapse AI Hackathon Challenge** 