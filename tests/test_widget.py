import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79 ** 6361"),
        ("Маэстро 1111222233334444", "Маэстро 1111 22 ** 4444"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]
)
def test_mask_account_card_valid(info, expected):
    """Проверка корректного распознавания типа входных данных (карта или счет)."""
    assert mask_account_card(info) == expected

@pytest.mark.parametrize(
    "invalid_info",
    [
        "Visa Platinum 123",
        "Счет 12",
        "",
    ]
)
def test_mask_account_card_invalid(invalid_info):
    """Тестирование устойчивости функции к ошибкам при некорректных данных."""
    res = mask_account_card(invalid_info)
    assert "Некорректный" in res or res == ""


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2026-09-21T17:45:00.000000", "21.09.2026"),
    ]
)
def test_get_date_valid(date_str, expected):
    """Тестирование правильности преобразования ISO-даты."""
    assert get_date(date_str) == expected

@pytest.mark.parametrize(
    "invalid_date",
    [
        "invalid-date-string",
        "",
    ]
)
def test_get_date_invalid(invalid_date):
    """Проверка корректности обработки строк, где формат даты нарушен."""
    with pytest.raises(Exception):
        get_date(invalid_date)