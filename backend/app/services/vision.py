import os
from PIL import Image
import pytesseract

def extract_text(image_path: str) -> str:
    """
    Lightweight OCR using Tesseract (safe for Render 512MB)
    """

    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        print("OCR error:", e)
        return ""
