import functools
from datetime import datetime
from functools import wraps
import json
import os
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from dateutil.relativedelta import relativedelta
from src.utils import get_excel
import logging
from src.config import config, file_path


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(levelname)s-%(message)s")
spending_by_weekday_logger = logging.getLogger("spending_by_weekday")
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("./logs/utils.log", "a")
file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(filename)s %(funcName)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir/'data'/'operations.xlsx'
print(dir_transactions_excel)

current_dir = Path(__file__).parent.parent.resolve()
file_path_log = current_dir/'./log', 'reports.log'
# base_dir = "tests"
# sub_dir = "data"
# file_name = "test_file.txt"
# full_path = os.path.join(base_dir, sub_dir, file_name)
# print(full_path)


def log_report_to_file(filename):
    """Декоратор для записи отчета в файл."""

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            df = func(*args, **kwargs)
            logger.info("Проверка: являются ли данные датафреймом")
            if isinstance(df, pd.DataFrame):
                logger.info("Запись отчёта в файл")
                df.to_json(filename, orient="records", lines=True, force_ascii=False)
            else:
                logger.error("Данные не являются датафреймом. В файл записаны не будут")
            return df

        return inner

    return wrapper


def date_now():
    """Функция, возвращающая текущую дату"""
    now = datetime.now()
    formatted_date = now.strftime("%d.%m.%Y")
    return formatted_date


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict[Any, Any]]:
    """ Функция возвращает траты по заданной категории за последние три месяца."""
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.Timestamp(date)

    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S"
    )

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]
    df_dict = filtered_transactions.to_dict(orient='records')
    result = []
    for i in df_dict:
        result.append({i["Категория"]: i["Сумма операции с округлением"]})
    logging.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")
    return result


@decorator_with_args('./logs/report.json')
def decorator_with_args(file: str):
    """Функция, которая записывает результаты из spending_by_category"""
    def my_big_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                with open(file, "w", encoding="utf-8") as file_2:
                    json.dump(result.to_dict("records"), file_2, ensure_ascii=False)
                return result
            except FileNotFoundError:
                print("Не получилось записать информацию в файл")
        return wrapper
    return my_big_decorator


@reports_decorator("report.txt")
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = str(datetime.now())) -> pd.DataFrame:
    """Функция, которая возвращает датафрейм с тратами по заданной категории
       за последние три месяца (от переданной даты)."""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
    transactions_by_category = transactions[(transactions['Дата операции']
                                             <= (pd.to_datetime(date, dayfirst=True) + relativedelta(months=2)))
                                            & (transactions['Дата операции'] >= pd.to_datetime(date, dayfirst=True))
                                            & (transactions['Категория'].str.upper() == category.upper())]
    trans = pd.DataFrame(transactions_by_category.groupby(['Категория'], as_index=False).
                         agg({'Сумма операции': 'sum'})['Сумма операции'].rename({'Сумма операции': category}))
    print(transactions_by_category.to_dict('records'))
    return trans


def print_spending_by_date(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(os.path.join("./print_decorators/report_1.txt"), "w"):
            return result.to_string(buf="report_1.txt", header=False)
    return wrapper


def print_name_spending_by_date(file_name):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(os.path.join(f"./print_decorators/{file_name}"), "w"):
                return result.to_string(buf=file_name, header=False)
        return wrapper
    return my_decorator


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Any | None:
    """возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""
    try:
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%Y-%m-%d")

        transactions["datetime"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        transactions["day_name"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True).dt.day_name()
        df = transactions[
            (transactions["datetime"] >= (date + relativedelta(months=-3))) & (transactions["datetime"] <= date)
        ].groupby(by="day_name")
        print(df.head(10))
        spending_by_weekday_logger.info("Успешное формирование отчета о средних тратах.")
        return (df["Сумма платежа"].mean().abs().round(2)).to_json()
    except Exception as e:
        spending_by_weekday_logger.warning(f"!!!! Неудачное формирование отчета. Ошибка - {e}")


def report_decorator(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "a") as f:
                f.write(f"{result}\n")
            return result

        return wrapper

    return decorator
