from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from auth.routes import router as auth_router
from repos.routes import router as repos_router
from chat.routes import router as chat_router

app = FastAPI(title="Git-RAG-Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(repos_router)
app.include_router(chat_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
