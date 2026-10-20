import functools
import logging
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)


def write_report_to_file(filename: Optional[str] = None):
    """
    Декоратор для функций-отчетов. Записывает результирующий DataFrame в файл.
    Если имя файла не передано, генерирует дефолтное название.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            df_result = func(*args, **kwargs)

            if filename:
                actual_filename = filename
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                actual_filename = f"report_{func.__name__}_{timestamp}.xlsx"

            try:
                df_result.to_excel(actual_filename, index=False)
                logger.info(f"Отчет успешно сохранен в файл: {actual_filename}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета в файл {actual_filename}: {e}")

            return df_result

        return wrapper

    if callable(filename):
        func = filename
        filename = None
        return decorator(func)

    return decorator


def _get_three_months_range(df: pd.DataFrame, date: Optional[str]) -> tuple:
    """Вспомогательная функция для расчета временного диапазона в 3 месяца."""
    if date:
        end_date = pd.to_datetime(date, dayfirst=True)
    else:
        end_date = pd.to_datetime(datetime.now())

    start_date = end_date - timedelta(days=90)
    return start_date, end_date


@write_report_to_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца."""
    logger.info(f"Формирование отчета по категории '{category}'")

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    start_date, end_date = _get_three_months_range(df, date)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date) &
        (df["Категория"] == category) &
        (df["Сумма операции"] < 0)
        ]
    return filtered_df


@write_report_to_file
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца."""
    logger.info("Формирование отчета по дням недели")

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    start_date, end_date = _get_three_months_range(df, date)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date) &
        (df["Сумма операции"] < 0)
        ].copy()

    filtered_df["День недели"] = filtered_df["Дата операции"].dt.day_name()

    result_df = filtered_df.groupby("День недели", as_index=False)["Сумма операции"].mean()
    result_df["Сумма операции"] = result_df["Сумма операции"].abs()
    result_df.rename(columns={"Сумма операции": "Средняя сумма трат"}, inplace=True)
    return result_df


@write_report_to_file
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в рабочие и выходные дни за последние три месяца."""
    logger.info("Формирование отчета по рабочим/выходным дням")

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    start_date, end_date = _get_three_months_range(df, date)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date) &
        (df["Сумма операции"] < 0)
        ].copy()

    filtered_df["Тип дня"] = filtered_df["Дата операции"].dt.weekday.apply(
        lambda x: "Выходной день" if x >= 5 else "Рабочий день"
    )

    result_df = filtered_df.groupby("Тип дня", as_index=False)["Сумма операции"].mean()
    result_df["Сумма операции"] = result_df["Сумма операции"].abs()
    result_df.rename(columns={"Сумма операции": "Средняя сумма трат"}, inplace=True)
    return result_df
