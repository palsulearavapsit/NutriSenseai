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
        img = Image.open(io.BytesIO(contents)).convert("RGB")

        results = reader.readtext(img, detail=0)
        return " ".join(results)

    except Exception as e:
        print(f"OCR error: {e}")
        return ""