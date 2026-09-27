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
    <div className="border border-neutral-300 bg-white p-6 space-y-6 shadow-sm">
      <div className="flex items-center justify-between border-b border-neutral-200 pb-4">
        <div>
          <span className="text-[10px] font-mono text-neutral-500 uppercase tracking-widest block font-semibold">
            Analysis Pipeline
          </span>
          <h3 className="font-serif text-lg font-bold text-black">
            {status === "failed" ? "Processing Failed" : "Analyzing Legal Document"}
          </h3>
        </div>
        {status !== "failed" && (
          <div className="flex items-center gap-2 text-xs font-mono text-neutral-600">
            <Loader2 className="w-4 h-4 animate-spin text-black" />
            <span>Processing...</span>
          </div>
        )}
      </div>

      {error ? (
        <div className="border border-red-300 bg-red-50 p-4 text-xs text-red-800 flex items-start gap-3 font-mono">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-bold mb-1">Pipeline encountered an error:</p>
            <p className="text-red-700">{error}</p>
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
                    ? "border-black bg-neutral-100 text-black font-semibold"
                    : isDone
                    ? "border-transparent text-neutral-700"
                    : "border-transparent text-neutral-400"
                }`}
              >
                <div
                  className={`w-5 h-5 flex items-center justify-center border text-[10px] ${
                    isDone
                      ? "border-green-600 bg-green-50 text-green-700 font-bold"
                      : isCurrent
                      ? "border-black bg-black text-white font-bold"
                      : "border-neutral-300 text-neutral-400 bg-white"
                  }`}
                >
                  {isDone ? <Check className="w-3 h-3 text-green-700" /> : idx + 1}
                </div>
                <span className={isCurrent ? "font-bold text-black" : ""}>
                  {s.label}
                </span>
                {isCurrent && (
                  <span className="ml-auto text-[10px] uppercase text-neutral-600 animate-pulse font-semibold">
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
