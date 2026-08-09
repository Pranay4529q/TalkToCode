from functools import lru_cache

from sentence_transformers import SentenceTransformer

from config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Loaded once and cached - avoids reloading the model on every call."""
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Free, local embeddings. Returns a list of vectors (each len == settings.EMBEDDING_DIM)."""
    model = get_embedding_model()
    vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
