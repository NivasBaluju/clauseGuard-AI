import React, { useState } from "react";
import { DocumentTypeSelect } from "../components/upload/DocumentTypeSelect";
import { Dropzone } from "../components/upload/Dropzone";
import { ProcessingStatus } from "../components/upload/ProcessingStatus";
import { DisclaimerBanner } from "../components/common/DisclaimerBanner";
import { usePolling } from "../hooks/usePolling";
import { api } from "../api/client";
import { ArrowLeft, ShieldAlert, ArrowRight, AlertCircle } from "lucide-react";

export function Upload({ onNavigate, initialDocType = "rental_agreement" }) {
  const [documentType, setDocumentType] = useState(initialDocType);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [processingDocId, setProcessingDocId] = useState(null);

  // Poll status when upload succeeds
  const { status, processingStage, errorMessage } = usePolling(processingDocId, {
    interval: 1000,
    onComplete: (data) => {
      // Auto navigate to analysis screen upon completion
      onNavigate("analysis", { documentId: processingDocId });
    },
    onError: (err) => {
      setError(err || "Processing failed");
    },
    enabled: Boolean(processingDocId),
  });

  const handleFileSelect = (selectedFile) => {
    setError(null);
    const validExtensions = [".pdf", ".docx", ".txt"];
    const ext = "." + selectedFile.name.split(".").pop().toLowerCase();

    if (!validExtensions.includes(ext)) {
      setError(`Unsupported file format "${ext}". Supported: .pdf, .docx, .txt`);
      return;
    }

    if (selectedFile.size > 20 * 1024 * 1024) {
      setError("File exceeds maximum allowable size of 20 MB.");
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a document file to upload.");
      return;
    }
    if (!documentType) {
      setError("Please select the document type.");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_type", documentType);

    try {
      const response = await api.uploadDocument(formData);
      setProcessingDocId(response.document_id || response.id);
    } catch (err) {
      setError(err.message || "Failed to initiate document upload.");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-rule pb-4">
        <div>
          <button
            onClick={() => onNavigate("landing")}
            className="inline-flex items-center gap-1.5 text-xs font-mono text-zinc-400 hover:text-white mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Overview</span>
          </button>
          <h1 className="font-serif text-3xl font-bold text-white">
            Upload Agreement for AI Audit
          </h1>
          <p className="text-xs text-zinc-400 mt-1 font-sans">
            Specify the document type and provide your PDF, DOCX, or TXT agreement.
          </p>
        </div>

        <button
          onClick={() => onNavigate("documents")}
          className="px-3.5 py-2 text-xs font-mono uppercase tracking-wider border border-rule hover:border-white text-zinc-300 hover:text-white transition-colors hidden sm:block"
        >
          View Library
        </button>
      </div>

      {/* If actively processing, show live pipeline stages */}
      {processingDocId ? (
        <div className="space-y-6">
          <ProcessingStatus
            stage={processingStage}
            status={status}
            error={errorMessage || error}
          />

          {status === "failed" && (
            <div className="text-center pt-4">
              <button
                onClick={() => {
                  setProcessingDocId(null);
                  setIsSubmitting(false);
                }}
                className="px-6 py-2.5 text-xs font-mono uppercase tracking-wider border border-white bg-white text-black hover:bg-zinc-200"
              >
                Try Another Document
              </button>
            </div>
          )}
        </div>
      ) : (
        /* Upload Form */
        <div className="space-y-8">
          {/* Step 1: Document Type Select */}
          <DocumentTypeSelect value={documentType} onChange={setDocumentType} />

          {/* Step 2: Dropzone */}
          <Dropzone
            file={file}
            onFileSelect={handleFileSelect}
            onClearFile={() => setFile(null)}
            error={error}
          />

          {/* Error Message */}
          {error && (
            <div className="border border-red-500/40 bg-red-950/20 p-4 text-xs font-mono text-red-300 flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* Privacy Note */}
          <div className="border border-rule bg-paper-dim p-4 text-xs text-zinc-400 font-sans leading-relaxed">
            <span className="font-mono text-zinc-300 uppercase tracking-wider text-[10px] block mb-1">
              Privacy Architecture Note:
            </span>
            Names, phone numbers, email addresses, and residential addresses are detected and masked via Presidio immediately upon text extraction. The raw unredacted text is encrypted at rest and is never sent to any ML classifier or external model.
          </div>

          {/* Submit CTA */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-rule">
            <button
              type="button"
              onClick={() => onNavigate("landing")}
              className="px-5 py-2.5 text-xs font-mono uppercase tracking-wider border border-rule hover:border-white/40 text-zinc-400 hover:text-white transition-colors"
            >
              Cancel
            </button>

            <button
              type="button"
              disabled={!file || !documentType || isSubmitting}
              onClick={handleUpload}
              className="px-8 py-3 text-xs font-mono uppercase tracking-wider border border-white bg-white text-black hover:bg-zinc-200 transition-colors flex items-center gap-2 font-bold disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <span className="animate-spin w-3.5 h-3.5 border-2 border-black border-t-transparent inline-block" />
                  <span>Uploading & Queuing...</span>
                </>
              ) : (
                <>
                  <span>Begin Risk Audit</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Mandatory Disclaimer */}
      <DisclaimerBanner />
    </div>
  );
}
