"""Модуль с настройками pytest"""


import pytest


def pytest_configure():
    """Метод настройки конфигурации pytest"""

    pytest.increased_item_ppc = None
