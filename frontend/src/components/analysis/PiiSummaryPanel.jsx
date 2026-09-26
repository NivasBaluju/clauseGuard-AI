import React, { useEffect, useState } from "react";
import { api } from "../../api/client";
import { ShieldCheck, Lock, EyeOff, AlertCircle } from "lucide-react";

export function PiiSummaryPanel({ documentId }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!documentId) return;
    setLoading(true);
    api
      .getPiiSummary(documentId)
      .then((data) => {
        setSummary(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [documentId]);

  if (loading) {
    return (
      <div className="border border-rule bg-paper-dim p-5">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-white/10 w-1/3"></div>
          <div className="h-10 bg-white/5 w-full"></div>
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return null;
  }

  const entityCounts = summary.entity_counts || {};
  const totalFindings = summary.total_findings || 0;

  return (
    <div className="border border-rule bg-paper-dim p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-rule pb-3 mb-4">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-green-400" />
          <h3 className="font-serif font-bold text-lg text-white">
            PII Redaction Summary
          </h3>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
          <Lock className="w-3.5 h-3.5 text-zinc-500" />
          <span>Encrypted at rest • Zero raw leakage</span>
        </div>
      </div>

      <p className="text-xs text-zinc-400 leading-relaxed mb-4">
        Microsoft Presidio redacted personal identifying information before clause segmentation, model inference, or storage. Downstream models and Gemini RAG only ever process anonymized placeholders.
      </p>

      {totalFindings === 0 ? (
        <div className="border border-rule bg-white/[0.02] p-4 text-center">
          <p className="text-xs font-mono text-zinc-400">
            No personal identifying information entities were detected in this document.
          </p>
        </div>
      ) : (
        <div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 mb-4">
            {Object.entries(entityCounts).map(([entityType, count]) => (
              <div
                key={entityType}
                className="border border-rule bg-white/[0.02] p-3 flex flex-col justify-between"
              >
                <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider block">
                  {entityType.replace(/_/g, " ")}
                </span>
                <span className="font-serif text-xl font-bold text-white mt-1">
                  {count} <span className="text-xs font-mono text-zinc-500 font-normal">redacted</span>
                </span>
              </div>
            ))}
          </div>

          <div className="border border-blue-500/30 bg-blue-950/20 p-3 flex items-start gap-2.5">
            <EyeOff className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <p className="text-xs text-blue-200/90 leading-relaxed">
              <strong>Zero-Storage Guarantee:</strong> The database only records entity types and character offsets. Actual names, phone numbers, or account numbers are never retained in plaintext.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
