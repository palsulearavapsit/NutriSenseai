CATEGORY_MAP = {
    "sugar": ("sugar", 9),
    "palm oil": ("fat", 8),
    "soy lecithin": ("additive", 4),
    "artificial flavor": ("additive", 6),
    "salt": ("other", 3),
    "cocoa solids": ("other", 2),
}

def classify(ingredients: list[str]):
    results = []
    for ing in ingredients:
        key = ing.lower()
        for k in CATEGORY_MAP:
            if k in key:
                cat, score = CATEGORY_MAP[k]
                results.append({
                    "name": ing,
                    "category": cat,
                    "impact": score
                })
                break
        else:
            results.append({
                "name": ing,
                "category": "other",
                "impact": 3
            })
    return results
