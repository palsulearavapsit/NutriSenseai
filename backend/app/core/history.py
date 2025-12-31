import json
from pathlib import Path

HISTORY_DIR = Path("history")
HISTORY_DIR.mkdir(exist_ok=True)

def _file(user_id: str) -> Path:
    return HISTORY_DIR / f"{user_id}.json"

def save_history(user_id: str, data: dict):
    f = _file(user_id)
    if f.exists():
        history = json.loads(f.read_text())
    else:
        history = []

    data["timestamp"] = datetime.utcnow().isoformat()
    history.append(data)

    f.write_text(json.dumps(history, indent=2))

def get_history(user_id: str):
    f = _file(user_id)
    if not f.exists():
        return []
    return json.loads(f.read_text())
