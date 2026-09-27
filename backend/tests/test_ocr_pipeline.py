import unittest
import sys
import tempfile
import os
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import fitz
from app.services.ingestion.extractor import (
    extract_pdf_with_metadata,
    extract_pdf,
    clean_ocr_text,
    should_use_ocr,
)

class TestRobustPdfOcr(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.gettempdir()

    def test_hyphen_normalization(self):
        # Line-break hyphen should be merged
        text = "This agreement allows early termina-\n  tion under section 4."
        cleaned = clean_ocr_text(text)
        self.assertIn("termination", cleaned)

        # Legitimate legal hyphen compound should be preserved
        legal_compound = "The employee agrees to a reasonable non-compete covenant."
        cleaned_compound = clean_ocr_text(legal_compound)
        self.assertIn("non-compete", cleaned_compound)

    def test_native_text_pdf(self):
        pdf_path = os.path.join(self.temp_dir, "test_native.pdf")
        doc = fitz.open()
        p1 = doc.new_page()
        p1.insert_text((50, 50), "ARTICLE 1: TERM AND TERMINATION\nThis lease shall continue for twelve full calendar months with standard notice covenants.")
        doc.save(pdf_path)
        doc.close()

        full_text, page_count, metadata = extract_pdf_with_metadata(pdf_path)
        self.assertEqual(page_count, 1)
        self.assertIn("[PAGE 1]", full_text)
        self.assertIn("ARTICLE 1: TERM AND TERMINATION", full_text)
        self.assertEqual(metadata[0]["extraction_method"], "native")
        self.assertFalse(metadata[0]["ocr_used"])
        os.remove(pdf_path)

    def test_scanned_image_pdf(self):
        pdf_path = os.path.join(self.temp_dir, "test_scanned.pdf")
        # Create an image containing text rendered with PIL
        img = Image.new("RGB", (600, 200), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((20, 40), "CONFIDENTIAL SETTLEMENT CLAUSE", fill="black")
        draw.text((20, 80), "The parties agree to mutual non-disclosure.", fill="black")
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Create PDF with ONLY this image and NO text layer
        doc = fitz.open()
        page = doc.new_page(width=600, height=200)
        page.insert_image(page.rect, stream=img_bytes.read())
        doc.save(pdf_path)
        doc.close()

        full_text, page_count, metadata = extract_pdf_with_metadata(pdf_path)
        self.assertEqual(page_count, 1)
        self.assertIn("[PAGE 1]", full_text)
        self.assertTrue(metadata[0]["ocr_used"])
        # Should have detected and extracted through OCR engine (Tesseract or RapidOCR fallback)
        self.assertIn(metadata[0]["extraction_method"], ["tesseract", "rapidocr", "embedded_image_ocr"])
        self.assertTrue(len(full_text) > 10)
        os.remove(pdf_path)

    def test_mixed_pdf(self):
        pdf_path = os.path.join(self.temp_dir, "test_mixed.pdf")
        doc = fitz.open()

        # Page 1: Native digital text
        p1 = doc.new_page()
        p1.insert_text((50, 50), "PAGE 1 CONTENT: Standard employment offer letter with statutory at-will provisions and compensation schedule.")

        # Page 2: Image-only page
        img = Image.new("RGB", (600, 200), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((20, 50), "EXHIBIT A: RESTRICTIVE COVENANTS", fill="black")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        p2 = doc.new_page(width=600, height=200)
        p2.insert_image(p2.rect, stream=img_bytes.read())

        doc.save(pdf_path)
        doc.close()

        full_text, page_count, metadata = extract_pdf_with_metadata(pdf_path)
        self.assertEqual(page_count, 2)
        # Page 1 must be native
        self.assertEqual(metadata[0]["extraction_method"], "native")
        self.assertFalse(metadata[0]["ocr_used"])
        # Page 2 must be OCR
        self.assertTrue(metadata[1]["ocr_used"])
        self.assertIn(metadata[1]["extraction_method"], ["tesseract", "rapidocr", "embedded_image_ocr"])
        self.assertIn("[PAGE 1]", full_text)
        self.assertIn("[PAGE 2]", full_text)
        os.remove(pdf_path)

    def test_embedded_image_inside_text_page(self):
        """
        Verifies that when a PDF page has digital text AND an embedded image containing text,
        both the native digital text and the embedded image text are extracted cleanly.
        """
        pdf_path = os.path.join(self.temp_dir, "test_embedded_inside_text.pdf")
        doc = fitz.open()
        page = doc.new_page(width=612, height=792)

        # 1. Native text on page
        page.insert_text((50, 50), "COMMERCIAL LEASE AGREEMENT SECTION 1: PREMISES\nLandlord leases to Tenant the commercial property.")

        # 2. Embedded image on page with addendum clause
        img = Image.new("RGB", (600, 150), color="white")
        d = ImageDraw.Draw(img)
        d.text((20, 20), "ADDENDUM CLAUSE: RENT ESCALATION", fill="black")
        d.text((20, 60), "Base rent shall escalate by five percent annually on lease anniversary.", fill="black")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        rect = fitz.Rect(50, 150, 550, 280)
        page.insert_image(rect, stream=img_bytes.read())
        page.insert_text((50, 320), "SECTION 2: DEFAULT REMEDIES\nFailure to cure within ten days constitutes default.")

        doc.save(pdf_path)
        doc.close()

        full_text, page_count, metadata = extract_pdf_with_metadata(pdf_path)
        self.assertEqual(page_count, 1)
        self.assertIn("[PAGE 1]", full_text)
        self.assertIn("COMMERCIAL LEASE AGREEMENT", full_text)
        self.assertIn("SECTION 2: DEFAULT REMEDIES", full_text)
        self.assertTrue(metadata[0]["ocr_used"])
        self.assertGreaterEqual(metadata[0]["embedded_images_found"], 1)
        self.assertGreaterEqual(metadata[0]["embedded_images_extracted"], 1)
        # Verify text from embedded image was captured
        full_lower = full_text.lower()
        self.assertTrue(
            "escalat" in full_lower or "rent" in full_lower or "addendum" in full_lower,
            f"Expected image text in extraction, got: {full_text}"
        )
        os.remove(pdf_path)

if __name__ == "__main__":
    unittest.main()

