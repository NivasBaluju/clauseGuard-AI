import os
import logging
from datetime import datetime, timezone
from pathlib import Path
from app.extensions import db
from app.models.document import Document
from app.models.clause import Clause
from app.models.missing_clause import MissingClause
from app.models.deadline import Deadline
from app.models.pii_finding import PIIFinding
from app.utils.encryption import encrypt_text
from app.services.ingestion.extractor import extract_text
from app.services.privacy.pii_redactor import redact
from app.services.nlp.segmenter import segment_clauses
from app.services.nlp.classifier_bert import classify_clause, classify_clauses_batch
from app.services.risk.risk_engine import compute_clause_risk, compute_document_risk, compute_risk_band
from app.services.missing_clauses.detector import detect_missing_clauses
from app.services.deadlines.deadline_extractor import extract_all_deadlines
from app.services.rag.embedder import embed_text, batch_embed_texts
from app.services.audit_service import log_audit_event

logger = logging.getLogger(__name__)

def process_document_pipeline(document_id: str, file_path: str, ext: str) -> Document:
    """
    Executes the full end-to-end processing pipeline for a legal document:
    1. Extract text (PyMuPDF / OCR / python-docx / txt)
    2. Redact PII (Presidio, DATE_TIME excluded)
    3. Segment into clauses (Rule-based + spaCy)
    4. Classify clause types and favorability (Context-windowed BERT / Baseline)
    5. Compute deterministic risk score & missing clause penalties
    6. Extract notice periods and deadlines
    7. Generate 768-dim embeddings for RAG
    8. Store results & update stage status
    """
    doc = db.session.get(Document, document_id)
    if not doc:
        raise ValueError(f"Document {document_id} not found in database.")

    try:
        doc.status = "processing"
        doc.processing_stage = "extracting_text"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 1: Extracting text from {file_path}")

        raw_text, page_count = extract_text(file_path, ext)
        if not raw_text or not raw_text.strip():
            raise ValueError("Document contains no readable text.")

        doc.page_count = page_count
        doc.raw_text_encrypted = encrypt_text(raw_text)
        db.session.commit()

        doc.processing_stage = "redacting_pii"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 2: Redacting PII")

        redacted_text, pii_findings = redact(raw_text)
        doc.redacted_text = redacted_text

        for f in pii_findings:
            pf = PIIFinding(
                document_id=doc.id,
                entity_type=f["entity_type"],
                start_offset=f["start"],
                end_offset=f["end"],
                confidence=f["confidence"],
            )
            db.session.add(pf)
        db.session.commit()

        doc.processing_stage = "segmenting_clauses"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 3: Segmenting clauses for {doc.document_type}")

        raw_segments = segment_clauses(redacted_text, document_type=doc.document_type)
        if not raw_segments:
            raw_segments = [{
                "clause_index": 0,
                "text": redacted_text.strip(),
                "start_offset": 0,
                "end_offset": len(redacted_text.strip()),
            }]

        clause_objs = []
        for seg in raw_segments:
            c = Clause(
                document_id=doc.id,
                clause_index=seg["clause_index"],
                redacted_text=seg["text"],
                start_offset=seg["start_offset"],
                end_offset=seg["end_offset"],
            )
            db.session.add(c)
            clause_objs.append(c)
        db.session.commit()

        doc.processing_stage = "classifying_clauses"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 4: Classifying {len(clause_objs)} clauses in high-speed batch mode")

        clause_items = []
        for i, c in enumerate(clause_objs):
            prev_t = clause_objs[i - 1].redacted_text if i > 0 else None
            next_t = clause_objs[i + 1].redacted_text if i + 1 < len(clause_objs) else None
            clause_items.append({
                "text": c.redacted_text,
                "prev_text": prev_t,
                "next_text": next_t,
            })

        type_results = classify_clauses_batch(clause_items, document_type=doc.document_type, task="clause_type")
        fav_results = classify_clauses_batch(clause_items, document_type=doc.document_type, task="favorability")

        model_version_used = "bert-windowed-v1"
        for i, c in enumerate(clause_objs):
            c_type, c_conf, m_ver = type_results[i]
            c.clause_type = c_type
            c.clause_type_confidence = c_conf
            model_version_used = m_ver

            fav_label, fav_conf, _ = fav_results[i]
            c.favorability_label = fav_label
            c.favorability_confidence = fav_conf

        doc.model_version = model_version_used
        db.session.commit()

        doc.processing_stage = "scoring_risk"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 5: Scoring risk and checking missing clauses")

        clause_scores = []
        for i, c in enumerate(clause_objs):
            prior_type = clause_objs[i - 1].clause_type if i > 0 else None
            r_score = compute_clause_risk(
                clause_type=c.clause_type,
                favorability_label=c.favorability_label,
                favorability_confidence=c.favorability_confidence,
                prior_clause_type=prior_type,
            )
            c.risk_score = r_score
            clause_scores.append(r_score)

        classified_dicts = [
            {"clause_type": c.clause_type, "clause_type_confidence": c.clause_type_confidence}
            for c in clause_objs
        ]
        missing_list = detect_missing_clauses(classified_dicts, document_type=doc.document_type)

        for m in missing_list:
            mc = MissingClause(
                document_id=doc.id,
                clause_type=m["clause_type"],
                severity=m["severity"],
                checklist_note=m["checklist_note"],
            )
            db.session.add(mc)

        doc_risk = compute_document_risk(clause_scores, missing_list)
        band = compute_risk_band(doc_risk)

        doc.overall_risk_score = doc_risk
        doc.risk_band = band
        db.session.commit()

        doc.processing_stage = "extracting_deadlines"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 6: Extracting deadlines")

        clause_dict_list = [{"id": c.id, "redacted_text": c.redacted_text} for c in clause_objs]
        extracted_deadlines = extract_all_deadlines(clause_dict_list)

        for dl in extracted_deadlines:
            d_obj = Deadline(
                document_id=doc.id,
                clause_id=dl.get("clause_id"),
                deadline_type=dl.get("deadline_type"),
                raw_text=dl.get("raw_text"),
                parsed_date=dl.get("parsed_date"),
                relative_days=dl.get("relative_days"),
                confidence=dl.get("confidence", "needs_review"),
            )
            db.session.add(d_obj)
        db.session.commit()

        doc.processing_stage = "generating_embeddings"
        db.session.commit()
        logger.info(f"[{doc.id}] Stage 7: Generating Gemini embeddings for {len(clause_objs)} clauses in batch")

        texts_to_embed = [c.redacted_text for c in clause_objs]
        batch_embs = batch_embed_texts(texts_to_embed, task_type="RETRIEVAL_DOCUMENT")
        for c, emb in zip(clause_objs, batch_embs):
            c.embedding = emb
        db.session.commit()

        doc.status = "analyzed"
        doc.processing_stage = "completed"
        doc.analyzed_at = datetime.now(timezone.utc)
        db.session.commit()
        logger.info(f"[{doc.id}] Document processing completed successfully! Risk Score: {doc.overall_risk_score} ({doc.risk_band})")

        log_audit_event(
            action="DOC_ANALYZED",
            resource_type="document",
            resource_id=str(doc.id),
            details={
                "filename": doc.filename,
                "overall_risk_score": doc.overall_risk_score,
                "risk_band": doc.risk_band,
                "clauses_count": len(clause_objs),
                "deadlines_count": len(extracted_deadlines),
                "missing_clauses_count": len(missing_list)
            }
        )

        return doc

    except Exception as e:
        logger.exception(f"Pipeline error for document {document_id}: {e}")
        try:
            db.session.rollback()
            failed_doc = db.session.get(Document, document_id)
            if failed_doc:
                failed_doc.status = "failed"
                failed_doc.processing_stage = "failed"
                failed_doc.error_message = str(e)[:500]
                db.session.commit()
        except Exception as rollback_err:
            logger.error(f"Failed to record pipeline failure state for {document_id}: {rollback_err}")
            try:
                db.session.rollback()
            except Exception:
                pass
        raise e
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
