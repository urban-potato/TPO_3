"""Модуль тестов"""


import random

import pytest

from pages import *
from preparations import test_filters_data

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# импорт инструментов для ожидания и условий
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()

# стратегии загрузки страницы - дождаться только загрузки DOM
options.page_load_strategy = "eager"
# запуск браузера в режиме инкогнито (позволяет не использовать кэш и не сохранять данные)
options.add_argument("--incognito")
# игнорирование ssl сертификатов (игнорирование ошибок сертификатов)
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--ignore-certificate-errors")
options.add_argument('--ignore-ssl-errors')

# размер окна браузера
options.add_argument("--window-size=1200,800")

driver = webdriver.Chrome(options=options)

# создание объекта для работы с цепочками действий
action = ActionChains(driver)

# создание объекта wait, который отвечает за явные ожидания.
wait = WebDriverWait(driver, 15)

# ---------------------------------
# страницы
catalog_laptops_page = CatalogLaptopsPage()
cart_page = CartPage()

# элементы
cookie_notification_element = CookieNotificationElement()
header_element = HeaderElement()

# urls
base_url = "https://tehnomaks.ru/"
catalog_laptops_url = "https://tehnomaks.ru/catalog/section/noutbuki"
cart_page_url = "https://tehnomaks.ru/basket"
# ---------------------------------


