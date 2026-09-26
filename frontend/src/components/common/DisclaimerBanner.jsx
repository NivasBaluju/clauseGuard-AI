import React from "react";
import { AlertTriangle } from "lucide-react";

export function DisclaimerBanner({ className = "" }) {
  return (
    <div
      className={`border border-red-500/30 bg-red-950/20 px-4 py-3 text-xs leading-relaxed text-red-200/90 flex items-start gap-3 ${className}`}
      role="alert"
    >
      <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
      <div>
        <span className="font-semibold text-red-300 uppercase tracking-wider text-[10px] block mb-0.5">
          Legal Disclaimer
        </span>
        <p>
          ClauseGuard AI provides automated, non-expert analysis for informational purposes only. It is not legal advice. Consult a qualified attorney for decisions with legal consequences.
        </p>
      </div>
    </div>
  );
}
