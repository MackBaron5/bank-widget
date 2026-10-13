from src.utils import process_bank_operations, process_bank_search


def test_process_bank_search():
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    assert len(process_bank_search(data, "Перевод")) == 1
    assert len(process_bank_search(data, "вклад")) == 1
    assert len(process_bank_search(data, "несуществующий")) == 0

def test_process_bank_operations():
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]
    result = process_bank_operations(data, categories)
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
