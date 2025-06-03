import json
from pathlib import Path


def load_config(config_path) -> dict:
    full_path = Path(config_path)
    with full_path.open("r", encoding="utf-8") as f:
        return json.load(f)
