import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from database import get_db
from auth.models import User
from core.security import get_current_user
from core.exceptions import RepoNotFoundError, RepoNotReadyError

from repos.models import Repo
from chat.models import ChatThread
from chat.schemas import ChatRequest, ChatResponse, Source, ThreadOut, ThreadHistoryOut, MessageOut
from chat.graph import get_graph

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{repo_id}/message", response_model=ChatResponse)
def send_message(
    repo_id: str,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = db.query(Repo).filter(Repo.id == repo_id, Repo.user_id == current_user.id).first()
    if not repo:
        raise RepoNotFoundError()
    if repo.status != "ready":
        raise RepoNotReadyError(repo.status)

    # New conversation vs resuming an existing one
    thread_id = payload.thread_id
    if not thread_id:
        thread_id = str(uuid.uuid4())
        db.add(
            ChatThread(
                id=thread_id,
                user_id=current_user.id,
                repo_id=repo_id,
                title=payload.message[:60],
            )
        )
        db.commit()

    graph = get_graph()
    config = {"configurable": {"thread_id": thread_id}}

    # We only need to pass the NEW human message + namespace.
    # LangGraph pulls prior `messages` from the checkpoint automatically via thread_id.
    result = graph.invoke(
        {
            "messages": [HumanMessage(content=payload.message)],
            "namespace": repo.namespace,
        },
        config=config,
    )

    ai_message = result["messages"][-1]
    sources = [
        Source(
            file_path=c["metadata"]["file_path"],
            chunk_type=c["metadata"]["chunk_type"],
            name=c["metadata"]["name"],
            start_line=c["metadata"]["start_line"],
            end_line=c["metadata"]["end_line"],
            score=c["score"],
        )
        for c in result.get("retrieved_chunks", [])
    ]

    return ChatResponse(answer=ai_message.content, thread_id=thread_id, sources=sources)


@router.get("/threads", response_model=list[ThreadOut])
def list_threads(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(ChatThread)
        .filter(ChatThread.user_id == current_user.id, ChatThread.repo_id == repo_id)
        .order_by(ChatThread.created_at.desc())
        .all()
    )


@router.get("/threads/{thread_id}/history", response_model=ThreadHistoryOut)
def get_thread_history(
    thread_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    thread = db.query(ChatThread).filter(ChatThread.id == thread_id, ChatThread.user_id == current_user.id).first()
    if not thread:
        raise RepoNotFoundError()  # reused: generic 404

    graph = get_graph()
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)

    messages = []
    for m in snapshot.values.get("messages", []):
        role = "user" if isinstance(m, HumanMessage) else "assistant"
        messages.append(MessageOut(role=role, content=m.content))

    return ThreadHistoryOut(thread_id=thread_id, messages=messages)
