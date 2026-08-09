import os
import shutil
import subprocess
from pathlib import Path

from config import settings

IGNORED_DIRS = {".git", "venv", ".venv", "__pycache__", "node_modules", "env", "site-packages"}


def clone_repo(git_url: str, repo_id: str) -> str:
    """
    Shallow-clones the given git repo into a unique local dir.
    Returns the local path. Raises RuntimeError on failure.
    """
    dest = os.path.join(settings.REPOS_CLONE_DIR, repo_id)
    os.makedirs(settings.REPOS_CLONE_DIR, exist_ok=True)

    if os.path.exists(dest):
        shutil.rmtree(dest)

    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", str(git_url), dest],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git clone failed: {e.stderr.strip()}")
    except subprocess.TimeoutExpired:
        raise RuntimeError("git clone timed out")

    return dest


def collect_python_files(repo_path: str) -> list[str]:
    """Walks the cloned repo and returns paths to all .py files, skipping noise dirs."""
    py_files = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    return py_files


def cleanup_repo(repo_path: str):
    """Delete cloned repo from disk after embedding is done (we don't need source on disk anymore)."""
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, ignore_errors=True)
