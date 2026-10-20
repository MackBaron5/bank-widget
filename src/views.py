import json
import logging
from datetime import datetime
import requests

logger = logging.getLogger(__name__)


def get_currency_rates(currencies: list) -> list:
    """Получает текущие курсы валют. В случае сбоя возвращает заглушки из ТЗ."""
    rates = []
    try:
        url = "https://exchangerate-api.com"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json().get("conversion_rates", {})
            for cur in currencies:
                if cur in data:
                    rates.append({"currency": cur, "rate": round(1 / data[cur], 2)})
        else:
            raise ValueError("Ошибка API")
    except Exception:
        logger.warning("Используются дефолтные курсы валют из-за ошибки API.")
        rates = [{"currency": "USD", "rate": 73.21}, {"currency": "EUR", "rate": 87.08}]
    return rates


def get_stock_prices(stocks: list) -> list:
    """Получает стоимости акций (заглушки согласно ТЗ)."""
    prices = []
    stock_mock = {"AAPL": 150.12, "AMZN": 3173.18, "GOOG": 2742.39, "MSFT": 296.71, "TSLA": 1007.08}
    for stock in stocks:
        prices.append({"stock": stock, "price": stock_mock.get(stock, 0.0)})
    return prices


def generate_main_page(date_time_str: str, transactions: list) -> str:
    """Формирует JSON для страницы 'Главная'."""
    logger.info(f"Генерация главной страницы для даты: {date_time_str}")

    dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour

    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    try:
        with open("user_setting.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
    except Exception:
        settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOG", "MSFT", "TSLA"]}

    cards_dict = {}
    valid_transactions = []

    for t in transactions:
        if t.get("Статус") != "OK" or not t.get("Номер карты"):
            continue

        card = str(t["Номер карты"])[-4:]
        amount = t.get("Сумма платежа", 0)

        if card not in cards_dict:
            cards_dict[card] = {"last_digits": card, "total_spent": 0.0, "cashback": 0.0}

        if amount < 0:
            cards_dict[card]["total_spent"] += abs(amount)
            cards_dict[card]["cashback"] += abs(amount) // 100

        valid_transactions.append(t)

    valid_transactions.sort(key=lambda x: abs(x.get("Сумма платежа", 0)), reverse=True)
    top_5 = []
    for t in valid_transactions[:5]:
        try:
            date_obj = datetime.strptime(str(t["Дата операции"]).split()[0], "%d.%m.%Y")
            formatted_date = date_obj.strftime("%d.%m.%Y")
        except Exception:
            formatted_date = str(t["Дата операции"])

        top_5.append({
            "date": formatted_date,
            "amount": t.get("Сумма операции", 0),
            "category": t.get("Категория", "Разное"),
            "description": t.get("Описание", "")
        })

    # Округляем финальные суммы по картам до 2 знаков после запятой
    for card_data in cards_dict.values():
        card_data["total_spent"] = round(card_data["total_spent"], 2)
        card_data["cashback"] = round(card_data["cashback"], 2)

    response_data = {
        "greeting": greeting,
        "cards": list(cards_dict.values()),
        "top_transactions": top_5,
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"])
    }

    return json.dumps(response_data, ensure_ascii=False, indent=4)


def generate_events_page(date_time_str: str, transactions: list) -> str:
    """
    Формирует JSON-ответ для страницы 'События' (аналитика за текущий месяц).
    """
    logger.info(f"Генерация страницы События для даты: {date_time_str}")

    dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    current_year = dt.year
    current_month = dt.month

    # Фильтруем транзакции только за указанный месяц и год
    monthly_transactions = []
    for t in transactions:
        if t.get("Статус") != "OK" or not t.get("Дата операции"):
            continue
        try:
            date_obj = datetime.strptime(str(t["Дата операции"]).split()[0], "%d.%m.%Y")
            if date_obj.year == current_year and date_obj.month == current_month:
                monthly_transactions.append(t)
        except Exception:
            continue

    # Считаем общие расходы и поступления за месяц
    total_expenses = sum(
        abs(t.get("Сумма операции", 0)) for t in monthly_transactions if t.get("Сумма операции", 0) < 0)
    total_income = sum(t.get("Сумma операции", 0) for t in monthly_transactions if t.get("Сумма операции", 0) > 0)

    response_data = {
        "period": f"{current_year}-{current_month:02d}",
        "total_transactions_count": len(monthly_transactions),
        "expenses_summary": round(total_expenses, 2),
        "income_summary": round(total_income, 2)
    }

    return json.dumps(response_data, ensure_ascii=False, indent=4)
