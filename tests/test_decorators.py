import pandas as pd
import pytest

from src.decorators import log


def test_decorator_with_non_dataframe_function() -> None:
    """Тест декоратора с функцией, возвращающей не DataFrame"""
    filename = "test_log.log"

    @log(filename=filename)
    def test_func():
        return "not a dataframe"

    result = test_func()
    assert result == "not a dataframe"


def test_decorator_file_permission_error(monkeypatch) -> None:
    """Тест обработки ошибок записи в файл"""
    filename = "/invalid_path/test.log"

    @log(filename=filename)
    def test_func():
        """Проверка при записи в недоступный путь"""
        return pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    # Ожидаем ошибку при записи в недоступный путь
    with pytest.raises(FileNotFoundError):
        test_func()
