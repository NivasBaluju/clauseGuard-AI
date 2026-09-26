import React from "react";
import { Navbar } from "./Navbar";
import { DisclaimerBanner } from "../common/DisclaimerBanner";

export function PageShell({ children, currentView, onNavigate }) {
  return (
    <div className="min-h-screen bg-paper text-ink flex flex-col selection:bg-white selection:text-black">
      <Navbar currentView={currentView} onNavigate={onNavigate} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="border-t border-rule bg-paper-dim py-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <DisclaimerBanner />
          <div className="flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-zinc-500 gap-4">
            <div>
              <span>ClauseGuard AI © 2026. Built with Presidio, BERT, Gemini API & pgvector.</span>
            </div>
            <div className="flex gap-4">
              <span>Rental Agreements</span>
              <span>•</span>
              <span>Job Offer Letters</span>
              <span>•</span>
              <span>Insurance Policies</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
