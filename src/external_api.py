import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def convert_currency(transaction: dict) -> float:
    """Принимает транзакцию (словарь) и возвращает сумму в рублях (float).

    Если валюта USD или EUR, делает запрос к Exchange Rates Data API.
    """
    try:
        # Безопасное извлечение суммы и валюты из структуры транзакции
        amount_data = transaction.get("operationAmount", {})
        amount = float(amount_data.get("amount", 0))
        currency = amount_data.get("currency", {}).get("code", "RUB")
    except (ValueError, TypeError, KeyError):
        return 0.0

    # Если валюта изначально рубли — конвертация не нужна
    if currency == "RUB":
        return amount

    # Делаем запрос к API для USD и EUR
    if currency in ["USD", "EUR"]:
        # Проверенный URL с явной передачей заголовка apikey
        url = (
            f"https://apilayer.com"
            f"{currency}&amount={amount}"
        )
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result_data = response.json()

            # Извлекаем итоговую сумму
            return float(result_data.get("result", 0.0))
        except (requests.RequestException, ValueError, KeyError):
            return 0.0

    return 0.0
