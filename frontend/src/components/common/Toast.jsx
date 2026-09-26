import React, { useEffect } from "react";
import { CheckCircle2, AlertCircle, X } from "lucide-react";

export function Toast({ message, type = "info", onClose, duration = 4000 }) {
  useEffect(() => {
    if (duration > 0 && onClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const borderColors = {
    success: "border-green-500 bg-zinc-950 text-green-300",
    error: "border-red-500 bg-zinc-950 text-red-300",
    info: "border-blue-500 bg-zinc-950 text-blue-300",
  };

  const Icon = type === "success" ? CheckCircle2 : AlertCircle;

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 border shadow-2xl ${borderColors[type] || borderColors.info} max-w-md transition-all duration-300`}
      role="alert"
    >
      <Icon className="w-4 h-4 shrink-0" />
      <span className="text-xs font-sans flex-1">{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          className="text-zinc-400 hover:text-white p-1"
          aria-label="Close"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
}
