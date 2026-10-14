import json
import logging
import datetime
import pandas as pd
from typing import Any
from src.reports import dir_transactions_excel, spending_by_category
from src.services import get_beneficial_cashback_categories
from src.views import analyze_data
from src.utils import get_data_range

logger = logging.getLogger("main")
log = os.path.join(os.path.dirname(__file__), "..", "logs", "main.log")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(__file__), "../logs/main.log"),
    "w",
    encoding="utf-8",
)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def main_page(data_user: str = None) -> Dict[str, Any]:
    """
    Функция для страницы «Главная» принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS,
    если дата пользователем не задана, то по умолчанию текущая дата и время.
    Функция для страницы «Главная» возвращает корректный JSON-ответ согласно ТЗ
    :param data_user: строка с датой и временем в формате YYYY-MM-DD HH:MM:SS, по умолчанию текущая дата
    :return: словарь
    """

    # Получаем имя текущей функции
    func_name = inspect.currentframe().f_code.co_name
    print("Функция для запуска всего проекта")

    logger.info(f'Начала выполняться функция "{func_name}"')

    try:
        if data_user is None:
            data_user = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(data_user)

        # Период с начала месяца по заданную пользователем дату
        period = get_data_range(date_str, data_range)

        # Список транзакций за заданный период формата ["01.05.2020", "20.05.2020"]
        list_of_transactions = read_excel_file(path_to_file=f"{file_path}/operations.xlsx", time_period=period)

        # Проверяем пустой ли список
        if not list_of_transactions:
            logger.info(f'Функция "{func_name}" возвратила пустой JSON-ответ, нет транзакций за заданный период')
            print(f'Функция "{func_name}" возвратила пустой JSON-ответ, нет транзакций за заданный период')
            return {}

        else:
            # Приветствие
            greeting = get_greeting(data_user)

            # По каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей):
            cards = get_data_card(list_of_transactions)

            # Топ-5 транзакций по сумме платежа
            top_transactions = get_top_transactions(list_of_transactions)

            # Курс валют
            currency_rates = get_currency_rates("RUB")

            # Стоимость акций из S&P500
            stock_prices = get_stock_prices()

            logger.info(f'Функция "{func_name}" возвратила JSON-ответ')

            return {
                "greeting": greeting,
                "cards": cards,
                "top_transactions": top_transactions,
                "currency_rates": currency_rates,
                "stock_prices": stock_prices
            }

    except Exception as ex:
        logger.info(f'Функция "{func_name}" возвратила ошибку общее исключение: {ex}')
        print(f'Функция "{func_name}" возвратила ошибку общее исключение:{ex}')


if __name__ == '__main__':
    print("\nГЛАВНАЯ СТРАНИЦА\n")
    main_page()

    logging.basicConfig(level=logging.INFO)

    data_time = pd.Timestamp("11-10-2026 00:00:00")
    result1, result2, result3, result4, result5 = website(data_time)
    # print("После вызова website")
    print(result1, result2, result3, result4, result5)

    print("\nСервисы.Простой поиск\n")
    search_str = input('Введите строку поиска: ')
    simple_search(search_str, transaction)

    print("\nОТЧЕТЫ\n")
    spending_by_category(pd.read_excel(dir_transactions_excel), 'Фастфуд', '11.11.2019')

    transactions = [
        {"date": "2023-10-01", "amount": -1500, "category": "Еда"},
        {"date": "2023-10-05", "amount": -2000, "category": "Транспорт"},
        {"date": "2023-10-10", "amount": -3000, "category": "Наличные"},
        {"date": "2023-10-12", "amount": -1000, "category": "Развлечения"},
        {"date": "2023-09-15", "amount": -500, "category": "Еда"},
    ]

    result = get_beneficial_cashback_categories(transactions, 2023, 10)
    print(result)

    # Вызов функции
    data = {
        "Дата операции": pd.to_datetime(["2021-12-31 16:44:00", "2021-12-31 16:42:04", "2021-12-31 16:39:04"]),
        "Сумма операции": [-160.89, -64.00, -118.12],
        "Категория": ["Супермаркеты", "Переводы", "Каршеринг"],
        }
    transactions_df = pd.DataFrame(data)
    transactions_df.to_excel(file_path, index=False)

    result = spending_by_category(transactions_df, "Переводы")
    print(result)

    # Вызов функции анализа данных к веб-странице События
    result = analyze_data(date_str="31.12.2021 16:44:00", data_range="M")
    print(json.dumps(result, ensure_ascii=False, indent=4))
