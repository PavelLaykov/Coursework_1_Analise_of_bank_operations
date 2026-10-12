import unittest
import pandas as pd
import pytest
from unittest.mock import patch
from datetime import datetime
from src.utils import greeting, get_excel


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class TestGreeting(unittest.TestCase):

    @patch('src.utils.datetime')  # Замокируем класс datetime
    def test_evening_greeting(self, mock_datetime):
        """Тестируем приветствие 'Добрый вечер!'."""
        # Устанавливаем возвращаемое значение для метода now
        mock_datetime.now.return_value = datetime.strptime('2023-01-01 22:00:57.689974', '%Y-%m-%d %H:%M:%S.%f')

        # Вызываем greeting, который будет использовать замокированный datetime
        result = greeting()
        self.assertEqual(result, "Добрый вечер!")


def test_get_excel(get_excel_0):
    assert get_excel("dict")[360] == get_excel_0
    assert get_excel("dataframe").equals(pd.read_excel("../data/operations.xlsx"))
    with pytest.raises(ValueError):
        assert get_excel("Invalid format") == ValueError


if __name__ == '__main__':
    unittest.main()
