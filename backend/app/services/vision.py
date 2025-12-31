import easyocr
import tempfile
from PIL import Image
import numpy as np

# Initialize OCR reader once (important for performance)
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_file):
    """
    Extracts text from an uploaded image using EasyOCR.
    Works in cloud environments like Render.

    image_file: file-like object or path
    returns: extracted text as string
    """

    try:
        # If it's a file-like object (UploadFile), convert to numpy array
        if hasattr(image_file, "read"):
            img = Image.open(image_file).convert("RGB")
            img_np = np.array(img)
        else:
            img_np = image_file  # assume it's already an image path or numpy array

        results = reader.readtext(img_np)

        # Combine detected text lines
        extracted_text = " ".join([res[1] for res in results])

        return extracted_text.strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""
