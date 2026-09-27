import React, { useState } from "react";
import {
  ShieldAlert,
  Layers,
  FileText,
  UploadCloud,
  Bot,
  Activity,
  BookOpen,
  LogOut,
  User,
  ChevronRight,
  Menu,
  X,
  Sparkles,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export function Sidebar({ currentView, onNavigate }) {
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    {
      group: "WORKSPACE",
      items: [
        { id: "landing", label: "Overview", icon: Layers, path: "/" },
        { id: "documents", label: "Documents", icon: FileText, path: "/documents" },
        { id: "upload", label: "Upload Document", icon: UploadCloud, path: "/upload" },
        {
          id: "chat",
          label: "AI Legal Copilot",
          icon: Bot,
          path: "/chat",
          badge: "Gemini RAG",
          badgeColor: "bg-blue-950/80 text-blue-300 border-blue-500/40",
        },
      ],
    },
    {
      group: "GOVERNANCE & HELP",
      items: [
        {
          id: "audit",
          label: "Audit & Trail",
          icon: Activity,
          path: "/audit",
          badge: "Logs",
          badgeColor: "bg-purple-950/80 text-purple-300 border-purple-500/40",
        },
        {
          id: "guide",
          label: "Platform Guide",
          icon: BookOpen,
          path: "/guide",
          badge: "Tour",
          badgeColor: "bg-emerald-950/80 text-emerald-300 border-emerald-500/40",
        },
      ],
    },
  ];

  const handleNavClick = (viewId) => {
    if (onNavigate) {
      onNavigate(viewId);
    }
    setMobileOpen(false);
  };

  const handleLogout = async () => {
    await logout();
    if (onNavigate) {
      onNavigate("login");
    }
  };

  return (
    <>
      {/* Mobile Top Header with toggle */}
      <div className="lg:hidden flex items-center justify-between px-4 py-3 bg-[#0a0d14] border-b border-[#1c2333] sticky top-0 z-50">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 border border-white/20 bg-zinc-950 flex items-center justify-center text-white">
            <ShieldAlert className="w-4 h-4 text-red-500" />
          </div>
          <span className="font-serif text-sm font-bold tracking-tight text-white">
            ClauseGuard AI
          </span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-1.5 border border-[#1f293d] text-zinc-400 hover:text-white bg-[#131822]"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Backdrop for mobile */}
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/70 backdrop-blur-sm z-40"
        />
      )}

      {/* Main Sidebar */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 sm:w-72 bg-[#0c1017] border-r border-[#1a2233] flex flex-col transition-transform duration-200 ease-in-out ${
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Brand Area */}
        <div className="p-5 border-b border-[#1a2233] bg-[#090c12]">
          <button
            onClick={() => handleNavClick("landing")}
            className="flex items-center gap-3 text-left w-full group"
          >
            <div className="w-9 h-9 rounded-lg border border-red-500/40 bg-red-950/20 flex items-center justify-center text-white group-hover:border-red-400 transition-colors shadow-lg shadow-red-950/20">
              <ShieldAlert className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <span className="font-serif text-base font-bold tracking-tight text-white block">
                ClauseGuard AI
              </span>
              <span className="text-[10px] font-mono text-zinc-500 tracking-wider uppercase block -mt-0.5">
                Deciva Legal Copilot
              </span>
            </div>
          </button>
        </div>

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-5 space-y-6">
          {navItems.map((group, gIdx) => (
            <div key={gIdx} className="space-y-1.5">
              <div className="px-3 text-[10px] font-mono text-zinc-500 tracking-widest uppercase">
                {group.group}
              </div>
              <div className="space-y-1">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = currentView === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => handleNavClick(item.id)}
                      className={`w-full flex items-center justify-between px-3 py-2.5 rounded-md text-xs font-mono transition-all ${
                        isActive
                          ? "bg-white/10 text-white font-semibold border border-white/20 shadow-sm"
                          : "text-zinc-400 hover:text-white hover:bg-white/5 border border-transparent"
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <Icon
                          className={`w-4 h-4 ${
                            isActive ? "text-white" : "text-zinc-400"
                          }`}
                        />
                        <span>{item.label}</span>
                      </div>
                      {item.badge && (
                        <span
                          className={`text-[9px] font-mono border px-1.5 py-0.5 rounded tracking-wide ${item.badgeColor}`}
                        >
                          {item.badge}
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* User Card & Sign Out at Bottom */}
        <div className="p-4 border-t border-[#1a2233] bg-[#090c12]">
          {user ? (
            <div className="space-y-3">
              <div className="flex items-center gap-3 px-2 py-1.5 rounded bg-[#131822] border border-[#1f293d]">
                <div className="w-8 h-8 rounded-full bg-blue-950 border border-blue-500/40 flex items-center justify-center text-blue-300">
                  <User size={16} />
                </div>
                <div className="flex-1 min-w-0">
                  <span className="text-xs font-mono font-medium text-white block truncate">
                    {user.name || user.email}
                  </span>
                  <span className="text-[10px] font-mono text-zinc-500 block truncate">
                    {user.email}
                  </span>
                </div>
                <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 bg-blue-950/80 border border-blue-500/30 text-blue-300 rounded">
                  {user.role || "user"}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded text-xs font-mono text-red-400 hover:text-red-300 hover:bg-red-950/20 border border-red-950/40 transition-colors"
              >
                <LogOut size={14} />
                <span>Sign Out</span>
              </button>
            </div>
          ) : (
            <button
              onClick={() => handleNavClick("login")}
              className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-mono font-medium rounded transition-colors"
            >
              Sign In to Account
            </button>
          )}
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
