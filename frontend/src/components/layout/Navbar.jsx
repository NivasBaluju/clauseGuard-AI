import React from "react";
import { ShieldAlert, FileText, UploadCloud, Compass } from "lucide-react";

export function Navbar({ currentView, onNavigate }) {
  return (
    <header className="border-b border-rule bg-paper sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <button
          onClick={() => onNavigate("landing")}
          className="flex items-center gap-3 text-left group"
        >
          <div className="w-8 h-8 border border-white/20 bg-zinc-950 flex items-center justify-center text-white group-hover:border-white transition-colors">
            <ShieldAlert className="w-4 h-4 text-red-500" />
          </div>
          <div>
            <span className="font-serif text-lg font-bold tracking-tight text-white block">
              ClauseGuard AI
            </span>
            <span className="text-[10px] font-mono text-zinc-500 tracking-wider uppercase block -mt-1">
              Legal Risk Analyzer
            </span>
          </div>
        </button>

        {/* Navigation items */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={() => onNavigate("landing")}
            className={`px-3 py-2 text-xs font-mono uppercase tracking-wider transition-colors border ${
              currentView === "landing"
                ? "border-white/40 text-white bg-white/5"
                : "border-transparent text-zinc-400 hover:text-white hover:border-white/10"
            }`}
          >
            Overview
          </button>

          <button
            onClick={() => onNavigate("documents")}
            className={`px-3 py-2 text-xs font-mono uppercase tracking-wider transition-colors border ${
              currentView === "documents"
                ? "border-white/40 text-white bg-white/5"
                : "border-transparent text-zinc-400 hover:text-white hover:border-white/10"
            }`}
          >
            Documents
          </button>

          <button
            onClick={() => onNavigate("upload")}
            className="ml-2 px-4 py-2 text-xs font-mono uppercase tracking-wider border border-white text-black bg-white hover:bg-zinc-200 transition-colors flex items-center gap-2"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            Upload Document
          </button>
        </nav>
      </div>
    </header>
  );
}
