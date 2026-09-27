import React from "react";
import { Clock, Calendar, AlertCircle, CheckCircle2 } from "lucide-react";

export function DeadlineTimeline({ deadlines = [] }) {
  return (
    <div className="border border-white/20 bg-paper-dim p-6 space-y-4">
      <div className="flex items-center justify-between border-b border-rule pb-3">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400 block">
            Time-Sensitive Panel
          </span>
          <h3 className="font-serif text-lg font-bold text-white">
            Deadlines & Notice Periods ({deadlines.length})
          </h3>
        </div>
        <span className="text-xs font-mono text-zinc-500">
          Sorted Soonest-First
        </span>
      </div>

      <p className="text-xs text-zinc-400 leading-relaxed font-sans">
        Identified notice windows, renewal triggers, and calendar-bound deadlines extracted from clause text. Deadlines are evaluated independently from the static risk score.
      </p>

      {deadlines.length > 0 ? (
        <div className="space-y-3 pt-2">
          {deadlines.map((dl, idx) => {
            const isReview = dl.confidence === "needs_review";

            return (
              <div
                key={idx}
                className={`border p-4 space-y-2 transition-colors ${
                  isReview
                    ? "border-amber-500/40 bg-amber-950/10"
                    : "border-rule bg-black/40 hover:border-white/30"
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="w-6 h-6 border border-rule bg-white/5 flex items-center justify-center text-white text-xs">
                      {dl.parsed_date ? (
                        <Calendar className="w-3.5 h-3.5 text-white" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-zinc-400" />
                      )}
                    </span>
                    <span className="font-serif font-bold text-sm text-white">
                      {dl.deadline_type
                        ? dl.deadline_type.replace(/_/g, " ").toUpperCase()
                        : "NOTICE OBLIGATION"}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    {dl.relative_days && (
                      <span className="text-xs font-mono px-2 py-0.5 border border-white/20 bg-white/5 text-white">
                        {dl.relative_days} DAYS
                      </span>
                    )}

                    {dl.parsed_date && (
                      <span className="text-xs font-mono px-2 py-0.5 border border-neutral-700 bg-neutral-900 text-white">
                        {dl.parsed_date}
                      </span>
                    )}

                    {isReview ? (
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 border border-amber-500/50 bg-amber-950/30 text-amber-300 flex items-center gap-1">
                        <AlertCircle className="w-3 h-3 text-amber-400" />
                        Needs Manual Verification
                      </span>
                    ) : (
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 border border-green-500/40 bg-green-950/20 text-green-400 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3 text-green-400" />
                        Confident
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-zinc-300 font-sans leading-relaxed">
                  "{dl.raw_text}"
                </p>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="border border-rule bg-black/30 p-6 text-center text-xs text-zinc-500 font-mono">
          No calendar deadlines or relative notice periods detected in this document.
        </div>
      )}
    </div>
  );
}
