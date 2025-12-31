from fastapi import APIRouter, UploadFile, File, Form, Request
from backend.app.core.reasoning import analyze_ingredients
from backend.app.core.history import get_history
from backend.app.core.limiter import limiter

router = APIRouter(prefix="/analyze", tags=["analysis"])

@router.post("/")
@limiter.limit("10/minute")
async def analyze(
    request: Request,
    image: UploadFile = File(None),
    text: str = Form(None),
    user_id: str = Form(...)
):
    return await analyze_ingredients(image, text, user_id)

@router.get("/history/{user_id}")
def history(user_id: str):
    return get_history(user_id)