class TestCartPositive:
    """Набор положительных тестов для тестирования корзины"""

    @pytest.mark.parametrize("url", [base_url, catalog_laptops_url])
    def test_add_item_to_cart(self, url):
        """Проверка добавления товара в корзину с главной страницы и со страницы каталога"""

        driver.get(url)

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # наведение курсора на корзину
        # (чтобы избежать ошибки, при добавлении товара, потому что меню может перекрывать товар)
        cart_icon_locator = header_element.cart_icon
        cart_icon = wait.until(EC.presence_of_element_located(cart_icon_locator))
        action.move_to_element(cart_icon).perform()

        # сбор всех кнопок добавления товара в корзину с главной страницы
        add_to_cart_buttons_locator = ("xpath", "//a[contains(@class, 'add_to_cart')]")
        add_to_cart_buttons_all = wait.until(EC.presence_of_all_elements_located(add_to_cart_buttons_locator))

        # выбор только тех кнопок, которые видны пользователю
        add_to_cart_buttons_all_interactive = []

        for button in add_to_cart_buttons_all:
            if button.is_displayed():
                add_to_cart_buttons_all_interactive.append(button)

        # рандомный выбор одной кнопки из тех, на которые можно нажать и нажатие на нее,
        # а также сохранение id этого товара
        chosen_item = random.choice(add_to_cart_buttons_all_interactive)
        chosen_item_ppc = chosen_item.get_attribute("data-ppc")

        chosen_item.click()

        # нажатие на иконку корзины, чтобы перейти в корзину
        cart_icon = wait.until(EC.presence_of_element_located(header_element.cart_icon))
        cart_icon.click()

        # проверка, есть ли в корзине товар с тем же id, что был сохранен
        cart_item_locator = cart_page.get_item_locator(chosen_item_ppc)

        pytest.assume(wait.until(EC.presence_of_element_located(cart_item_locator)))

    @pytest.mark.dependency()
    def test_add_item_to_cart_from_item_page(self):
        """Проверка добавления товара в корзину со страницы товара"""

        driver.get(catalog_laptops_url)

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # сбор всех товаров на странице каталога
        items_locator = ("xpath", "//a[@class='product-card-list__name']")
        items = wait.until(EC.presence_of_all_elements_located(items_locator))

        # рандомный выбор одного товара и переход на его страницу
        chosen_item = random.choice(items)
        chosen_item.click()

        # нахождение кнопки добавление товара в корзину
        add_to_cart_button_locator = ("xpath", "(//a[contains(@class, 'add_to_cart')])[1]")
        add_to_cart_button = wait.until(EC.element_to_be_clickable(add_to_cart_button_locator))

        # сохранение id этого товара
        chosen_item_ppc = add_to_cart_button.get_attribute("data-ppc")

        # добавление выбранного товара в корзину
        add_to_cart_button.click()

        # нажатие на иконку корзины, чтобы перейти в корзину
        cart_icon = wait.until(EC.presence_of_element_located(header_element.cart_icon))
        cart_icon.click()

        # проверка, есть ли в корзине товар с тем же id, что был сохранен
        cart_item_locator = cart_page.get_item_locator(chosen_item_ppc)

        assert wait.until(EC.presence_of_element_located(cart_item_locator))

    @pytest.mark.dependency()
    @pytest.mark.dependency(depends=['tests.py::TestCartPositive::test_add_item_to_cart_from_item_page'],
                            scope="session")
    def test_increase_number_of_items_in_cart(self):
        """Проверка увеличения количества товара в корзине"""

        driver.get(cart_page_url)

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        all_cart_items = wait.until(EC.presence_of_all_elements_located(all_cart_items_locator))

        # рандомный выбор одного товара,
        # а также сохранение его id в подготовленное в конфигурации pytest поле
        chosen_item = random.choice(all_cart_items)
        chosen_item_ppc = chosen_item.get_attribute("data-ppc")
        pytest.increased_item_ppc = chosen_item_ppc

        # сохранение числа, показывающего количество товара
        quantity_input_locator = cart_page.get_item_input_field_locator(chosen_item_ppc)
        quantity_input = wait.until(EC.presence_of_element_located(quantity_input_locator))
        initial_quantity = quantity_input.get_attribute("value")

        # увеличение количества товара
        increase_quantity_locator = cart_page.get_item_increase_quantity_locator(chosen_item_ppc)
        increase_quantity_button = wait.until(EC.element_to_be_clickable(increase_quantity_locator))
        increase_quantity_button.click()

        # обновление страницы
        driver.refresh()

        # проверка, увеличилось ли количество товара
        quantity_input = wait.until(EC.presence_of_element_located(quantity_input_locator))
        current_quantity = quantity_input.get_attribute("value")

        assert int(current_quantity) == int(initial_quantity) + 1

    @pytest.mark.dependency(depends=['tests.py::TestCartPositive::test_add_item_to_cart_from_item_page',
                                     'tests.py::TestCartPositive::test_increase_number_of_items_in_cart'],
                            scope="session")
    def test_decrease_number_of_items_in_cart(self):
        """Проверка уменьшения количества товара в корзине"""

        driver.get(cart_page_url)

        # id товара, количество которого было увеличено в предыдущем тесте
        item_ppc = pytest.increased_item_ppc

        # сохранение числа, показывающего количество товара
        quantity_input_locator = cart_page.get_item_input_field_locator(item_ppc)
        quantity_input = wait.until(EC.presence_of_element_located(quantity_input_locator))
        initial_quantity = quantity_input.get_attribute("value")

        # уменьшение количества товара
        decrease_quantity_locator = cart_page.get_item_decrease_quantity_locator(item_ppc)
        decrease_quantity_button = wait.until(EC.element_to_be_clickable(decrease_quantity_locator))
        decrease_quantity_button.click()

        # обновление страницы
        driver.refresh()

        # проверка, уменьшилось ли количество товара
        quantity_input = wait.until(EC.presence_of_element_located(quantity_input_locator))
        current_quantity = quantity_input.get_attribute("value")

        assert int(current_quantity) == int(initial_quantity) - 1

    @pytest.mark.dependency(depends=['tests.py::TestCartPositive::test_add_item_to_cart_from_item_page'],
                            scope="session")
    def test_remove_items_from_cart(self):
        """Проверка удаления товара из корзины с помощью кнопки 'Удалить'"""

        driver.get(cart_page_url)

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        all_cart_items = wait.until(EC.presence_of_all_elements_located(all_cart_items_locator))

        # рандомный выбор одного товара,
        # а также сохранение его id
        chosen_item = random.choice(all_cart_items)
        chosen_item_ppc = chosen_item.get_attribute("data-ppc")

        # удаление товара из корзины, нажатием на кнопку 'Удалить'
        remove_item_locator = cart_page.get_remove_item_locator(chosen_item_ppc)
        remove_item_button = wait.until(EC.element_to_be_clickable(remove_item_locator))
        remove_item_button.click()

        # обновление страницы
        driver.refresh()

        # проверка, присутствует ли на странице удаленный товар
        item_locator = cart_page.get_item_locator(chosen_item_ppc)
        items_found = driver.find_elements(*item_locator)

        assert not items_found

    @pytest.mark.dependency(depends=['tests.py::TestCartPositive::test_add_item_to_cart_from_item_page'],
                            scope="session")
    def test_remove_items_from_cart_by_decrease(self):
        """Проверка удаления товара из корзины уменьшением его количества до 0"""

        driver.get(cart_page_url)

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        all_cart_items = wait.until(EC.presence_of_all_elements_located(all_cart_items_locator))

        # рандомный выбор одного товара,
        # а также сохранение его id
        chosen_item = random.choice(all_cart_items)
        chosen_item_ppc = chosen_item.get_attribute("data-ppc")

        # уменьшение количества товара
        decrease_quantity_locator = cart_page.get_item_decrease_quantity_locator(chosen_item_ppc)
        decrease_quantity_button = wait.until(EC.element_to_be_clickable(decrease_quantity_locator))
        decrease_quantity_button.click()

        # обновление страницы
        driver.refresh()

        # проверка, присутствует ли на странице удаленный товар
        item_locator = cart_page.get_item_locator(chosen_item_ppc)
        items_found = driver.find_elements(*item_locator)

        assert not items_found

    @pytest.mark.dependency(depends=['tests.py::TestCartPositive::test_add_item_to_cart_from_item_page'],
                            scope="session")
    def test_cart_is_empty_after_removing_all_items(self):
        """Проверка того, что корзина становится пустой после удаление всех товаров"""

        driver.get(cart_page_url)

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        all_cart_items = wait.until(EC.presence_of_all_elements_located(all_cart_items_locator))

        # сбор id всех найденных товаров
        all_items_ppc = []

        for item in all_cart_items:
            all_items_ppc.append(item.get_attribute("data-ppc"))

        # удаление каждого товара
        for item_ppc in all_items_ppc:
            remove_item_locator = cart_page.get_remove_item_locator(item_ppc)
            remove_item_button = wait.until(EC.element_to_be_clickable(remove_item_locator))
            remove_item_button.click()

        # обновление страницы
        driver.refresh()

        # проверка, присутствуют ли на странице товары
        cart_items_found = driver.find_elements(*all_cart_items_locator)

        assert not cart_items_found


