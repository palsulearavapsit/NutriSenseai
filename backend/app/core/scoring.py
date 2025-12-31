def compute_scores(classified):
    health = 10
    processing = 10

    for item in classified:
        if item["category"] == "sugar":
            health -= 3
        if item["category"] == "fat":
            health -= 2
        if item["category"] == "additive":
            health -= 2
            processing -= 3

    return {
        "health_score": max(1, health),
        "processing_score": max(1, processing)
    }
