from langchain_core.messages import HumanMessage, AIMessage

from repos.embedder import embed_query
from vectorstore.pinecone_client import query_vectors

TOP_K = 5


def retrieve_node(state: dict) -> dict:
    """
    RAG retrieval step.
    Takes the latest human message, embeds it (free local model), and does a
    similarity search against this repo's Pinecone namespace.
    """
    last_message = state["messages"][-1]
    query_text = last_message.content

    query_vector = embed_query(query_text)
    matches = query_vectors(namespace=state["namespace"], query_vector=query_vector, top_k=TOP_K)

    return {"retrieved_chunks": matches}


def generate_node(state: dict) -> dict:
    """
    Generation step.
    NOTE: LLM call is intentionally a stub for now (per project scope -
    focus is on RAG retrieval + Pinecone + LangGraph checkpointing first).
    Swap `call_llm_stub` for a real model call (OpenAI/Anthropic/local HF)
    once the retrieval pipeline is validated.
    """
    chunks = state.get("retrieved_chunks", [])
    question = state["messages"][-1].content

    context = "\n\n---\n\n".join(
        f"File: {c['metadata']['file_path']} "
        f"({c['metadata']['chunk_type']} `{c['metadata']['name']}`, "
        f"lines {c['metadata']['start_line']}-{c['metadata']['end_line']})\n"
        f"{c['metadata']['text']}"
        for c in chunks
    )

    answer = call_llm_stub(question, context)

    return {"messages": [AIMessage(content=answer)]}


def call_llm_stub(question: str, context: str) -> str:
    """
    Placeholder for the actual LLM call. Replace this function body with a
    real API call, e.g.:

        response = anthropic_client.messages.create(
            model="claude-...",
            messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
        )
        return response.content[0].text

    For now it just echoes back what context was retrieved, so you can
    verify the RAG pipeline (Pinecone search + metadata) is working end to end.
    """
    if not context:
        return "I couldn't find any relevant code for that question in this repo."

    return (
        f"[STUB RESPONSE - plug in a real LLM here]\n\n"
        f"Question: {question}\n\n"
        f"Retrieved context that would be sent to the LLM:\n\n{context}"
    )