class TestCartNegative:
    """Набор негативных тестов для тестирования корзины"""

    def test_prohibiting_proceed_with_empty_basket(self):
        """Проверка невозможности продолжения оформления заказа с пустой корзиной"""

        driver.get(cart_page_url)

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        cart_items_found = driver.find_elements(*all_cart_items_locator)

        # если товары нашлись
        if cart_items_found:

            # сбор id всех найденных товаров
            all_items_ppc = []

            for item in cart_items_found:
                all_items_ppc.append(item.get_attribute("data-ppc"))

            # удаление каждого товара
            for item_ppc in all_items_ppc:
                remove_item_locator = cart_page.get_remove_item_locator(item_ppc)
                remove_item_button = wait.until(EC.element_to_be_clickable(remove_item_locator))
                remove_item_button.click()

            # обновление страницы
            driver.refresh()

        # проверка, присутствуют ли на странице товары
        cart_items_found = driver.find_elements(*all_cart_items_locator)

        if cart_items_found:
            assert False

        # проверка, присутствует ли на странице и является ли активной кнопка продолжения оформления заказа
        proceed_purchase_button_locator = cart_page.proceed_purchase_button
        purchase_button_items_found = driver.find_elements(*proceed_purchase_button_locator)

        if purchase_button_items_found:
            assert not driver.find_element(*proceed_purchase_button_locator).is_enabled()
        else:
            assert True

    def test_prohibiting_proceed_after_all_items_removed(self):
        """Проверка невозможности продолжения оформления заказа после того,
        как в корзину были добавлены товары и удалены все товары"""

        driver.get(catalog_laptops_url)

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # сбор всех кнопок добавления товара в корзину
        add_to_cart_buttons_locator = ("xpath", "//a[contains(@class, 'add_to_cart')]")
        add_to_cart_buttons_all = wait.until(EC.presence_of_all_elements_located(add_to_cart_buttons_locator))

        # выбор только тех кнопок, которые видны пользователю
        add_to_cart_buttons_all_interactive = []

        for button in add_to_cart_buttons_all:
            if button.is_displayed():
                add_to_cart_buttons_all_interactive.append(button)

        # рандомный выбор одной кнопки из тех, на которые можно нажать и нажатие на нее
        chosen_item = random.choice(add_to_cart_buttons_all_interactive)
        chosen_item.click()

        # нажатие на иконку корзины, чтобы перейти в корзину
        cart_icon = wait.until(EC.presence_of_element_located(header_element.cart_icon))
        cart_icon.click()

        # сбор всех товаров, находящихся в корзине
        all_cart_items_locator = cart_page.all_cart_items
        all_cart_items = wait.until(EC.presence_of_all_elements_located(all_cart_items_locator))

        # сбор id всех найденных товаров
        all_items_ppc = []

        for item in all_cart_items:
            all_items_ppc.append(item.get_attribute("data-ppc"))

        # удаление каждого товара
        for item_ppc in all_items_ppc:
            remove_item_locator = cart_page.get_remove_item_locator(item_ppc)
            remove_item_button = wait.until(EC.element_to_be_clickable(remove_item_locator))
            remove_item_button.click()

        # проверка, присутствует ли на странице и является ли активной кнопка продолжения оформления заказа
        proceed_purchase_button_locator = cart_page.proceed_purchase_button
        purchase_button_items_found = driver.find_elements(*proceed_purchase_button_locator)

        if purchase_button_items_found:
            assert not driver.find_element(*proceed_purchase_button_locator).is_enabled()
        else:
            assert True


