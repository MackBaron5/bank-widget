from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_success() -> None:
    mock_data = '[{"id": 1, "state": "EXECUTED"}]'
    # Добавляем patch для проверки существования файла path.exists
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_data)):
            result = read_json_file("dummy.json")
            assert result == [{"id": 1, "state": "EXECUTED"}]



def test_read_json_file_not_found() -> None:
    with patch("pathlib.Path.exists", return_value=False):
        assert read_json_file("missing.json") == []


def test_read_json_file_invalid_json() -> None:
    with patch("builtins.open", mock_open(read_data="invalid json")):
        assert read_json_file("invalid.json") == []
