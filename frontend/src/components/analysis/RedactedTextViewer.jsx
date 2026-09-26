import React, { useState } from "react";
import { ShieldCheck, Copy, Check } from "lucide-react";

export function RedactedTextViewer({ redactedText = "", clauses = [], selectedClauseId, onSelectClause }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(redactedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="border border-white/20 bg-paper-dim p-6 space-y-4">
      <div className="flex items-center justify-between border-b border-rule pb-3">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-green-400" />
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400 block">
              Redacted Document Text
            </span>
            <h3 className="font-serif text-lg font-bold text-white">
              Full Text (PII-Clean)
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-[11px] font-mono text-green-400 border border-green-500/30 bg-green-950/20 px-2.5 py-1">
            ALL PII MASKED WITH [ENTITIES]
          </span>
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 border border-rule hover:border-white/40 text-xs font-mono text-zinc-300 hover:text-white flex items-center gap-1.5 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? "Copied" : "Copy Text"}
          </button>
        </div>
      </div>

      <p className="text-xs text-zinc-400 leading-relaxed font-sans">
        This is the sole version of the document text processed downstream by machine learning models and displayed in the interface. Raw text is encrypted at rest for audit-only purposes.
      </p>

      {/* Text Container */}
      <div className="border border-rule bg-black p-5 max-h-[550px] overflow-y-auto font-mono text-xs leading-relaxed space-y-4">
        {clauses.length > 0 ? (
          clauses.map((c) => {
            const isSelected = selectedClauseId === c.id;
            const isUnfavorable = c.favorability_label === "unfavorable";
            const isReview = c.favorability_label === "needs_review";

            let bgClass = "hover:bg-white/5";
            if (isSelected) {
              bgClass = "bg-white/10 border-l-2 border-white pl-2";
            } else if (isUnfavorable) {
              bgClass = "bg-red-950/15 border-l-2 border-red-500 pl-2";
            } else if (isReview) {
              bgClass = "bg-amber-950/15 border-l-2 border-amber-500 pl-2";
            }

            return (
              <div
                key={c.id}
                onClick={() => onSelectClause(c.id)}
                className={`p-2 transition-colors cursor-pointer ${bgClass}`}
              >
                <div className="flex items-center gap-2 mb-1 text-[10px] text-zinc-500">
                  <span className="text-zinc-400 font-bold">Clause #{c.clause_index + 1}</span>
                  <span>•</span>
                  <span className="uppercase text-zinc-400">
                    {c.clause_type ? c.clause_type.replace(/_/g, " ") : "General"}
                  </span>
                  <span>•</span>
                  <span>Risk {c.risk_score}</span>
                </div>
                <div className="text-zinc-300 whitespace-pre-wrap">
                  {c.redacted_text}
                </div>
              </div>
            );
          })
        ) : (
          <div className="whitespace-pre-wrap text-zinc-300">
            {redactedText || "No text available."}
          </div>
        )}
      </div>
    </div>
  );
}
