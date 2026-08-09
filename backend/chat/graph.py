from typing import TypedDict, Annotated
from functools import lru_cache

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from chat.nodes import retrieve_node, generate_node
from chat.checkpointer import get_checkpointer


class GraphState(TypedDict):
    messages: Annotated[list, add_messages]  # conversation history, auto-appended + checkpointed
    namespace: str                            # which repo's Pinecone namespace to search
    retrieved_chunks: list[dict]              # last retrieval result (for building `sources` in the response)


@lru_cache(maxsize=1)
def get_graph():
    """
    Builds and compiles the RAG graph once:

        retrieve --> generate --> END

    Compiled with a checkpointer so that passing the same thread_id on a
    later call resumes the conversation (full message history reloaded
    automatically by LangGraph).
    """
    builder = StateGraph(GraphState)

    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)

    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    return builder.compile(checkpointer=get_checkpointer())
