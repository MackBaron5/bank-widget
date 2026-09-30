from typing import Iterator, List, Dict, Any

def filter_by_currency(transactions: List[Dict[Any, Any]], currency: str) -> Iterator[Dict[Any, Any]]:
    """
    Фильтрует транзакции по заданной валюте операции.
    Возвращает итератор, который поочередно выдает подходящие транзакции.
    """
    for transaction in transactions:
        op_amount = transaction.get("operationAmount")
        if op_amount and isinstance(op_amount, dict):
            curr_info = op_amount.get("currency")
            if curr_info and isinstance(curr_info, dict):
                if curr_info.get("code") == currency:
                    yield transaction


def transaction_descriptions(transactions: List[Dict[Any, Any]]) -> Iterator[str]:
    """
    Принимает список транзакций и возвращает итератор с описанием (description)
    каждой операции по очереди.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне (включительно).
    Формат вывода: XXXX XXXX XXXX XXXX
    """
    for num in range(start, stop + 1):
        str_num = f"{num:016d}"
        formatted_card = f"{str_num[0:4]} {str_num[4:8]} {str_num[8:12]} {str_num[12:16]}"
        yield formatted_card