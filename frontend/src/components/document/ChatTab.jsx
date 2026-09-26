import React, { useState, useEffect, useRef } from "react";

export const ChatTab = ({ documentId }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const chatWindowRef = useRef(null);

  const suggestions = [
    "What are the key obligations and payment terms?",
    "What are the termination conditions?",
    "Are there any penalties, liabilities, or deadlines?",
    "What is the governing law or jurisdiction?",
  ];

  // 1. Load chat history on mount
  useEffect(() => {
    let isMounted = true;
    async function loadHistory() {
      try {
        const url = documentId
          ? `/api/chat/history?documentId=${documentId}`
          : "/api/chat/history";
        const res = await fetch(url, { credentials: "include" });
        if (res.ok) {
          const data = await res.json();
          if (isMounted) setMessages(data.messages || []);
        }
      } catch (err) {
        console.error("Failed to load chat history", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    loadHistory();
    return () => {
      isMounted = false;
    };
  }, [documentId]);

  // 2. Auto-scroll to bottom
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, sending]);

  // 3. Send message handler
  const handleSend = async (questionText) => {
    const q = (questionText || input).trim();
    if (!q || sending) return;

    setInput("");
    const userMsg = { id: `user-${Date.now()}`, role: "USER", content: q };
    setMessages((prev) => [...prev, userMsg]);
    setSending(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ question: q, documentId }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || "Server error");
      }

      const data = await res.json();
      const assistantMsg = {
        id: data.id || `assistant-${Date.now()}`,
        role: "ASSISTANT",
        content: data.answer,
        confidence: data.confidence,
        grounded: data.grounded,
        sources: data.sources || [],
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: "ASSISTANT",
          content: `⚠️ Error: ${err.message}`,
          grounded: false,
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loading) {
    return (
      <div style={{ padding: "32px", textAlign: "center", color: "#888" }}>
        Loading AI Chat Session…
      </div>
    );
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "650px",
        border: "1px solid #222",
        borderRadius: "12px",
        background: "#0f1117",
        color: "#fff",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "16px 20px",
          borderBottom: "1px solid #222",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "#161922",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600, fontSize: "15px" }}>
          <span style={{ height: "8px", width: "8px", borderRadius: "50%", background: "#22c55e" }} />
          Deciva AI Assistant
        </div>
        <span
          style={{
            fontSize: "11px",
            background: "rgba(255,255,255,0.06)",
            padding: "4px 8px",
            borderRadius: "4px",
            color: "#aaa",
          }}
        >
          Grounded Copilot
        </span>
      </div>

      {/* Suggested Questions */}
      <div
        style={{
          padding: "12px 16px",
          display: "flex",
          gap: "8px",
          overflowX: "auto",
          borderBottom: "1px solid #1a1e28",
        }}
      >
        {suggestions.map((s, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(s)}
            disabled={sending}
            style={{
              whiteSpace: "nowrap",
              padding: "6px 12px",
              borderRadius: "20px",
              border: "1px solid #2e3648",
              background: "#1a1f2c",
              color: "#cbd5e1",
              fontSize: "12px",
              cursor: sending ? "not-allowed" : "pointer",
            }}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Messages Scroll Area */}
      <div
        ref={chatWindowRef}
        style={{
          flex: 1,
          padding: "20px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
        }}
      >
        {messages.length === 0 ? (
          <div style={{ margin: "auto", textAlign: "center", color: "#64748b" }}>
            <div style={{ fontSize: "32px", marginBottom: "8px" }}>🤖</div>
            <div style={{ fontWeight: 600, color: "#e2e8f0" }}>How can I assist you today?</div>
            <div style={{ fontSize: "13px" }}>Ask any question or click a suggestion chip above.</div>
          </div>
        ) : (
          messages.map((m, idx) => {
            const isUser = m.role === "USER" || m.role === "user";
            return (
              <div
                key={m.id || idx}
                style={{
                  alignSelf: isUser ? "flex-end" : "flex-start",
                  maxWidth: "80%",
                  background: isUser ? "#2563eb" : "#1e2330",
                  color: "#fff",
                  borderRadius: isUser ? "16px 16px 2px 16px" : "16px 16px 16px 2px",
                  padding: "12px 16px",
                  fontSize: "14px",
                  lineHeight: "1.5",
                  boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
                }}
              >
                {!isUser && (
                  <div style={{ marginBottom: "6px", display: "flex", alignItems: "center", gap: "6px" }}>
                    <span
                      style={{
                        fontSize: "10px",
                        textTransform: "uppercase",
                        padding: "2px 6px",
                        borderRadius: "4px",
                        background: m.grounded ? "rgba(34,197,94,0.15)" : "rgba(234,179,8,0.15)",
                        color: m.grounded ? "#4ade80" : "#facc15",
                      }}
                    >
                      {m.grounded ? "✓ Grounded" : "Notice"}
                    </span>
                    {typeof m.confidence === "number" && (
                      <span style={{ fontSize: "11px", color: "#94a3b8" }}>
                        ({Math.round(m.confidence * 100)}% confidence)
                      </span>
                    )}
                  </div>
                )}
                <div>{m.content}</div>

                {/* Evidence Citations */}
                {!isUser && m.sources && m.sources.length > 0 && (
                  <div style={{ marginTop: "10px", paddingTop: "8px", borderTop: "1px solid rgba(255,255,255,0.1)" }}>
                    <div style={{ fontSize: "11px", fontWeight: 600, color: "#94a3b8", marginBottom: "4px" }}>
                      📎 Citations:
                    </div>
                    {m.sources.map((src, sIdx) => (
                      <div
                        key={sIdx}
                        style={{
                          fontSize: "12px",
                          background: "rgba(0,0,0,0.2)",
                          padding: "6px 8px",
                          borderRadius: "4px",
                          fontStyle: "italic",
                          color: "#cbd5e1",
                          marginTop: sIdx > 0 ? "4px" : "0",
                        }}
                      >
                        "{src.excerpt}"
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
        {sending && (
          <div
            style={{
              alignSelf: "flex-start",
              background: "#1e2330",
              padding: "10px 16px",
              borderRadius: "16px",
              fontSize: "13px",
              color: "#94a3b8",
            }}
          >
            ✦ Generating response…
          </div>
        )}
      </div>

      {/* Input Row */}
      <div
        style={{
          padding: "16px",
          borderTop: "1px solid #222",
          background: "#161922",
          display: "flex",
          gap: "10px",
        }}
      >
        <input
          type="text"
          placeholder="Ask a question about this document…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={sending}
          style={{
            flex: 1,
            padding: "12px 16px",
            borderRadius: "8px",
            border: "1px solid #334155",
            background: "#0f172a",
            color: "#fff",
            fontSize: "14px",
            outline: "none",
          }}
        />
        <button
          onClick={() => handleSend()}
          disabled={sending || !input.trim()}
          style={{
            padding: "12px 24px",
            borderRadius: "8px",
            border: "none",
            background: sending || !input.trim() ? "#475569" : "#2563eb",
            color: "#fff",
            fontWeight: 600,
            cursor: sending || !input.trim() ? "not-allowed" : "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatTab;
