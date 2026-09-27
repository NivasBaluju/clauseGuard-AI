import io
import os
import logging
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import cv2
import pytesseract
from flask import current_app

logger = logging.getLogger(__name__)

# Fallback OCR engine if Tesseract is missing
_rapidocr_engine = None

def get_tesseract_lang() -> str:
    """Configurable Tesseract OCR language (default 'eng')."""
    return os.environ.get("TESSERACT_LANG", "eng")

def get_tesseract_config() -> str:
    """Configurable Tesseract page segmentation mode (default '--oem 3 --psm 3')."""
    return os.environ.get("TESSERACT_CONFIG", "--oem 3 --psm 3")

def configure_tesseract_cmd():
    """Configures pytesseract command from TESSERACT_CMD env or Flask config if present."""
    cmd = os.environ.get("TESSERACT_CMD")
    if not cmd and current_app:
        cmd = current_app.config.get("TESSERACT_CMD")
    if cmd and os.path.exists(cmd):
        pytesseract.pytesseract.tesseract_cmd = cmd

def is_tesseract_available() -> bool:
    """Verifies whether Tesseract executable is installed and runnable."""
    try:
        configure_tesseract_cmd()
        version = pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

def get_rapidocr():
    """Initializes or returns singleton RapidOCR ONNX fallback engine."""
    global _rapidocr_engine
    if _rapidocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _rapidocr_engine = RapidOCR()
            logger.info("RapidOCR fallback engine initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not initialize RapidOCR fallback: {e}")
    return _rapidocr_engine

def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Grayscale, noise reduction, and contrast enhancement for legal document scans.
    Preserves clean text boundaries without over-thresholding.
    """
    try:
        # Convert PIL to CV2 grayscale
        cv_img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

        # Contrast adjustment & gentle denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        # Otsu binary thresholding
        blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return Image.fromarray(thresh)
    except Exception as e:
        logger.debug(f"OpenCV advanced preprocessing failed, falling back to Pillow: {e}")
        try:
            gray = ImageOps.grayscale(image)
            return gray.filter(ImageFilter.SHARPEN)
        except Exception:
            return image

def ocr_image_detailed(image: Image.Image) -> Dict[str, Any]:
    """
    Performs OCR on an image with full audit metadata.
    Attempts Tesseract first (--oem 3 --psm 3), calculating average confidence.
    Gracefully falls back to RapidOCR if Tesseract is unavailable or fails.
    Never crashes the calling process.
    """
    processed = preprocess_for_ocr(image)
    lang = get_tesseract_lang()
    config = get_tesseract_config()
    configure_tesseract_cmd()

    # 1. Try pytesseract first
    try:
        # Check if tesseract binary is runnable
        data = pytesseract.image_to_data(processed, lang=lang, config=config, output_type=pytesseract.Output.DICT)
        text = pytesseract.image_to_string(processed, lang=lang, config=config).strip()

        # Compute average confidence from detected word tokens
        confs = [float(c) for c in data.get("conf", []) if str(c).strip() not in ("-1", "")]
        avg_conf = round(float(np.mean(confs)), 2) if confs else 0.0
        word_count = len([w for w in data.get("text", []) if w.strip()])

        if text:
            logger.info(f"[OCR] Tesseract extraction succeeded (Confidence: {avg_conf}%, Words: {word_count})")
            return {
                "text": text,
                "method": "tesseract",
                "ocr_confidence": avg_conf,
                "word_count": word_count,
                "error": None,
            }
    except Exception as e:
        logger.info(f"[OCR] Tesseract unavailable or failed ({e}). Proceeding to RapidOCR fallback...")

    # 2. Try RapidOCR fallback
    rapid = get_rapidocr()
    if rapid:
        try:
            cv_img = np.array(processed)
            result, _ = rapid(cv_img)
            if result:
                lines = []
                confs = []
                for item in result:
                    lines.append(item[1])
                    if len(item) > 2 and isinstance(item[2], (int, float)):
                        confs.append(float(item[2]) * 100.0)

                combined_text = "\n".join(lines).strip()
                avg_conf = round(float(np.mean(confs)), 2) if confs else 85.0
                word_count = len(combined_text.split())

                logger.info(f"[OCR] RapidOCR extraction succeeded (Confidence: {avg_conf}%, Words: {word_count})")
                return {
                    "text": combined_text,
                    "method": "rapidocr",
                    "ocr_confidence": avg_conf,
                    "word_count": word_count,
                    "error": None,
                }
        except Exception as ex:
            logger.error(f"[OCR] RapidOCR fallback failed: {ex}")

    # 3. Both failed gracefully
    logger.warning("[OCR] Both Tesseract and RapidOCR were unable to extract text.")
    return {
        "text": "",
        "method": "ocr_failed",
        "ocr_confidence": 0.0,
        "word_count": 0,
        "error": "OCR engines unavailable or image unreadable",
    }

def ocr_image(image: Image.Image) -> str:
    """
    Standard interface: returns extracted text string.
    """
    res = ocr_image_detailed(image)
    return res.get("text", "")

