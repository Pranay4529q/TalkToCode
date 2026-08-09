import uuid

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from database import get_db
from auth.models import User
from core.security import get_current_user
from core.exceptions import RepoNotFoundError

from repos.models import Repo
from repos.schemas import RepoIngestRequest, RepoOut, RepoStatusOut
from repos.cloner import clone_repo, collect_python_files, cleanup_repo
from repos.chunker import chunk_repo
from repos.embedder import embed_texts
from vectorstore.pinecone_client import upsert_vectors, delete_namespace

router = APIRouter(prefix="/repos", tags=["repos"])


def run_ingestion_pipeline(repo_id: str, git_url: str, namespace: str):
    """
    Background task: clone -> ast-chunk -> embed (free local model) -> upsert to Pinecone.
    Runs after the response is already sent back to the client.
    Uses its own DB session since it runs outside the request lifecycle.
    """
    from database import SessionLocal

    db = SessionLocal()
    repo_path = None
    try:
        repo = db.query(Repo).filter(Repo.id == repo_id).first()

        repo_path = clone_repo(git_url, repo_id)
        py_files = collect_python_files(repo_path)
        chunks = chunk_repo(py_files, repo_path)

        if not chunks:
            repo.status = "failed"
            repo.error_message = "No Python files/chunks found in repo"
            db.commit()
            return

        texts = [c.text for c in chunks]
        vectors = embed_texts(texts)

        pinecone_vectors = []
        for chunk, vector in zip(chunks, vectors):
            pinecone_vectors.append(
                {
                    "id": str(uuid.uuid4()),
                    "values": vector,
                    "metadata": {
                        "file_path": chunk.file_path,
                        "chunk_type": chunk.chunk_type,
                        "name": chunk.name,
                        "start_line": chunk.start_line,
                        "end_line": chunk.end_line,
                        "text": chunk.text[:2000],  # cap stored text size
                        "repo_url": git_url,
                    },
                }
            )

        upsert_vectors(namespace, pinecone_vectors)

        repo.status = "ready"
        repo.chunk_count = len(chunks)
        db.commit()

    except Exception as e:
        repo = db.query(Repo).filter(Repo.id == repo_id).first()
        if repo:
            repo.status = "failed"
            repo.error_message = str(e)[:500]
            db.commit()
    finally:
        if repo_path:
            cleanup_repo(repo_path)
        db.close()


@router.post("/ingest", response_model=RepoOut)
def ingest_repo(
    payload: RepoIngestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo_id = str(uuid.uuid4())
    namespace = f"{current_user.id}_{repo_id}"
    name = str(payload.git_url).rstrip("/").split("/")[-1].replace(".git", "")

    repo = Repo(
        id=repo_id,
        user_id=current_user.id,
        git_url=str(payload.git_url),
        name=name,
        namespace=namespace,
        status="processing",
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)

    background_tasks.add_task(run_ingestion_pipeline, repo_id, str(payload.git_url), namespace)

    return repo


@router.get("", response_model=list[RepoOut])
def list_repos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Repo).filter(Repo.user_id == current_user.id).order_by(Repo.created_at.desc()).all()


@router.get("/{repo_id}/status", response_model=RepoStatusOut)
def get_repo_status(repo_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = db.query(Repo).filter(Repo.id == repo_id, Repo.user_id == current_user.id).first()
    if not repo:
        raise RepoNotFoundError()
    return repo


@router.delete("/{repo_id}", status_code=204)
def delete_repo(repo_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = db.query(Repo).filter(Repo.id == repo_id, Repo.user_id == current_user.id).first()
    if not repo:
        raise RepoNotFoundError()

    delete_namespace(repo.namespace)
    db.delete(repo)
    db.commit()
