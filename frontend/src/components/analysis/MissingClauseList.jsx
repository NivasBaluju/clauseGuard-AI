import React from "react";
import { AlertTriangle, CheckCircle2 } from "lucide-react";
import { Badge } from "../common/Badge";

export function MissingClauseList({ missingClauses = [] }) {
  const severityColors = {
    high: "border-red-500/40 bg-red-950/20 text-red-400",
    medium: "border-amber-500/40 bg-amber-950/20 text-amber-400",
    low: "border-green-500/40 bg-green-950/20 text-green-400",
  };

  return (
    <div className="border border-white/20 bg-paper-dim p-6 space-y-4">
      <div className="flex items-center justify-between border-b border-rule pb-3">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400 block">
            Completeness Checklist
          </span>
          <h3 className="font-serif text-lg font-bold text-white">
            Missing Expected Clauses ({missingClauses.length})
          </h3>
        </div>
        <span className="text-xs font-mono text-zinc-500">
          Set-Difference Analysis
        </span>
      </div>

      <p className="text-xs text-zinc-400 leading-relaxed font-sans">
        The following standard clauses are commonly expected in this document type but were absent or detected below confidence threshold. Note: This is an engineering checklist of common provisions, not a statutory compliance mandate.
      </p>

      {missingClauses.length > 0 ? (
        <div className="space-y-3 pt-2">
          {missingClauses.map((m, idx) => (
            <div
              key={idx}
              className="border border-rule bg-black/40 p-4 space-y-2 hover:border-white/30 transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="font-serif font-bold text-sm text-white">
                  {m.clause_type.replace(/_/g, " ").toUpperCase()}
                </span>
                <span
                  className={`text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 border ${
                    severityColors[m.severity] || severityColors.medium
                  }`}
                >
                  {m.severity} Severity
                </span>
              </div>
              <p className="text-xs text-zinc-400 font-sans leading-relaxed">
                {m.checklist_note || "Standard protection for this document category."}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="border border-green-500/30 bg-green-950/20 p-5 text-center text-xs text-green-300 font-mono flex items-center justify-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-green-400" />
          All standard expected clauses for this document type were identified.
        </div>
      )}
    </div>
  );
}
