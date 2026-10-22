import json
from src.services import investment_bank, simple_search


def test_investment_bank_savings():
    """Тест округления транзакций в инвесткопилку."""
    transactions = [
        {"Статус": "OK", "Дата операции": "2026-10-15", "Сумма операции": -1712.0},
        {"Статус": "OK", "Дата операции": "2026-10-16", "Сумма операции": -1500.0},
        {"Статус": "FAILED", "Дата операции": "2026-10-17", "Сумма операции": -100.0}
    ]
    # Для -1712 округление до 50 даст 1750 (сбережения 38)
    # Для -1500 округление до 50 даст 1500 (сбережения 0)
    # Третья транзакция FAILED — игнорируется
    result = investment_bank("2026-10", transactions, 50)
    assert result == 38.0


def test_simple_search():
    """Тест простого поиска по описанию."""
    data = [
        {"Описание": "Покупка в Супермаркете Lenta", "Категория": "Супермаркеты"},
        {"Описание": "Оплата ЖКХ Квартира", "Категория": "Коммунальные платежи"}
    ]
    search_result_str = simple_search(data, "lenta")
    search_result = json.loads(search_result_str)

    assert len(search_result) == 1
    assert "Lenta" in search_result[0]["Описание"]
