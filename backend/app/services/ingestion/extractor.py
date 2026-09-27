import io
import os
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
from PIL import Image
import fitz  # PyMuPDF
import docx
from app.services.ingestion.ocr import ocr_image_detailed

logger = logging.getLogger(__name__)

# Known legal and standard hyphenated compounds that must preserve their hyphens
PRESERVED_HYPHEN_TERMS = {
    "non-compete",
    "non-solicitation",
    "non-disclosure",
    "court-appointed",
    "well-known",
    "pro-rata",
    "attorney-in-fact",
    "cross-default",
    "force-majeure",
    "tax-exempt",
    "third-party",
    "arms-length",
    "hold-harmless",
    "good-faith",
    "inter-alia",
    "time-sensitive",
    "end-user",
    "right-of-way",
    "co-signer",
    "pre-existing",
    "sub-lease",
}

class UnsupportedFormatError(Exception):
    pass

def clean_ocr_text(text: str) -> str:
    """
    Cleans OCR/native extraction artifacts while preserving strict legal meaning.
    - Normalizes line-break hyphenations (e.g. 'termina-\\n tion' -> 'termination')
      while preserving legitimate hyphenated terms (e.g. 'non-compete').
    - Normalizes excessive blank lines and trailing whitespace.
    - Never changes dates, numbers, clause numbers, names, or legal words.
    """
    if not text:
        return ""

    # 1. Normalize line-break hyphenations across line wraps
    def hyphen_replacer(match):
        part1 = match.group(1)
        part2 = match.group(2)
        compound = f"{part1.lower()}-{part2.lower()}"
        if compound in PRESERVED_HYPHEN_TERMS:
            return f"{part1}-{part2}"
        return f"{part1}{part2}"

    cleaned = re.sub(r"\b([a-zA-Z]{2,})-\s*\n\s*([a-zA-Z]{2,})\b", hyphen_replacer, text)

    # 2. Normalize whitespace while preserving paragraph structure
    # Remove carriage returns
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse 3+ newlines to 2 newlines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    # Strip trailing whitespace on each line
    cleaned = "\n".join(line.rstrip() for line in cleaned.splitlines())

    return cleaned.strip()

def should_use_ocr(page: fitz.Page, extracted_text: str) -> Tuple[bool, str]:
    """
    Intelligently evaluates whether a PDF page requires OCR based on text quality,
    rather than only whether text is empty.
    
    Checks:
    - Condition A: Almost no text (length < 40 chars)
    - Condition B: Low word count (< 8 words)
    - Condition C: Image-heavy or scanned page
    - Condition D: Suspicious text (low alphabetic ratio, encoding corruption)
    - Condition E: Image-only page
    """
    stripped = (extracted_text or "").strip()
    char_count = len(stripped)

    # Condition A: Almost no text
    if char_count < 40:
        return True, "insufficient_text_length"

    # Condition B: Low word count
    words = stripped.split()
    if len(words) < 8:
        return True, "low_word_count"

    # Condition C & E: Image-heavy page check
    images = page.get_images(full=True)
    if images:
        if char_count < 150:
            return True, "image_heavy_page"

        # Check if an image dominates the page geometry (e.g. scanned page with partial OCR garbage)
        page_area = page.rect.width * page.rect.height
        for img_info in images:
            xref = img_info[0]
            try:
                rects = page.get_image_rects(xref)
                for r in rects:
                    coverage = (r.width * r.height) / max(1.0, page_area)
                    if coverage > 0.45 and char_count < 350:
                        return True, "scanned_image_dominates_page"
            except Exception:
                pass

    # Condition D: Suspicious text / encoding artifacts
    alpha_chars = sum(1 for c in stripped if c.isalpha())
    alpha_ratio = alpha_chars / max(1, char_count)
    if alpha_ratio < 0.50 and char_count < 300:
        return True, "suspicious_low_alpha_ratio"

    # Encoding corruption / replacement character frequency
    if stripped.count("\ufffd") > 3 or stripped.count("?") > char_count * 0.25:
        return True, "encoding_artifacts_detected"

    return False, "sufficient_native_text"

