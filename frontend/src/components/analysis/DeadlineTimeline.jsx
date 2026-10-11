import React from "react";
import { Clock, Calendar, AlertCircle, CheckCircle2 } from "lucide-react";

export function DeadlineTimeline({ deadlines = [] }) {
  return (
    <div className="border border-neutral-200 bg-white p-6 space-y-4 shadow-sm">
      <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-widest text-neutral-500 block font-semibold">
            Time-Sensitive Panel
          </span>
          <h3 className="font-serif text-lg font-bold text-black">
            Deadlines & Notice Periods ({deadlines.length})
          </h3>
        </div>
        <span className="text-xs font-mono text-neutral-500 font-semibold">
          Sorted Soonest-First
        </span>
      </div>

      <p className="text-xs text-neutral-600 leading-relaxed font-sans">
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
                    ? "border-amber-300 bg-amber-50"
                    : "border-neutral-200 bg-neutral-50 hover:border-neutral-400"
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="w-6 h-6 border border-neutral-300 bg-white flex items-center justify-center text-black text-xs">
                      {dl.parsed_date ? (
                        <Calendar className="w-3.5 h-3.5 text-black" />
                      ) : (
                        <Clock className="w-3.5 h-3.5 text-neutral-500" />
                      )}
                    </span>
                    <span className="font-serif font-bold text-sm text-black">
                      {dl.deadline_type
                        ? dl.deadline_type.replace(/_/g, " ").toUpperCase()
                        : "NOTICE OBLIGATION"}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    {dl.relative_days && (
                      <span className="text-xs font-mono px-2 py-0.5 border border-neutral-300 bg-white text-black font-semibold">
                        {dl.relative_days} DAYS
                      </span>
                    )}

                    {dl.parsed_date && (
                      <span className="text-xs font-mono px-2 py-0.5 border border-neutral-300 bg-white text-black font-semibold">
                        {dl.parsed_date}
                      </span>
                    )}

                    {isReview ? (
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 border border-amber-300 bg-amber-50 text-amber-800 flex items-center gap-1 font-semibold">
                        <AlertCircle className="w-3 h-3 text-amber-600" />
                        Needs Manual Verification
                      </span>
                    ) : (
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 border border-green-300 bg-green-50 text-green-800 flex items-center gap-1 font-semibold">
                        <CheckCircle2 className="w-3 h-3 text-green-600" />
                        Confident
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-neutral-800 font-sans leading-relaxed">
                  "{dl.raw_text}"
                </p>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="border border-neutral-200 bg-white p-6 text-center text-xs text-neutral-500 font-mono shadow-sm">
          No calendar deadlines or relative notice periods detected in this document.
        </div>
      )}
    </div>
  );
}
