import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer

from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Repo(Base):
    __tablename__ = "repos"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    git_url = Column(String, nullable=False)
    name = Column(String, nullable=False)          # derived from git_url
    namespace = Column(String, nullable=False)      # pinecone namespace = f"{user_id}_{repo_id}"

    status = Column(String, default="processing")   # processing | ready | failed
    error_message = Column(String, nullable=True)

    chunk_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
