from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа входных данных"""
    if not info:
        return "Некоректные данные"

    parts = info.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        return f"{name} {get_mask_account(number)}"
    else:
        return f"{name} {get_mask_card_number(number)}"


def get_date(date_str: str) -> str:
    """Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ."""
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y")