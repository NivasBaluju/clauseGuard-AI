import React, { useState } from "react";
import {
  BookOpen,
  ShieldCheck,
  Cpu,
  FileText,
  Clock,
  Bot,
  Activity,
  UploadCloud,
  CheckCircle,
  ArrowRight,
  HelpCircle,
  Lock,
  AlertTriangle,
  Layers,
} from "lucide-react";

export function PlatformGuide({ onNavigate }) {
  const [activeSection, setActiveSection] = useState("quickstart");

  const sections = [
    {
      id: "quickstart",
      title: "1. Quick Start Workflow",
      icon: UploadCloud,
      badge: "Start Here",
    },
    {
      id: "pii",
      title: "2. Zero-PII Redaction Engine",
      icon: Lock,
      badge: "Privacy",
    },
    {
      id: "classification",
      title: "3. ML Clause Classification",
      icon: Cpu,
      badge: "AI Models",
    },
    {
      id: "risk",
      title: "4. Risk Scoring & Missing Clauses",
      icon: AlertTriangle,
      badge: "Risk Engine",
    },
    {
      id: "deadlines",
      title: "5. Deadlines & Notice Windows",
      icon: Clock,
      badge: "Timelines",
    },
    {
      id: "copilot",
      title: "6. Grounded AI Legal Copilot",
      icon: Bot,
      badge: "Gemini RAG",
    },
    {
      id: "audit",
      title: "7. Audit & Compliance Trail",
      icon: Activity,
      badge: "Governance",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="border border-[#1f293d] bg-[#0f1420] p-6 rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-950/60 border border-blue-500/40 flex items-center justify-center text-blue-400 shrink-0">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-serif text-2xl font-bold text-white">
                Platform Guide & Architecture Tour
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/30 text-emerald-300">
                Official Manual
              </span>
            </div>
            <p className="text-xs font-mono text-zinc-400 mt-1">
              Master how ClauseGuard AI audits legal agreements, computes risk scores, detects deadlines, and powers grounded AI assistance.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => onNavigate("upload")}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-mono font-medium rounded flex items-center gap-2 transition-colors shadow-lg shadow-blue-600/20"
          >
            <UploadCloud size={14} />
            <span>Upload Document</span>
          </button>
          <button
            onClick={() => onNavigate("chat")}
            className="px-4 py-2 border border-blue-500/40 bg-blue-950/30 text-blue-300 hover:bg-blue-900/40 text-xs font-mono rounded flex items-center gap-2 transition-colors"
          >
            <Bot size={14} />
            <span>Try AI Copilot</span>
          </button>
        </div>
      </div>

      {/* Guide Content: Sidebar Tabs + Detailed Explanation */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Navigation list */}
        <div className="lg:col-span-1 space-y-1.5 bg-[#0c1017] p-3 rounded-lg border border-[#1a2233]">
          <div className="text-[10px] font-mono text-zinc-500 uppercase px-3 py-1 tracking-wider">
            Table of Contents
          </div>
          {sections.map((sec) => {
            const Icon = sec.icon;
            const isActive = activeSection === sec.id;
            return (
              <button
                key={sec.id}
                onClick={() => setActiveSection(sec.id)}
                className={`w-full text-left px-3 py-2.5 rounded-md text-xs font-mono flex items-center justify-between transition-all ${
                  isActive
                    ? "bg-blue-600/15 border border-blue-500/40 text-blue-300 font-semibold"
                    : "text-zinc-400 hover:text-white hover:bg-white/5 border border-transparent"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon size={14} className={isActive ? "text-blue-400" : "text-zinc-500"} />
                  <span className="truncate">{sec.title}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Content Panel */}
        <div className="lg:col-span-3 bg-[#0f1420] border border-[#1f293d] rounded-xl p-6 sm:p-8 space-y-6">
          {/* 1. Quickstart */}
          {activeSection === "quickstart" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-500/30">
                  Step 1
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  How Does ClauseGuard AI Work?
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  A high-level overview of uploading a legal document and reviewing automated risk findings.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-lg bg-[#131822] border border-[#1f293d] space-y-2">
                  <div className="w-7 h-7 rounded bg-blue-600/20 text-blue-400 flex items-center justify-center font-bold text-xs">
                    1
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Upload Contract</h3>
                  <p className="text-xs text-zinc-400">
                    Upload any PDF, DOCX, or TXT file under 20MB. Select your document type: Residential Lease, Job Offer, or Insurance Specimen.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-[#131822] border border-[#1f293d] space-y-2">
                  <div className="w-7 h-7 rounded bg-purple-600/20 text-purple-400 flex items-center justify-center font-bold text-xs">
                    2
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Autonomous Audit</h3>
                  <p className="text-xs text-zinc-400">
                    Text is sanitized with Microsoft Presidio PII redaction, segmented via spaCy, and evaluated with fine-tuned context-windowed BERT models.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-[#131822] border border-[#1f293d] space-y-2">
                  <div className="w-7 h-7 rounded bg-emerald-600/20 text-emerald-400 flex items-center justify-center font-bold text-xs">
                    3
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Inspect & Inquire</h3>
                  <p className="text-xs text-zinc-400">
                    Explore the overall Risk Score (0-100), review flagged unfair terms, track deadlines, and ask the AI Copilot for contract advice.
                  </p>
                </div>
              </div>

              <div className="p-4 bg-blue-950/20 border border-blue-500/30 rounded-lg flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-mono font-bold text-blue-300">Ready to try your first document?</h4>
                  <p className="text-xs text-zinc-400 mt-0.5">We provide instant analysis on security deposits, notice periods, and liabilities.</p>
                </div>
                <button
                  onClick={() => onNavigate("upload")}
                  className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-mono font-medium rounded transition-colors shrink-0"
                >
                  Go to Upload →
                </button>
              </div>
            </div>
          )}

          {/* 2. PII Redaction */}
          {activeSection === "pii" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-500/30">
                  Privacy Safeguards
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Zero-PII Leakage Architecture
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  How client confidential data is stripped before any AI classifier or cloud service sees it.
                </p>
              </div>

              <div className="space-y-3 text-xs leading-relaxed text-zinc-300">
                <p>
                  ClauseGuard AI utilizes **Microsoft Presidio Analyzer and Anonymizer** to sanitize document text before segmentation or classification. Personal identifiers are replaced with anonymous cryptographic tokens:
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-[11px]">
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;PERSON&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;EMAIL_ADDRESS&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;PHONE_NUMBER&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;LOCATION&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;US_SSN&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;CREDIT_CARD&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;IP_ADDRESS&gt;</div>
                  <div className="p-2.5 rounded bg-[#131822] border border-[#1f293d] text-emerald-300">&lt;IBAN_CODE&gt;</div>
                </div>
                <div className="p-3 bg-amber-950/20 border border-amber-500/30 rounded text-amber-300 text-xs">
                  <strong>Notice on Calendar Dates:</strong> Date entities (e.g. "October 1, 2026", "30 days") are deliberately excluded from PII redaction so that the deadline detection module can calculate legal notice periods accurately.
                </div>
              </div>
            </div>
          )}

          {/* 3. ML Models */}
          {activeSection === "classification" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-purple-950/80 text-purple-300 border border-purple-500/30">
                  Natural Language Processing
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Dual-Task Context-Windowed BERT Classification
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  How clauses are categorized and assessed for tenant, employee, or policyholder favorability.
                </p>
              </div>

              <div className="space-y-4 text-xs text-zinc-300 leading-relaxed">
                <p>
                  Every segmented clause is processed by two fine-tuned transformers:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-lg bg-[#131822] border border-[#1f293d] space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Task 1: Clause Type Identification</h4>
                    <p className="text-zinc-400">
                      Identifies the exact legal domain of the clause (e.g., <em>Security Deposit, Termination, Non-Compete, Governing Law, Indemnification</em>).
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-[#131822] border border-[#1f293d] space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Task 2: Favorability Labeling</h4>
                    <p className="text-zinc-400">
                      Determines if the clause is <strong>Unfavorable</strong> (high liability / aggressive terms), <strong>Needs Review</strong> (unclear or asymmetric terms), or <strong>Fair</strong> (standard industry protection).
                    </p>
                  </div>
                </div>
                <p>
                  <strong>Context-Windowing:</strong> The model looks at the preceding clause and the succeeding clause with <code>[TARGET] ... [/TARGET]</code> markers to understand context continuity across sections.
                </p>
              </div>
            </div>
          )}

          {/* 4. Risk Engine */}
          {activeSection === "risk" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-red-950/80 text-red-300 border border-red-500/30">
                  Scoring Math
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Deterministic Risk Score Calculation
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  How ClauseGuard AI synthesizes clause favorability and missing protection checklists into a 0–100 score.
                </p>
              </div>

              <div className="space-y-4 text-xs text-zinc-300 leading-relaxed">
                <p>
                  The overall risk score ranges from <strong>0 (No Risk)</strong> to <strong>100 (Critical Risk)</strong>:
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="p-3 bg-emerald-950/20 border border-emerald-500/30 rounded text-center">
                    <span className="text-emerald-400 font-bold font-serif text-lg block">0 — 33</span>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase">Low Risk (Standard)</span>
                  </div>
                  <div className="p-3 bg-amber-950/20 border border-amber-500/30 rounded text-center">
                    <span className="text-amber-400 font-bold font-serif text-lg block">34 — 66</span>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase">Medium Risk (Review Advised)</span>
                  </div>
                  <div className="p-3 bg-red-950/20 border border-red-500/30 rounded text-center">
                    <span className="text-red-400 font-bold font-serif text-lg block">67 — 100</span>
                    <span className="text-[10px] font-mono text-zinc-400 uppercase">High Risk (Severe Liabilities)</span>
                  </div>
                </div>

                <div className="p-4 bg-[#131822] border border-[#1f293d] rounded-lg space-y-2">
                  <h4 className="font-serif font-bold text-sm text-white">Missing Clause Penalties</h4>
                  <p className="text-zinc-400">
                    A contract is not just risky because of what it says—it is also risky because of what it <em>omits</em>. For example, a residential lease that lacks a <strong>Security Deposit Return Timeline</strong> or a <strong>Landlord Repair Obligation</strong> receives automated penalty points added directly to the risk score.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 5. Deadlines */}
          {activeSection === "deadlines" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-500/30">
                  Obligations
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Time-Sensitive Deadlines & Notice Windows
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  Detecting critical statutory and contractual countdowns.
                </p>
              </div>

              <div className="space-y-4 text-xs text-zinc-300 leading-relaxed">
                <p>
                  The system scans every clause for explicit timeframes, relative notice periods, and critical dates:
                </p>
                <div className="space-y-2">
                  <div className="p-3 bg-[#131822] border border-[#1f293d] rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Notice to Vacate:</strong>
                      <span className="text-zinc-400 ml-2">Identifies required notice windows (e.g. 30, 60 days before expiration).</span>
                    </div>
                    <span className="text-[10px] font-mono text-blue-400 border border-blue-500/30 px-2 py-0.5 rounded">30-60 Days</span>
                  </div>

                  <div className="p-3 bg-[#131822] border border-[#1f293d] rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Security Deposit Refund:</strong>
                      <span className="text-zinc-400 ml-2">Tracks statutory return windows following surrender of premises.</span>
                    </div>
                    <span className="text-[10px] font-mono text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded">14-30 Days</span>
                  </div>

                  <div className="p-3 bg-[#131822] border border-[#1f293d] rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Rent Due & Grace Periods:</strong>
                      <span className="text-zinc-400 ml-2">Monitors payment due dates and late charge assessment grace days.</span>
                    </div>
                    <span className="text-[10px] font-mono text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded">1st–5th Day</span>
                  </div>

                  <div className="p-3 bg-[#131822] border border-[#1f293d] rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Right of Entry Inspection:</strong>
                      <span className="text-zinc-400 ml-2">Verifies advance notice landlord must give prior to entering premises.</span>
                    </div>
                    <span className="text-[10px] font-mono text-purple-400 border border-purple-500/30 px-2 py-0.5 rounded">24-48 Hours</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 6. AI Copilot */}
          {activeSection === "copilot" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-500/30">
                  Grounded Intelligence
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Deciva Grounded AI Legal Copilot
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  How Gemini API and pgvector embeddings ensure accurate answers with exact citations.
                </p>
              </div>

              <div className="space-y-4 text-xs text-zinc-300 leading-relaxed">
                <p>
                  You can chat with Deciva AI at any time—either across the whole platform or locked to a specific uploaded document.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded bg-[#131822] border border-[#1f293d] space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Grounded Citations</h4>
                    <p className="text-zinc-400">
                      When analyzing an agreement, every answer is verified against the document text. The assistant displays exact clause excerpts as citations.
                    </p>
                  </div>
                  <div className="p-4 rounded bg-[#131822] border border-[#1f293d] space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Legal Guidance & Negotiation</h4>
                    <p className="text-zinc-400">
                      Ask about local tenant statutes, non-compete enforceability, indemnification clauses, or negotiate fairer terms with custom counter-proposals.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 7. Audit Trail */}
          {activeSection === "audit" && (
            <div className="space-y-6">
              <div className="border-b border-[#1f293d] pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-purple-950/80 text-purple-300 border border-purple-500/30">
                  Compliance
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Audit & Compliance Trail
                </h2>
                <p className="text-xs font-mono text-zinc-400 mt-1">
                  Cryptographic, immutable activity tracking for enterprise and legal compliance.
                </p>
              </div>

              <div className="space-y-4 text-xs text-zinc-300 leading-relaxed">
                <p>
                  Every operation on the platform is logged in our Neon PostgreSQL <code>audit_logs</code> table:
                </p>
                <ul className="list-disc pl-5 space-y-1.5 text-zinc-400">
                  <li><strong>Document Ingestion:</strong> Timestamp, original filename, format, and document UUID.</li>
                  <li><strong>Analysis Completion:</strong> Final computed risk score, risk band, and clause counts.</li>
                  <li><strong>AI Inquiries:</strong> Questions posed to the AI copilot, grounding status, and confidence metrics.</li>
                  <li><strong>Security Events:</strong> User sign-ins, registrations, failed attempts, and session revocations.</li>
                </ul>
                <div className="pt-2">
                  <button
                    onClick={() => onNavigate("audit")}
                    className="px-4 py-2 border border-purple-500/40 bg-purple-950/40 text-purple-300 hover:bg-purple-900/50 rounded text-xs font-mono flex items-center gap-2 transition-colors"
                  >
                    <Activity size={14} />
                    <span>View Your Audit & Trail Log →</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PlatformGuide;
