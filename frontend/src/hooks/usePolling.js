import { useState, useEffect, useRef, useCallback } from "react";
import { api } from "../api/client";

export function usePolling(documentId, options = {}) {
  const {
    interval = 1500,
    onComplete = null,
    onError = null,
    enabled = true,
  } = options;

  const [status, setStatus] = useState("queued");
  const [processingStage, setProcessingStage] = useState("queued");
  const [errorMessage, setErrorMessage] = useState(null);
  const [isPolling, setIsPolling] = useState(enabled && Boolean(documentId));

  const timerRef = useRef(null);
  const isCancelledRef = useRef(false);

  const stopPolling = useCallback(() => {
    setIsPolling(false);
    isCancelledRef.current = true;
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const poll = useCallback(async () => {
    if (!documentId || isCancelledRef.current) return;

    try {
      const data = await api.getDocumentStatus(documentId);
      setStatus(data.status);
      setProcessingStage(data.processing_stage);

      if (data.status === "analyzed") {
        stopPolling();
        if (onComplete) onComplete(data);
      } else if (data.status === "failed") {
        stopPolling();
        setErrorMessage(data.error_message || "Document processing failed.");
        if (onError) onError(data.error_message);
      } else {
        // Keep polling
        if (!isCancelledRef.current) {
          timerRef.current = setTimeout(poll, interval);
        }
      }
    } catch (err) {
      setErrorMessage(err.message);
      stopPolling();
      if (onError) onError(err.message);
    }
  }, [documentId, interval, onComplete, onError, stopPolling]);

  useEffect(() => {
    if (enabled && documentId) {
      isCancelledRef.current = false;
      setIsPolling(true);
      poll();
    }
    return () => {
      stopPolling();
    };
  }, [enabled, documentId, poll, stopPolling]);

  return {
    status,
    processingStage,
    errorMessage,
    isPolling,
    stopPolling,
  };
}
