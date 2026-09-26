import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ShieldCheck, ArrowRight, AlertCircle } from "lucide-react";

export function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) return setError("Please enter your full name");
    if (!email.trim()) return setError("Please enter your email address");
    if (password.length < 8) return setError("Password must be at least 8 characters");
    if (password !== confirmPassword) return setError("Passwords do not match");

    setSubmitting(true);
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim().toLowerCase(),
          password,
          confirmPassword,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Registration failed");

      login(data.user);
      navigate("/documents", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "80vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
        background: "#0a0d14",
        color: "#fff",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "440px",
          padding: "40px",
          background: "#131822",
          border: "1px solid #1f293d",
          borderRadius: "12px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.5)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "center", marginBottom: "16px" }}>
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "10px",
              background: "rgba(37, 99, 235, 0.15)",
              border: "1px solid #2563eb",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#60a5fa",
            }}
          >
            <ShieldCheck size={26} />
          </div>
        </div>

        <h1 style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "8px", textAlign: "center" }}>
          Create Account
        </h1>
        <p style={{ fontSize: "13px", color: "#94a3b8", textAlign: "center", marginBottom: "28px" }}>
          Register for full access to ClauseGuard AI workspace
        </p>

        {error && (
          <div
            style={{
              padding: "10px 14px",
              background: "rgba(239,68,68,0.15)",
              border: "1px solid #ef4444",
              borderRadius: "6px",
              color: "#fca5a5",
              fontSize: "13px",
              marginBottom: "20px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#cbd5e1" }}>
              Full Name
            </label>
            <input
              type="text"
              required
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Alex Johnson"
              style={{
                width: "100%",
                padding: "12px 14px",
                borderRadius: "6px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
                fontSize: "14px",
                boxSizing: "border-box",
                outline: "none",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#cbd5e1" }}>
              Corporate / Personal Email
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="alex@company.com"
              style={{
                width: "100%",
                padding: "12px 14px",
                borderRadius: "6px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
                fontSize: "14px",
                boxSizing: "border-box",
                outline: "none",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#cbd5e1" }}>
              Password (min 8 chars)
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              style={{
                width: "100%",
                padding: "12px 14px",
                borderRadius: "6px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
                fontSize: "14px",
                boxSizing: "border-box",
                outline: "none",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#cbd5e1" }}>
              Confirm Password
            </label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••••••"
              style={{
                width: "100%",
                padding: "12px 14px",
                borderRadius: "6px",
                border: "1px solid #334155",
                background: "#0f172a",
                color: "#fff",
                fontSize: "14px",
                boxSizing: "border-box",
                outline: "none",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "14px",
              borderRadius: "6px",
              border: "none",
              background: submitting ? "#475569" : "#2563eb",
              color: "#fff",
              fontWeight: 600,
              fontSize: "15px",
              cursor: submitting ? "not-allowed" : "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "8px",
              transition: "background 0.2s",
            }}
          >
            {submitting ? "Creating Account…" : "Register"}
            {!submitting && <ArrowRight size={16} />}
          </button>
        </form>

        <p style={{ marginTop: "24px", textAlign: "center", fontSize: "13px", color: "#94a3b8" }}>
          Already have an account?{" "}
          <Link to="/login" style={{ color: "#38bdf8", textDecoration: "none", fontWeight: 500 }}>
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
