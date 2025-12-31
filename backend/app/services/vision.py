from PIL import Image
import pytesseract

async def extract_text(image_file):
    try:
        contents = await image_file.read()
        img = Image.open(io.BytesIO(contents))

        # Optional: improve OCR quality
        img = img.convert("L")

        text = pytesseract.image_to_string(img)
        return text.strip()

    except Exception as e:
        print("OCR error:", e)
        return ""