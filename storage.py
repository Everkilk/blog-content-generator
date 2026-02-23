import json
import os
from pathlib import Path

BASE_DIR     = Path(__file__).parent
HISTORY_DIR  = BASE_DIR / "history"
IMAGES_DIR   = HISTORY_DIR / "images"
HISTORY_JSON = HISTORY_DIR / "history.json"

# Ensure directories exist on import
HISTORY_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def load_history_from_disk() -> list:
    """Load history metadata from JSON. Returns list of dicts."""
    if not HISTORY_JSON.exists():
        return []
    try:
        with open(HISTORY_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_history_to_disk(history: list):
    """Persist history metadata to JSON."""
    with open(HISTORY_JSON, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def save_image_to_disk(entry_id: str, image_bytes: bytes) -> str:
    """Save image bytes as full-resolution JPEG. Returns absolute path string."""
    img_path = IMAGES_DIR / f"{entry_id}.jpg"
    with open(img_path, "wb") as f:
        f.write(image_bytes)
    return str(img_path)


def delete_image_from_disk(image_path: str):
    """Delete an image file from disk if it exists."""
    try:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
    except OSError:
        pass
