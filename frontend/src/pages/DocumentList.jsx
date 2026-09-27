import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { Badge } from "../components/common/Badge";
import {
  FileText,
  Trash2,
  ExternalLink,
  Download,
  AlertTriangle,
  UploadCloud,
  RefreshCw,
  Search,
  Filter,
} from "lucide-react";

export function DocumentList({ onNavigate }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [deletingId, setDeletingId] = useState(null);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const data = await api.getDocuments();
      setDocuments(data || []);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to load document list.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this document and all its derived analysis?")) {
      return;
    }

    setDeletingId(id);
    try {
      await api.deleteDocument(id);
      setDocuments((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      alert("Failed to delete document: " + err.message);
    } finally {
      setDeletingId(null);
    }
  };

  const filteredDocs = documents.filter((doc) => {
    const matchesSearch =
      doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.document_type.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = typeFilter === "all" || doc.document_type === typeFilter;
    return matchesSearch && matchesType;
  });

  const getDocTypeLabel = (type) => {
    switch (type) {
      case "rental_agreement":
        return "Rental / Lease";
      case "job_offer_letter":
        return "Job Offer";
      case "insurance_policy":
        return "Insurance (HO-4)";
      default:
        return type;
    }
  };

  return (
    <div className="space-y-8 py-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-rule pb-4">
        <div>
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider block">
            Workspace Repository
          </span>
          <h1 className="font-serif text-3xl font-bold text-white">
            Analyzed Legal Documents
          </h1>
          <p className="text-xs text-zinc-400 mt-1 font-sans">
            Review past risk audits, inspect classified clauses, and retrieve grounded answers.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchDocuments}
            disabled={loading}
            className="p-2 border border-rule hover:border-white/40 text-zinc-400 hover:text-white transition-colors"
            title="Refresh documents"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>

          <button
            onClick={() => onNavigate("upload")}
            className="px-4 py-2 text-xs font-mono uppercase tracking-wider border border-white bg-white text-black hover:bg-zinc-200 transition-colors flex items-center gap-2 font-semibold"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload New</span>
          </button>
        </div>
      </div>

      {/* Filter / Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-zinc-500" />
          <input
            type="text"
            placeholder="Search by filename or document type..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-paper-dim border border-rule pl-9 pr-4 py-2.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-white font-sans"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-zinc-500 hidden sm:block" />
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="bg-paper-dim border border-rule px-3 py-2.5 text-xs font-mono text-white focus:outline-none focus:border-white"
          >
            <option value="all">All Document Types</option>
            <option value="rental_agreement">Rental / Lease Agreements</option>
            <option value="job_offer_letter">Job Offer Letters</option>
            <option value="insurance_policy">Insurance Policies</option>
          </select>
        </div>
      </div>

      {/* Loading state */}
      {loading ? (
        <div className="border border-rule bg-paper-dim p-12 text-center space-y-3 animate-pulse">
          <div className="w-8 h-8 border border-white/20 mx-auto"></div>
          <p className="text-xs font-mono text-zinc-400">Loading document repository...</p>
        </div>
      ) : error ? (
        <div className="border border-red-500/40 bg-red-950/20 p-6 text-center space-y-3 font-mono text-xs text-red-300">
          <AlertTriangle className="w-6 h-6 mx-auto text-red-400" />
          <p>{error}</p>
          <button
            onClick={fetchDocuments}
            className="px-4 py-1.5 border border-red-500/50 bg-red-900/30 text-white uppercase tracking-wider"
          >
            Retry
          </button>
        </div>
      ) : filteredDocs.length === 0 ? (
        <div className="border border-rule bg-paper-dim p-12 text-center space-y-4">
          <FileText className="w-10 h-10 text-zinc-600 mx-auto" />
          <div>
            <h3 className="font-serif text-lg font-bold text-white mb-1">
              No documents found
            </h3>
            <p className="text-xs text-zinc-400 max-w-sm mx-auto font-sans leading-relaxed">
              {searchQuery || typeFilter !== "all"
                ? "No uploaded documents match your current filter criteria."
                : "Upload your first residential lease, job offer, or insurance policy to begin automated risk analysis."}
            </p>
          </div>
          <button
            onClick={() => onNavigate("upload")}
            className="px-5 py-2 text-xs font-mono uppercase tracking-wider border border-white bg-white text-black hover:bg-zinc-200 transition-colors inline-flex items-center gap-2"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload Document</span>
          </button>
        </div>
      ) : (
        /* Document Cards / Grid */
        <div className="grid grid-cols-1 gap-4">
          {filteredDocs.map((doc) => {
            const isAnalyzed = doc.status === "analyzed";
            const score = doc.overall_risk_score;
            const band = doc.risk_band || "medium";

            return (
              <div
                key={doc.id}
                onClick={() => onNavigate("analysis", { documentId: doc.id })}
                className="border border-rule bg-paper-dim p-5 hover:border-white/40 transition-all cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-xs text-zinc-500 uppercase border border-rule px-1.5 py-0.5">
                      {doc.original_format || "PDF"}
                    </span>
                    <h3 className="font-serif text-base font-bold text-white truncate max-w-md">
                      {doc.filename}
                    </h3>
                    <Badge variant="default" className="text-zinc-400">
                      {getDocTypeLabel(doc.document_type)}
                    </Badge>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono text-zinc-400 flex-wrap">
                    <span>Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}</span>
                    {doc.page_count && <span>• {doc.page_count} pages</span>}
                    {doc.model_version && <span>• Model: {doc.model_version}</span>}
                  </div>
                </div>

                {/* Status & Risk Score Section */}
                <div className="flex items-center gap-4 sm:gap-6 self-stretch sm:self-auto justify-between sm:justify-end border-t sm:border-t-0 border-rule pt-3 sm:pt-0">
                  {isAnalyzed ? (
                    <div className="text-right">
                      <div className="flex items-center gap-2">
                        <span className="font-serif text-2xl font-bold text-white">
                          {score !== null ? Math.round(score) : "—"}
                        </span>
                        <Badge variant={band}>{band}</Badge>
                      </div>
                      <span className="text-[10px] font-mono text-zinc-500 uppercase block">
                        Composite Risk / 100
                      </span>
                    </div>
                  ) : (
                    <div className="text-right">
                      <Badge variant="info">{doc.status}</Badge>
                      <span className="text-[10px] font-mono text-zinc-500 block uppercase mt-0.5">
                        {doc.processing_stage || "Queued"}
                      </span>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    {isAnalyzed && (
                      <a
                        href={api.getReportPdfUrl(doc.id)}
                        target="_blank"
                        rel="noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="p-2 border border-rule hover:border-white/40 text-zinc-400 hover:text-white transition-colors"
                        title="Download PDF Audit Report"
                      >
                        <Download className="w-4 h-4" />
                      </a>
                    )}

                    <button
                      onClick={(e) => handleDelete(e, doc.id)}
                      disabled={deletingId === doc.id}
                      className="p-2 border border-rule hover:border-red-500 text-zinc-400 hover:text-red-400 transition-colors disabled:opacity-40"
                      title="Delete document and analysis"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
