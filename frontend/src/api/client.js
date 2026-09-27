const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = { ...(options.headers || {}) };
  
  // Attach token from localStorage if present
  try {
    const token = localStorage.getItem("cg_token") || localStorage.getItem("token");
    if (token && !headers["Authorization"]) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  } catch (e) {
    // ignore in environments without localStorage
  }

  const fetchOptions = {
    ...options,
    credentials: "include",
    headers,
  };

  const response = await fetch(url, fetchOptions);

  if (!response.ok) {
    let errMsg = `Request failed: ${response.status} ${response.statusText}`;
    try {
      const errData = await response.json();
      if (errData && errData.error) {
        errMsg = errData.error;
      }
    } catch {
      // ignore
    }
    throw new Error(errMsg);
  }

  // Handle file blob responses (PDF)
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/pdf")) {
    return response.blob();
  }

  return response.json();
}

export const api = {
  // Documents
  getDocuments: () => request("/documents"),
  getDocument: (id) => request(`/documents/${id}`),
  getDocumentStatus: (id) => request(`/documents/${id}/status`),
  uploadDocument: (formData) =>
    request("/documents", {
      method: "POST",
      body: formData,
    }),
  deleteDocument: (id) =>
    request(`/documents/${id}`, {
      method: "DELETE",
    }),

  // Analysis Details
  getClauses: (id) => request(`/documents/${id}/clauses`),
  getMissingClauses: (id) => request(`/documents/${id}/missing-clauses`),
  getDeadlines: (id) => request(`/documents/${id}/deadlines`),
  getPiiSummary: (id) => request(`/documents/${id}/pii-summary`),
  getReportPdf: (id) => request(`/documents/${id}/report.pdf`),
  getReportPdfUrl: (id) => `${BASE_URL}/documents/${id}/report.pdf`,

  // Chat / RAG
  sendChatMessage: (docId, question, sessionId = null) =>
    request(`/documents/${docId}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, session_id: sessionId }),
    }),
  getChatHistory: (docId) => request(`/documents/${docId}/chat/history`),
};
