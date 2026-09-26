import React, { useState, useEffect, useRef } from "react";
import { api } from "../../api/client";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { Bot, MessageSquare, AlertCircle } from "lucide-react";

export function ChatPanel({ documentId, documentType, clauses = [], onSelectClause }) {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Build clause lookup table: id -> clause
  const clauseLookup = React.useMemo(() => {
    const lookup = {};
    (clauses || []).forEach((c) => {
      lookup[c.id] = c;
    });
    return lookup;
  }, [clauses]);

  // Load chat history on mount
  useEffect(() => {
    if (!documentId) return;

    api
      .getChatHistory(documentId)
      .then((sessions) => {
        if (sessions && sessions.length > 0) {
          const latestSession = sessions[0];
          setSessionId(latestSession.id);
          setMessages(latestSession.messages || []);
        }
      })
      .catch((err) => {
        console.warn("Could not load chat history:", err);
      });
  }, [documentId]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSendMessage = async (question) => {
    if (!question.trim()) return;

    // Optimistically add user message
    const userMsg = {
      id: "temp-" + Date.now(),
      role: "user",
      content: question,
      grounded: true,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.sendChatMessage(documentId, question, sessionId);

      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      const asstMsg = {
        id: response.message_id || "msg-" + Date.now(),
        role: "assistant",
        content: response.answer,
        cited_clause_ids: response.cited_clause_ids || [],
        grounded: response.grounded,
        retrieved_clauses: response.retrieved_clauses || [],
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, asstMsg]);
    } catch (err) {
      setError(err.message || "Failed to receive response from AI model.");
      const errorMsg = {
        id: "err-" + Date.now(),
        role: "assistant",
        content: `Error: ${err.message || "Could not generate grounded response."}`,
        grounded: false,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="border border-rule bg-paper flex flex-col h-[700px]">
      {/* Header */}
      <div className="border-b border-rule bg-paper-dim px-5 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 border border-blue-500/40 bg-blue-950/40 flex items-center justify-center text-blue-400">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-serif font-bold text-sm text-white flex items-center gap-2">
              Document Assistant (RAG)
              <span className="text-[10px] font-mono border border-blue-500/40 bg-blue-950/30 text-blue-300 px-1.5 py-0.2">
                GEMINI 3.8 FLASH
              </span>
            </h3>
            <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider block">
              768-dim pgvector retrieval • strict clause citation
            </span>
          </div>
        </div>

        <div className="text-xs font-mono text-zinc-400 hidden sm:block">
          {messages.length} message{messages.length === 1 ? "" : "s"}
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 border border-dashed border-rule">
            <div className="w-12 h-12 border border-rule bg-paper-dim flex items-center justify-center text-zinc-500 mb-3">
              <MessageSquare className="w-6 h-6" />
            </div>
            <h4 className="font-serif text-lg font-bold text-white mb-2">
              Ask Grounded Questions
            </h4>
            <p className="text-xs text-zinc-400 max-w-md leading-relaxed mb-4">
              Ask about notice periods, security deposits, indemnification, or renewal clauses. The assistant searches this document via pgvector embeddings and cites the exact clauses used.
            </p>
            <div className="text-[11px] font-mono text-zinc-500 border border-rule bg-paper-dim px-3 py-1.5">
              Strict Non-Hallucination Policy: If not in the text, it says so plainly.
            </div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <ChatMessage
              key={msg.id || index}
              message={msg}
              onSelectClause={onSelectClause}
              clauseLookup={clauseLookup}
            />
          ))
        )}

        {isLoading && (
          <div className="border border-rule bg-paper-dim p-4 mr-4 sm:mr-12 animate-pulse">
            <div className="flex items-center gap-2 text-xs font-mono text-blue-400 mb-2">
              <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
              Embedding query and retrieving clauses via pgvector...
            </div>
            <div className="space-y-2">
              <div className="h-3 bg-white/10 w-3/4"></div>
              <div className="h-3 bg-white/5 w-1/2"></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Error alert if any */}
      {error && (
        <div className="bg-red-950/30 border-t border-red-500/30 px-4 py-2 text-xs font-mono text-red-400 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        documentType={documentType}
      />
    </div>
  );
}
