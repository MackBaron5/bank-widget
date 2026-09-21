import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    """Фикстура для предоставления тестовых списков словарей (state и date)."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-12T02:26:18.671407"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-10T02:26:18.671407"},
    ]

@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", []), # Проверка при отсутствии словарей с указанным статусом
    ]
)
def test_filter_by_state(sample_data, state, expected_ids):
    """Тестирование фильтрации списка словарей по заданному статусу."""
    result = filter_by_state(sample_data, state)
    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_descending(sample_data):
    """Тестирование сортировки по датам в порядке убывания (по умолчанию)."""
    result = sort_by_date(sample_data)
    assert [item["id"] for item in result] == [2, 1, 3]

def test_sort_by_date_ascending(sample_data):
    """Тестирование сортировки по датам в порядке возрастания."""
    result = sort_by_date(sample_data, reverse=False)
    assert [item["id"] for item in result] == [3, 1, 2]

def test_sort_by_date_same_dates():
    """Проверка корректности сортировки при абсолютно одинаковых датах."""
    data = [
        {"id": 1, "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "date": "2024-03-11T02:26:18.671407"},
    ]
    result = sort_by_date(data)
    assert len(result) == 2

@pytest.mark.parametrize(
    "bad_data",
    [
        [{"id": 1, "date": ""}], # Пустая дата
        [{"id": 1}],             # Отсутствует ключ 'date'
    ]
)
def test_sort_by_date_invalid_formats(bad_data):
    """Проверка работы функции с некорректными или нестандартными форматами дат."""
    result = sort_by_date(bad_data)
    assert len(result) == 1