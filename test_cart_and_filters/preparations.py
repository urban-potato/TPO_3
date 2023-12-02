"""Модуль с подготовкой наборов данных для тестов"""


from pages import *


# ---------------------------------
# страницы
catalog_laptops_page = CatalogLaptopsPage()
# ---------------------------------


class TestFiltersDataObject:
    """Класс представляющий собой набор данный для тестирования фильтрации товаров"""
    def __init__(self, expand_button_locator: tuple[str], expected_result: bool = None,
                 status_locators: list[tuple[str]] = None, action_locators: list[tuple[str]] = None,

                 price_min_locator: tuple[str] = None, price_max_locator: tuple[str] = None,
                 price_min_data: str = None, price_max_data: str = None,
                 is_price_field: bool = False):
        """Метод инициализации объекта"""

        self.expand_button_locator = expand_button_locator
        self.expected_result = expected_result

        self.status_locators = status_locators
        self.action_locators = action_locators

        self.price_min_locator = price_min_locator
        self.price_max_locator = price_max_locator

        self.price_min_data = price_min_data
        self.price_max_data = price_max_data

        self.is_price_field = is_price_field


test_filters_data = [
    [
        TestFiltersDataObject(
            catalog_laptops_page.price.expand_button,
            price_min_locator=catalog_laptops_page.price.price_min,
            price_max_locator=catalog_laptops_page.price.price_max,
            price_min_data="30000",
            is_price_field=True
        ),
        TestFiltersDataObject(
            catalog_laptops_page.availability.expand_button,
            expected_result=True,
            status_locators=[catalog_laptops_page.availability.in_stock_status],
            action_locators=[catalog_laptops_page.availability.in_stock_action]
        ),
        TestFiltersDataObject(
            catalog_laptops_page.manufacturer.expand_button,
            expected_result=True,
            status_locators=[catalog_laptops_page.manufacturer.acer_status,
                             catalog_laptops_page.manufacturer.colorful_status],
            action_locators=[catalog_laptops_page.manufacturer.acer_action,
                             catalog_laptops_page.manufacturer.colorful_action]
        )
    ],

    [
        TestFiltersDataObject(
            catalog_laptops_page.manufacturer.expand_button,
            expected_result=True,
            status_locators=[catalog_laptops_page.manufacturer.hp_status],
            action_locators=[catalog_laptops_page.manufacturer.hp_action]
        ),
        TestFiltersDataObject(catalog_laptops_page.additional_filters.graphics_card_type.expand_button,
                              expected_result=True,
                              status_locators=[
                                  catalog_laptops_page.additional_filters.graphics_card_type.integrated_status],
                              action_locators=[
                                  catalog_laptops_page.additional_filters.graphics_card_type.integrated_action])
    ]
]
