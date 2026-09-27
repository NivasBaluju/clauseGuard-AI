import React, { useState } from "react";
import { Send, Sparkles, Shield } from "lucide-react";

const SUGGESTED_QUESTIONS = {
  rental_agreement: [
    "Under what conditions can the security deposit be withheld?",
    "How much advance notice is required before landlord entry?",
    "What are the penalties or late fees for overdue rent?",
    "Can the tenant sublet or assign the lease?",
  ],
  job_offer_letter: [
    "What are the non-compete or non-solicitation restrictions?",
    "Is employment at-will, and what are termination conditions?",
    "What are the contingencies for the start date?",
    "How is intellectual property and invention assignment handled?",
  ],
  insurance_policy: [
    "What specific perils or damages are excluded from coverage?",
    "What are the policyholder's duties after a loss occurs?",
    "What is the cancellation procedure and notice window?",
    "What is the deductible and limit of liability?",
  ],
};

export function ChatInput({ onSendMessage, isLoading, documentType = "rental_agreement" }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!question.trim() || isLoading) return;
    onSendMessage(question.trim());
    setQuestion("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const suggestions = SUGGESTED_QUESTIONS[documentType] || SUGGESTED_QUESTIONS.rental_agreement;

  return (
    <div className="border-t border-rule bg-paper-dim p-4 space-y-3">
      {/* Suggestions */}
      <div>
        <div className="flex items-center gap-1.5 text-[11px] font-mono text-zinc-500 uppercase tracking-wider mb-2">
          <Sparkles className="w-3 h-3 text-white" />
          <span>Suggested Inquiries for this Document:</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {suggestions.map((s, idx) => (
            <button
              key={idx}
              type="button"
              disabled={isLoading}
              onClick={() => onSendMessage(s)}
              className="text-xs font-sans text-zinc-300 border border-rule bg-white/[0.02] hover:border-white/40 hover:bg-white/5 px-2.5 py-1 text-left transition-colors disabled:opacity-50"
            >
              "{s}"
            </button>
          ))}
        </div>
      </div>

      {/* Input box */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <textarea
          rows={2}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask any question about this document's clauses, liabilities, or deadlines..."
          disabled={isLoading}
          className="flex-1 bg-black border border-rule p-3 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-white resize-none font-sans disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!question.trim() || isLoading}
          className="border border-white bg-white text-black px-5 flex items-center justify-center font-mono text-xs uppercase tracking-wider hover:bg-zinc-200 transition-colors disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
        >
          {isLoading ? (
            <span className="animate-spin w-4 h-4 border-2 border-black border-t-transparent inline-block" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </form>

      <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500 pt-1">
        <span className="flex items-center gap-1 text-neutral-400">
          <Shield className="w-3 h-3 text-neutral-300" />
          Strict RAG Grounding: AI answers solely using retrieved document clauses.
        </span>
        <span>Press Enter to send, Shift+Enter for newline</span>
      </div>
    </div>
  );
}
