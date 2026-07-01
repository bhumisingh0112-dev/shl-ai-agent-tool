from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str
    score: Optional[float] = None
    reason: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool