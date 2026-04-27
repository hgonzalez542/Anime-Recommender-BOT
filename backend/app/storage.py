import json
from pathlib import Path

# Get correct path regardless of where you run the server
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure folder exists
DATA_DIR.mkdir(exist_ok=True)

FILE_PATH = DATA_DIR / "history.json"


def save_history(prompt, response):
    data = []

    if FILE_PATH.exists():
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append({
        "prompt": prompt,
        "response": response
    })

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def recent_recommended_titles():
    import os
    import json

    path = "backend/data/history.json"

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except:
            return []

    titles = []

    for entry in data[-10:]:  # last 10 searches
        for anime in entry.get("response", []):
            if anime["title"] not in titles:
                titles.append(anime["title"])

    return titles