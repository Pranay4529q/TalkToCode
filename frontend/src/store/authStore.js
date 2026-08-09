import { create } from "zustand";

const STORAGE_KEY = "gitchat_token";

export const useAuthStore = create((set) => ({
  token: localStorage.getItem(STORAGE_KEY) || null,

  setToken: (token) => {
    localStorage.setItem(STORAGE_KEY, token);
    set({ token });
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEY);
    set({ token: null });
  },
}));
