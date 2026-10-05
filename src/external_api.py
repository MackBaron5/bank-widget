import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def convert_currency(transaction: dict) -> float:
    """Принимает транзакцию и возвращает сумму в рублях (float).

    Если валюта транзакции USD или EUR, делает запрос к Exchange Rates Data API.
    """
    try:
        amount_data = transaction.get("operationAmount", {})
        amount = float(amount_data.get("amount", 0))
        currency = amount_data.get("currency", {}).get("code", "RUB")
    except (ValueError, TypeError, KeyError):
        return 0.0

    if currency == "RUB":
        return amount

    if currency in ["USD", "EUR"]:
        url = f"https://apilayer.com{currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result_data = response.json()
            return float(result_data.get("result", 0.0))
        except (requests.RequestException, ValueError, KeyError):
            return 0.0

    return 0.0
