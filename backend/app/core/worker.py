import asyncio
from app.core.queue import queue
from app.core.reasoning import analyze_ingredients

async def worker():
    while True:
        image, text = await queue.get()
        try:
            await analyze_ingredients(image, text)
        except Exception as e:
            print("Worker error:", e)
        finally:
            queue.task_done()
