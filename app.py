from fastapi import FastAPI
from models.schemas import ChatRequest, ChatResponse
from services.agent import handle_chat
from services.embeddings import catalog


app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Conversational AI agent for recommending SHL assessments.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommendation API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/version")
def version():
    return {
        "version": "1.0.0",
        "llm": "Gemini 2.5 Flash",
        "retrieval": "FAISS + all-MiniLM-L6-v2"
    }


@app.get("/metrics")
def metrics():
    return {
        "catalog_size": len(catalog),
        "embedding_model": "all-MiniLM-L6-v2",
        "retrieval": "FAISS",
        "llm": "Gemini 2.5 Flash"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return handle_chat(request.messages)