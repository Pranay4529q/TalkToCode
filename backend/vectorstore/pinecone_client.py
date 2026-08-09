from pinecone import Pinecone, ServerlessSpec

from config import settings

_pc = Pinecone(api_key=settings.PINECONE_API_KEY)


def get_index():
    """Creates the index once (if missing) and returns a handle to it."""
    existing = [i.name for i in _pc.list_indexes()]
    if settings.PINECONE_INDEX_NAME not in existing:
        _pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=settings.EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=settings.PINECONE_CLOUD, region=settings.PINECONE_REGION),
        )
    return _pc.Index(settings.PINECONE_INDEX_NAME)


def upsert_vectors(namespace: str, vectors: list[dict]):
    """
    vectors: [{"id": str, "values": [float,...], "metadata": {...}}, ...]
    Upserted in batches of 100 (Pinecone recommended batch size).
    """
    index = get_index()
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)


def query_vectors(namespace: str, query_vector: list[float], top_k: int = 5) -> list[dict]:
    """Returns list of {id, score, metadata} for the top_k most similar chunks."""
    index = get_index()
    result = index.query(
        namespace=namespace,
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
    )
    return [
        {"id": match.id, "score": match.score, "metadata": match.metadata}
        for match in result.matches
    ]


def delete_namespace(namespace: str):
    """Wipes all vectors for a repo - used when a repo is deleted."""
    index = get_index()
    try:
        index.delete(namespace=namespace, delete_all=True)
    except Exception:
        # namespace may not exist yet (e.g. ingestion failed before any upsert) - safe to ignore
        pass
