import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { getRepoStatus, listRepos } from "../api/repos";
import { sendMessage } from "../api/chat";
import { useChatStore } from "../store/chatStore";

import ThreadSidebar from "../components/ThreadSidebar";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import StatusBadge from "../components/StatusBadge";
import "./ChatWorkspace.css";

export default function ChatWorkspace() {
  const { repoId } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: repo } = useQuery({
    queryKey: ["repo-status", repoId],
    queryFn: () => getRepoStatus(repoId),
  });

  // Reuses the dashboard's cached repo list (falls back to a fetch if visited directly)
  const { data: repos = [] } = useQuery({ queryKey: ["repos"], queryFn: listRepos });
  const repoName = repos.find((r) => r.id === repoId)?.name || repoId;

  const activeThreadId = useChatStore((s) => s.activeThreadId);
  const messages = useChatStore((s) => s.messages);
  const isSending = useChatStore((s) => s.isSending);
  const setActiveThread = useChatStore((s) => s.setActiveThread);
  const appendUserMessage = useChatStore((s) => s.appendUserMessage);
  const appendAssistantMessage = useChatStore((s) => s.appendAssistantMessage);
  const setSending = useChatStore((s) => s.setSending);
  const startNewThread = useChatStore((s) => s.startNewThread);

  // reset chat state when switching repos
  useEffect(() => {
    startNewThread();
  }, [repoId]);

  const mutation = useMutation({
    mutationFn: (message) => sendMessage(repoId, { message, threadId: activeThreadId }),
    onMutate: (message) => {
      appendUserMessage(message);
      setSending(true);
    },
    onSuccess: (data) => {
      setActiveThread(data.thread_id);
      appendAssistantMessage(data.answer, data.sources);
      queryClient.invalidateQueries({ queryKey: ["threads", repoId] });
    },
    onSettled: () => setSending(false),
  });

  if (!repo) return null;

  if (repo.status !== "ready") {
    return (
      <div className="workspace">
        <div className="repo-not-ready">
          {repo.status === "processing" ? "Still indexing this repo…" : "Ingestion failed for this repo."}
        </div>
      </div>
    );
  }

  return (
    <div className="workspace">
      <ThreadSidebar repoId={repoId} />

      <div className="chat-pane">
        <div className="chat-header">
          <button className="chat-header-back btn-ghost btn" onClick={() => navigate("/dashboard")}>
            ← repos
          </button>
          <span className="chat-header-name">{repoName}</span>
          <StatusBadge status={repo.status} />
        </div>

        <MessageList messages={messages} isSending={isSending} />

        <MessageInput onSend={(msg) => mutation.mutate(msg)} disabled={isSending} />
      </div>
    </div>
  );
}
