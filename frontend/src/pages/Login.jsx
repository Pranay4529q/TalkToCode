import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { loginUser } from "../api/auth";
import { useAuthStore } from "../store/authStore";
import "./Auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const setToken = useAuthStore((s) => s.setToken);

  const mutation = useMutation({
    mutationFn: loginUser,
    onSuccess: (data) => {
      setToken(data.access_token);
      navigate("/dashboard");
    },
  });

  function handleSubmit(e) {
    e.preventDefault();
    mutation.mutate({ email, password });
  }

  return (
    <div className="auth-page">
      <div className="auth-card card">
        <div className="auth-logo">
          git<span>chat</span>
        </div>
        <p className="auth-tagline">Sign in to keep talking to your repos.</p>

        <form onSubmit={handleSubmit}>
          <div className="auth-field">
            <label>Email</label>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="auth-field">
            <label>Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {mutation.isError && (
            <p className="error-text">{mutation.error?.response?.data?.detail || "Login failed"}</p>
          )}

          <button className="btn auth-submit" type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="auth-switch">
          No account? <Link to="/register">Create one</Link>
        </p>
      </div>
    </div>
  );
}
