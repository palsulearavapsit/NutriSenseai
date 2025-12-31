import re
from backend.app.services.llm import run_llm
from backend.app.core.history import save_history

MAX_LEN = 2000

def normalize_ingredients(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\n\r\t]", " ", text)
    text = re.sub(r"[^a-z0-9,.\s]", "", text)
    text = re.sub(r"ingredients\s*:", "", text)
    text = re.sub(r"\s*,\s*", ", ", text)
    text = re.sub(r"\s{2,}", " ", text)

    parts = [p.strip() for p in text.split(",")]
    seen, clean = set(), []
    for p in parts:
        if p and p not in seen:
            seen.add(p)
            clean.append(p)

    return ", ".join(clean)

async def analyze_ingredients(image, text, user_id: str):
    ingredients = (text or "").strip()
    ingredients = normalize_ingredients(ingredients)[:MAX_LEN]

    if not ingredients:
        return {"error": "No ingredients provided"}

    try:
        explanation = await run_llm(ingredients)
    except Exception:
        explanation = "AI service temporarily unavailable."

    parts = [p.strip() for p in ingredients.split(",")]

    categories = []
    for p in parts:
        if "sugar" in p:
            cat, impact = "sugar", 9
        elif "oil" in p or "butter" in p:
            cat, impact = "fat", 8
        elif "lecithin" in p or "flavor" in p:
            cat, impact = "additive", 6
        else:
            cat, impact = "other", 3

        categories.append({"name": p, "category": cat, "impact": impact})

    total = sum(c["impact"] for c in categories)
    health_score = max(1, min(10, 10 - total // 6))
    label = "Good" if health_score >= 7 else "Moderate" if health_score >= 4 else "Poor"

    result = {
        "ingredients": ingredients,
        "categories": categories,
        "health_score": health_score,
        "health_label": label,
        "analysis": explanation
    }

    save_history(user_id, result)
    return result
