import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { listRepos } from "../api/repos";
import RepoCard from "../components/RepoCard";
import AddRepoModal from "../components/AddRepoModal";
import { useAuthStore } from "../store/authStore";
import "./Dashboard.css";

export default function Dashboard() {
  const [showModal, setShowModal] = useState(false);
  const logout = useAuthStore((s) => s.logout);
  const queryClient = useQueryClient();

  const { data: repos = [], isLoading } = useQuery({
    queryKey: ["repos"],
    queryFn: listRepos,
    // Poll while any repo is still processing, so status flips to ready/failed live
    refetchInterval: (query) => {
      const hasProcessing = query.state.data?.some((r) => r.status === "processing");
      return hasProcessing ? 3000 : false;
    },
  });

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Your repos</h1>
          <p className="dashboard-sub">Chunked, embedded, and searchable — pick one to start chatting.</p>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn btn-ghost" onClick={logout}>
            Log out
          </button>
          <button className="btn" onClick={() => setShowModal(true)}>
            + Add repo
          </button>
        </div>
      </div>

      {isLoading && <p className="mono" style={{ color: "var(--text-muted)" }}>loading…</p>}

      {!isLoading && repos.length === 0 && (
        <div className="empty-state">
          <p>No repos indexed yet. Add a public Python repo to get started.</p>
        </div>
      )}

      <div className="repo-grid">
        {repos.map((repo) => (
          <RepoCard key={repo.id} repo={repo} />
        ))}
      </div>

      {showModal && (
        <AddRepoModal
          onClose={() => {
            setShowModal(false);
            queryClient.invalidateQueries({ queryKey: ["repos"] });
          }}
        />
      )}
    </div>
  );
}
