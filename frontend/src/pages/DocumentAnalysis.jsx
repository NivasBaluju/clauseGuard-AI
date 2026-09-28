import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { RiskScoreGauge } from "../components/analysis/RiskScoreGauge";
import { ClauseList } from "../components/analysis/ClauseList";
import { MissingClauseList } from "../components/analysis/MissingClauseList";
import { DeadlineTimeline } from "../components/analysis/DeadlineTimeline";
import { RedactedTextViewer } from "../components/analysis/RedactedTextViewer";
import { PiiSummaryPanel } from "../components/analysis/PiiSummaryPanel";
import { ChatPanel } from "../components/chat/ChatPanel";
import { Badge } from "../components/common/Badge";
import {
  ArrowLeft,
  Download,
  AlertTriangle,
  FileText,
  Clock,
  MessageSquare,
  ShieldCheck,
  Layers,
  Cpu,
  RefreshCw,
} from "lucide-react";

export function DocumentAnalysis({ documentId, onNavigate }) {
  const [doc, setDoc] = useState(null);
  const [clauses, setClauses] = useState([]);
  const [missingClauses, setMissingClauses] = useState([]);
  const [deadlines, setDeadlines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedClauseId, setSelectedClauseId] = useState(null);
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  const fetchAnalysisData = async () => {
    if (!documentId) return;
    setLoading(true);
    setError(null);

    try {
      const [docData, clausesData, missingData, deadlinesData] = await Promise.all([
        api.getDocument(documentId),
        api.getClauses(documentId).catch(() => []),
        api.getMissingClauses(documentId).catch(() => []),
        api.getDeadlines(documentId).catch(() => []),
      ]);

      setDoc(docData);
      setClauses(clausesData || []);
      setMissingClauses(missingData || []);
      setDeadlines(deadlinesData || []);
    } catch (err) {
      setError(err.message || "Failed to load document analysis data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysisData();
  }, [documentId]);

  const handleSelectClause = (clauseId) => {
    setSelectedClauseId(clauseId);

    if (activeTab === "chat" || activeTab === "overview") {
      setActiveTab("clauses");
    }
  };

  const handleDownloadPdf = async (e) => {
    e.preventDefault();
    if (downloadingPdf || !doc) return;
    setDownloadingPdf(true);
    try {
      await api.downloadReportPdf(doc.id, doc.filename);
    } catch (err) {
      console.warn("Direct PDF download blob failed, attempting URL open fallback:", err);
      window.open(api.getReportPdfUrl(doc.id), "_blank");
    } finally {
      setDownloadingPdf(false);
    }
  };

  const getDocTypeLabel = (type) => {
    switch (type) {
      case "rental_agreement":
        return "Residential Lease";
      case "job_offer_letter":
        return "Job Offer Letter";
      case "insurance_policy":
        return "Insurance Specimen (HO-4)";
      default:
        return type || "Document";
    }
  };

  if (loading) {
    return (
      <div className="space-y-6 py-8">
        <div className="border border-neutral-200 bg-white p-8 text-center space-y-4 animate-pulse">
          <div className="w-10 h-10 border border-neutral-300 mx-auto"></div>
          <p className="text-xs font-mono text-neutral-600">Loading document audit details...</p>
        </div>
      </div>
    );
  }

  if (error || !doc) {
    return (
      <div className="space-y-6 py-8">
        <div className="border border-red-300 bg-red-50 p-6 text-center space-y-3 font-mono text-xs text-red-700">
          <AlertTriangle className="w-6 h-6 mx-auto text-red-600" />
          <p>{error || "Document not found"}</p>
          <button
            onClick={() => onNavigate("documents")}
            className="px-4 py-1.5 border border-red-600 bg-red-600 text-white uppercase tracking-wider"
          >
            Back to Documents
          </button>
        </div>
      </div>
    );
  }

  const unfavorableCount = clauses.filter((c) => c.favorability_label === "unfavorable").length;
  const reviewCount = clauses.filter((c) => c.favorability_label === "needs_review").length;
  const fairCount = clauses.filter((c) => c.favorability_label === "fair").length;

  return (
    <div className="space-y-6 py-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-neutral-200 pb-4">
        <div>
          <button
            onClick={() => onNavigate("documents")}
            className="inline-flex items-center gap-1.5 text-xs font-mono text-neutral-600 hover:text-black mb-2 transition-colors font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Documents</span>
          </button>
          <div className="flex items-center gap-3 flex-wrap">
            <h1 className="font-serif text-2xl sm:text-3xl font-bold text-black">
              {doc.filename}
            </h1>
            <Badge variant="default" className="text-neutral-800 border-neutral-300 bg-neutral-100">
              {getDocTypeLabel(doc.document_type)}
            </Badge>
            <span className="text-xs font-mono uppercase px-2 py-0.5 border border-neutral-300 bg-neutral-100 text-neutral-700">
              {doc.original_format}
            </span>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono text-neutral-600 mt-1 flex-wrap">
            <span>Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}</span>
            {doc.page_count && <span>• {doc.page_count} Pages</span>}
            {doc.model_version && (
              <span className="flex items-center gap-1 text-neutral-700">
                <Cpu className="w-3.5 h-3.5 text-neutral-500" />
                Model: {doc.model_version}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3 self-stretch sm:self-auto justify-end">
          <button
            onClick={fetchAnalysisData}
            className="p-2.5 border border-neutral-300 hover:border-black text-neutral-600 hover:text-black bg-white transition-colors"
            title="Refresh Analysis"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          <button
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
            className="px-4 py-2 text-xs font-mono uppercase tracking-wider border border-black bg-black text-white hover:bg-neutral-800 transition-colors flex items-center gap-2 font-bold cursor-pointer disabled:opacity-50"
            title="Download PDF Audit Report"
          >
            {downloadingPdf ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Downloading...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Download PDF Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="flex border-b border-neutral-200 overflow-x-auto gap-1">
        {[
          { key: "overview", label: "Executive Risk Overview", icon: Layers },
          { key: "clauses", label: `Clauses (${clauses.length})`, icon: FileText },
          { key: "deadlines", label: `Deadlines (${deadlines.length})`, icon: Clock },
          { key: "text", label: "Redacted Text", icon: ShieldCheck },
          { key: "chat", label: "AI RAG Assistant", icon: MessageSquare },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-3 text-xs font-mono uppercase tracking-wider border-b-2 flex items-center gap-2 transition-all whitespace-nowrap ${
                isActive
                  ? "border-black text-black font-bold bg-neutral-100"
                  : "border-transparent text-neutral-600 hover:text-black hover:border-neutral-300"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      <div className="space-y-6">
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <RiskScoreGauge
                  score={doc.overall_risk_score}
                  band={doc.risk_band || "medium"}
                />
              </div>

              <div className="lg:col-span-2 grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between shadow-sm">
                  <span className="text-[10px] font-mono text-neutral-500 uppercase tracking-wider block font-semibold">
                    Total Clauses
                  </span>
                  <span className="font-serif text-3xl font-bold text-black mt-1">
                    {clauses.length}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-500 mt-2 block">
                    Segmented by spaCy
                  </span>
                </div>

                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between shadow-sm">
                  <span className="text-[10px] font-mono text-red-600 uppercase tracking-wider block font-semibold">
                    Unfavorable
                  </span>
                  <span className="font-serif text-3xl font-bold text-red-600 mt-1">
                    {unfavorableCount}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-500 mt-2 block">
                    High legal liability
                  </span>
                </div>

                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between shadow-sm">
                  <span className="text-[10px] font-mono text-amber-600 uppercase tracking-wider block font-semibold">
                    Needs Review
                  </span>
                  <span className="font-serif text-3xl font-bold text-amber-600 mt-1">
                    {reviewCount}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-500 mt-2 block">
                    Human check flagged
                  </span>
                </div>

                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between shadow-sm">
                  <span className="text-[10px] font-mono text-green-600 uppercase tracking-wider block font-semibold">
                    Fair / Standard
                  </span>
                  <span className="font-serif text-3xl font-bold text-green-600 mt-1">
                    {fairCount}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-500 mt-2 block">
                    Balanced terms
                  </span>
                </div>

                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between col-span-2 shadow-sm">
                  <span className="text-[10px] font-mono text-neutral-500 uppercase tracking-wider block font-semibold">
                    Missing Expected Clauses
                  </span>
                  <span className="font-serif text-3xl font-bold text-black mt-1">
                    {missingClauses.length}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-600 mt-2 block">
                    Identified via set-difference checklist
                  </span>
                </div>

                <div className="border border-neutral-200 bg-white p-4 flex flex-col justify-between col-span-2 shadow-sm">
                  <span className="text-[10px] font-mono text-neutral-500 uppercase tracking-wider block font-semibold">
                    Time-Sensitive Deadlines
                  </span>
                  <span className="font-serif text-3xl font-bold text-black mt-1">
                    {deadlines.length}
                  </span>
                  <span className="text-[11px] font-mono text-neutral-600 mt-2 block">
                    Notice windows & renewal dates
                  </span>
                </div>
              </div>
            </div>

            <MissingClauseList missingClauses={missingClauses} />

            <PiiSummaryPanel documentId={doc.id} />
          </div>
        )}

        {activeTab === "clauses" && (
          <ClauseList
            clauses={clauses}
            selectedClauseId={selectedClauseId}
            onSelectClause={setSelectedClauseId}
          />
        )}

        {activeTab === "deadlines" && (
          <DeadlineTimeline deadlines={deadlines} />
        )}

        {activeTab === "text" && (
          <RedactedTextViewer
            redactedText={doc.redacted_text}
            clauses={clauses}
            selectedClauseId={selectedClauseId}
            onSelectClause={handleSelectClause}
          />
        )}

        {activeTab === "chat" && (
          <ChatPanel
            documentId={doc.id}
            documentType={doc.document_type}
            clauses={clauses}
            onSelectClause={handleSelectClause}
          />
        )}
      </div>
    </div>
  );
}
