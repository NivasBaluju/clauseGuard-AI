import React from "react";
import { Check, Loader2, AlertCircle } from "lucide-react";

export const PIPELINE_STAGES = [
  { key: "extracting_text", label: "Extracting text layer (with OCR fallback)" },
  { key: "redacting_pii", label: "Redacting personally identifiable information (PII)" },
  { key: "segmenting_clauses", label: "Segmenting clauses and boundary offsets" },
  { key: "classifying_clauses", label: "Classifying clause types and favorability (BERT / Baseline)" },
  { key: "scoring_risk", label: "Calculating transparent risk scores and missing clauses" },
  { key: "extracting_deadlines", label: "Extracting notice periods and calendar deadlines" },
  { key: "generating_embeddings", label: "Generating 768-dim embeddings for grounded RAG" },
];

export function ProcessingStatus({ stage, status, error }) {
  const currentStageIndex = PIPELINE_STAGES.findIndex((s) => s.key === stage);

  return (
    <div className="border border-white/20 bg-paper-dim p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-rule pb-4">
        <div>
          <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest block">
            Analysis Pipeline
          </span>
          <h3 className="font-serif text-lg font-bold text-white">
            {status === "failed" ? "Processing Failed" : "Analyzing Legal Document"}
          </h3>
        </div>
        {status !== "failed" && (
          <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
            <Loader2 className="w-4 h-4 animate-spin text-white" />
            <span>Processing...</span>
          </div>
        )}
      </div>

      {error ? (
        <div className="border border-red-500/30 bg-red-950/20 p-4 text-xs text-red-300 flex items-start gap-3 font-mono">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold mb-1">Pipeline encountered an error:</p>
            <p className="text-red-400">{error}</p>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {PIPELINE_STAGES.map((s, idx) => {
            const isDone = currentStageIndex > idx || stage === "completed";
            const isCurrent = currentStageIndex === idx;

            return (
              <div
                key={s.key}
                className={`flex items-center gap-3 text-xs font-mono transition-colors p-2.5 border ${
                  isCurrent
                    ? "border-white/40 bg-white/5 text-white"
                    : isDone
                    ? "border-transparent text-zinc-400"
                    : "border-transparent text-zinc-600"
                }`}
              >
                <div
                  className={`w-5 h-5 flex items-center justify-center border text-[10px] ${
                    isDone
                      ? "border-green-500 bg-green-500/20 text-green-400"
                      : isCurrent
                      ? "border-white bg-white text-black font-bold"
                      : "border-zinc-800 text-zinc-600"
                  }`}
                >
                  {isDone ? <Check className="w-3 h-3 text-green-400" /> : idx + 1}
                </div>
                <span className={isCurrent ? "font-bold text-white" : ""}>
                  {s.label}
                </span>
                {isCurrent && (
                  <span className="ml-auto text-[10px] uppercase text-zinc-400 animate-pulse">
                    Running
                  </span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
