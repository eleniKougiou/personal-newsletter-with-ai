import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_FILE = "../config/state.json"

def get_last_run() -> datetime:
    if os.getenv("DEV_MODE", "false").lower() == "true":
        return datetime.now(timezone.utc) - timedelta(weeks=1)
    if not Path(STATE_FILE).exists():
        return datetime.now(timezone.utc) - timedelta(weeks=1)
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return datetime.fromisoformat(data["last_run"])

def save_last_run():
    with open(STATE_FILE, "w") as f:
        json.dump({"last_run": datetime.now(timezone.utc).isoformat()}, f)