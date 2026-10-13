import re
from collections import Counter


def process_bank_search(data: list[dict], search_str: str) -> list[dict]:
    """Ищет операции по заданной строке в описании с помощью re."""
    if not search_str:
        return data

    result = []
    pattern = re.compile(re.escape(search_str), re.IGNORECASE)

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество определенных банковских операций.

    Возвращает словарь вида {название_категории: количество}.
    """
    descriptions = [
        transaction.get("description", "") for transaction in data
    ]
    counts = Counter(descriptions)

    return {category: counts[category] for category in categories}
