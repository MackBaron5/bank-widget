from typing import Any

import pandas as pd


def read_csv_file(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Возвращает список словарей с транзакциями.
    Если файл не найден или пуст, возвращает пустой список.
    """
    try:
        # Читаем CSV с разделителем точки с запятой
        df = pd.read_csv(file_path, sep=";")

        # Заменяем значения NaN на пустые строки, чтобы не сломать логику
        df = df.fillna("")

        # Конвертируем датафрейм в список словарей
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []
    except Exception:
        return []


def read_excel_file(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (XLSX).

    Возвращает список словарей с транзакциями.
    Если файл не найден или пуст, возвращает пустой список.
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)

        # Заменяем значения NaN на пустые строки
        df = df.fillna("")

        # Конвертируем датафрейм в список словарей
        return df.to_dict(orient="records")
    except (FileNotFoundError, ValueError):
        return []
    except Exception:
        return []
