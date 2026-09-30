import os
import pytest
from decorators import log


# --- Тесты для вывода в консоль (filename не задан) ---

def test_log_console_success(capsys):
    @log()
    def add(x, y):
        return x + y

    assert add(2, 3) == 5
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_console_error(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
        
    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (1, 0), {}\n"


# --- Тесты для вывода в файл (filename задан) ---

def test_log_file_success(tmp_path):
    # Создаем путь во временной папке pytest
    log_file = tmp_path / "test_success.txt"
    log_path = str(log_file)

    @log(filename=log_path)
    def greet(name):
        return f"Hello, {name}"

    assert greet("Alice") == "Hello, Alice"
    
    # Проверяем содержимое файла
    assert log_file.read_text(encoding="utf-8") == "greet ok\n"


def test_log_file_error(tmp_path):
    log_file = tmp_path / "test_error.txt"
    log_path = str(log_file)

    @log(filename=log_path)
    def get_element(lst, index):
        return lst[index]

    with pytest.raises(IndexError):
        get_element([1, 2], 5)

    expected_log = "get_element error: IndexError. Inputs: ([1, 2], 5), {}\n"
    assert log_file.read_text(encoding="utf-8") == expected_log
