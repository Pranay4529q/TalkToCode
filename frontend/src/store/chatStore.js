import { create } from "zustand";

export const useChatStore = create((set, get) => ({
  activeThreadId: null,
  messages: [], // [{ role: "user"|"assistant", content, sources? }]
  isSending: false,

  setActiveThread: (threadId) => set({ activeThreadId: threadId }),

  loadMessages: (messages) => set({ messages }),

  startNewThread: () => set({ activeThreadId: null, messages: [] }),

  appendUserMessage: (content) =>
    set({ messages: [...get().messages, { role: "user", content }] }),

  appendAssistantMessage: (content, sources) =>
    set({ messages: [...get().messages, { role: "assistant", content, sources }] }),

  setSending: (val) => set({ isSending: val }),
}));
