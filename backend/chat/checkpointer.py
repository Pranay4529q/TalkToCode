import sqlite3
from functools import lru_cache

from langgraph.checkpoint.sqlite import SqliteSaver

from config import settings


@lru_cache(maxsize=1)
def get_checkpointer() -> SqliteSaver:
    """
    Single shared SqliteSaver connection for the whole app.
    This is what makes `thread_id` resumable: LangGraph automatically
    loads/saves the full graph state (messages, retrieved context, etc.)
    under that key on every invoke.

    Swap for PostgresSaver later when scaling beyond a single instance.
    """
    conn = sqlite3.connect(settings.CHECKPOINT_DB_PATH, check_same_thread=False)
    return SqliteSaver(conn)
