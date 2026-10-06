import json
import logging
import os
from pathlib import Path
from typing import Any

# Создаем папку logs в корне проекта, если её еще нет
os.makedirs("logs", exist_ok=True)

# 1. Создаем объект логера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# 2. Настраиваем file_handler для записи в файл с перезаписью ('w')
file_handler = logging.FileHandler(
    "logs/utils.log", mode="w", encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# 3. Настраиваем формат записи логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# 4. Устанавливаем хендлер для логера
logger.addHandler(file_handler)


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает JSON-файл с транзакциями и возвращает список словарей."""
    path = Path(file_path)

    if not path.exists():
        # Логирование ошибочного случая (уровень ERROR)
        logger.error(f"Файл не найден по пути: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # Логирование успешного случая (уровень INFO)
                logger.info(
                    f"Успешно прочитан JSON-файл: {path}. "
                    f"Найдено транзакций: {len(data)}"
                )
                return data

            logger.error(
                f"Неверный формат данных в файле {path}: "
                f"ожидался список, получен {type(data)}"
            )
            return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении файла {path}: {e}")
        return []
