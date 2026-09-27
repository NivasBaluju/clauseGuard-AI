import React, { useState } from "react";
import {
  ShieldAlert,
  Shield,
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
          badge: "AI Copilot",
          badgeColor: "bg-neutral-800 text-neutral-300 border-neutral-700",
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
          badgeColor: "bg-neutral-800 text-neutral-300 border-neutral-700",
        },
        {
          id: "guide",
          label: "Platform Guide",
          icon: BookOpen,
          path: "/guide",
          badge: "Guide",
          badgeColor: "bg-neutral-800 text-neutral-300 border-neutral-700",
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
      <div className="lg:hidden flex items-center justify-between px-4 py-3 bg-black border-b border-neutral-900 sticky top-0 z-50">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 border border-neutral-700 bg-neutral-900 flex items-center justify-center text-white">
            <Shield className="w-4 h-4 text-white" />
          </div>
          <span className="font-serif text-sm font-bold tracking-tight text-white">
            ClauseGuard AI
          </span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-1.5 border border-neutral-800 text-neutral-400 hover:text-white bg-neutral-950"
        >
          {mobileOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Backdrop for mobile */}
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-40"
        />
      )}

      {/* Main Sidebar */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 sm:w-72 bg-black border-r border-neutral-900 flex flex-col transition-transform duration-200 ease-in-out ${
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Brand Area */}
        <div className="p-5 border-b border-neutral-900 bg-black">
          <button
            onClick={() => handleNavClick("landing")}
            className="flex items-center gap-3 text-left w-full group"
          >
            <div className="w-9 h-9 rounded-lg border border-neutral-700 bg-neutral-900 flex items-center justify-center text-white group-hover:border-neutral-500 transition-colors">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-serif text-base font-bold tracking-tight text-white block">
                ClauseGuard AI
              </span>
              <span className="text-[10px] font-mono text-neutral-500 tracking-wider uppercase block -mt-0.5">
                Enterprise Legal AI
              </span>
            </div>
          </button>
        </div>

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-5 space-y-6">
          {navItems.map((group, gIdx) => (
            <div key={gIdx} className="space-y-1.5">
              <div className="px-3 text-[10px] font-mono text-neutral-500 tracking-widest uppercase">
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
                          ? "bg-white text-black font-semibold shadow-sm"
                          : "text-neutral-400 hover:text-white hover:bg-neutral-900 border border-transparent"
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <Icon
                          className={`w-4 h-4 ${
                            isActive ? "text-black" : "text-neutral-400"
                          }`}
                        />
                        <span>{item.label}</span>
                      </div>
                      {item.badge && (
                        <span
                          className={`text-[9px] font-mono border px-1.5 py-0.5 rounded tracking-wide ${
                            isActive ? "bg-neutral-200 text-black border-neutral-300" : item.badgeColor
                          }`}
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
        <div className="p-4 border-t border-neutral-900 bg-black">
          {user ? (
            <div className="space-y-3">
              <div className="flex items-center gap-3 px-2 py-1.5 rounded bg-neutral-950 border border-neutral-800">
                <div className="w-8 h-8 rounded-full bg-neutral-900 border border-neutral-700 flex items-center justify-center text-white">
                  <User size={16} />
                </div>
                <div className="flex-1 min-w-0">
                  <span className="text-xs font-mono font-medium text-white block truncate">
                    {user.name || user.email}
                  </span>
                  <span className="text-[10px] font-mono text-neutral-500 block truncate">
                    {user.email}
                  </span>
                </div>
                <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 bg-neutral-900 border border-neutral-700 text-neutral-300 rounded">
                  {user.role || "user"}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded text-xs font-mono text-neutral-300 hover:text-white hover:bg-neutral-900 border border-neutral-800 transition-colors"
              >
                <LogOut size={14} />
                <span>Sign Out</span>
              </button>
            </div>
          ) : (
            <button
              onClick={() => handleNavClick("login")}
              className="w-full py-2 bg-white hover:bg-neutral-200 text-black font-semibold text-xs font-mono rounded transition-colors"
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
