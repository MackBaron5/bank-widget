import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура, предоставляющая тестовый набор транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет"
        }
    ]



def test_filter_by_currency_valid(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка корректной фильтрации транзакций по существующей валюте."""
    usd_iterator = filter_by_currency(sample_transactions, "USD")
    result = list(usd_iterator)
    assert len(result) == 2
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268

def test_filter_by_currency_missing(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка случая, когда транзакции в заданной валюте отсутствуют."""
    eur_iterator = filter_by_currency(sample_transactions, "EUR")
    assert list(eur_iterator) == []

def test_filter_by_currency_empty_list() -> None:
    """Убеждаемся, что генератор не падает при обработке пустого списка."""
    assert list(filter_by_currency([], "USD")) == []



@pytest.mark.parametrize(
    "input_data, expected_descriptions",
    [
        (
            [{"description": "Оплата услуг"}, {"description": "Перевод другу"}],
            ["Оплата услуг", "Перевод другу"]
        ),
        ([], []),
        ([{"id": 123}], [""])
    ]
)
def test_transaction_descriptions(input_data: List[Dict[str, Any]], expected_descriptions: List[str]) -> None:
    """Тестирование получения описаний транзакций с разным количеством входных данных."""
    desc_iterator = transaction_descriptions(input_data)
    assert list(desc_iterator) == expected_descriptions



@pytest.mark.parametrize(
    "start, stop, expected_list",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
        (5, 5, ["0000 0000 0000 0005"])  # Граничное значение диапазона из одного элемента
    ]
)
def test_card_number_generator_range(start: int, stop: int, expected_list: List[str]) -> None:
    """Проверяет генерацию правильных номеров карт и форматирование в заданных диапазонах."""
    gen = card_number_generator(start, stop)
    assert list(gen) == expected_list