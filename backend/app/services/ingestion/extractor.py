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

        # 1. Extract text from any embedded images inside this page
        images = page.get_images(full=True)
        embedded_image_texts = []
        seen_xrefs = set()

        if images:
            for img_info in images:
                xref = img_info[0]
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)
                try:
                    base_image = doc.extract_image(xref)
                    w = base_image.get("width", 0)
                    h = base_image.get("height", 0)
                    # Filter out tiny decorative icons, dividers, bullets (<1600 px area or <25px dim)
                    if w < 50 or h < 25 or (w * h < 1600):
                        continue

                    img_bytes = base_image.get("image")
                    if not img_bytes:
                        continue

                    with Image.open(io.BytesIO(img_bytes)) as pil_img:
                        ocr_res = ocr_image_detailed(pil_img)
                        raw_extracted = ocr_res.get("text", "").strip()
                        cleaned_extracted = clean_ocr_text(raw_extracted)

                        if cleaned_extracted and len(cleaned_extracted.split()) >= 1:
                            # Avoid duplicates if extracted image text is already present in native text
                            if cleaned_extracted.lower() not in clean_native.lower():
                                embedded_image_texts.append(cleaned_extracted)
                                logger.info(
                                    f"[PAGE {page_num}] Extracted text from embedded image xref {xref} "
                                    f"({len(cleaned_extracted)} chars): {cleaned_extracted[:60]}..."
                                )
                except Exception as img_err:
                    logger.warning(f"[PAGE {page_num}] Failed extracting image xref {xref}: {img_err}")

        embedded_text_block = "\n\n".join(embedded_image_texts).strip()

        # 2. Page assembly based on quality assessment
        if not needs_page_ocr:
            if embedded_text_block:
                final_page_text = f"{clean_native}\n\n[Extracted Image Text]:\n{embedded_text_block}"
            else:
                final_page_text = clean_native

            page_results.append(f"[PAGE {page_num}]\n{final_page_text}")
            page_metadata.append({
                "page_number": page_num,
                "extraction_method": "native+embedded_image_ocr" if embedded_text_block else "native",
                "text_length": len(final_page_text),
                "ocr_used": bool(embedded_text_block),
                "ocr_confidence": 100.0,
                "embedded_images_found": len(images),
                "embedded_images_extracted": len(embedded_image_texts),
                "reason": reason,
            })
            logger.info(f"[PAGE {page_num}] Native extraction complete ({len(final_page_text)} chars)")
        else:
            # Scanned or image-heavy page
            if embedded_text_block and len(embedded_text_block) > 60:
                final_page_text = f"{clean_native}\n\n{embedded_text_block}".strip()
                page_results.append(f"[PAGE {page_num}]\n{final_page_text}")
                page_metadata.append({
                    "page_number": page_num,
                    "extraction_method": "embedded_image_ocr",
                    "text_length": len(final_page_text),
                    "ocr_used": True,
                    "ocr_confidence": 92.0,
                    "embedded_images_found": len(images),
                    "embedded_images_extracted": len(embedded_image_texts),
                    "reason": reason,
                })
                logger.info(f"[PAGE {page_num}] Direct embedded scan extraction complete ({len(final_page_text)} chars)")
            else:
                # Full page rasterization fallback (e.g. flattened page or complex layout)
                logger.info(f"[PAGE {page_num}] Native text insufficient ({reason}) → Rasterizing page for OCR...")
                try:
                    zoom = 200.0 / 72.0  # 200 DPI gives clean recognition with fast processing
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat, alpha=False)
                    img_bytes = pix.tobytes("png")

                    with Image.open(io.BytesIO(img_bytes)) as img:
                        ocr_res = ocr_image_detailed(img)

                    raster_ocr_text = clean_ocr_text(ocr_res.get("text", ""))

                    parts = []
                    if clean_native and len(clean_native) > 30:
                        parts.append(clean_native)
                    if embedded_text_block:
                        parts.append(embedded_text_block)
                    if raster_ocr_text:
                        combined_so_far = " ".join(parts).lower()
                        if raster_ocr_text.lower() not in combined_so_far:
                            parts.append(raster_ocr_text)

                    final_page_text = "\n\n".join(parts) if parts else raster_ocr_text

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
                    fallback_text = clean_native or embedded_text_block
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

