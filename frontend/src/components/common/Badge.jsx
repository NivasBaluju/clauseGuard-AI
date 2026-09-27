import React from "react";

export function Badge({ variant = "default", children, className = "" }) {
  const variantStyles = {
    // Risk bands
    low: "border-green-500/40 bg-green-950/20 text-green-400",
    medium: "border-amber-500/40 bg-amber-950/20 text-amber-400",
    high: "border-orange-500/40 bg-orange-950/20 text-orange-400",
    critical: "border-red-500/40 bg-red-950/30 text-red-400",

    // Favorability
    fair: "border-green-500/40 bg-green-950/20 text-green-400",
    needs_review: "border-amber-500/40 bg-amber-950/20 text-amber-400",
    unfavorable: "border-red-500/40 bg-red-950/30 text-red-400",

    // Status / info
    info: "border-neutral-700 bg-neutral-900 text-white",
    default: "border-neutral-800 bg-neutral-900 text-neutral-300",
  };

  const style = variantStyles[variant.toLowerCase()] || variantStyles.default;

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 text-[11px] font-mono uppercase tracking-wider border ${style} ${className}`}
    >
      {children}
    </span>
  );
}
