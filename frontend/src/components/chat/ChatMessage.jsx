import React, { useState } from "react";
import { User, Bot, CheckCircle2, AlertTriangle, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "../common/Badge";

export function ChatMessage({ message, onSelectClause, clauseLookup = {} }) {
  const isUser = message.role === "user";
  const [showRetrieved, setShowRetrieved] = useState(false);

  return (
    <div
      className={`border p-4 transition-all ${
        isUser
          ? "border-white/20 bg-white/5 ml-4 sm:ml-12"
          : "border-rule bg-paper-dim mr-4 sm:mr-12"
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between gap-3 border-b border-rule pb-2 mb-3">
        <div className="flex items-center gap-2">
          {isUser ? (
            <div className="w-6 h-6 border border-white/30 bg-white/10 flex items-center justify-center text-white">
              <User className="w-3.5 h-3.5" />
            </div>
          ) : (
            <div className="w-6 h-6 border border-blue-500/40 bg-blue-950/40 flex items-center justify-center text-blue-400">
              <Bot className="w-3.5 h-3.5" />
            </div>
          )}
          <span className="font-mono text-xs text-zinc-400 uppercase tracking-wider">
            {isUser ? "You" : "ClauseGuard AI (Grounded Gemini RAG)"}
          </span>
        </div>

        {!isUser && (
          <div className="flex items-center gap-2">
            {message.grounded ? (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-green-400 border border-green-500/40 bg-green-950/30 px-2 py-0.5">
                <CheckCircle2 className="w-3 h-3" />
                Grounded ({message.cited_clause_ids?.length || 0} citations)
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-amber-400 border border-amber-500/40 bg-amber-950/30 px-2 py-0.5">
                <AlertTriangle className="w-3 h-3" />
                Not Grounded / No Document Support
              </span>
            )}
          </div>
        )}
      </div>

      {/* Message content */}
      <div className="text-sm leading-relaxed text-zinc-200 whitespace-pre-wrap font-sans">
        {message.content}
      </div>

      {/* Citations section for Assistant */}
      {!isUser && message.cited_clause_ids && message.cited_clause_ids.length > 0 && (
        <div className="mt-4 pt-3 border-t border-rule">
          <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 block mb-2">
            Directly Cited Clauses in Document:
          </span>
          <div className="flex flex-wrap gap-2">
            {message.cited_clause_ids.map((clauseId) => {
              const clause = clauseLookup[clauseId];
              return (
                <button
                  key={clauseId}
                  onClick={() => onSelectClause && onSelectClause(clauseId)}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono border border-blue-500/40 bg-blue-950/20 text-blue-300 hover:border-blue-400 hover:bg-blue-900/40 transition-colors"
                  title="Click to view clause in document"
                >
                  <FileText className="w-3 h-3 text-blue-400" />
                  <span>
                    {clause ? `Clause #${clause.clause_index + 1}: ${clause.clause_type?.replace(/_/g, " ").toUpperCase()}` : `Clause ${clauseId.slice(0, 8)}`}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Retrieved Context Accordion for transparency */}
      {!isUser && message.retrieved_clauses && message.retrieved_clauses.length > 0 && (
        <div className="mt-3 pt-2">
          <button
            onClick={() => setShowRetrieved(!showRetrieved)}
            className="text-[11px] font-mono text-zinc-500 hover:text-zinc-300 flex items-center gap-1 transition-colors"
          >
            {showRetrieved ? (
              <>
                <ChevronUp className="w-3 h-3" />
                <span>Hide {message.retrieved_clauses.length} pgvector retrieved clauses</span>
              </>
            ) : (
              <>
                <ChevronDown className="w-3 h-3" />
                <span>Inspect {message.retrieved_clauses.length} pgvector retrieved clauses passed to Gemini</span>
              </>
            )}
          </button>

          {showRetrieved && (
            <div className="mt-2 space-y-2 border-l-2 border-blue-500/30 pl-3 pt-1">
              {message.retrieved_clauses.map((rc, idx) => (
                <div key={idx} className="bg-black/40 border border-rule p-2.5 text-xs">
                  <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 mb-1">
                    <span>Clause #{rc.clause_index + 1} ({rc.clause_type})</span>
                    <span>Distance: {rc.distance?.toFixed(4) || "N/A"}</span>
                  </div>
                  <p className="text-zinc-300 text-xs italic font-serif line-clamp-3">
                    "{rc.redacted_text}"
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
