import React from "react";

export function SkeletonLoader({ count = 3, className = "" }) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="h-12 w-full border border-white/10 shimmer bg-zinc-900/40"
        />
      ))}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="border border-white/10 p-5 bg-zinc-950 space-y-4">
      <div className="h-5 w-1/3 shimmer border border-white/5" />
      <div className="h-4 w-full shimmer border border-white/5" />
      <div className="h-4 w-5/6 shimmer border border-white/5" />
      <div className="h-4 w-2/3 shimmer border border-white/5" />
    </div>
  );
}
