import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Auth ---
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-dev-secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # --- Database ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # --- Pinecone ---
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "git-rag-index")
    PINECONE_CLOUD: str = os.getenv("PINECONE_CLOUD", "aws")
    PINECONE_REGION: str = os.getenv("PINECONE_REGION", "us-east-1")

    # --- Embedding model (free, local, sentence-transformers) ---
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    EMBEDDING_DIM: int = 384  # matches all-MiniLM-L6-v2

    # --- Repo storage ---
    REPOS_CLONE_DIR: str = os.getenv("REPOS_CLONE_DIR", "./cloned_repos")

    # --- LangGraph checkpointing ---
    CHECKPOINT_DB_PATH: str = os.getenv("CHECKPOINT_DB_PATH", "./checkpoints.sqlite")


settings = Settings()
