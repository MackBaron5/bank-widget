from unittest.mock import patch
import pandas as pd
from src.utils import read_excel_transactions


def test_read_excel_transactions_success():
    """Тест успешного чтения транзакций (мокаем существование файла и чтение Pandas)."""
    mock_data = pd.DataFrame([{"Номер карты": "1234567812345678", "Сумма операции": -100}])

    with patch("os.path.exists", return_value=True), \
            patch("pandas.read_excel", return_value=mock_data):
        result = read_excel_transactions("dummy_path.xlsx")
        assert len(result) == 1
        assert result[0]["Номер карты"] == "1234567812345678"


def test_read_excel_transactions_not_found():
    """Тест поведения функции, если файл на диске отсутствует."""
    with patch("os.path.exists", return_value=False):
        result = read_excel_transactions("non_existent_file.xlsx")
        assert result == []
