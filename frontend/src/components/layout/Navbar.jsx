import React from "react";
import { ShieldAlert, FileText, UploadCloud, Bot, LogOut, LogIn, UserPlus, User } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export function Navbar({ currentView, onNavigate }) {
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    if (onNavigate) {
      onNavigate("landing");
    }
  };

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
              Legal Risk Analyzer & Copilot
            </span>
          </div>
        </button>

        {/* Navigation items & Auth */}
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
            onClick={() => onNavigate("chat")}
            className={`px-3 py-2 text-xs font-mono uppercase tracking-wider transition-colors border flex items-center gap-1.5 ${
              currentView === "chat"
                ? "border-blue-400/60 text-blue-300 bg-blue-950/30"
                : "border-transparent text-zinc-400 hover:text-blue-300 hover:border-blue-400/20"
            }`}
          >
            <Bot className="w-3.5 h-3.5 text-blue-400" />
            <span>AI Copilot</span>
          </button>

          <button
            onClick={() => onNavigate("upload")}
            className="px-3.5 py-2 text-xs font-mono uppercase tracking-wider border border-white text-black bg-white hover:bg-zinc-200 transition-colors flex items-center gap-1.5"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Upload Document</span>
            <span className="sm:hidden">Upload</span>
          </button>

          {/* Divider */}
          <div className="h-6 w-px bg-rule mx-1 hidden sm:block" />

          {/* Authentication State */}
          {isAuthenticated && user ? (
            <div className="flex items-center gap-2">
              <div className="hidden md:flex items-center gap-2 px-2.5 py-1.5 border border-rule bg-paper-dim text-xs font-mono">
                <User className="w-3.5 h-3.5 text-blue-400" />
                <span className="text-zinc-200 max-w-[120px] truncate">{user.name || user.email}</span>
                <span className="text-[10px] uppercase px-1 py-0.2 bg-blue-950/60 border border-blue-500/30 text-blue-300 rounded">
                  {user.role || "user"}
                </span>
              </div>
              <button
                onClick={handleLogout}
                title="Sign Out"
                className="p-2 text-xs font-mono border border-transparent hover:border-red-500/40 text-zinc-400 hover:text-red-400 hover:bg-red-950/20 transition-colors flex items-center gap-1"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden lg:inline text-[11px] uppercase tracking-wider">Sign Out</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => onNavigate("login")}
                className={`px-3 py-1.5 text-xs font-mono uppercase tracking-wider border transition-colors flex items-center gap-1.5 ${
                  currentView === "login"
                    ? "border-blue-500/60 text-blue-300 bg-blue-950/20"
                    : "border-transparent text-zinc-300 hover:text-white hover:border-rule"
                }`}
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In</span>
              </button>
              <button
                onClick={() => onNavigate("register")}
                className="hidden sm:flex px-3 py-1.5 text-xs font-mono uppercase tracking-wider border border-blue-600 bg-blue-600/20 hover:bg-blue-600/30 text-blue-200 transition-colors items-center gap-1.5"
              >
                <UserPlus className="w-3.5 h-3.5" />
                <span>Register</span>
              </button>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
