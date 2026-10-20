from unittest.mock import patch
import pytest
from src.external_api import convert_currency


@pytest.fixture
def usd_transaction() -> dict:
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }


@pytest.fixture
def rub_transaction() -> dict:
    return {
        "operationAmount": {
            "amount": "5000.00",
            "currency": {"name": "руб.", "code": "RUB"}
        }
    }


def test_convert_currency_rub(rub_transaction: dict) -> None:
    assert convert_currency(rub_transaction) == 5000.0


@patch("requests.get")
def test_convert_currency_usd(mock_get: patch, usd_transaction: dict) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 7500.0}

    result = convert_currency(usd_transaction)
    assert result == 7500.0
    mock_get.assert_called_once()
