# ClauseGuard AI — Legal Document Risk Analyzer

ClauseGuard AI is an automated, non-expert AI legal document risk analyzer covering three document types: **Residential Lease Agreements**, **Job Offer Letters**, and **Insurance Policy Specimens** (ISO HO-4 broad form).

> **Permanent Legal Disclaimer:**
> *ClauseGuard AI provides automated, non-expert analysis for informational purposes only. It is not legal advice. Consult a qualified attorney for decisions with legal consequences.*

---

## System Architecture

```
React SPA (Vite + Tailwind CSS, Port 5173)
      │  REST (JSON) over HTTP / Proxy
      ▼
Flask API (Python 3.11, Port 5000)
      │
      ├── Ingestion Service ───────► PyMuPDF / Tesseract OCR / python-docx / txt
      ├── PII Redaction Service ───► Microsoft Presidio (DATE_TIME preserved for deadlines)
      ├── Clause Segmentation ─────► Rule-based Multiline Regex + spaCy (en_core_web_sm)
      ├── Clause Classification ───► Baseline TF-IDF + Logistic Regression / DistilBERT
      ├── Risk Scoring Engine ─────► Deterministic formula (risk_config.json)
      ├── Missing-Clause Detector ─► Checklist set-difference (confidence-thresholded)
      ├── Deadline Extractor ──────► spaCy DATE entities + duration regex + relative days parser
      ├── Grounded RAG Engine ─────► Gemini Embedding (768-dim) + Gemini 3.8 Flash
      └── PDF Report Generator ────► ReportLab (Executive summary, clauses, PII counts, disclaimers)
      │
      ▼
Neon PostgreSQL (Serverless Cloud with pgvector extension)
```

---

## Key Engineering Pillars

1. **Zero-PII Leakage Pipeline:**
   - Microsoft Presidio anonymizes personal identifying information (`PERSON`, `PHONE_NUMBER`, `EMAIL_ADDRESS`, `LOCATION`, `US_SSN`, `CREDIT_CARD`, `IBAN_CODE`, `IP_ADDRESS`) immediately upon text extraction.
   - `DATE_TIME` is explicitly preserved so notice periods, renewal windows, and calendar deadlines remain extractable.
   - Downstream models, the UI, and the Gemini API **only ever process the anonymized redacted text**. Raw text is encrypted at rest using AES/Fernet for audit purposes only.

2. **Empirical 3-Way Model Evaluation (No Hallucinated Data):**
   - Built authentic datasets from verified public sources (Minnesota State Bar / Rochester Housing Authority, California DRE, South Dakota DHS, University of Iowa HR, Virginia TownHall, State Departments of Insurance HO-4 specimens).
   - Evaluated 3 architectures: **Baseline TF-IDF + Logistic Regression**, **BERT-no-context**, and **BERT-windowed** (`[TARGET]` tokens).
   - In accordance with Section 11.4 of the specification, the winning model per task was selected and documented:
     - **Clause Type Classification**: TF-IDF + Logistic Regression achieved superior macro-F1 (0.7333 on Leases, 0.6667 on Offer Letters, 0.4848 on Insurance).
     - **Favorability Classification**: Fine-tuned BERT achieved higher macro-F1 on nuanced context (+0.041 lift on Leases, +0.18 lift on Insurance).
   - Results recorded in `ml/artifacts/model_comparison_report.json`.

3. **Deterministic, Config-Driven Risk Scoring:**
   - Managed in `backend/app/services/risk/risk_config.json`.
   - Clause risk: `base_weight * favorability_multiplier * confidence * 100`.
   - Overall risk: `0.7 * mean_clause_risk + 0.3 * missing_clauses_penalty`.
   - Risk bands: Low (0–25), Medium (26–50), High (51–75), Critical (76–100).
   - All weights are explicitly labeled as tunable engineering defaults, not statutory legal conclusions.

4. **Grounded Gemini 3.8 Flash RAG Chatbot:**
   - Clause embeddings: `gemini-embedding-001` with `output_dimensionality: 768`.
   - Vector search: PostgreSQL `pgvector` HNSW cosine similarity.
   - Generation: `gemini-3.8-flash` with strict grounding prompt instruction.
   - Citations: Automatically tracks and highlights cited clauses (`[Clause X]`).
   - Non-hallucination guarantee: When queried about terms not present in the document, the model explicitly responds: *"The provided document does not contain information addressing this question."*
   - Prompt-injection defense: Pre-scans queries for injection patterns (`"ignore previous instructions"`, `"DAN mode"`, etc.).

---

## Database Schema (PostgreSQL + pgvector)

- `documents`: Stores filename, format, document_type, processing status, risk score, risk band, encrypted raw text, redacted text, and model version.
- `clauses`: Stores document_id, clause_index, clause_type, confidence, favorability_label, risk_score, redacted_text, offsets, and `embedding VECTOR(768)`.
- `missing_clauses`: Stores document_id, clause_type, severity, and checklist note.
- `deadlines`: Stores document_id, clause_id, deadline_type, raw_text, relative_days, parsed_date, confidence.
- `pii_findings`: Stores entity_type, offsets, and confidence (never stores actual sensitive text).
- `chat_sessions` & `chat_messages`: Stores session history, user questions, assistant responses, grounded boolean flag, and cited clause UUIDs.

---

## Local Development & Running

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL with `pgvector` extension (or cloud Neon PostgreSQL)

### Backend Setup
```bash
cd backend
# Create and populate .env with DATABASE_URL, GEMINI_API_KEY, SECRET_KEY, FIELD_ENCRYPTION_KEY
py wsgi.py
# Runs on http://127.0.0.1:5000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173 (proxies /api to 127.0.0.1:5000)
```

---

## Verification & Test Results

- **Unit & Integration Tests**: 18 unit tests passed in `backend/tests/` covering ingestion, PII masking, risk math, and REST endpoints.
- **End-to-End Pipeline**: Verified via `test_upload_pipeline.py` with live uploads across all 3 document categories:
  - `sample_residential_lease.txt`: 14 clauses segmented, 6 deadlines extracted, 25 PII entities redacted, Gemini RAG response grounded with citations, PDF report generated.
  - `sample_tech_offer_letter.txt`: 11 clauses segmented, 6 deadlines extracted, 7 PII entities redacted, PDF report generated.
  - `sample_ho4_renters_policy.txt`: 21 clauses segmented, 8 deadlines extracted, 5 PII entities redacted, PDF report generated.
