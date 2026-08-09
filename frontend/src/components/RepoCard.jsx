import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import StatusBadge from "./StatusBadge";
import { deleteRepo } from "../api/repos";
import { timeAgo } from "../lib/format";

export default function RepoCard({ repo }) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  async function handleDelete(e) {
    e.stopPropagation();
    if (!confirm(`Delete "${repo.name}"? This removes its index permanently.`)) return;
    await deleteRepo(repo.id);
    queryClient.invalidateQueries({ queryKey: ["repos"] });
  }

  const clickable = repo.status === "ready";

  return (
    <div
      className="repo-card card"
      onClick={() => clickable && navigate(`/repo/${repo.id}`)}
      style={{ cursor: clickable ? "pointer" : "default" }}
    >
      <div className="repo-card-top">
        <span className="repo-card-name">{repo.name}</span>
        <StatusBadge status={repo.status} />
      </div>

      <div className="repo-card-url mono">{repo.git_url}</div>

      <div className="repo-card-bottom">
        <span className="repo-card-meta">
          {repo.status === "ready" && `${repo.chunk_count} chunks indexed`}
          {repo.status === "processing" && <span className="pulse">cloning & embedding…</span>}
          {repo.status === "failed" && (
            <span className="error-text">{repo.error_message || "ingestion failed"}</span>
          )}
        </span>
        <span className="repo-card-time">{timeAgo(repo.created_at)}</span>
      </div>

      <button className="repo-card-delete" onClick={handleDelete} aria-label="Delete repo">
        ×
      </button>
    </div>
  );
}
