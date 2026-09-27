import React from "react";
import { ChatTab } from "../document/ChatTab";

/**
 * ChatPanel wrapper that integrates the user's Enterprise AI Chat System (ChatTab)
 * with grounded citations, confidence scoring, and grounded RAG fallback.
 */
export function ChatPanel({ documentId }) {
  return (
    <div className="w-full">
      <ChatTab documentId={documentId} />
    </div>
  );
}

export default ChatPanel;
