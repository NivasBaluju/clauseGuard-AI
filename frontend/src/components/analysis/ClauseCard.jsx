import React, { useState } from "react";
import { Badge } from "../common/Badge";
import { AlertCircle, Copy, Check, ChevronDown, ChevronUp } from "lucide-react";

export function ClauseCard({ clause, isSelected, onSelect }) {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const copyToClipboard = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(clause.redacted_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isLong = clause.redacted_text.length > 280;
  const displayText = isLong && !isExpanded
    ? clause.redacted_text.slice(0, 280) + "..."
    : clause.redacted_text;

  const riskColor =
    clause.risk_score >= 70
      ? "text-red-400 border-red-500/40 bg-red-950/20"
      : clause.risk_score >= 40
      ? "text-amber-400 border-amber-500/40 bg-amber-950/20"
      : "text-green-400 border-green-500/40 bg-green-950/20";

  return (
    <div
      onClick={onSelect}
      className={`border p-5 transition-all cursor-pointer ${
        isSelected
          ? "border-white bg-white/10"
          : "border-rule bg-paper-dim hover:border-white/30"
      }`}
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-rule pb-3 mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-mono text-xs text-zinc-500">
            #{clause.clause_index + 1}
          </span>
          <span className="font-serif font-bold text-base text-white">
            {clause.clause_type ? clause.clause_type.replace(/_/g, " ").toUpperCase() : "UNCLASSIFIED"}
          </span>
          <Badge variant={clause.favorability_label || "fair"}>
            {clause.favorability_label || "fair"}
          </Badge>

          {clause.favorability_label === "needs_review" && (
            <span className="inline-flex items-center gap-1 text-[11px] font-mono text-amber-400 border border-amber-500/40 bg-amber-950/30 px-2 py-0.5">
              <AlertCircle className="w-3 h-3" />
              HUMAN REVIEW FLAGGED
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] font-mono text-zinc-500 block uppercase">
              Clause Risk
            </span>
            <span className={`text-xs font-mono font-bold px-2 py-0.5 border ${riskColor}`}>
              {clause.risk_score} / 100
            </span>
          </div>

          <button
            onClick={copyToClipboard}
            className="p-1.5 border border-rule hover:border-white/40 text-zinc-400 hover:text-white"
            title="Copy redacted text"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      <p className="text-xs text-zinc-300 font-sans leading-relaxed whitespace-pre-wrap">
        {displayText}
      </p>

      {isLong && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            setIsExpanded(!isExpanded);
          }}
          className="mt-3 text-[11px] font-mono text-zinc-400 hover:text-white flex items-center gap-1"
        >
          {isExpanded ? (
            <>
              Show less <ChevronUp className="w-3 h-3" />
            </>
          ) : (
            <>
              Show full clause text <ChevronDown className="w-3 h-3" />
            </>
          )}
        </button>
      )}
    </div>
  );
}
