import io
import os
import logging
from typing import Dict, Any, Optional
import numpy as np
from PIL import Image, ImageOps, ImageFilter
try:
    import cv2
except Exception as _cv_err:
    cv2 = None
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

# Cached Tesseract availability flag
_tesseract_available_cached = None

def is_tesseract_available() -> bool:
    """Verifies whether Tesseract executable is installed and runnable (cached)."""
    global _tesseract_available_cached
    if _tesseract_available_cached is not None:
        return _tesseract_available_cached
    try:
        configure_tesseract_cmd()
        pytesseract.get_tesseract_version()
        _tesseract_available_cached = True
    except Exception:
        _tesseract_available_cached = False
    return _tesseract_available_cached

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

def preprocess_for_tesseract(image: Image.Image) -> Image.Image:
    """
    Fast grayscale, Gaussian blur, and Otsu binary thresholding for Tesseract.
    Avoids slow denoising filters for maximum throughput.
    """
    try:
        cv_img = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return Image.fromarray(thresh)
    except Exception as e:
        logger.debug(f"Tesseract preprocessing failed, falling back to Pillow: {e}")
        try:
            return ImageOps.grayscale(image).filter(ImageFilter.SHARPEN)
        except Exception:
            return image

def preprocess_for_rapidocr(image: Image.Image) -> np.ndarray:
    """
    Prepares images for RapidOCR deep learning model.
    Handles transparency by compositing onto pure white background.
    Preserves natural RGB and performs high-quality upscaling on small images
    for optimal character stroke detection.
    """
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        alpha = image.convert("RGBA").split()[-1]
        bg = Image.new("RGB", image.size, (255, 255, 255))
        bg.paste(image, mask=alpha)
        image = bg
    elif image.mode != "RGB":
        image = image.convert("RGB")

    w, h = image.size
    # If image dimensions are small, upscale with Lanczos so font contours are sharp
    if w < 450 or h < 90:
        scale = max(2.0, 450.0 / max(1, w), 90.0 / max(1, h))
        if scale > 1.2:
            new_w, new_h = int(w * scale), int(h * scale)
            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return np.array(image)

def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """Backwards compatibility alias for image preprocessing."""
    return preprocess_for_tesseract(image)

def ocr_image_detailed(image: Image.Image) -> Dict[str, Any]:
    """
    Performs OCR on an image with full audit metadata.
    Tries Tesseract if available, or seamlessly leverages RapidOCR deep-learning engine.
    Includes inverted-color retry for white-on-dark text and transparency handling.
    Never crashes the calling process.
    """
    # 1. Try Tesseract first if installed
    if is_tesseract_available():
        try:
            processed = preprocess_for_tesseract(image)
            lang = get_tesseract_lang()
            config = get_tesseract_config()
            configure_tesseract_cmd()

            data = pytesseract.image_to_data(processed, lang=lang, config=config, output_type=pytesseract.Output.DICT)
            text = pytesseract.image_to_string(processed, lang=lang, config=config).strip()

            confs = [float(c) for c in data.get("conf", []) if str(c).strip() not in ("-1", "")]
            avg_conf = round(float(np.mean(confs)), 2) if confs else 0.0
            word_count = len([w for w in data.get("text", []) if w.strip()])

            if text and len(text.split()) >= 1:
                logger.info(f"[OCR] Tesseract extraction succeeded (Confidence: {avg_conf}%, Words: {word_count})")
                return {
                    "text": text,
                    "method": "tesseract",
                    "ocr_confidence": avg_conf,
                    "word_count": word_count,
                    "error": None,
                }
        except Exception as e:
            logger.info(f"[OCR] Tesseract failed ({e}). Proceeding to RapidOCR...")

    # 2. RapidOCR engine (highly accurate deep-learning model)
    rapid = get_rapidocr()
    if rapid:
        try:
            cv_img = preprocess_for_rapidocr(image)
            result, _ = rapid(cv_img)

            # Retry with color inversion if initial pass yields no text (e.g. white text on dark background)
            if not result:
                try:
                    rgb_img = image.convert("RGB")
                    inv_img = ImageOps.invert(rgb_img)
                    cv_img_inv = preprocess_for_rapidocr(inv_img)
                    result, _ = rapid(cv_img_inv)
                except Exception:
                    pass

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

                if combined_text:
                    logger.info(f"[OCR] RapidOCR extraction succeeded (Confidence: {avg_conf}%, Words: {word_count})")
                    return {
                        "text": combined_text,
                        "method": "rapidocr",
                        "ocr_confidence": avg_conf,
                        "word_count": word_count,
                        "error": None,
                    }
        except Exception as ex:
            logger.error(f"[OCR] RapidOCR extraction failed: {ex}")

    # 3. Graceful fallback if nothing recognized
    return {
        "text": "",
        "method": "ocr_none",
        "ocr_confidence": 0.0,
        "word_count": 0,
        "error": None,
    }

def ocr_image(image: Image.Image) -> str:
    """Standard interface: returns extracted text string."""
    res = ocr_image_detailed(image)
    return res.get("text", "")


