# NimbusLLM Wrapper

NimbusLLM is a **production-style LLM gateway / wrapper** built with **FastAPI, SQLAlchemy, and PostgreSQL**. It provides a **single normalized API** for text generation across providers while logging every request for observability. This project is designed as **real backend infrastructure**, not a tutorial demo.

---

## Features
- Unified `/generate` API
- Provider abstraction layer (mock provider implemented)
- PostgreSQL-backed request logging
- FastAPI OpenAPI documentation
- Docker-based database setup
- Clean, extensible project structure

---

## Architecture
Client / Frontend  
→ FastAPI API (`nimbusllm_api`)  
→ Provider Factory (`get_provider`)  
→ LLM Provider (Mock / future OpenAI, Gemini, vLLM, Ollama)  
→ PostgreSQL (`nimbusllm_db`)

All `/generate` requests are logged with:
- request ID  
- provider and model  
- prompt and response  
- latency  
- token usage  
- status and error (if any)

---

## Project Structure
├─ app/
│  ├─ api/
│  │  ├─ routes_generate.py
│  │  └─ routes_health.py
│  ├─ core/
│  │  └─ auth.py
│  ├─ db/
│  │  ├─ deps.py
│  │  ├─ init_db.py
│  │  ├─ models.py
│  │  └─ session.py
│  ├─ providers/
│  │  ├─ base.py
│  │  ├─ factory.py
│  │  └─ mock.py
│  ├─ __init__.py
│  └─ main.py
├─ docker-compose.yml
├─ Dockerfile
├─ requirements.txt
└─ .env



---

## Requirements
- Python 3.12 (Conda recommended)
- Docker Desktop

---

## Environment Configuration
Create a `.env` file in the project root:

ENV=dev  
DATABASE_URL=postgresql+psycopg2://nimbus:nimbus@localhost:5433/nimbusllm  
OPENAI_API_KEY=  
GEMINI_API_KEY=

Port **5433** is intentionally used to avoid conflicts with local PostgreSQL services on Windows.

---

## Database Setup (Docker)
Start PostgreSQL:
- `docker compose up -d`

Reset database (removes data):
- `docker compose down -v`
- `docker compose up -d`

Verify database access:
- `docker exec -it nimbusllm_db psql -U nimbus -d nimbusllm`

---

## Running the API Locally
From the project root:
- `python -m uvicorn app.main:app --reload --env-file .\.env`

Access:
- Swagger UI: http://127.0.0.1:8000/docs
- Health endpoint: http://127.0.0.1:8000/health

---

## API Endpoints

### GET /health
Simple health check endpoint.  
Returns `"ok"` when the service is running.

### POST /generate
Unified text generation endpoint.

Request example:
- provider: `mock`
- model: `mock-1`
- messages: list of role/content pairs
- temperature and max_tokens supported

Response includes:
- request ID
- provider and model
- generated text
- token usage
- latency
- raw provider output (if any)

---

## Logging & Observability
Every `/generate` request is persisted to PostgreSQL with:
- request_id
- provider
- model
- prompt
- response_text
- latency_ms
- input_tokens
- output_tokens
- status (success / fail)
- error message (if applicable)

This enables debugging, benchmarking, and future analytics dashboards.

---

## Common Notes
- `/` returning 404 is expected (no root route defined)
- `/docs` is the primary interface for testing
- Database connection issues are usually related to port conflicts or stale Docker volumes

---

## Roadmap
- Add strict Pydantic schemas module
- Add real LLM providers (OpenAI, Gemini, vLLM, Ollama)
- Add API key authentication
- Add rate limiting
- Add Alembic migrations
- Add metrics and tracing

---

## License
MIT
