import json
import logging
import os
from typing import Any, Dict, List
import pandas as pd

logger = logging.getLogger(__name__)


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel-файла и возвращает список словарей.
    Если файл отсутствует или поврежден, возвращает пустой список.
    """
    logger.info(f"Попытка считывания транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Критическая ошибка: Файл {file_path} не найден.")
        return []

    try:
        # Читаем Excel с помощью pandas
        df = pd.read_excel(file_path)

        # Заменяем все NaN/NaT значения на None, чтобы избежать ошибок при конвертации в JSON
        df = df.astype(object).where(pd.notnull(df), None)

        # Превращаем DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно загружено {len(transactions)} транзакций.")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при парсинге Excel-файла: {e}")
        return []
