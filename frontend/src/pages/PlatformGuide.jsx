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
      icon: BookOpen,
      badge: "Overview",
    },
    {
      id: "pii",
      title: "2. Privacy & PII Redaction",
      icon: ShieldCheck,
      badge: "Security",
    },
    {
      id: "classification",
      title: "3. ML Clause Classification",
      icon: Cpu,
      badge: "Neural Models",
    },
    {
      id: "risk",
      title: "4. Risk Scoring Engine",
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
      badge: "Neural RAG",
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
      <div className="border border-neutral-800 bg-neutral-950 p-6 rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-neutral-900 border border-neutral-700 flex items-center justify-center text-white shrink-0">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-serif text-2xl font-bold text-white">
                Platform Guide & Architecture Tour
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-neutral-900 border border-neutral-700 text-neutral-300">
                Official Manual
              </span>
            </div>
            <p className="text-xs font-mono text-neutral-400 mt-1">
              Master how ClauseGuard AI audits legal agreements, computes risk scores, detects deadlines, and powers grounded AI assistance.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => onNavigate("upload")}
            className="px-4 py-2 bg-white hover:bg-neutral-200 text-black text-xs font-mono font-medium rounded flex items-center gap-2 transition-colors"
          >
            <UploadCloud size={14} />
            <span>Upload Document</span>
          </button>
          <button
            onClick={() => onNavigate("chat")}
            className="px-4 py-2 border border-neutral-700 bg-neutral-900 text-white hover:bg-neutral-800 text-xs font-mono rounded flex items-center gap-2 transition-colors"
          >
            <Bot size={14} />
            <span>Try AI Copilot</span>
          </button>
        </div>
      </div>

      {/* Guide Content: Sidebar Tabs + Detailed Explanation */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Navigation list */}
        <div className="lg:col-span-1 space-y-1.5 bg-neutral-950 p-3 rounded-lg border border-neutral-800">
          <div className="text-[10px] font-mono text-neutral-500 uppercase px-3 py-1 tracking-wider">
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
                    ? "bg-white text-black font-semibold"
                    : "text-neutral-400 hover:text-white hover:bg-neutral-900 border border-transparent"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Icon size={14} className={isActive ? "text-black" : "text-neutral-500"} />
                  <span className="truncate">{sec.title}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Content Panel */}
        <div className="lg:col-span-3 bg-neutral-950 border border-neutral-800 rounded-xl p-6 sm:p-8 space-y-6">
          {/* 1. Quickstart */}
          {activeSection === "quickstart" && (
            <div className="space-y-6">
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Step 1
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  How Does ClauseGuard AI Work?
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  A high-level overview of uploading a legal document and reviewing automated risk findings.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-lg bg-neutral-900 border border-neutral-800 space-y-2">
                  <div className="w-7 h-7 rounded bg-neutral-800 border border-neutral-700 text-white flex items-center justify-center font-bold text-xs">
                    1
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Upload Contract</h3>
                  <p className="text-xs text-neutral-400">
                    Upload any PDF, DOCX, or TXT file under 20MB. Select your document type: Residential Lease, Job Offer, or Insurance Specimen.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-neutral-900 border border-neutral-800 space-y-2">
                  <div className="w-7 h-7 rounded bg-neutral-800 border border-neutral-700 text-white flex items-center justify-center font-bold text-xs">
                    2
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Autonomous Audit</h3>
                  <p className="text-xs text-neutral-400">
                    Text is sanitized with Microsoft Presidio PII redaction, segmented via spaCy, and evaluated with fine-tuned context-windowed BERT models.
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-neutral-900 border border-neutral-800 space-y-2">
                  <div className="w-7 h-7 rounded bg-neutral-800 border border-neutral-700 text-white flex items-center justify-center font-bold text-xs">
                    3
                  </div>
                  <h3 className="font-serif text-sm font-bold text-white">Inspect & Inquire</h3>
                  <p className="text-xs text-neutral-400">
                    Explore the overall Risk Score (0-100), review flagged unfair terms, track deadlines, and ask the AI Copilot for contract advice.
                  </p>
                </div>
              </div>

              <div className="p-4 bg-neutral-900 border border-neutral-800 rounded-lg flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-mono font-bold text-white">Ready to try your first document?</h4>
                  <p className="text-xs text-neutral-400 mt-0.5">We provide instant analysis on security deposits, notice periods, and liabilities.</p>
                </div>
                <button
                  onClick={() => onNavigate("upload")}
                  className="px-3.5 py-1.5 bg-white hover:bg-neutral-200 text-black text-xs font-mono font-medium rounded transition-colors shrink-0"
                >
                  Go to Upload →
                </button>
              </div>
            </div>
          )}

          {/* 2. PII Redaction */}
          {activeSection === "pii" && (
            <div className="space-y-6">
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Privacy Safeguards
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Zero-PII Leakage Architecture
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  How client confidential data is stripped before any AI classifier or cloud service sees it.
                </p>
              </div>

              <div className="space-y-3 text-xs leading-relaxed text-neutral-300">
                <p>
                  ClauseGuard AI utilizes <strong>Microsoft Presidio Analyzer and Anonymizer</strong> to sanitize document text before segmentation or classification. Personal identifiers are replaced with anonymous cryptographic tokens:
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-[11px]">
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;PERSON&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;EMAIL_ADDRESS&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;PHONE_NUMBER&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;LOCATION&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;US_SSN&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;CREDIT_CARD&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;IP_ADDRESS&gt;</div>
                  <div className="p-2.5 rounded bg-neutral-900 border border-neutral-800 text-neutral-200">&lt;IBAN_CODE&gt;</div>
                </div>
                <div className="p-3 bg-neutral-900 border border-neutral-700 rounded text-neutral-300 text-xs">
                  <strong>Notice on Calendar Dates:</strong> Date entities (e.g. "October 1, 2026", "30 days") are deliberately excluded from PII redaction so that the deadline detection module can calculate legal notice periods accurately.
                </div>
              </div>
            </div>
          )}

          {/* 3. ML Models */}
          {activeSection === "classification" && (
            <div className="space-y-6">
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Natural Language Processing
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Dual-Task Context-Windowed BERT Classification
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  How clauses are categorized and assessed for tenant, employee, or policyholder favorability.
                </p>
              </div>

              <div className="space-y-4 text-xs text-neutral-300 leading-relaxed">
                <p>
                  Every segmented clause is processed by two fine-tuned transformers:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-lg bg-neutral-900 border border-neutral-800 space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Task 1: Clause Type Identification</h4>
                    <p className="text-neutral-400">
                      Identifies the exact legal domain of the clause (e.g., <em>Security Deposit, Termination, Non-Compete, Governing Law, Indemnification</em>).
                    </p>
                  </div>
                  <div className="p-4 rounded-lg bg-neutral-900 border border-neutral-800 space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Task 2: Favorability Labeling</h4>
                    <p className="text-neutral-400">
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
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Scoring Math
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Deterministic Risk Score Calculation
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  How ClauseGuard AI synthesizes clause favorability and missing protection checklists into a 0–100 score.
                </p>
              </div>

              <div className="space-y-4 text-xs text-neutral-300 leading-relaxed">
                <p>
                  The overall risk score ranges from <strong>0 (No Risk)</strong> to <strong>100 (Critical Risk)</strong>:
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded text-center">
                    <span className="text-white font-bold font-serif text-lg block">0 — 33</span>
                    <span className="text-[10px] font-mono text-neutral-400 uppercase">Low Risk (Standard)</span>
                  </div>
                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded text-center">
                    <span className="text-white font-bold font-serif text-lg block">34 — 66</span>
                    <span className="text-[10px] font-mono text-neutral-400 uppercase">Medium Risk (Review Advised)</span>
                  </div>
                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded text-center">
                    <span className="text-white font-bold font-serif text-lg block">67 — 100</span>
                    <span className="text-[10px] font-mono text-neutral-400 uppercase">High Risk (Severe Liabilities)</span>
                  </div>
                </div>

                <div className="p-4 bg-neutral-900 border border-neutral-800 rounded-lg space-y-2">
                  <h4 className="font-serif font-bold text-sm text-white">Missing Clause Penalties</h4>
                  <p className="text-neutral-400">
                    A contract is not just risky because of what it says—it is also risky because of what it <em>omits</em>. For example, a residential lease that lacks a <strong>Security Deposit Return Timeline</strong> or a <strong>Landlord Repair Obligation</strong> receives automated penalty points added directly to the risk score.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 5. Deadlines */}
          {activeSection === "deadlines" && (
            <div className="space-y-6">
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Obligations
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Time-Sensitive Deadlines & Notice Windows
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  Detecting critical statutory and contractual countdowns.
                </p>
              </div>

              <div className="space-y-4 text-xs text-neutral-300 leading-relaxed">
                <p>
                  The system scans every clause for explicit timeframes, relative notice periods, and critical dates:
                </p>
                <div className="space-y-2">
                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Notice to Vacate:</strong>
                      <span className="text-neutral-400 ml-2">Identifies required notice windows (e.g. 30, 60 days before expiration).</span>
                    </div>
                    <span className="text-[10px] font-mono text-neutral-300 border border-neutral-700 px-2 py-0.5 rounded">30-60 Days</span>
                  </div>

                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Security Deposit Refund:</strong>
                      <span className="text-neutral-400 ml-2">Tracks statutory return windows following surrender of premises.</span>
                    </div>
                    <span className="text-[10px] font-mono text-neutral-300 border border-neutral-700 px-2 py-0.5 rounded">14-30 Days</span>
                  </div>

                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Rent Due & Grace Periods:</strong>
                      <span className="text-neutral-400 ml-2">Monitors payment due dates and late charge assessment grace days.</span>
                    </div>
                    <span className="text-[10px] font-mono text-neutral-300 border border-neutral-700 px-2 py-0.5 rounded">1st–5th Day</span>
                  </div>

                  <div className="p-3 bg-neutral-900 border border-neutral-800 rounded flex items-center justify-between">
                    <div>
                      <strong className="text-white">Right of Entry Inspection:</strong>
                      <span className="text-neutral-400 ml-2">Verifies advance notice landlord must give prior to entering premises.</span>
                    </div>
                    <span className="text-[10px] font-mono text-neutral-300 border border-neutral-700 px-2 py-0.5 rounded">24-48 Hours</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 6. AI Copilot */}
          {activeSection === "copilot" && (
            <div className="space-y-6">
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Grounded Intelligence
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  ClauseGuard Grounded AI Legal Copilot
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  How semantic retrieval and vector embeddings ensure accurate answers with exact citations.
                </p>
              </div>

              <div className="space-y-4 text-xs text-neutral-300 leading-relaxed">
                <p>
                  You can chat with ClauseGuard AI at any time—either across the whole platform or locked to a specific uploaded document.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded bg-neutral-900 border border-neutral-800 space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Grounded Citations</h4>
                    <p className="text-neutral-400">
                      When analyzing an agreement, every answer is verified against the document text. The assistant displays exact clause excerpts as citations.
                    </p>
                  </div>
                  <div className="p-4 rounded bg-neutral-900 border border-neutral-800 space-y-2">
                    <h4 className="font-serif font-bold text-sm text-white">Legal Guidance & Negotiation</h4>
                    <p className="text-neutral-400">
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
              <div className="border-b border-neutral-800 pb-4">
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-neutral-900 text-neutral-300 border border-neutral-700">
                  Compliance
                </span>
                <h2 className="font-serif text-xl font-bold text-white mt-2">
                  Audit & Compliance Trail
                </h2>
                <p className="text-xs font-mono text-neutral-400 mt-1">
                  Cryptographic, immutable activity tracking for enterprise and legal compliance.
                </p>
              </div>

              <div className="space-y-4 text-xs text-neutral-300 leading-relaxed">
                <p>
                  Every operation on the platform is logged in our database <code>audit_logs</code> table:
                </p>
                <ul className="list-disc pl-5 space-y-1.5 text-neutral-400">
                  <li><strong>Document Ingestion:</strong> Timestamp, original filename, format, and document UUID.</li>
                  <li><strong>Analysis Completion:</strong> Final computed risk score, risk band, and clause counts.</li>
                  <li><strong>AI Inquiries:</strong> Questions posed to the AI copilot, grounding status, and confidence metrics.</li>
                  <li><strong>Security Events:</strong> User sign-ins, registrations, failed attempts, and session revocations.</li>
                </ul>
                <div className="pt-2">
                  <button
                    onClick={() => onNavigate("audit")}
                    className="px-4 py-2 border border-neutral-700 bg-neutral-900 text-white hover:bg-neutral-800 rounded text-xs font-mono flex items-center gap-2 transition-colors"
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
