from datetime import datetime
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None  # None -> start a new LangGraph thread


class Source(BaseModel):
    file_path: str
    chunk_type: str
    name: str
    start_line: int
    end_line: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    thread_id: str
    sources: list[Source]


class ThreadOut(BaseModel):
    id: str
    repo_id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ThreadHistoryOut(BaseModel):
    thread_id: str
    messages: list[MessageOut]
