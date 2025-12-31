import json
from pathlib import Path

BASE = Path("backend/history")
BASE.mkdir(exist_ok=True)

def save_history(user_id: str, data: dict):
    try:
        file = BASE / f"{user_id}.json"
        history = []

        if file.exists():
            history = json.loads(file.read_text())

        history.append(data)
        file.write_text(json.dumps(history, indent=2))

    except Exception as e:
        print("History error:", e)
