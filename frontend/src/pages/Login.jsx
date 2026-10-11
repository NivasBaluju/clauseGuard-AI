import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ShieldCheck, Lock, Mail, ArrowRight, AlertCircle, Eye, EyeOff } from "lucide-react";

import { api } from "../api/client";

export function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password) {
      setError("Please fill in both email and password.");
      return;
    }

    setSubmitting(true);
    try {
      const data = await api.login(email.trim().toLowerCase(), password);

      if (data.token) {
        try {
          localStorage.setItem("cg_token", data.token);
        } catch (e) {}
      }

      login(data.user);
      navigate("/documents", { replace: true });
    } catch (err) {
      setError(err.message || "Failed to sign in. Please verify your credentials.");
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
        background: "#ffffff",
        color: "#000000",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "420px",
          padding: "40px",
          background: "#ffffff",
          border: "1px solid #e5e5e5",
          borderRadius: "12px",
          boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
        }}
      >
        <div style={{ display: "flex", justifyContent: "center", marginBottom: "16px" }}>
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "10px",
              background: "#f4f4f5",
              border: "1px solid #e4e4e7",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#000000",
            }}
          >
            <ShieldCheck size={26} />
          </div>
        </div>

        <h1 style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "8px", textAlign: "center", color: "#000000" }}>
          Sign In
        </h1>
        <p style={{ fontSize: "13px", color: "#71717a", textAlign: "center", marginBottom: "28px" }}>
          Enter your credentials to access your ClauseGuard workspace
        </p>

        {error && (
          <div
            style={{
              padding: "10px 14px",
              background: "#fef2f2",
              border: "1px solid #fecaca",
              borderRadius: "6px",
              color: "#b91c1c",
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

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#3f3f46", fontWeight: 500 }}>
              Email Address
            </label>
            <input
              type="email"
              required
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@company.com"
              style={{
                width: "100%",
                padding: "12px 14px",
                borderRadius: "6px",
                border: "1px solid #d4d4d8",
                background: "#f9fafb",
                color: "#000000",
                fontSize: "14px",
                boxSizing: "border-box",
                outline: "none",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", fontSize: "13px", marginBottom: "6px", color: "#3f3f46", fontWeight: 500 }}>
              Password
            </label>
            <div style={{ position: "relative" }}>
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                style={{
                  width: "100%",
                  padding: "12px 42px 12px 14px",
                  borderRadius: "6px",
                  border: "1px solid #d4d4d8",
                  background: "#f9fafb",
                  color: "#000000",
                  fontSize: "14px",
                  boxSizing: "border-box",
                  outline: "none",
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "12px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  background: "transparent",
                  border: "none",
                  color: "#71717a",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                }}
                title={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "12px",
              borderRadius: "6px",
              border: "1px solid #000000",
              background: submitting ? "#e4e4e7" : "#000000",
              color: submitting ? "#a1a1aa" : "#ffffff",
              fontWeight: 600,
              fontSize: "15px",
              cursor: submitting ? "not-allowed" : "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "8px",
              transition: "all 0.15s ease",
            }}
          >
            {submitting ? "Signing in…" : "Sign In"}
            {!submitting && <ArrowRight size={16} />}
          </button>
        </form>

        <p style={{ marginTop: "24px", textAlign: "center", fontSize: "13px", color: "#71717a" }}>
          Don't have an account?{" "}
          <Link to="/register" style={{ color: "#000000", textDecoration: "underline", fontWeight: 600 }}>
            Create Account
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
