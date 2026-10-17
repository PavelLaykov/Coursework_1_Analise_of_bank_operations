from unittest.mock import patch
import pytest
import pandas as pd

from src.utils import (data_cards, exchange_rate,
                       greeting, read_xls, stock_price, top_transactions)


def test_top_five_transactions(excel_data: list[dict]) -> None:
    """Тест вывода топ-5 транзакций."""

    data = top_transactions(pd.DataFrame(excel_data))
    assert data == [
        {"amount": 9700.0, "category": "Пополнения", "date": "25.01.2018", "description": "Перевод с карты"},
        {"amount": 5748.0, "category": "Авиабилеты", "date": "25.01.2018", "description": "Aviacassa"},
        {"amount": 375.0, "category": "Транспорт", "date": "26.01.2018", "description": "Яндекс Такси"},
        {"amount": 325.0, "category": "Фастфуд", "date": "26.01.2018", "description": "OOO Fruittella"},
        {"amount": 295.0, "category": "Фастфуд", "date": "27.01.2018", "description": "OOO Fruittella"},
    ]


def test_greeting() -> None:
    date = greeting("2022-02-12 12:12:12")
    assert date == "Доброе утро"
    date = greeting("2022-02-12 00:12:12")
    assert date == "Доброй ночи"
    date = greeting("2022-02-12 14:12:12")
    assert date == "Добрый день"
    date = greeting("2022-02-12 20:12:12")
    assert date == "Добрый вечер"


def test_read_xlsx() -> None:
    assert read_xlsx("") is None


def test_data_cards() -> None:
    assert data_cards("") == []


def test_data_card(sample_df: pd.DataFrame) -> None:
    """Тест вывода топ-5 транзакций."""
    assert data_cards(sample_df) == [
        {"cashback": 2.0, "last_digits": "1111", "total_spent": 200.0},
        {"cashback": 3.0, "last_digits": "2222", "total_spent": 300.0},
        {"cashback": 4.0, "last_digits": "3333", "total_spent": 400.0},
        {"cashback": 5.0, "last_digits": "4444", "total_spent": 500.0},
        {"cashback": 1.0, "last_digits": "5091", "total_spent": 100.0},
        {"cashback": 6.0, "last_digits": "5555", "total_spent": 600.0},
        {"cashback": 7.0, "last_digits": "6666", "total_spent": 700.0},
        {"cashback": 8.0, "last_digits": "7777", "total_spent": 800.0},
        {"cashback": 9.0, "last_digits": "8888", "total_spent": 900.0},
    ]


def test_exchange_rate() -> None:
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok", "values": [{"close": "100"}]}
        assert exchange_rate() == [{"currency": "USD", "rate": 100.0}, {"currency": "EUR", "rate": 100.0}]


def tests_stock_price() -> None:
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok", "values": [{"price": 222.00}]}
        assert stock_price() == []
