import io
import os
import logging
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF
import docx
from app.services.ingestion.ocr import ocr_image

logger = logging.getLogger(__name__)

MIN_CHARS_TO_TRUST_TEXT_LAYER = 25

class UnsupportedFormatError(Exception):
    pass

def read_plain_text(file_path: str) -> tuple[str, int]:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    # Estimate pages for plain text (~3000 chars per page)
    page_count = max(1, (len(text) // 3000) + 1)
    return text, page_count

def extract_docx(file_path: str) -> tuple[str, int]:
    """
    Extracts text from DOCX files preserving paragraph and table structure in document order.
    """
    doc = docx.Document(file_path)
    content = []
    
    # Iterate over body elements to preserve order of paragraphs and tables
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
                    
    full_text = "\n\n".join(content)
    page_count = max(1, (len(full_text) // 3000) + 1)
    return full_text, page_count

def extract_pdf(file_path: str) -> tuple[str, int]:
    """
    Extracts text from digital PDFs using PyMuPDF.
    If the extracted text layer is empty or below threshold (scanned PDF),
    falls back to page-by-page OCR rasterized at 300 DPI.
    """
    doc = fitz.open(file_path)
    page_count = len(doc)
    text_layer = "".join(page.get_text() for page in doc)
    
    if len(text_layer.strip()) >= MIN_CHARS_TO_TRUST_TEXT_LAYER:
        logger.info(f"PDF {file_path} has valid digital text layer ({len(text_layer.strip())} chars). Skipping OCR.")
        doc.close()
        return text_layer, page_count
        
    logger.info(f"PDF {file_path} appears scanned or lacks text layer. Starting OCR rasterization at 300 DPI...")
    pages_text = []
    for i, page in enumerate(doc):
        # 300 DPI = zoom factor 300/72 ≈ 4.166
        zoom = 300 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        page_text = ocr_image(img)
        pages_text.append(page_text)
        
    doc.close()
    return "\n\n".join(pages_text), page_count

def extract_text(file_path: str, ext: str) -> tuple[str, int]:
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
