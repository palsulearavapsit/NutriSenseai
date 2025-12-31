import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.core.prompts import SYSTEM_PROMPT
import asyncio
from cachetools import TTLCache

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)

# KEEPING YOUR MODEL NAME
model = genai.GenerativeModel("gemini-2.5-flash")

cache = TTLCache(maxsize=256, ttl=3600)

async def run_llm(ingredients: str):
    if ingredients in cache:
        return cache[ingredients]

    prompt = SYSTEM_PROMPT + "\n\nUser is looking at this product or ingredient list:\n" + ingredients

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        text = response.text
    except Exception as e:
        print("Gemini error:", e)
        return "AI service temporarily unavailable. Please try again."

    cache[ingredients] = text
    return text
