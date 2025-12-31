import json
from pathlib import Path

BASE = Path("backend/history")
BASE.mkdir(exist_ok=True, parents=True)


def save_history(user_id: str, data: dict):
    """
    Append a scan result to the user's history file.
    """
    try:
        file = BASE / f"{user_id}.json"
        history = []

        if file.exists():
            history = json.loads(file.read_text())

        history.append(data)
        file.write_text(json.dumps(history, indent=2))

    except Exception as e:
        print("History save error:", e)


def get_history(user_id: str):
    """
    Load and return the user's scan history.
    """
    try:
        file = BASE / f"{user_id}.json"

        if not file.exists():
            return []

        return json.loads(file.read_text())

    except Exception as e:
        print("History load error:", e)
        return []