class TestFilters:
    """Набор тестов для тестирования фильтрации товаров"""

    @pytest.mark.parametrize(("price_field_locator", "test_input", "expected_result"), [
        (catalog_laptops_page.price.price_min, "word", ""),
        (catalog_laptops_page.price.price_min, " ", ""),
        (catalog_laptops_page.price.price_min, "*#^$@", ""),
        (catalog_laptops_page.price.price_min, "-1", "1"),
        (catalog_laptops_page.price.price_min, "5.3", "53"),
        (catalog_laptops_page.price.price_min, "0", "0"),
        (catalog_laptops_page.price.price_min, "254", "254"),

        (catalog_laptops_page.price.price_max, "word", ""),
        (catalog_laptops_page.price.price_max, " ", ""),
        (catalog_laptops_page.price.price_max, "*#^$@", ""),
        (catalog_laptops_page.price.price_max, "-1", "1"),
        (catalog_laptops_page.price.price_max, "5.3", "53"),
        (catalog_laptops_page.price.price_max, "0", "0"),
        (catalog_laptops_page.price.price_max, "254", "254"),
    ])
    def test_price_fields(self, price_field_locator, test_input, expected_result):
        """Проверка полей для ввода минимальной цены и максимальной цены"""

        driver.get(catalog_laptops_url)

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # раскрытие блока фильтра
        price_block_expand_button_locator = catalog_laptops_page.price.expand_button
        wait.until(EC.element_to_be_clickable(price_block_expand_button_locator)).click()

        # ввод значений в поле цены
        wait.until(EC.element_to_be_clickable(price_field_locator)).send_keys(test_input)
        # нажатие на кнопку применения фильтров
        accept_filters_button_locator = catalog_laptops_page.accept_filters_button
        wait.until(EC.element_to_be_clickable(accept_filters_button_locator)).click()
        # вновь получение элемента с полем цены после перезагрузки страницы
        price_input = wait.until(EC.presence_of_element_located(price_field_locator))

        # проверка, соответствует ли значение в поле ожидаемому
        pytest.assume(price_input.get_attribute("value") == expected_result)

    def test_prohibiting_choose_few_filters_in_availability(self):
        """Проверка невозможности выбрать одновременно несколько фильтров в блоке фильтров 'Наличие'"""

        driver.get(catalog_laptops_url)

        # локаторы фильтров
        all_stock_status_locator = catalog_laptops_page.availability.all_stock_status
        all_stock_action_locator = catalog_laptops_page.availability.all_stock_action

        in_stock_status_locator = catalog_laptops_page.availability.in_stock_status
        in_stock_action_locator = catalog_laptops_page.availability.in_stock_action

        out_stock_status_locator = catalog_laptops_page.availability.out_stock_status
        out_stock_action_locator = catalog_laptops_page.availability.out_stock_action

        # локатор кнопки применения фильтров
        accept_filters_button_locator = catalog_laptops_page.accept_filters_button

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # раскрытие блока фильтров 'Наличие'
        availability_filters_expand_button_locator = catalog_laptops_page.availability.expand_button
        availability_filters_expand_button = wait.until(
            EC.element_to_be_clickable(availability_filters_expand_button_locator))
        if not availability_filters_expand_button.get_attribute("open") == "true":
            availability_filters_expand_button.click()

        # нажатие на фильтр 'Все'
        wait.until(EC.element_to_be_clickable(all_stock_action_locator)).click()
        # нажатие на кнопку применения фильтров
        wait.until(EC.element_to_be_clickable(accept_filters_button_locator)).click()

        # проверка, что выбран фильтр 'Все'
        all_stock_filter_element = wait.until(EC.presence_of_element_located(all_stock_status_locator))

        pytest.assume(all_stock_filter_element.is_selected())

        # нажатие на фильтр 'В наличии'
        wait.until(EC.element_to_be_clickable(in_stock_action_locator)).click()
        # нажатие на кнопку применения фильтров
        wait.until(EC.element_to_be_clickable(accept_filters_button_locator)).click()

        # проверка, что выбран фильтр 'В наличии' и не выбран фильтр 'Все'
        all_stock_filter_element = wait.until(EC.presence_of_element_located(all_stock_status_locator))
        in_stock_filter_element = wait.until(EC.presence_of_element_located(in_stock_status_locator))

        pytest.assume(in_stock_filter_element.is_selected())
        pytest.assume(not all_stock_filter_element.is_selected())

        # нажатие на фильтр 'Под заказ'
        wait.until(EC.element_to_be_clickable(out_stock_action_locator)).click()
        # нажатие на кнопку применения фильтров
        wait.until(EC.element_to_be_clickable(accept_filters_button_locator)).click()

        # проверка, что выбран фильтр 'Под заказ' и не выбраны фильтры 'В наличии' и 'Все'
        all_stock_filter_element = wait.until(EC.presence_of_element_located(all_stock_status_locator))
        in_stock_filter_element = wait.until(EC.presence_of_element_located(in_stock_status_locator))
        out_stock_filter_element = wait.until(EC.presence_of_element_located(out_stock_status_locator))

        pytest.assume(out_stock_filter_element.is_selected())
        pytest.assume(not in_stock_filter_element.is_selected())
        pytest.assume(not all_stock_filter_element.is_selected())

    @pytest.mark.parametrize("test_data", test_filters_data)
    def test_filters(self, test_data):
        """Проверка фильтрации товаров"""

        driver.get(catalog_laptops_url)

        # закрытие мешающего окошка с уведомлением о кукисах, если оно есть
        close_cookie_informer_button_locator = cookie_notification_element.close_button
        close_cookie_informer_button = wait.until(EC.presence_of_element_located(close_cookie_informer_button_locator))
        if close_cookie_informer_button.is_displayed() and close_cookie_informer_button.is_enabled():
            close_cookie_informer_button.click()

        # раскрытие дополнительных фильтров
        additional_filters_expand_button_locator = catalog_laptops_page.additional_filters.expand_button
        additional_filters_expand_button = wait.until(
            EC.element_to_be_clickable(additional_filters_expand_button_locator))
        if additional_filters_expand_button.get_attribute("close") == "true":
            additional_filters_expand_button.click()

        # применение фильтров
        for data_obj in test_data:
            # раскрытие блока фильтра
            expand_button_locator = data_obj.expand_button_locator
            wait.until(EC.element_to_be_clickable(expand_button_locator)).click()

            # если этот блок фильтров - Цена, выполнение специальных действий,
            # отличных от действий с фильтрами-"кнопками"
            if data_obj.is_price_field:
                if data_obj.price_min_data:
                    price_min_locator = data_obj.price_min_locator
                    wait.until(EC.element_to_be_clickable(price_min_locator)).send_keys(data_obj.price_min_data)
                if data_obj.price_max_data:
                    price_max_locator = data_obj.price_max_locator
                    wait.until(EC.element_to_be_clickable(price_max_locator)).send_keys(data_obj.price_max_data)
            # если этот блок фильтров - не Цена, выполнение действий с фильтрами-"кнопками"
            else:
                action_locators = data_obj.action_locators

                for action_locator in action_locators:
                    wait.until(EC.element_to_be_clickable(action_locator)).click()

        # нажатие на кнопку применения фильтров
        accept_filters_button_locator = catalog_laptops_page.accept_filters_button
        wait.until(EC.element_to_be_clickable(accept_filters_button_locator)).click()

        # проверка, применились ли фильтры
        for data_obj in test_data:
            # для блока - Цена
            if data_obj.is_price_field:
                if data_obj.price_min_data:
                    price_min_locator = data_obj.price_min_locator
                    price_min_field = wait.until(EC.presence_of_element_located(price_min_locator))
                    price_min_field_value = price_min_field.get_attribute("value")
                    if price_min_field_value:
                        price_min_field_value = int(price_min_field_value)

                    pytest.assume(price_min_field_value == int(data_obj.price_min_data))

                if data_obj.price_max_data:
                    price_max_locator = data_obj.price_max_locator
                    price_max_field = wait.until(EC.presence_of_element_located(price_max_locator))
                    price_max_field_value = price_max_field.get_attribute("value")
                    if price_max_field_value:
                        price_max_field_value = int(price_max_field_value)

                    pytest.assume(price_max_field_value == int(data_obj.price_max_data))

            # для остальных блоков
            else:
                status_locators = data_obj.status_locators

                for status_locator in status_locators:
                    filter_element = wait.until(EC.presence_of_element_located(status_locator))

                    pytest.assume(filter_element.is_selected())
