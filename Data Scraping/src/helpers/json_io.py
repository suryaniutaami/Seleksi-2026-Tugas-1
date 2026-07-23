from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def read_json(file_path: str | Path) -> Any:
    path = Path(file_path)
    
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"File JSON tidak valid: {path}"
        ) from error

def write_json(file_path: str | Path, data: Any, *, indent: int = 2) -> None:
    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)