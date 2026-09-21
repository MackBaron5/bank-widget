import pytest
from src.masks import get_mask_card_number, get_mask_account

@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79 ** 6361"),
        ("1111222233334444", "1111 22 ** 4444"),
    ]
)
def test_get_mask_card_number_valid(card_number, expected):
    """Тестирование правильности маскирования валидного ноaмера карты."""
    assert get_mask_card_number(card_number) == expected

@pytest.mark.parametrize(
    "invalid_card",
    [
        "12345",
        "123456789012345a",
        "",
    ]
)
def test_get_mask_card_number_invalid(invalid_card):
    """Проверка работы при некорректных входных форматах номеров карт."""
    assert get_mask_card_number(invalid_card) == "Некорректный номер карты"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
    ]
)
def test_get_mask_account_number_valid(account_number, expected):
    """Тестирование правильности маскирования номера счета."""
    assert get_mask_account(account_number) == expected

@pytest.mark.parametrize(
    "invalid_account",
    [
        "123",
        "123a",
        "",
    ]
)
def test_get_mask_account_number_invalid(invalid_account):
    """Проверка обработки входных данных, где номер счета меньше ожидаемого."""
    assert get_mask_account(invalid_account) == "Некорректный номер счета"