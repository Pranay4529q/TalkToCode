from datetime import datetime
from pydantic import BaseModel, HttpUrl


class RepoIngestRequest(BaseModel):
    git_url: HttpUrl


class RepoOut(BaseModel):
    id: str
    git_url: str
    name: str
    status: str
    error_message: str | None = None
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class RepoStatusOut(BaseModel):
    id: str
    status: str
    error_message: str | None = None
    chunk_count: int
