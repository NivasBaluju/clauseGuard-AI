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

- **Unit & Integration Tests**: 23 tests passed in `backend/tests/` covering ingestion, OCR pipeline, PII masking, risk math, and REST endpoints.
- **End-to-End Pipeline**: Verified via `test_upload_pipeline.py` with live uploads across all 3 document categories:
  - `sample_residential_lease.txt`: 14 clauses segmented, 6 deadlines extracted, 25 PII entities redacted, Gemini RAG response grounded with citations, PDF report generated.
  - `sample_tech_offer_letter.txt`: 11 clauses segmented, 6 deadlines extracted, 7 PII entities redacted, PDF report generated.
  - `sample_ho4_renters_policy.txt`: 21 clauses segmented, 8 deadlines extracted, 5 PII entities redacted, PDF report generated.

---

# Production Deployment

## Architecture Overview

```
User Browser
    │
    ▼
Vercel (React + Vite SPA)
Directory: frontend/
    │
    │ HTTPS API Requests (with Authorization: Bearer <token>)
    ▼
Render (ONE Unified Flask Backend Web Service)
Directory: backend/
    │
    ├── In-Process ML / NLP / OCR Pipeline:
    │   ├── Baseline TF-IDF & Logistic Regression Models (backend/models/)
    │   ├── Fine-Tuned DistilBERT Models (backend/models/)
    │   ├── RapidOCR / ONNX Runtime (CPU Ingestion Engine)
    │   ├── spaCy (en_core_web_sm embedded wheel)
    │   ├── Microsoft Presidio (PII redaction)
    │   ├── Risk Scoring Engine & Clause Extractor
    │   └── ReportLab PDF Generator
    │
    ├── External Services:
    │   ├── Neon Serverless PostgreSQL (DATABASE_URL with pgvector)
    │   └── Google Gemini Managed API (GEMINI_API_KEY)
```

## Backend Deployment (Render)

- **Service Type**: Web Service
- **Environment**: Python 3
- **Root Directory**: `backend`
- **Python Version**: `3.11` (specified in runtime configuration)
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Pre-Deploy Command**:
  ```bash
  python run_migrations.py
  ```
- **Start Command**:
  ```bash
  gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300 wsgi:app
  ```
- **Health Check Path**: `/health` (also supports `/api/health`)
- **Worker Configuration**:
  - Initial worker count: **1 worker with 4 threads** (`--workers 1 --threads 4`).
  - *Rationale*: ML models (TF-IDF, PyTorch/BERT, RapidOCR, spaCy) are loaded in-process. A single worker prevents memory duplication across worker processes while threads handle concurrent I/O.
- **Measured Hardware Requirements**:
  - *Idle Flask + Extensions*: ~532 MB RAM
  - *After RapidOCR + spaCy/Presidio*: ~651 MB RAM
  - *After DistilBERT loaded + active inference*: ~929 MB RAM
  - *Peak observed during realistic document pipeline*: **973.8 MB RAM**
  - *Absolute Minimum*: 1 GB (Render Starter — viable for TF-IDF baseline mode only; 512 MB will OOM kill on startup)
  - *Recommended Production*: **Standard (2 GB RAM)** for full concurrent DistilBERT + RapidOCR execution without OOM risk.

## Frontend Deployment (Vercel)

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Environment Variables**:
  ```bash
  VITE_API_BASE_URL=https://<your-render-service-name>.onrender.com/api
  ```

## Required Environment Variables

All sensitive values must be injected via Render / Vercel dashboard environment settings. Never commit secrets to Git.

### Backend (Render Web Service)
| Variable Name | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection URI (`postgresql://user:pass@host/dbname?sslmode=require`) |
| `SECRET_KEY` | Yes | Cryptographic secret for Flask session cookies (32+ chars) |
| `JWT_SECRET` | Yes | Cryptographic secret for signing HS256 auth tokens (32+ chars) |
| `FIELD_ENCRYPTION_KEY` | Yes | Fernet AES-256 key for encrypting raw text at rest (generate via `Fernet.generate_key()`) |
| `GEMINI_API_KEY` | Yes | Google AI Studio API key for Gemini RAG and copilot chat |
| `FRONTEND_URL` | Yes | Allowed CORS origin (e.g., `https://clauseguard-ai.vercel.app` or comma-separated list) |
| `FLASK_ENV` | Optional | Set to `production` |
| `FLASK_DEBUG` | Optional | Set to `false` (default) |
| `MODELS_DIR` | Optional | Defaults to deterministic `backend/models` |
| `PORT` | Auto | Provided automatically by Render (binds `0.0.0.0:$PORT`) |

### Frontend (Vercel)
| Variable Name | Required | Description |
|---|---|---|
| `VITE_API_BASE_URL` | Yes | Public HTTPS URL of the Render backend `/api` endpoint |

## Database Migration Command

The migration system is idempotent and safe for zero-downtime deployments. It creates missing tables, adds missing columns, and verifies indexes without dropping data:
```bash
# In backend directory:
python run_migrations.py
```

## Local Production Simulation

To run the production WSGI server locally using Gunicorn:
```bash
cd backend
gunicorn --bind 127.0.0.1:5000 --workers 1 --threads 4 --timeout 300 wsgi:app
```

## ML Model Runtime Requirements

All production model artifacts are bundled directly inside the backend service at `backend/models/`:
- **TF-IDF + Logistic Regression**: Bundled in `backend/models/<doc_type>/baseline/` (`.joblib` format, ~1.2 MB total).
- **DistilBERT**: Optional transformer weights loaded from `backend/models/<doc_type>/bert/` or initialized via HuggingFace cache.
- **spaCy NLP**: Pinned to `en_core_web_sm` (v3.7.1 / v3.8.0 wheel specified in `requirements.txt`).
- **Microsoft Presidio**: Uses the bundled spaCy NLP pipeline; requires zero external server.
- **RapidOCR / ONNX Runtime**: Uses `rapidocr-onnxruntime` + `opencv-python-headless` for headless CPU inference on scanned documents. All 3 ONNX models (detection, classification, recognition ~16 MB total) are bundled directly inside the installed Python package wheel; zero network downloads are required on startup or container restart.

## File Storage & Retention Architecture

- **User Uploads**:
  - Stored temporarily in OS system temporary storage (`tempfile.gettempdir()`) solely during document extraction.
  - Immediately deleted in the `finally:` block of `process_document_pipeline`.
- **Extracted Text & PII**:
  - Anonymized text and metadata are stored in the Neon PostgreSQL database.
  - Raw sensitive text is encrypted at rest using AES-256 Fernet before database storage.
- **Render Storage Requirement**:
  - Render **does NOT require a persistent disk**. The stateless web service container is fully sufficient.
