import ast
from dataclasses import dataclass


@dataclass
class CodeChunk:
    text: str
    file_path: str
    chunk_type: str   # "function" | "class" | "module"
    name: str
    start_line: int
    end_line: int


def chunk_python_file(file_path: str, repo_root: str) -> list[CodeChunk]:
    """
    Parses a .py file with `ast` and extracts top-level functions/classes as
    individual chunks (semantic units, not arbitrary line splits).
    Falls back to whole-file chunk if parsing fails or file has no top-level defs.
    """
    rel_path = file_path.replace(repo_root, "").lstrip("/\\")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return []

    lines = source.splitlines()
    chunks: list[CodeChunk] = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = getattr(node, "end_lineno", node.lineno)
            snippet = "\n".join(lines[start:end])

            chunk_type = "class" if isinstance(node, ast.ClassDef) else "function"
            chunks.append(
                CodeChunk(
                    text=snippet,
                    file_path=rel_path,
                    chunk_type=chunk_type,
                    name=node.name,
                    start_line=start + 1,
                    end_line=end,
                )
            )

    # Fallback: no functions/classes found (e.g. script-style file) -> whole file as one chunk
    if not chunks and lines:
        chunks.append(
            CodeChunk(
                text=source,
                file_path=rel_path,
                chunk_type="module",
                name=rel_path,
                start_line=1,
                end_line=len(lines),
            )
        )

    return chunks


def chunk_repo(py_files: list[str], repo_root: str) -> list[CodeChunk]:
    all_chunks: list[CodeChunk] = []
    for file_path in py_files:
        all_chunks.extend(chunk_python_file(file_path, repo_root))
    return all_chunks
