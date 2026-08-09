import { useQuery } from "@tanstack/react-query";
import { listThreads, getThreadHistory } from "../api/chat";
import { useChatStore } from "../store/chatStore";
import { timeAgo } from "../lib/format";

export default function ThreadSidebar({ repoId }) {
  const { data: threads = [] } = useQuery({
    queryKey: ["threads", repoId],
    queryFn: () => listThreads(repoId),
  });

  const activeThreadId = useChatStore((s) => s.activeThreadId);
  const setActiveThread = useChatStore((s) => s.setActiveThread);
  const loadMessages = useChatStore((s) => s.loadMessages);
  const startNewThread = useChatStore((s) => s.startNewThread);

  async function openThread(threadId) {
    setActiveThread(threadId);
    const history = await getThreadHistory(threadId);
    loadMessages(history.messages);
  }

  return (
    <aside className="thread-sidebar">
      <button className="btn new-chat-btn" onClick={startNewThread}>
        + New chat
      </button>

      <div className="thread-graph">
        {threads.length === 0 && <p className="thread-empty">No conversations yet</p>}

        {threads.map((t) => (
          <button
            key={t.id}
            className={`thread-node ${activeThreadId === t.id ? "active" : ""}`}
            onClick={() => openThread(t.id)}
          >
            <span className="thread-dot" />
            <span className="thread-info">
              <span className="thread-title">{t.title}</span>
              <span className="thread-time mono">{timeAgo(t.created_at)}</span>
            </span>
          </button>
        ))}
      </div>
    </aside>
  );
}
