import React from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useParams, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { PageShell } from "./components/layout/PageShell";
import { Landing } from "./pages/Landing";
import { Upload } from "./pages/Upload";
import { DocumentList } from "./pages/DocumentList";
import { DocumentAnalysis } from "./pages/DocumentAnalysis";
import { StandaloneChat } from "./pages/StandaloneChat";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";

// Step 4 ProtectedRoute implementation as requested
export function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="py-16 text-center text-zinc-400 font-mono text-xs animate-pulse">
        Verifying secure session token…
      </div>
    );
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Wrapper for DocumentAnalysis extracting route params
function DocumentAnalysisWrapper({ onNavigate }) {
  const { id } = useParams();
  return <DocumentAnalysis documentId={id} onNavigate={onNavigate} />;
}

// Wrapper for Upload reading optional location state
function UploadWrapper({ onNavigate }) {
  const location = useLocation();
  const initialDocType = location.state?.defaultDocType || "rental_agreement";
  return <Upload onNavigate={onNavigate} initialDocType={initialDocType} />;
}

// Inner App with routing and centralized navigation handler
function AppRoutes() {
  const navigate = useNavigate();
  const location = useLocation();

  // Map pathname to currentView for Navbar active indicator
  const getCurrentView = () => {
    const path = location.pathname;
    if (path === "/") return "landing";
    if (path.startsWith("/documents/")) return "analysis";
    if (path === "/documents") return "documents";
    if (path === "/upload") return "upload";
    if (path === "/chat") return "chat";
    if (path === "/login") return "login";
    if (path === "/register") return "register";
    return "";
  };

  const handleNavigate = (view, params = {}) => {
    switch (view) {
      case "landing":
        navigate("/");
        break;
      case "upload":
        navigate("/upload", { state: params });
        break;
      case "documents":
        navigate("/documents");
        break;
      case "analysis":
        if (params.documentId) {
          navigate(`/documents/${params.documentId}`);
        } else {
          navigate("/documents");
        }
        break;
      case "chat":
        navigate("/chat");
        break;
      case "login":
        navigate("/login");
        break;
      case "register":
        navigate("/register");
        break;
      default:
        navigate("/");
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const currentView = getCurrentView();

  return (
    <PageShell currentView={currentView} onNavigate={handleNavigate}>
      <Routes>
        {/* Public Authentication Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Public Application Routes */}
        <Route path="/" element={<Landing onNavigate={handleNavigate} />} />
        <Route path="/upload" element={<UploadWrapper onNavigate={handleNavigate} />} />
        <Route path="/documents" element={<DocumentList onNavigate={handleNavigate} />} />
        <Route path="/documents/:id" element={<DocumentAnalysisWrapper onNavigate={handleNavigate} />} />
        <Route path="/dashboard" element={<Navigate to="/documents" replace />} />

        {/* Protected Enterprise AI Chat Route */}
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <StandaloneChat onNavigate={handleNavigate} />
            </ProtectedRoute>
          }
        />

        {/* Catch-all fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </PageShell>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
