import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def get_cashback_profit(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует, сколько кэшбэка можно заработать по каждой категории за указанный период.
    """
    logger.info(f"Запуск анализа кэшбэка за {year}-{month:02d}")

    # Фильтруем успешные транзакции за нужный месяц и год
    filtered = []
    for t in data:
        if t.get("Статус") != "OK" or not t.get("Дата операции"):
            continue
        try:
            # Парсим дату формата DD.MM.YYYY hh:mm:ss
            date_obj = datetime.strptime(str(t["Дата операции"]), "%d.%m.%Y %H:%M:%S")
            if date_obj.year == year and date_obj.month == month:
                filtered.append(t)
        except Exception:
            continue

    cashback_by_category = {}
    for t in filtered:
        category = t.get("Категория")
        cashback = t.get("Кэшбэк")

        if not cashback and t.get("Сумма операции"):
            cashback = abs(t["Сумма операции"]) // 100

        if category and cashback:
            cashback_by_category[category] = cashback_by_category.get(category, 0) + int(cashback)

    return json.dumps(cashback_by_category, ensure_ascii=False, indent=4)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму округления трат в инвесткопилку за месяц 'YYYY-MM'.
    """
    logger.info(f"Расчет инвесткопилки за {month} с шагом {limit}")
    total_saved = 0.0

    for t in transactions:
        if t.get("Статус") != "OK" or not t.get("Дата операции"):
            continue

        # Для сервиса инвесткопилки даты приходят в формате YYYY-MM-DD по ТЗ
        date_str = str(t["Дата операции"])
        if not date_str.startswith(month):
            continue

        amount = t.get("Сумма операции")
        if amount and amount < 0:
            expense = abs(amount)
            if expense % limit == 0:
                rounded = expense
            else:
                rounded = ((expense // limit) + 1) * limit
            total_saved += (rounded - expense)

    return round(total_saved, 2)


def simple_search(data: List[Dict[str, Any]], query: str) -> str:
    """Простой поиск по подстроке в категории или описании."""
    q = query.lower()
    res = [
        t for t in data
        if q in str(t.get("Описание", "")).lower() or q in str(t.get("Категория", "")).lower()
    ]
    return json.dumps(res, ensure_ascii=False, indent=4)


def search_by_phone_number(data: List[Dict[str, Any]]) -> str:
    """Поиск транзакций, содержащих телефонные номера."""
    phone_pattern = re.compile(r"(\+7|8)?\s*\(?\d{3}\)?\s*\d{3}-?\d{2}-?\d{2}")
    res = [t for t in data if t.get("Описание") and phone_pattern.search(str(t["Описание"]))]
    return json.dumps(res, ensure_ascii=False, indent=4)


def search_transfers_to_individuals(data: List[Dict[str, Any]]) -> str:
    """Поиск переводов физлицам (Категория 'Переводы' и имя И.)."""
    name_pattern = re.compile(r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.")
    res = [
        t for t in data
        if t.get("Категория") == "Переводы" and t.get("Описание") and name_pattern.search(str(t["Описание"]))
    ]
    return json.dumps(res, ensure_ascii=False, indent=4)
