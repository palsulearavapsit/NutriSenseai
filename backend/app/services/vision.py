from fastapi import UploadFile
import easyocr
from PIL import Image
import io

reader = easyocr.Reader(["en"], gpu=False)

async def extract_text(image: UploadFile | None) -> str:
    if not image:
        return ""

    try:
        contents = await image.read()
        if not contents:
            return ""

        img = Image.open(io.BytesIO(contents)).convert("RGB")
        results = reader.readtext(img)

        text = " ".join(r[1] for r in results if isinstance(r, (list, tuple)) and len(r) > 1)

        return text.strip()

    except Exception as e:
        print("OCR error:", e)
        return ""