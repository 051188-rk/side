# SIDE Backend

SIDE (Signal Desk) - AI-powered Omnichannel Customer Feedback Intelligence Platform

## Overview

SIDE is a production-ready AI Agent platform that receives customer feedback from multiple platforms, understands it using AI Agents, detects duplicate issues, prioritizes them, remembers previous incidents, creates intelligent tickets, and exposes everything through APIs.

## Features

- **Multi-Channel Feedback Collection**: Discord, Telegram, Gmail, GitHub, Webhooks
- **AI-Powered Analysis**: 14 specialized agents for classification, sentiment, severity, duplicate detection
- **LangGraph Workflow**: Production multi-agent architecture with conditional routing
- **Long-Term Memory**: Cognee integration for historical context and pattern detection
- **Intelligent Ticketing**: Auto-generated tickets with priority scoring
- **Dashboard APIs**: Analytics, reports, and insights
- **Background Workers**: Async processing for emails, webhooks, and insights
- **LLM Fallback**: Automatic switching between Groq and Gemini

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Package Manager**: uv
- **Server**: Uvicorn
- **Validation**: Pydantic V2
- **ORM**: Firebase Firestore Admin SDK
- **Authentication**: Firebase Authentication
- **Agent Framework**: LangGraph + LangChain
- **LLM Providers**: Groq API, Google Gemini API
- **Memory**: Cognee
- **Integrations**: Discord, Telegram, Gmail, GitHub, TinyFish, SMTP

## Architecture

```
backend/
├── app/
│   ├── agents/          # 14 AI agents
│   ├── graphs/          # LangGraph workflows
│   ├── memory/          # Cognee memory manager
│   ├── integrations/    # External service integrations
│   ├── routers/         # FastAPI routers
│   ├── schemas/         # Pydantic schemas
│   ├── repositories/    # Firestore repositories
│   ├── middleware/      # Custom middleware
│   ├── core/            # Security, logging, exceptions
│   ├── config/          # Configuration
│   ├── utils/           # Helper functions
│   ├── workers/         # Background workers
│   └── tests/           # Unit and integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Installation

### Prerequisites

- Python 3.12+
- uv package manager
- Firebase project with Firestore enabled
- Groq API key
- Gemini API key
- Cognee API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Configure your `.env` file with your API keys and credentials.

5. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

See `.env.example` for all required environment variables:

- Firebase credentials
- Groq API key
- Gemini API key
- Cognee API key
- Discord bot token
- Telegram bot token
- GitHub access token
- Gmail credentials
- SMTP settings

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/signup` - User signup
- `POST /api/v1/feedback` - Create feedback
- `POST /api/v1/tickets` - Create ticket
- `POST /api/v1/webhooks/{source}` - Receive webhooks
- `POST /api/v1/agents/process-feedback` - Process feedback with AI
- `GET /api/v1/dashboard/*` - Dashboard analytics

## AI Agents

### 1. Feedback Collector Agent
Collects feedback from Discord, Telegram, Gmail, GitHub, and webhooks.

### 2. Feedback Cleaner Agent
Removes spam, normalizes text, detects language, extracts attachments.

### 3. Classification Agent
Classifies feedback into: Bug, Feature Request, Question, Complaint, Praise, Security, Payment, Account, Other.

### 4. Severity Agent
Predicts severity: Low, Medium, High, Critical.

### 5. Sentiment Agent
Analyzes sentiment: Positive, Neutral, Negative, Angry, Frustrated, Urgent.

### 6. Duplicate Detection Agent
Uses embeddings and Cognee memory to find similar issues.

### 7. Ticket Generation Agent
Generates comprehensive tickets with titles, descriptions, reproduction steps.

### 8. Priority Agent
Calculates priority based on severity, sentiment, duplicates, affected users.

### 9. Memory Agent
Stores processed issues in Cognee for long-term memory.

### 10. Insight Agent
Generates daily/weekly summaries, trending issues, top bugs, feature requests.

### 11. Response Draft Agent
Drafts professional responses for email, Discord, Telegram, GitHub.

### 12. Search Agent
Searches documentation, release notes, known issues using TinyFish.

### 13. Fetch Agent
Extracts page content to provide context to other agents.

### 14. Routing Agent
Determines which agents should execute using LangGraph conditional routing.

## LangGraph Workflow

```
Feedback → Cleaning → Classification → Sentiment → Severity → Search → Fetch → 
Duplicate Detection → Cognee Memory → Priority → Ticket Creation → Insights → 
Response Draft → Store Results
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_utils.py
```

## Docker Deployment

Build and run with Docker Compose:

```bash
docker-compose up -d
```

## Background Workers

Start background workers for async processing:

```python
from app.workers import email_worker, webhook_worker, insight_worker
import asyncio

async def main():
    await asyncio.gather(
        email_worker.start(),
        webhook_worker.start(),
        insight_worker.start(),
    )

asyncio.run(main())
```

## Firebase Setup

1. Create a Firebase project
2. Enable Firestore Database
3. Enable Authentication
4. Create a service account key
5. Add the service account credentials to your `.env` file

## Cognee Setup

1. Sign up for Cognee API key
2. Configure vector database (Weaviate)
3. Configure knowledge graph (Neo4j)
4. Add credentials to `.env`

## Groq & Gemini Setup

1. Get Groq API key from https://console.groq.com
2. Get Gemini API key from https://makersuite.google.com/app/apikey
3. Add to `.env`

## Discord Bot Setup

1. Create Discord application
2. Create bot user
3. Get bot token
4. Enable required intents
5. Add to `.env`

## Telegram Bot Setup

1. Create bot via @BotFather
2. Get bot token
3. Set webhook URL
4. Add to `.env`

## Gmail Setup

1. Create Google Cloud project
2. Enable Gmail API
3. Create OAuth credentials
4. Download credentials JSON
5. Add path to `.env`

## GitHub Setup

1. Create GitHub personal access token
2. Configure webhook in repository settings
3. Add webhook secret to `.env`

## Monitoring

- Health check: `GET /health`
- Readiness check: `GET /health/ready`
- Liveness check: `GET /health/live`

## Logging

Logs are stored in `logs/app.log` with structured JSON format.

## Security

- JWT authentication with Firebase
- Role-based access control (Admin, Moderator, User, Guest)
- Rate limiting
- Webhook signature verification
- Input sanitization
- CORS configuration

## License

Proprietary - All rights reserved

## Support

For issues and questions, contact the development team.
