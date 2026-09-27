import React, { useState, useEffect } from "react";
import {
  Activity,
  FileText,
  Bot,
  ShieldCheck,
  RefreshCw,
  Search,
  Filter,
  CheckCircle,
  AlertCircle,
  LogIn,
  LogOut,
  UploadCloud,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function AuditTrail({ onNavigate }) {
  const { user } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedLogId, setExpandedLogId] = useState(null);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/audit?limit=200", {
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setLogs(data.logs || []);
      }
    } catch (err) {
      console.error("Failed to load audit logs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  // Filter logs based on category and search
  const filteredLogs = logs.filter((log) => {
    if (filterType === "documents" && !log.action.startsWith("DOC_")) return false;
    if (filterType === "chat" && !log.action.startsWith("CHAT_")) return false;
    if (
      filterType === "auth" &&
      !log.action.startsWith("USER_") &&
      !log.action.startsWith("LOGIN_")
    )
      return false;

    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      const matchAction = log.action.toLowerCase().includes(term);
      const matchUser = (log.user_email || "").toLowerCase().includes(term);
      const matchDetails = JSON.stringify(log.details || {}).toLowerCase().includes(term);
      return matchAction || matchUser || matchDetails;
    }
    return true;
  });

  // KPI counts
  const totalEvents = logs.length;
  const docEvents = logs.filter((l) => l.action.startsWith("DOC_")).length;
  const chatEvents = logs.filter((l) => l.action.startsWith("CHAT_")).length;
  const authEvents = logs.filter(
    (l) => l.action.startsWith("USER_") || l.action.startsWith("LOGIN_")
  ).length;

  const getActionBadge = (action) => {
    switch (action) {
      case "USER_LOGIN":
        return {
          bg: "bg-emerald-950/50 text-emerald-300 border-emerald-500/40",
          icon: LogIn,
          label: "User Sign In",
        };
      case "USER_REGISTER":
        return {
          bg: "bg-blue-950/50 text-blue-300 border-blue-500/40",
          icon: ShieldCheck,
          label: "Account Created",
        };
      case "USER_LOGOUT":
        return {
          bg: "bg-zinc-900 text-zinc-400 border-zinc-700",
          icon: LogOut,
          label: "User Sign Out",
        };
      case "LOGIN_FAILED":
        return {
          bg: "bg-red-950/50 text-red-300 border-red-500/40",
          icon: AlertCircle,
          label: "Failed Login",
        };
      case "DOC_UPLOADED":
        return {
          bg: "bg-blue-950/50 text-blue-300 border-blue-500/40",
          icon: UploadCloud,
          label: "Document Uploaded",
        };
      case "DOC_ANALYZED":
        return {
          bg: "bg-cyan-950/50 text-cyan-300 border-cyan-500/40",
          icon: CheckCircle,
          label: "Analysis Finished",
        };
      case "DOC_DELETED":
        return {
          bg: "bg-red-950/50 text-red-300 border-red-500/40",
          icon: AlertCircle,
          label: "Document Deleted",
        };
      case "CHAT_QUERY":
        return {
          bg: "bg-purple-950/50 text-purple-300 border-purple-500/40",
          icon: Bot,
          label: "AI Copilot Query",
        };
      case "CHAT_OPENED":
        return {
          bg: "bg-purple-950/30 text-purple-400 border-purple-500/20",
          icon: Bot,
          label: "Chat Opened",
        };
      default:
        return {
          bg: "bg-zinc-800 text-zinc-300 border-zinc-700",
          icon: Activity,
          label: action,
        };
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="border border-[#1f293d] bg-[#0f1420] p-6 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-950/60 border border-purple-500/40 flex items-center justify-center text-purple-400 shrink-0">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-serif text-2xl font-bold text-white flex items-center gap-2">
              Audit & Compliance Trail
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950/80 text-purple-300 border border-purple-500/30">
                PostgreSQL Ledger
              </span>
            </h1>
            <p className="text-xs font-mono text-zinc-400 mt-1">
              Immutable chronological record of document uploads, automated risk evaluations, AI copilot queries, and security sessions.
            </p>
          </div>
        </div>

        <button
          onClick={fetchLogs}
          disabled={loading}
          className="px-3.5 py-2 border border-[#1f293d] bg-[#131822] hover:bg-[#1a2233] text-zinc-300 hover:text-white rounded text-xs font-mono flex items-center gap-2 transition-colors"
        >
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
          <span>Refresh Trail</span>
        </button>
      </div>

      {/* KPI Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="border border-[#1f293d] bg-[#0c1017] p-4 rounded-lg flex flex-col justify-between">
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">
            Total Logged Events
          </span>
          <span className="font-serif text-2xl font-bold text-white mt-1">
            {totalEvents}
          </span>
          <span className="text-[10px] font-mono text-zinc-500 mt-1">System-wide actions</span>
        </div>

        <div className="border border-[#1f293d] bg-[#0c1017] p-4 rounded-lg flex flex-col justify-between">
          <span className="text-[10px] font-mono text-blue-400 uppercase tracking-wider">
            Document Ingestions
          </span>
          <span className="font-serif text-2xl font-bold text-blue-300 mt-1">
            {docEvents}
          </span>
          <span className="text-[10px] font-mono text-zinc-500 mt-1">Uploads & Audits</span>
        </div>

        <div className="border border-[#1f293d] bg-[#0c1017] p-4 rounded-lg flex flex-col justify-between">
          <span className="text-[10px] font-mono text-purple-400 uppercase tracking-wider">
            AI Inquiries
          </span>
          <span className="font-serif text-2xl font-bold text-purple-300 mt-1">
            {chatEvents}
          </span>
          <span className="text-[10px] font-mono text-zinc-500 mt-1">Grounded RAG Queries</span>
        </div>

        <div className="border border-[#1f293d] bg-[#0c1017] p-4 rounded-lg flex flex-col justify-between">
          <span className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider">
            Auth & Sessions
          </span>
          <span className="font-serif text-2xl font-bold text-emerald-300 mt-1">
            {authEvents}
          </span>
          <span className="text-[10px] font-mono text-zinc-500 mt-1">Logins & Registrations</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="border border-[#1f293d] bg-[#0f1420] p-4 rounded-lg flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Category Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto">
          {[
            { id: "all", label: "All Events" },
            { id: "documents", label: "Documents" },
            { id: "chat", label: "AI Copilot" },
            { id: "auth", label: "Security & Auth" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilterType(tab.id)}
              className={`px-3 py-1.5 rounded text-xs font-mono whitespace-nowrap transition-colors border ${
                filterType === tab.id
                  ? "bg-white/10 text-white font-semibold border-white/30"
                  : "text-zinc-400 hover:text-white border-transparent hover:bg-white/5"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search size={14} className="absolute left-3 top-2.5 text-zinc-500" />
          <input
            type="text"
            placeholder="Search action or details…"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-[#131822] border border-[#1f293d] rounded text-xs font-mono pl-8 pr-3 py-1.5 text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {/* Trail List Table */}
      <div className="border border-[#1f293d] bg-[#0c1017] rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-zinc-500 animate-pulse">
            Loading audit records from database…
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="p-12 text-center space-y-2">
            <Activity className="w-8 h-8 text-zinc-600 mx-auto" />
            <h4 className="font-serif text-sm text-zinc-300">No Audit Events Found</h4>
            <p className="text-xs font-mono text-zinc-500">
              No actions match the selected filter criteria.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-[#1a2233]">
            {filteredLogs.map((log) => {
              const badge = getActionBadge(log.action);
              const Icon = badge.icon;
              const isExpanded = expandedLogId === log.id;
              const formattedDate = log.created_at
                ? new Date(log.created_at).toLocaleString()
                : "Just now";

              return (
                <div
                  key={log.id}
                  className="p-4 hover:bg-[#0f1420] transition-colors"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-start sm:items-center gap-3">
                      <div
                        className={`w-7 h-7 rounded border flex items-center justify-center shrink-0 ${badge.bg}`}
                      >
                        <Icon size={14} />
                      </div>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span
                            className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${badge.bg}`}
                          >
                            {badge.label}
                          </span>
                          {log.resource_type && (
                            <span className="text-[10px] font-mono text-zinc-400">
                              • {log.resource_type}
                            </span>
                          )}
                          {log.user_email && (
                            <span className="text-[10px] font-mono text-zinc-300 bg-white/5 px-2 py-0.5 rounded">
                              {log.user_email}
                            </span>
                          )}
                        </div>

                        {/* Summary description from details */}
                        <div className="text-xs font-mono text-zinc-300 mt-1">
                          {log.action === "DOC_UPLOADED" && (
                            <span>
                              Uploaded <strong>{log.details?.filename}</strong> (
                              {log.details?.document_type})
                            </span>
                          )}
                          {log.action === "DOC_ANALYZED" && (
                            <span>
                              Analysis completed for <strong>{log.details?.filename}</strong> —
                              Risk Score:{" "}
                              <strong className="text-red-400">
                                {log.details?.overall_risk_score}
                              </strong>{" "}
                              ({log.details?.risk_band})
                            </span>
                          )}
                          {log.action === "CHAT_QUERY" && (
                            <span>
                              Asked: <em>"{log.details?.question}"</em>
                            </span>
                          )}
                          {log.action === "USER_LOGIN" && (
                            <span>
                              Signed in from IP: <code>{log.ip_address || "127.0.0.1"}</code>
                            </span>
                          )}
                          {log.action === "USER_REGISTER" && (
                            <span>Registered account for {log.details?.name}</span>
                          )}
                          {log.action === "DOC_DELETED" && (
                            <span>Deleted document {log.details?.filename}</span>
                          )}
                          {!["DOC_UPLOADED", "DOC_ANALYZED", "CHAT_QUERY", "USER_LOGIN", "USER_REGISTER", "DOC_DELETED"].includes(log.action) && (
                            <span>{JSON.stringify(log.details || {})}</span>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 self-end sm:self-center">
                      <span className="text-[11px] font-mono text-zinc-500 whitespace-nowrap">
                        {formattedDate}
                      </span>
                      <button
                        onClick={() =>
                          setExpandedLogId(isExpanded ? null : log.id)
                        }
                        className="text-zinc-500 hover:text-white p-1 rounded transition-colors"
                        title="Inspect Event JSON"
                      >
                        {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </button>
                    </div>
                  </div>

                  {/* Expanded JSON Inspector */}
                  {isExpanded && (
                    <div className="mt-3 p-3 rounded bg-[#090c12] border border-[#1f293d] text-[11px] font-mono space-y-1">
                      <div className="text-zinc-500 text-[10px] uppercase">Event Payload Metadata:</div>
                      <pre className="text-emerald-400 overflow-x-auto p-2 bg-black/40 rounded">
                        {JSON.stringify(log, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default AuditTrail;
