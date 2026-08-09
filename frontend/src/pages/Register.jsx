import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { registerUser } from "../api/auth";
import "./Auth.css";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const mutation = useMutation({
    mutationFn: registerUser,
    onSuccess: () => navigate("/login"),
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
        <p className="auth-tagline">Create an account to start indexing repos.</p>

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
              minLength={8}
              required
            />
          </div>

          {mutation.isError && (
            <p className="error-text">{mutation.error?.response?.data?.detail || "Registration failed"}</p>
          )}

          <button className="btn auth-submit" type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Creating…" : "Create account"}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
