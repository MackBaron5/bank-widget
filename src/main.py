from datetime import datetime
from src.utils import read_json_file, process_bank_search
from src.data_files import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.masks import get_mask_card_number, get_mask_account


def format_amount(transaction: dict) -> str:
    """Форматирует сумму операции."""
    amount_data = transaction.get("operationAmount", {})
    amount = amount_data.get("amount", "0")
    currency = amount_data.get("currency", {}).get("name", "RUB")
    return f"{amount} {currency}"


def format_date(date_str: str) -> str:
    """Преобразует строку даты в формат ДД.ММ.ГГГГ."""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("%d.%m.%Y")
    except Exception:
        return date_str


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            transactions = read_json_file("data/operations.json")
            break
        elif choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            transactions = read_csv_file("data/transactions.csv")
            break
        elif choice == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            transactions = read_excel_file("data/transactions_excel.xlsx")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    if not transactions:
        print("Программа: Не удалось загрузить транзакции или файл пуст.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус для фильтрации.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Пользователь: ").strip().upper()

        if status_input in valid_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(f'Программа: Отфильтровано по "{status_input}"')
            break
        else:
            print(f'Программа: Статус "{status_input}" недоступен.')

    # Сортировка по дате
    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    sort_choice = input("Пользователь: ").strip().lower()
    if sort_choice == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        order_choice = input("Пользователь: ").strip().lower()
        reverse = True if "убыван" in order_choice else False
        transactions = sort_by_date(transactions, reverse=reverse)

    # Фильтрация по валюте (Рубли)
    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Пользователь: ").strip().lower()
    if rub_choice == "да":
        transactions = [
            t for t in transactions
            if t.get("operationAmount", {}).get(
                "currency", {}
            ).get("code") == "RUB"
        ]

    # Фильтрация по слову
    print("\nПрограмма: Отфильтровать список по слову в описании? Да/Нет")
    word_choice = input("Пользователь: ").strip().lower()
    if word_choice == "да":
        search_word = input("Пользователь (слово): ").strip()
        transactions = process_bank_search(transactions, search_word)

    # Итоговый вывод
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Программа: Не найдено подходящих транзакций.")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        date = format_date(t.get("date", ""))
        desc = t.get("description", "")

        from_info = t.get("from", "")
        to_info = t.get("to", "")

        def mask_source(source_str: str) -> str:
            if not source_str:
                return "Неизвестный источник"
            if "Счет" in source_str:
                num = "".join(filter(str.isdigit, source_str))
                return f"Счет {get_mask_account(num)}"
            else:
                name = "".join(filter(str.isalpha, source_str))
                num = "".join(filter(str.isdigit, source_str))
                return f"{name} {get_mask_card_number(num)}"

        from_masked = mask_source(from_info) if from_info else ""
        to_masked = mask_source(to_info)

        print(f"{date} {desc}")
        if from_masked:
            print(f"{from_masked} -> {to_masked}")
        else:
            print(f"{to_masked}")
        print(f"Сумма: {format_amount(t)}\n")


if __name__ == "__main__":
    main()
