# 📄 Technical Specification (TZ)

## Project: radius-ai-service

---

# 1. 📌 Overview

**Service Name:** `radius-ai-service`
**Architecture:** Microservice
**Framework:** FastAPI (Python 3.11+)
**Purpose:**
CRM tizimi uchun AI-powered funksiyalarni taqdim etish (OpenAI orqali)

---

# 2. 🎯 Goals

Service quyidagi 4 ta asosiy feature’ni ta’minlashi kerak:

1. Follow-up email generation
2. Lead scoring (AI-based)
3. Meeting notes summarization
4. CRM chat assistant (Q&A)

---

# 3. 🏗️ Architecture

## 3.1 High-level flow

Frontend → API Gateway → AI Service → (User, Order, CRM services)

---

## 3.2 Responsibilities

AI Service:

* OpenAI API bilan ishlash
* Prompt generation
* Context aggregation
* Response formatting
* Caching (optional but recommended)

---

# 4. 📦 Tech Stack

* FastAPI
* Pydantic v2
* httpx (async requests)
* OpenAI API
* Redis (caching)
* PostgreSQL (optional logs)
* Docker

---

# 5. 📁 Project Structure

```
radius-ai-service/
│
├── app/
│   ├── api/
│   │   ├── email.py
│   │   ├── lead.py
│   │   ├── summary.py
│   │   ├── chat.py
│   │
│   ├── services/
│   │   ├── openai_client.py
│   │   ├── prompt_builder.py
│   │   ├── context_builder.py
│   │   ├── cache_service.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │
│   └── main.py
│
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# 6. 🔐 Environment Variables

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
REDIS_URL=
USER_SERVICE_URL=
ORDER_SERVICE_URL=
CRM_SERVICE_URL=
TIMEOUT=10
```

---

# 7. 🔌 External Integrations

## 7.1 OpenAI

* Chat Completion API
* Streaming support (optional)

## 7.2 Internal Services

* user-service
* order-service
* crm-service (agar mavjud bo‘lsa)

---

# 8. 🧠 Core Features

---

## 8.1 Follow-up Email Generator

### Endpoint

```
POST /ai/email/generate
```

### Input

```json
{
  "customer_id": "string",
  "tone": "formal | friendly | sales",
  "language": "en | ru | uz"
}
```

### Process

1. Customer data fetch
2. Interaction history fetch
3. Prompt build
4. OpenAI call

### Output

```json
{
  "subject": "string",
  "body": "string"
}
```

---

## 8.2 Lead Scoring

### Endpoint

```
POST /ai/lead/score
```

### Input

```json
{
  "customer_id": "string"
}
```

### Output

```json
{
  "score": 0-100,
  "priority": "low | medium | high",
  "reason": "string"
}
```

---

## 8.3 Meeting Notes Summarizer

### Endpoint

```
POST /ai/summary
```

### Input

```json
{
  "text": "raw meeting notes"
}
```

### Output

```json
{
  "summary": "string",
  "action_items": ["string"],
  "key_points": ["string"]
}
```

---

## 8.4 CRM Chat Assistant

### Endpoint

```
POST /ai/chat
```

### Input

```json
{
  "customer_id": "string",
  "question": "string"
}
```

### Output

```json
{
  "answer": "string"
}
```

---

# 9. 🧩 Internal Services

---

## 9.1 OpenAI Client

Responsibilities:

* API call
* Retry logic
* Error handling
* Timeout

---

## 9.2 Prompt Builder

Functions:

* build_email_prompt()
* build_lead_prompt()
* build_summary_prompt()
* build_chat_prompt()

---

## 9.3 Context Builder

Responsibilities:

* Customer data aggregation
* Order history
* Activity logs

---

## 9.4 Cache Service

* Redis based
* Key format:

```
ai:{feature}:{hash}
```

---

# 10. ⚡ Performance

* Async endpoints
* Timeout: ≤10s
* Caching enabled
* Max token limit enforced

---

# 11. 🛡️ Error Handling

Standard response:

```json
{
  "error": true,
  "message": "string"
}
```

Cases:

* OpenAI timeout
* Invalid input
* Service unavailable

---

# 12. 📊 Logging

Log:

* request_id
* endpoint
* response_time
* token_usage

---

# 13. 🔒 Security

* API Gateway orqali auth
* Rate limiting (optional)
* Input sanitization

---

# 14. 🧪 Testing

* Unit tests (prompt + services)
* Integration tests (API endpoints)

---

# 15. 🐳 Deployment

* Docker container
* Kubernetes ready
* Health check endpoint:

```
GET /health
```

---

# 16. 🚀 Future Extensions

* Recommendation system
* Voice assistant
* AI analytics dashboard

---

# 17. 📌 Acceptance Criteria

* All 4 endpoints working
* OpenAI integration stable
* < 10s response time
* Clean architecture
* Fully documented API

---

# 18. 📚 Notes

* Use structured prompts (JSON output)
* Avoid hallucinations via system instructions
* Prefer cheaper models if possible
* Keep prompts reusable

---
