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
    success: "border-green-300 bg-white text-green-950 shadow-xl",
    error: "border-red-300 bg-white text-red-950 shadow-xl",
    info: "border-neutral-300 bg-white text-black shadow-xl",
  };

  const Icon = type === "success" ? CheckCircle2 : AlertCircle;

  return (
    <div
      className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 border ${borderColors[type] || borderColors.info} max-w-md transition-all duration-300 rounded`}
      role="alert"
    >
      <Icon className="w-4 h-4 shrink-0" />
      <span className="text-xs font-sans flex-1 font-medium">{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          className="text-neutral-400 hover:text-black p-1 transition-colors"
          aria-label="Close"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
}
