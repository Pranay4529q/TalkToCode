import client from "./client";

export async function sendMessage(repoId, { message, threadId }) {
  const { data } = await client.post(`/chat/${repoId}/message`, {
    message,
    thread_id: threadId ?? null,
  });
  return data; // { answer, thread_id, sources }
}

export async function listThreads(repoId) {
  const { data } = await client.get("/chat/threads", { params: { repo_id: repoId } });
  return data;
}

export async function getThreadHistory(threadId) {
  const { data } = await client.get(`/chat/threads/${threadId}/history`);
  return data; // { thread_id, messages }
}
