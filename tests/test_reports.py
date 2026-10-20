from unittest.mock import patch
import pandas as pd
from src.reports import spending_by_category


def test_spending_by_category():
    """Тест фильтрации трат по конкретной категории за период."""
    # Создаем тестовый DataFrame транзакций
    data = pd.DataFrame([
        {"Дата операции": "20.10.2026", "Категория": "Супермаркеты", "Сумма операции": -150.0},
        {"Дата операции": "19.10.2026", "Категория": "Фастфуд", "Сумма операции": -200.0},
        {"Дата операции": "18.10.2026", "Категория": "Супермаркеты", "Сумма операции": 500.0}  # Поступление,игнорируем
    ])

    # Мокаем декоратор, чтобы он просто возвращал DataFrame без записи в Excel
    with patch("src.reports.write_report_to_file", lambda x: x):
        result_df = spending_by_category(data, "Супермаркеты", date="20.10.2026")

        assert len(result_df) == 1
        assert result_df.iloc[0]["Сумма операции"] == -150.0
