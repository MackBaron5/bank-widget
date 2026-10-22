import json
from src.views import generate_events_page, generate_main_page
from unittest.mock import patch
from src.views import get_stock_prices


def test_generate_main_page():
    """Тест формирования структуры JSON для главной страницы."""
    transactions = [
        {
            "Статус": "OK",
            "Номер карты": "4321",
            "Сумма платежа": -500.0,
            "Сумма операции": -500.0,
            "Дата операции": "20.10.2026 14:30:00",
            "Категория": "Кино",
            "Описание": "Билеты",
        }
    ]
    result_str = generate_main_page("2026-10-20 14:30:00", transactions)
    result = json.loads(result_str)

    assert "greeting" in result
    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 1
    assert result["cards"][0]["total_spent"] == 500.0


def test_generate_events_page():
    """Тест агрегации расходов и доходов за месяц на странице События."""
    transactions = [
        {"Статус": "OK", "Дата операции": "20.10.2026 12:00:00", "Сумма операции": -300.0},
        {"Статус": "OK", "Дата операции": "21.10.2026 15:00:00", "Сумма операции": 1000.0},
        {"Статус": "OK", "Дата операции": "15.09.2026 10:00:00", "Сумma операции": -500.0},
    ]
    result_str = generate_events_page("2026-10-20 14:30:00", transactions)
    result = json.loads(result_str)

    assert result["period"] == "2026-10"
    assert result["total_transactions_count"] == 2
    assert result["expenses_summary"] == 300.0
    assert result["income_summary"] == 1000.0


def test_get_stock_prices_success():
    """Тест успешного парсинга ответа от Alpha Vantage API."""
    mock_response = {
        "Global Quote": {
            "05. price": "180.50"
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_stock_prices(["AAPL"])
        assert result == [{"stock": "AAPL", "price": 180.50}]
