import React from "react";
import { ChatTab } from "../document/ChatTab";

export function ChatPanel({ documentId }) {
  return (
    <div className="w-full">
      <ChatTab documentId={documentId} />
    </div>
  );
}

export default ChatPanel;
