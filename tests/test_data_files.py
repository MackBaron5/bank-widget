from unittest.mock import patch

import pandas as pd
import pytest

from src.data_files import read_csv_file, read_excel_file


@pytest.fixture
def sample_data() -> list[dict]:
    return [{"id": 1, "amount": 100.0, "currency": "RUB"}]


@patch("pandas.read_csv")
def test_read_csv_file_success(mock_read_csv, sample_data) -> None:
    # Имитируем, что pandas успешно прочитал DataFrame
    mock_read_csv.return_value = pd.DataFrame(sample_data)

    result = read_csv_file("dummy.csv")
    assert result == sample_data


@patch("pandas.read_csv")
def test_read_csv_file_not_found(mock_read_csv) -> None:
    # Имитируем ошибку отсутствия файла
    mock_read_csv.side_effect = FileNotFoundError()

    assert read_csv_file("missing.csv") == []


@patch("pandas.read_excel")
def test_read_excel_file_success(mock_read_excel, sample_data) -> None:
    # Имитируем успешное чтение Excel
    mock_read_excel.return_value = pd.DataFrame(sample_data)

    result = read_excel_file("dummy.xlsx")
    assert result == sample_data


@patch("pandas.read_excel")
def test_read_excel_file_not_found(mock_read_excel) -> None:
    mock_read_excel.side_effect = FileNotFoundError()

    assert read_excel_file("missing.xlsx") == []
