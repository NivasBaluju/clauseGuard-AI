import io
import logging
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import cv2
import pytesseract
from flask import current_app

logger = logging.getLogger(__name__)

# Fallback OCR engine if Tesseract is missing
_rapidocr_engine = None

def get_rapidocr():
    global _rapidocr_engine
    if _rapidocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _rapidocr_engine = RapidOCR()
        except Exception as e:
            logger.warning(f"Could not initialize RapidOCR fallback: {e}")
    return _rapidocr_engine

def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Grayscale, deskew/normalize, and contrast-enhance image for higher OCR accuracy.
    """
    try:
        # Convert PIL to CV2 grayscale
        cv_img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)

        # Contrast adjustment (adaptive thresholding or Otsu)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return Image.fromarray(thresh)
    except Exception as e:
        logger.warning(f"OpenCV preprocessing failed, falling back to Pillow: {e}")
        gray = ImageOps.grayscale(image)
        return gray.filter(ImageFilter.SHARPEN)

def ocr_image(image: Image.Image) -> str:
    """
    Performs OCR on an image. Uses Tesseract if configured/installed,
    falling back seamlessly to RapidOCR.
    """
    processed = preprocess_for_ocr(image)

    # 1. Try pytesseract first
    try:
        tess_cmd = current_app.config.get("TESSERACT_CMD") if current_app else None
        if tess_cmd:
            pytesseract.pytesseract.tesseract_cmd = tess_cmd
        text = pytesseract.image_to_string(processed)
        if text and len(text.strip()) > 0:
            return text
    except Exception as e:
        logger.info(f"Tesseract not available or failed: {e}. Trying RapidOCR fallback...")

    # 2. Try RapidOCR fallback
    rapid = get_rapidocr()
    if rapid:
        try:
            cv_img = np.array(processed)
            result, _ = rapid(cv_img)
            if result:
                lines = [line[1] for line in result]
                return "\n".join(lines)
        except Exception as ex:
            logger.error(f"RapidOCR failed: {ex}")

    return ""
