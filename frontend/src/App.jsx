import React, { useState } from "react";
import { PageShell } from "./components/layout/PageShell";
import { Landing } from "./pages/Landing";
import { Upload } from "./pages/Upload";
import { DocumentList } from "./pages/DocumentList";
import { DocumentAnalysis } from "./pages/DocumentAnalysis";

export function App() {
  const [currentView, setCurrentView] = useState("landing");
  const [selectedDocId, setSelectedDocId] = useState(null);
  const [initialDocType, setInitialDocType] = useState("rental_agreement");

  const handleNavigate = (view, params = {}) => {
    if (params.documentId) {
      setSelectedDocId(params.documentId);
    }
    if (params.defaultDocType) {
      setInitialDocType(params.defaultDocType);
    }
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <PageShell currentView={currentView} onNavigate={handleNavigate}>
      {currentView === "landing" && (
        <Landing onNavigate={handleNavigate} />
      )}

      {currentView === "upload" && (
        <Upload
          onNavigate={handleNavigate}
          initialDocType={initialDocType}
        />
      )}

      {currentView === "documents" && (
        <DocumentList onNavigate={handleNavigate} />
      )}

      {currentView === "analysis" && selectedDocId && (
        <DocumentAnalysis
          documentId={selectedDocId}
          onNavigate={handleNavigate}
        />
      )}
    </PageShell>
  );
}

export default App;
