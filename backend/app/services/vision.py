from PIL import Image
import pytesseract
import io

async def extract_text(file):
    if not file:
        return ""

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    text = pytesseract.image_to_string(image)
    return text.strip()