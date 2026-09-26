import React, { useState, useEffect } from "react";
import { ChatTab } from "../components/document/ChatTab";
import { api } from "../api/client";
import { Bot, FileText, Sparkles, ShieldCheck } from "lucide-react";

export function StandaloneChat({ onNavigate }) {
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState("");
  const [loadingDocs, setLoadingDocs] = useState(true);

  useEffect(() => {
    let isMounted = true;
    api
      .getDocuments()
      .then((docs) => {
        if (isMounted) {
          setDocuments(docs || []);
        }
      })
      .catch((err) => {
        console.warn("Could not load documents for chat picker:", err);
      })
      .finally(() => {
        if (isMounted) setLoadingDocs(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="border border-rule bg-paper-dim p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 border border-blue-500/40 bg-blue-950/40 flex items-center justify-center text-blue-400">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-serif text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
              Deciva Enterprise AI Chat Copilot
              <span className="text-[10px] font-mono border border-emerald-500/40 bg-emerald-950/30 text-emerald-300 px-2 py-0.5 rounded">
                Grounded RAG
              </span>
            </h1>
            <p className="text-xs font-mono text-zinc-400 mt-1">
              Ask legal copilot questions, analyze clauses, or inspect specific uploaded documents with verified citations.
            </p>
          </div>
        </div>

        {/* Document Scope Selector */}
        <div className="w-full sm:w-auto flex flex-col sm:flex-row items-start sm:items-center gap-2">
          <label className="text-xs font-mono text-zinc-400 whitespace-nowrap flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5 text-zinc-400" />
            Context Scope:
          </label>
          <select
            value={selectedDocId}
            onChange={(e) => setSelectedDocId(e.target.value)}
            disabled={loadingDocs}
            className="w-full sm:w-64 bg-zinc-900 border border-rule text-white text-xs font-mono py-2 px-3 focus:outline-none focus:border-blue-500 rounded"
          >
            <option value="">General Copilot Mode</option>
            {documents.map((d) => (
              <option key={d.id} value={d.id}>
                {d.filename} ({d.document_type ? d.document_type.replace("_", " ") : "Document"})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Grounded Chat Component */}
      <div className="border border-rule bg-paper rounded-lg shadow-xl overflow-hidden">
        <ChatTab
          key={selectedDocId || "general"}
          documentId={selectedDocId || null}
        />
      </div>

      {/* Architecture Footer Note */}
      <div className="flex flex-wrap items-center justify-between text-[11px] font-mono text-zinc-500 px-2 py-1">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Strict Hallucination Prevention • Confidence Scoring • Citation Excerpts</span>
        </div>
        <div className="flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span>Google Gemini 1.5 Flash + Local Heuristic Engine</span>
        </div>
      </div>
    </div>
  );
}

export default StandaloneChat;
