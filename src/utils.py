import json
from pathlib import Path
from typing import Any


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает JSON-файл с транзакциями и возвращает список словарей.

    Если файл пустой, не найден или содержит не список, возвращает пустой список.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, TypeError):
        return []
