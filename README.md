# Виджет банковских операций

Проект предназначен для фильтрации и сортировки банковских операций клиента.

## Установка
1. Клонируйте репозиторий.
2. Перейдите в директорию проекта.

## Использование
В модуле processing доступны функции filter_by_state и sort_by_date.

## Модуль генераторов (generators.py)

Модуль содержит функции для эффективной работы с большими массивами транзакций с использованием итераторов.

### Примеры использования:

1. Фильтрация по валюте:
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))
2. Получение описаний операций:
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
print(next(descriptions))
3. Генератор номеров карт:
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)

## Модуль декораторов (decorators)

В проект добавлен модуль `decorators.py`, содержащий функционал для автоматического логирования работы функций.

### Декоратор `@log`
Автоматически регистрирует детали выполнения функций (имя, статус выполнения, возвращаемое значение или параметры и тип ошибки в случае сбоя).

**Синтаксис:**
- `@log()` — логирование выводится напрямую в консоль (`sys.stdout`).
- `@log(filename="mylog.txt")` — логирование записывается в указанный файл.
