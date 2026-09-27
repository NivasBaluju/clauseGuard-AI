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
    <header className="border-b border-neutral-800 bg-black sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <button
          onClick={() => onNavigate("landing")}
          className="flex items-center gap-3 text-left group"
        >
          <div className="w-8 h-8 border border-neutral-700 bg-neutral-900 flex items-center justify-center text-white group-hover:border-neutral-500 transition-colors rounded">
            <ShieldAlert className="w-4 h-4 text-white" />
          </div>
          <div>
            <span className="font-serif text-lg font-bold tracking-tight text-white block">
              ClauseGuard AI
            </span>
            <span className="text-[10px] font-mono text-neutral-500 tracking-wider uppercase block -mt-1">
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
                ? "border-white text-white bg-white/10 font-semibold"
                : "border-transparent text-neutral-400 hover:text-white hover:border-neutral-800"
            }`}
          >
            Overview
          </button>

          <button
            onClick={() => onNavigate("documents")}
            className={`px-3 py-2 text-xs font-mono uppercase tracking-wider transition-colors border ${
              currentView === "documents"
                ? "border-white text-white bg-white/10 font-semibold"
                : "border-transparent text-neutral-400 hover:text-white hover:border-neutral-800"
            }`}
          >
            Documents
          </button>

          <button
            onClick={() => onNavigate("chat")}
            className={`px-3 py-2 text-xs font-mono uppercase tracking-wider transition-colors border flex items-center gap-1.5 ${
              currentView === "chat"
                ? "border-white text-white bg-white/10 font-semibold"
                : "border-transparent text-neutral-400 hover:text-white hover:border-neutral-800"
            }`}
          >
            <Bot className="w-3.5 h-3.5 text-white" />
            <span>AI Copilot</span>
          </button>

          <button
            onClick={() => onNavigate("upload")}
            className="px-3.5 py-2 text-xs font-mono uppercase tracking-wider border border-white text-black bg-white hover:bg-neutral-200 transition-colors flex items-center gap-1.5 font-semibold"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Upload Document</span>
            <span className="sm:hidden">Upload</span>
          </button>

          {/* Divider */}
          <div className="h-6 w-px bg-neutral-800 mx-1 hidden sm:block" />

          {/* Authentication State */}
          {isAuthenticated && user ? (
            <div className="flex items-center gap-2">
              <div className="hidden md:flex items-center gap-2 px-2.5 py-1.5 border border-neutral-800 bg-neutral-900 text-xs font-mono">
                <User className="w-3.5 h-3.5 text-white" />
                <span className="text-white max-w-[120px] truncate">{user.name || user.email}</span>
                <span className="text-[10px] uppercase px-1 py-0.2 bg-neutral-800 border border-neutral-700 text-neutral-300 rounded">
                  {user.role || "user"}
                </span>
              </div>
              <button
                onClick={handleLogout}
                title="Sign Out"
                className="p-2 text-xs font-mono border border-transparent hover:border-neutral-700 text-neutral-400 hover:text-white hover:bg-neutral-900 transition-colors flex items-center gap-1"
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
                    ? "border-white text-black bg-white font-semibold"
                    : "border-transparent text-neutral-300 hover:text-white hover:border-neutral-800"
                }`}
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In</span>
              </button>
              <button
                onClick={() => onNavigate("register")}
                className="hidden sm:flex px-3 py-1.5 text-xs font-mono uppercase tracking-wider border border-white bg-white text-black hover:bg-neutral-200 transition-colors items-center gap-1.5 font-semibold"
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
