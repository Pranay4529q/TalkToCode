import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ingestRepo } from "../api/repos";

export default function AddRepoModal({ onClose }) {
  const [gitUrl, setGitUrl] = useState("");
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: ingestRepo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["repos"] });
      onClose();
    },
  });

  function handleSubmit(e) {
    e.preventDefault();
    if (!gitUrl.trim()) return;
    mutation.mutate(gitUrl.trim());
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal card" onClick={(e) => e.stopPropagation()}>
        <h3 className="modal-title">Add a repository</h3>
        <p className="modal-sub">
          We'll clone it, chunk every Python file by function/class, and index it for chat.
        </p>

        <form onSubmit={handleSubmit}>
          <input
            className="input mono"
            placeholder="https://github.com/user/repo.git"
            value={gitUrl}
            onChange={(e) => setGitUrl(e.target.value)}
            autoFocus
          />

          {mutation.isError && (
            <p className="error-text" style={{ marginTop: 8 }}>
              {mutation.error?.response?.data?.detail || "Something went wrong"}
            </p>
          )}

          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn" disabled={mutation.isPending}>
              {mutation.isPending ? "Starting…" : "Index repo"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
