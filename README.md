# SHL Conversational Assessment Recommendation API

## Overview

This project is an AI-powered conversational assistant that recommends SHL assessments based on hiring requirements. The assistant supports multi-turn conversations, asks clarifying questions when information is missing, recommends suitable assessments, refines recommendations as requirements change, and compares SHL assessments using catalog data.

The solution combines Retrieval-Augmented Generation (RAG) with Google's Gemini 2.5 Flash and semantic search using Sentence Transformers and FAISS.

---

## Features

- Conversational hiring assistant
- Multi-turn dialogue support
- Clarifying questions for incomplete requirements
- SHL assessment recommendation
- Assessment comparison
- Semantic search using FAISS
- Gemini-powered requirement extraction
- Grounded responses using SHL catalog
- REST API using FastAPI

---

## Tech Stack

- Python 3.10
- FastAPI
- Google Gemini 2.5 Flash
- Sentence Transformers (all-MiniLM-L6-v2)
- FAISS
- Pydantic
- NumPy

---

## Project Structure

```
shl-ai-agent/
│
├── app.py
├── requirements.txt
├── runtime.txt
│
├── data/
│   └── shl_catalog.json
│
├── models/
│   └── schemas.py
│
├── services/
│   ├── agent.py
│   ├── catalog.py
│   ├── comparator.py
│   ├── conversation_state.py
│   ├── embeddings.py
│   ├── llm.py
│   └── recommender.py
│
└── tests/
    ├── conversations/
    ├── run_eval.py
    ├── evaluate.py
    └── utils.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/bhumisingh0112-dev/shl-ai-agent-tool.git

cd shl-ai-agent-tool
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run the server

```bash
uvicorn app:app --reload
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status":"ok"
}
```

---

### Chat

```
POST /chat
```

Example Request

```json
{
  "messages":[
    {
      "role":"user",
      "content":"We are hiring a Java Backend Engineer with 5 years experience for selection."
    }
  ]
}
```

---

## Deployment

Public API

```
https://shl-ai-agent-tool-production.up.railway.app
```

Swagger

```
https://shl-ai-agent-tool-production.up.railway.app/docs
```

---

## Evaluation

The solution was evaluated using the provided SHL conversation datasets.

Evaluation focused on

- Retrieval quality
- Recommendation relevance
- Groundedness
- Multi-turn conversation handling
- Assessment comparison

---

## Future Improvements

- Hybrid BM25 + FAISS retrieval
- Embedding caching
- Streaming responses
- Better reranking
- Conversation memory optimization

---

## LLM Used

Google Gemini 2.5 Flash

---
