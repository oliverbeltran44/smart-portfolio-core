# src/smart_portfolio/json_storage.py
import json
from pathlib import Path


def guardar_portafolio(data: dict, filename: str = "portafolio.json") -> None:
    path = Path(filename)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
