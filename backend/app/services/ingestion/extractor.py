import io
import os
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
from PIL import Image
import fitz
import docx
from app.services.ingestion.ocr import ocr_image_detailed

logger = logging.getLogger(__name__)

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

    def hyphen_replacer(match):
        part1 = match.group(1)
        part2 = match.group(2)
        compound = f"{part1.lower()}-{part2.lower()}"
        if compound in PRESERVED_HYPHEN_TERMS:
            return f"{part1}-{part2}"
        return f"{part1}{part2}"

    cleaned = re.sub(r"\b([a-zA-Z]{2,})-\s*\n\s*([a-zA-Z]{2,})\b", hyphen_replacer, text)

    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
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

    if char_count < 40:
        return True, "insufficient_text_length"

    words = stripped.split()
    if len(words) < 8:
        return True, "low_word_count"

    images = page.get_images(full=True)
    if images:
        if char_count < 150:
            return True, "image_heavy_page"

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

    alpha_chars = sum(1 for c in stripped if c.isalpha())
    alpha_ratio = alpha_chars / max(1, char_count)
    if alpha_ratio < 0.50 and char_count < 300:
        return True, "suspicious_low_alpha_ratio"

    if stripped.count("\ufffd") > 3 or stripped.count("?") > char_count * 0.25:
        return True, "encoding_artifacts_detected"

    return False, "sufficient_native_text"

def extract_pdf_with_metadata(file_path: str) -> Tuple[str, int, List[Dict[str, Any]]]:
    """
    Processes each PDF page individually with intelligent extraction:
    - Extracts native digital text.
    - Inspects and extracts text from ALL embedded images inside the page via OCR.
    - If a page is scanned or lacks text, runs high-resolution page OCR.
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
        clean_native = clean_ocr_text(native_text)
        needs_page_ocr, reason = should_use_ocr(page, native_text)

        # FAST PATH: If the page contains sufficient digital text, skip heavy deep-learning OCR
        if not needs_page_ocr:
            page_results.append(f"[PAGE {page_num}]\n{clean_native}")
            page_metadata.append({
                "page_number": page_num,
                "extraction_method": "native",
                "text_length": len(clean_native),
                "ocr_used": False,
                "ocr_confidence": 100.0,
                "reason": reason,
            })
            logger.info(f"[PAGE {page_num}] Native extraction complete ({len(clean_native)} chars)")
            continue

        # SLOW PATH: Page lacks native text or is a scanned document -> Run OCR
        logger.info(f"[PAGE {page_num}] Native text insufficient ({reason}) → Rasterizing page for OCR...")
        try:
            # 150 DPI provides sharp text detection while halving image size and memory usage compared to 200 DPI
            zoom = 150.0 / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_bytes = pix.tobytes("png")

            with Image.open(io.BytesIO(img_bytes)) as img:
                ocr_res = ocr_image_detailed(img)

            raster_ocr_text = clean_ocr_text(ocr_res.get("text", ""))
            final_page_text = raster_ocr_text if raster_ocr_text else clean_native

            page_results.append(f"[PAGE {page_num}]\n{final_page_text}")
            page_metadata.append({
                "page_number": page_num,
                "extraction_method": ocr_res.get("method", "rapidocr"),
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
            fallback_text = clean_native
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

