from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    tool_calls_made: int = 0
    sources: list[str] = []


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    chromadb_connected: bool