def extract_pdf_with_metadata(file_path: str) -> Tuple[str, int, List[Dict[str, Any]]]:
    """
    Processes each PDF page individually with intelligent Tesseract OCR fallback.
    - Native extraction first for fast, high-quality digital text.
    - 300 DPI high-resolution rasterization + Tesseract OCR for scanned/image pages.
    - Retains page boundaries [PAGE X] and prevents duplicate text.
    """
    doc = fitz.open(file_path)
    page_count = len(doc)
    page_results = []
    page_metadata = []

    logger.info(f"[PDF] Processing document: {os.path.basename(file_path)} | Total Pages: {page_count}")

    for idx, page in enumerate(doc):
        page_num = idx + 1
        native_text = page.get_text("text") or ""
        needs_ocr, reason = should_use_ocr(page, native_text)

        if not needs_ocr:
            clean_text = clean_ocr_text(native_text)
            page_results.append(f"[PAGE {page_num}]\n{clean_text}")
            page_metadata.append({
                "page_number": page_num,
                "extraction_method": "native",
                "text_length": len(clean_text),
                "ocr_used": False,
                "ocr_confidence": 100.0,
                "reason": reason,
            })
            logger.info(f"[PAGE {page_num}] Native extraction successful ({len(clean_text)} chars)")
        else:
            logger.info(f"[PAGE {page_num}] Native text insufficient ({reason}) → Triggering 300 DPI OCR...")
            try:
                # 300 DPI = zoom factor 300 / 72 ≈ 4.166667
                zoom = 300.0 / 72.0
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_bytes = pix.tobytes("png")

                with Image.open(io.BytesIO(img_bytes)) as img:
                    ocr_res = ocr_image_detailed(img)

                ocr_text = clean_ocr_text(ocr_res.get("text", ""))

                # Avoid duplicate text if native text already captured parts
                if native_text.strip() and len(native_text.strip()) > 50:
                    if ocr_text.lower() in native_text.lower():
                        final_page_text = clean_ocr_text(native_text)
                    elif native_text.lower() in ocr_text.lower():
                        final_page_text = ocr_text
                    else:
                        final_page_text = f"{clean_ocr_text(native_text)}\n\n{ocr_text}"
                else:
                    final_page_text = ocr_text

                page_results.append(f"[PAGE {page_num}]\n{final_page_text}")
                page_metadata.append({
                    "page_number": page_num,
                    "extraction_method": ocr_res.get("method", "tesseract"),
                    "text_length": len(final_page_text),
                    "ocr_used": True,
                    "ocr_confidence": ocr_res.get("ocr_confidence", 0.0),
                    "word_count": ocr_res.get("word_count", 0),
                    "reason": reason,
                })
                logger.info(
                    f"[PAGE {page_num}] OCR complete via {ocr_res.get('method')} "
                    f"(Confidence: {ocr_res.get('ocr_confidence')}%, Chars: {len(final_page_text)})"
                )
            except Exception as e:
                logger.error(f"[PAGE {page_num}] OCR rendering failed: {e}")
                fallback_text = clean_ocr_text(native_text)
                page_results.append(f"[PAGE {page_num}]\n{fallback_text}")
                page_metadata.append({
                    "page_number": page_num,
                    "extraction_method": "ocr_failed",
                    "text_length": len(fallback_text),
                    "ocr_used": True,
                    "ocr_confidence": 0.0,
                    "error": str(e),
                })

    doc.close()
    full_text = "\n\n".join(page_results)
    return full_text, page_count, page_metadata

def extract_pdf(file_path: str) -> Tuple[str, int]:
    """
    Standard interface for PDF extraction: returns (full_text, page_count).
    """
    full_text, page_count, _ = extract_pdf_with_metadata(file_path)
    return full_text, page_count

def read_plain_text(file_path: str) -> Tuple[str, int]:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    page_count = max(1, (len(text) // 3000) + 1)
    return clean_ocr_text(text), page_count

def extract_docx(file_path: str) -> Tuple[str, int]:
    """
    Extracts text from DOCX files preserving paragraph and table structure in document order.
    """
    doc = docx.Document(file_path)
    content = []
    
    for child in doc.element.body:
        if child.tag.endswith("p"):
            p = docx.text.paragraph.Paragraph(child, doc)
            if p.text.strip():
                content.append(p.text.strip())
        elif child.tag.endswith("tbl"):
            tbl = docx.table.Table(child, doc)
            for row in tbl.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    content.append(" | ".join(row_cells))
                    
    full_text = clean_ocr_text("\n\n".join(content))
    page_count = max(1, (len(full_text) // 3000) + 1)
    return full_text, page_count

def extract_text(file_path: str, ext: str) -> Tuple[str, int]:
    """
    Main extraction dispatcher.
    Returns: (extracted_text, page_count)
    """
    ext = ext.lower().lstrip(".")
    if ext == "txt":
        return read_plain_text(file_path)
    elif ext == "docx":
        return extract_docx(file_path)
    elif ext == "pdf":
        return extract_pdf(file_path)
    else:
        raise UnsupportedFormatError(f"Unsupported file format: .{ext}")

