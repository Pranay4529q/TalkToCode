import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey

from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class ChatThread(Base):
    """
    Lightweight metadata table so we can list a user's chat threads per repo.
    The actual conversation state/messages live in LangGraph's checkpointer
    (chat/checkpointer.py), keyed by this same thread_id.
    just the temp changes that we need to make the chat threads work in the backend. The actual conversation state/messages live in LangGraph's checkpointer (chat/checkpointer.py), keyed by this same thread_id.
    """
    __tablename__ = "chat_threads"

    id = Column(String, primary_key=True, default=gen_uuid)  # == LangGraph thread_id
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    repo_id = Column(String, ForeignKey("repos.id"), nullable=False, index=True)

    title = Column(String, default="New chat")
    created_at = Column(DateTime, default=datetime.utcnow)
